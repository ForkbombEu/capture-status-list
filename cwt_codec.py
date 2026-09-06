"""Dependency-light COSE_Sign1 / CWT codec.

The wire representation produced here is a deterministic CBOR tag 18 value:
``18([protected, unprotected, payload, signature])``.  The payload and the
protected header map are encoded canonically before the ES256 signature is
created. This codec intentionally implements the reference service's direct
protected-bytes plus payload-bytes signing contract and its small CBOR subset
instead of pulling in a general-purpose CBOR or COSE package.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
    encode_dss_signature,
)


STATUS_LIST_CWT_MEDIA_TYPE = "application/statuslist+cwt"
IDENTIFIER_LIST_CWT_MEDIA_TYPE = "application/identifierlist+cwt"
_COSE_SIGN1_TAG = 18
_ES256_COSE_ALG = -7


@dataclass(frozen=True)
class _CborTag:
    number: int
    value: Any


class _CborDecoder:
    """Small strict parser for the definite-length CBOR data model."""

    def __init__(self, data: bytes) -> None:
        self.data = data
        self.offset = 0

    def decode(self) -> Any:
        value = self._item()
        if self.offset != len(self.data):
            raise ValueError("trailing bytes after CBOR value")
        return value

    def _item(self) -> Any:
        if self.offset >= len(self.data):
            raise ValueError("truncated CBOR value")
        initial = self._byte()
        major = initial >> 5
        additional = initial & 0x1F

        if major in (0, 1):
            argument = self._argument(additional)
            return argument if major == 0 else -1 - argument
        if major == 2:
            return self._read_bytes(self._argument(additional))
        if major == 3:
            raw = self._read_bytes(self._argument(additional))
            try:
                return raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValueError("invalid UTF-8 in CBOR text string") from exc
        if major == 4:
            return [self._item() for _ in range(self._length(additional))]
        if major == 5:
            result: dict[Any, Any] = {}
            for _ in range(self._length(additional)):
                key = self._item()
                try:
                    duplicate = key in result
                except TypeError as exc:
                    raise ValueError("CBOR map key is not hashable") from exc
                if duplicate:
                    raise ValueError("duplicate CBOR map key")
                result[key] = self._item()
            return result
        if major == 6:
            return _CborTag(self._argument(additional), self._item())
        # Only the three JSON-compatible simple values are needed here.  In
        # particular, silently accepting a float would make canonicalisation
        # and the signed payload ambiguous.
        if additional == 20:
            return False
        if additional == 21:
            return True
        if additional == 22:
            return None
        raise ValueError("unsupported CBOR simple or floating-point value")

    def _length(self, additional: int) -> int:
        if additional == 31:
            raise ValueError("indefinite-length CBOR is not supported")
        return self._argument(additional)

    def _argument(self, additional: int) -> int:
        if additional < 24:
            return additional
        if additional == 24:
            return self._uint(1)
        if additional == 25:
            return self._uint(2)
        if additional == 26:
            return self._uint(4)
        if additional == 27:
            return self._uint(8)
        raise ValueError("invalid CBOR additional information")

    def _uint(self, width: int) -> int:
        if self.offset + width > len(self.data):
            raise ValueError("truncated CBOR argument")
        value = int.from_bytes(self.data[self.offset : self.offset + width], "big")
        self.offset += width
        return value

    def _byte(self) -> int:
        value = self.data[self.offset]
        self.offset += 1
        return value

    def _read_bytes(self, length: int) -> bytes:
        if self.offset + length > len(self.data):
            raise ValueError("truncated CBOR byte or text string")
        value = self.data[self.offset : self.offset + length]
        self.offset += length
        return value


def _encode_argument(major: int, value: int) -> bytes:
    if value < 0:
        raise ValueError("CBOR argument cannot be negative")
    if value < 24:
        return bytes([(major << 5) | value])
    if value <= 0xFF:
        return bytes([(major << 5) | 24, value])
    if value <= 0xFFFF:
        return bytes([(major << 5) | 25]) + value.to_bytes(2, "big")
    if value <= 0xFFFFFFFF:
        return bytes([(major << 5) | 26]) + value.to_bytes(4, "big")
    if value <= 0xFFFFFFFFFFFFFFFF:
        return bytes([(major << 5) | 27]) + value.to_bytes(8, "big")
    raise OverflowError("integer is too large for the supported CBOR form")


def _encode_cbor(value: Any) -> bytes:
    """Encode the supported CBOR data model using deterministic ordering."""

    if value is None:
        return b"\xf6"
    if value is False:
        return b"\xf4"
    if value is True:
        return b"\xf5"
    if isinstance(value, int):
        if value >= 0:
            return _encode_argument(0, value)
        magnitude = -1 - value
        return _encode_argument(1, magnitude)
    if isinstance(value, bytes):
        return _encode_argument(2, len(value)) + value
    if isinstance(value, str):
        encoded = value.encode("utf-8")
        return _encode_argument(3, len(encoded)) + encoded
    if isinstance(value, (list, tuple)):
        return _encode_argument(4, len(value)) + b"".join(
            _encode_cbor(item) for item in value
        )
    if isinstance(value, Mapping):
        # RFC 8949 deterministic maps sort by encoded key length, then by the
        # encoded key bytes.  Sorting Python keys directly is not sufficient:
        # CBOR maps may mix text, byte, and integer keys.
        encoded_items = [
            (_encode_cbor(key), _encode_cbor(item))
            for key, item in value.items()
        ]
        encoded_items.sort(key=lambda pair: (len(pair[0]), pair[0]))
        return _encode_argument(5, len(encoded_items)) + b"".join(
            key + item for key, item in encoded_items
        )
    if isinstance(value, _CborTag):
        return _encode_argument(6, value.number) + _encode_cbor(value.value)
    raise TypeError(f"unsupported value for canonical CBOR: {type(value).__name__}")


def _decode_cbor(data: bytes) -> Any:
    return _CborDecoder(data).decode()


def _pem_bytes(value: str | bytes | bytearray | memoryview) -> bytes:
    if isinstance(value, str):
        return value.encode("ascii")
    if isinstance(value, (bytes, bytearray, memoryview)):
        return bytes(value)
    raise TypeError("PEM key must be str or bytes")


def _private_key(private_key_pem: str | bytes) -> ec.EllipticCurvePrivateKey:
    key = serialization.load_pem_private_key(_pem_bytes(private_key_pem), password=None)
    if not isinstance(key, ec.EllipticCurvePrivateKey):
        raise TypeError("private key must be an EC key")
    if not isinstance(key.curve, ec.SECP256R1):
        raise ValueError("ES256 requires a P-256 private key")
    return key


def _public_key(public_key_pem: str | bytes) -> ec.EllipticCurvePublicKey:
    key = serialization.load_pem_public_key(_pem_bytes(public_key_pem))
    if not isinstance(key, ec.EllipticCurvePublicKey):
        raise TypeError("public key must be an EC key")
    if not isinstance(key.curve, ec.SECP256R1):
        raise ValueError("ES256 requires a P-256 public key")
    return key


def _sig_structure(protected: bytes, payload: bytes) -> bytes:
    # The reference implementation signs the two encoded COSE components
    # directly. Preserve that wire contract for interoperability.
    return protected + payload


def encode_cwt(
    payload: Mapping[Any, Any],
    private_key_pem: str | bytes,
    media_type: str,
    certificate_der: bytes | None = None,
) -> bytes:
    """Encode and ES256-sign a status/identifier-list CWT.

    ``payload`` is the CWT payload map.  Its keys are intentionally not
    interpreted: both status-list and identifier-list profiles can use their
    own registered numeric labels, while application/private claims can use
    text labels.  ``certificate_der``, when present, is carried as the COSE
    x5chain (label 33) protected header value.
    """

    if not isinstance(payload, Mapping):
        raise TypeError("CWT payload must be a map")
    if not isinstance(media_type, str):
        raise TypeError("media_type must be text")
    if certificate_der is not None and not isinstance(
        certificate_der, (bytes, bytearray, memoryview)
    ):
        raise TypeError("certificate_der must be bytes or None")

    protected_map: dict[int, Any] = {1: _ES256_COSE_ALG, 16: media_type}
    if certificate_der is not None:
        protected_map[33] = bytes(certificate_der)
    protected = _encode_cbor(protected_map)
    payload_bytes = _encode_cbor(payload)
    signature = _private_key(private_key_pem).sign(
        _sig_structure(protected, payload_bytes), ec.ECDSA(hashes.SHA256())
    )

    token = _CborTag(
        _COSE_SIGN1_TAG,
        [protected, {4: b"1"}, payload_bytes, signature],
    )
    return _encode_cbor(token)


def decode_cwt(
    token: bytes,
    public_key_pem: str | bytes,
) -> tuple[dict[Any, Any], dict[Any, Any]]:
    """Verify a COSE_Sign1 CWT and return its merged headers and payload map."""

    if not isinstance(token, (bytes, bytearray, memoryview)):
        raise TypeError("CWT token must be bytes")
    try:
        decoded = _decode_cbor(bytes(token))
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"invalid CWT CBOR: {exc}") from exc

    if not isinstance(decoded, _CborTag) or decoded.number != _COSE_SIGN1_TAG:
        raise ValueError("CWT must be a CBOR COSE_Sign1 tag 18")
    sign1 = decoded.value
    if not isinstance(sign1, list) or len(sign1) != 4:
        raise ValueError("COSE_Sign1 value must have four elements")
    protected, unprotected, payload_bytes, signature = sign1
    if not isinstance(protected, bytes):
        raise ValueError("COSE protected headers must be a byte string")
    if not isinstance(unprotected, dict):
        raise ValueError("COSE unprotected headers must be a map")
    if not isinstance(signature, bytes):
        raise ValueError("COSE_Sign1 signature must be a byte string")

    try:
        protected_headers = _decode_cbor(protected)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"invalid protected header CBOR: {exc}") from exc
    if not isinstance(protected_headers, dict):
        raise ValueError("protected headers must contain a CBOR map")
    if protected_headers.get(1) != _ES256_COSE_ALG:
        raise ValueError("CWT protected alg header must be -7 (ES256)")
    media_type = protected_headers.get(16)
    if not isinstance(media_type, str):
        raise ValueError("CWT protected media-type header is missing")
    if 33 in protected_headers and not isinstance(protected_headers[33], bytes):
        raise ValueError("CWT protected certificate header must be bytes")
    if any(key in unprotected for key in protected_headers):
        raise ValueError("COSE header parameter appears in both header maps")

    try:
        payload = _decode_cbor(payload_bytes)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"invalid CWT payload CBOR: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("CWT payload must be a CBOR map")

    if len(signature) == 64:
        r = int.from_bytes(signature[:32], "big")
        s = int.from_bytes(signature[32:], "big")
        signature_der = encode_dss_signature(r, s)
    else:
        signature_der = signature
    try:
        _public_key(public_key_pem).verify(
            signature_der,
            _sig_structure(protected, payload_bytes),
            ec.ECDSA(hashes.SHA256()),
        )
    except InvalidSignature as exc:
        raise ValueError("CWT ES256 signature verification failed") from exc

    headers = dict(protected_headers)
    headers.update(unprotected)
    return headers, payload


__all__ = [
    "IDENTIFIER_LIST_CWT_MEDIA_TYPE",
    "STATUS_LIST_CWT_MEDIA_TYPE",
    "decode_cwt",
    "encode_cwt",
]
