"""Decode a pasted Token Status List payload for the explorer.

The explorer inspects payloads produced by any issuer, so it decodes without
verifying signatures: the signing key of a foreign list is not known here.
Accepted inputs, detected in this order:

- a JSON object: a JWT payload carrying ``status_list``, or the bare
  ``{"bits": ..., "lst": ...}`` claim;
- a Status List JWT (``header.payload.signature``);
- a Status List CWT (COSE_Sign1), as hex or base64/base64url bytes;
- the ``lst`` field on its own (base64url zlib bytes), decoded with the
  caller-supplied ``bits``.
"""

from __future__ import annotations

import binascii
import json
import re
import zlib
from dataclasses import dataclass
from typing import Any

import jwt

from cwt_codec import _CborTag, _decode_cbor
from status_list import ALLOWED_BITS, base64url_decode, unpack_status_values


# 128 KiB inflated holds 1,048,576 entries at 1 bit: well above any list this
# server issues, small enough that a hostile payload cannot exhaust memory.
MAX_INFLATED_BYTES = 128 * 1024

_COSE_SIGN1_TAG = 18
_CWT_TAG = 61
_CWT_STATUS_LIST_CLAIM = 65533
_HEX = re.compile(r"^(?:[0-9a-fA-F]{2})+$")


class ExplorerError(ValueError):
    pass


@dataclass(frozen=True)
class ExploredStatusList:
    format: str
    header: dict[str, Any]
    payload: dict[str, Any]
    bits: int
    compressed_bytes: int
    inflated_bytes: int
    statuses: list[int]


def explore_status_list(text: str, bits: int = 1) -> ExploredStatusList:
    """Decode ``text`` into its status values; ``bits`` applies to a bare ``lst``."""
    value = text.strip()
    if not value:
        raise ExplorerError("paste a status list JWT, CWT, JSON payload or lst value")

    if value.startswith("{"):
        return _from_json(value)
    if value.count(".") == 2:
        return _from_jwt(value)

    for raw in _candidate_bytes(value):
        cwt = _try_cwt(raw)
        if cwt is not None:
            return cwt
    return _from_lst("lst", {}, {}, _base64url_bytes(value), bits)


def _from_json(value: str) -> ExploredStatusList:
    try:
        document = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ExplorerError(f"invalid JSON: {exc.msg}") from exc
    if not isinstance(document, dict):
        raise ExplorerError("JSON input must be an object")
    claim = document.get("status_list", document)
    if not isinstance(claim, dict) or "lst" not in claim:
        raise ExplorerError('JSON input has no "status_list" claim or "lst" field')
    bits, lst = _claim_fields(claim)
    if not isinstance(lst, str):
        raise ExplorerError('"lst" must be a base64url string in JSON form')
    return _from_lst("json", {}, document, _base64url_bytes(lst), bits)


def _from_jwt(value: str) -> ExploredStatusList:
    try:
        header = jwt.get_unverified_header(value)
        payload = jwt.decode(value, options={"verify_signature": False})
    except jwt.PyJWTError as exc:
        raise ExplorerError(f"invalid JWT: {exc}") from exc
    claim = payload.get("status_list")
    if not isinstance(claim, dict):
        raise ExplorerError('JWT payload has no "status_list" claim')
    bits, lst = _claim_fields(claim)
    if not isinstance(lst, str):
        raise ExplorerError('"lst" must be a base64url string in a JWT')
    return _from_lst("jwt", header, payload, _base64url_bytes(lst), bits)


def _try_cwt(raw: bytes) -> ExploredStatusList | None:
    """Return the decoded CWT, or ``None`` when ``raw`` is not a COSE_Sign1."""
    try:
        decoded = _decode_cbor(raw)
    except (TypeError, ValueError, OverflowError):
        return None
    if isinstance(decoded, _CborTag) and decoded.number == _CWT_TAG:
        decoded = decoded.value
    if isinstance(decoded, _CborTag) and decoded.number == _COSE_SIGN1_TAG:
        decoded = decoded.value
    if not (isinstance(decoded, list) and len(decoded) == 4 and isinstance(decoded[0], bytes)):
        return None

    protected, unprotected, payload_bytes, _signature = decoded
    try:
        protected_headers = _decode_cbor(protected) if protected else {}
        payload = _decode_cbor(payload_bytes)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ExplorerError(f"invalid COSE_Sign1 content: {exc}") from exc
    if not isinstance(protected_headers, dict) or not isinstance(unprotected, dict):
        raise ExplorerError("COSE headers must be CBOR maps")
    if not isinstance(payload, dict):
        raise ExplorerError("CWT payload must be a CBOR map")

    claim = payload.get(_CWT_STATUS_LIST_CLAIM, payload.get("status_list"))
    if not isinstance(claim, dict):
        raise ExplorerError("CWT payload has no status_list claim (label 65533)")
    bits, lst = _claim_fields(claim)
    if not isinstance(lst, bytes):
        raise ExplorerError('"lst" must be a byte string in a CWT')
    header = {**protected_headers, **unprotected}
    return _from_lst("cwt", _json_safe(header), _json_safe(payload), lst, bits)


def _claim_fields(claim: dict) -> tuple[int, Any]:
    bits = claim.get("bits")
    if not isinstance(bits, int) or isinstance(bits, bool):
        raise ExplorerError('status_list "bits" must be an integer')
    return bits, claim.get("lst")


def _from_lst(
    format_name: str,
    header: dict[str, Any],
    payload: dict[str, Any],
    compressed: bytes,
    bits: int,
) -> ExploredStatusList:
    if bits not in ALLOWED_BITS:
        allowed = ", ".join(str(value) for value in sorted(ALLOWED_BITS))
        raise ExplorerError(f"bits must be one of {allowed}: {bits}")
    inflated = _inflate(compressed)
    return ExploredStatusList(
        format=format_name,
        header=header,
        payload=payload,
        bits=bits,
        compressed_bytes=len(compressed),
        inflated_bytes=len(inflated),
        statuses=unpack_status_values(inflated, bits=bits),
    )


def _inflate(compressed: bytes) -> bytes:
    inflater = zlib.decompressobj()
    try:
        inflated = inflater.decompress(compressed, MAX_INFLATED_BYTES)
    except zlib.error as exc:
        raise ExplorerError(f"lst is not zlib/DEFLATE data: {exc}") from exc
    if inflater.unconsumed_tail:
        raise ExplorerError(f"lst inflates beyond {MAX_INFLATED_BYTES} bytes")
    if not inflater.eof:
        raise ExplorerError("lst is truncated: the zlib stream does not end")
    return inflated


def _candidate_bytes(value: str) -> list[bytes]:
    candidates = []
    if _HEX.match(value):
        candidates.append(bytes.fromhex(value))
    try:
        candidates.append(_base64url_bytes(value))
    except ExplorerError:
        pass
    return candidates


def _base64url_bytes(value: str) -> bytes:
    normalized = value.strip().rstrip("=").replace("+", "-").replace("/", "_")
    try:
        return base64url_decode(normalized)
    except (binascii.Error, ValueError) as exc:
        raise ExplorerError("value is not base64url encoded") from exc


def _json_safe(value: Any) -> Any:
    """Render CBOR values as JSON; byte strings use CBOR diagnostic ``h'…'``."""
    if isinstance(value, bytes):
        return f"h'{value.hex()}'"
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, _CborTag):
        return {"tag": value.number, "value": _json_safe(value.value)}
    return value


__all__ = [
    "MAX_INFLATED_BYTES",
    "ExploredStatusList",
    "ExplorerError",
    "explore_status_list",
]
