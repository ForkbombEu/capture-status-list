from __future__ import annotations

import os
import secrets
import time
import zlib
from dataclasses import dataclass
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from cwt_codec import (
    IDENTIFIER_LIST_CWT_MEDIA_TYPE,
    STATUS_LIST_CWT_MEDIA_TYPE,
    encode_cwt,
)
from key_material import material_for
from list_registry import IDENTIFIER_LIST_KIND, TOKEN_LIST_KIND, StatusListRegistry
from models import CredentialResponse, RevokeResponse
from status_list import (
    DEFAULT_BITS,
    DEFAULT_STATUS_LIST_SIZE,
    STATUS_INVALID,
    STATUS_VALID,
    IndexScatter,
    InvalidStatusListIndex,
    generate_identifier_list_token,
    generate_status_list_token,
    pack_status_values,
    status_label,
)


ISSUER = (
    os.environ.get("STATUS_LIST_PUBLIC_URL") or "http://localhost:8000"
).rstrip("/")
STATUS_LIST_URI = f"{ISSUER}/status/1"
KEY_ID = "mock-eudi-status-list-1"
INDEX_CURSOR_START = 42
KEYS_DIR = Path(__file__).resolve().parent / "keys"
PRIVATE_KEY_PATH = KEYS_DIR / "private.pem"
PUBLIC_KEY_PATH = KEYS_DIR / "public.pem"


eudi_registry = StatusListRegistry(ISSUER)


@dataclass(frozen=True)
class CredentialRecord:
    credential_id: str
    idx: int
    status_list_uri: str = STATUS_LIST_URI
    eudi_status_list_uri: str | None = None
    eudi_idx: int | None = None
    def status_reference(self) -> dict[str, dict[str, int | str]]:
        return {
            "status_list": {
                "idx": self.idx,
                "uri": self.status_list_uri,
            }
        }


class TestKeyStore:
    def __init__(self) -> None:
        self._private_key = None

    def private_key(self):
        if self._private_key is None:
            self._private_key = self._load_or_create_private_key()
        return self._private_key

    def private_pem(self) -> str:
        return (
            self.private_key()
            .private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
            .decode("ascii")
        )

    def public_pem(self) -> str:
        return (
            self.private_key()
            .public_key()
            .public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            .decode("ascii")
        )

    def jwks(self) -> dict[str, list[dict[str, str]]]:
        numbers = self.private_key().public_key().public_numbers()
        return {
            "keys": [
                {
                    "kty": "EC",
                    "crv": "P-256",
                    "kid": KEY_ID,
                    "use": "sig",
                    "alg": "ES256",
                    "x": _base64url_uint(numbers.x, 32),
                    "y": _base64url_uint(numbers.y, 32),
                }
            ]
        }

    def _load_or_create_private_key(self):
        if PRIVATE_KEY_PATH.exists():
            return serialization.load_pem_private_key(
                PRIVATE_KEY_PATH.read_bytes(),
                password=None,
            )

        KEYS_DIR.mkdir(parents=True, exist_ok=True)
        key = ec.generate_private_key(ec.SECP256R1())
        PRIVATE_KEY_PATH.write_bytes(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
        os.chmod(PRIVATE_KEY_PATH, 0o600)
        PUBLIC_KEY_PATH.write_bytes(
            key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
        return key


class InMemoryIssuer:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.statuses = [STATUS_VALID] * DEFAULT_STATUS_LIST_SIZE
        self.credentials: dict[str, CredentialRecord] = {}
        self.verification_results: dict[str, str] = {}
        self._cursor = INDEX_CURSOR_START
        self._scatter = IndexScatter(
            DEFAULT_STATUS_LIST_SIZE, seed=secrets.token_bytes(32)
        )
        self.version = 0

    def create_credential(
        self,
        credential_id: str,
        idx: int | None = None,
        eudi_reference: tuple[str, int] | None = None,
    ) -> CredentialResponse:
        if credential_id in self.credentials:
            raise KeyError(f"credential already exists: {credential_id}")

        assigned_idx = idx if idx is not None else self._next_unused_idx()
        self._validate_unused_idx(assigned_idx)

        record = CredentialRecord(
            credential_id=credential_id,
            idx=assigned_idx,
            eudi_status_list_uri=eudi_reference[0] if eudi_reference else None,
            eudi_idx=eudi_reference[1] if eudi_reference else None,
        )
        self.credentials[credential_id] = record
        return CredentialResponse(
            credential_id=record.credential_id,
            idx=record.idx,
            status_list_uri=record.status_list_uri,
            referenced_token_status=record.status_reference(),
        )

    def revoke_credential(self, credential_id: str) -> RevokeResponse:
        record = self.get_credential(credential_id)
        self.statuses[record.idx] = STATUS_INVALID
        if record.eudi_status_list_uri is not None and record.eudi_idx is not None:
            eudi_registry.set_status(record.eudi_status_list_uri, record.eudi_idx)
        self.version += 1
        return RevokeResponse(
            credential_id=record.credential_id,
            idx=record.idx,
            status="REVOKED",
        )

    def get_credential(self, credential_id: str) -> CredentialRecord:
        try:
            return self.credentials[credential_id]
        except KeyError as exc:
            raise KeyError(f"unknown credential: {credential_id}") from exc

    def debug_status(self, idx: int) -> str:
        if idx < 0 or idx >= len(self.statuses):
            raise InvalidStatusListIndex(idx, len(self.statuses))
        return status_label(self.statuses[idx])

    def mark_verification(self, credential_id: str, result: str) -> None:
        self.verification_results[credential_id] = result

    def verification_result(self, credential_id: str) -> str | None:
        return self.verification_results.get(credential_id)

    def status_list_token(self, private_key_pem: str) -> str:
        return generate_status_list_token(
            self.statuses,
            private_key_pem=private_key_pem,
            issuer=ISSUER,
            subject=STATUS_LIST_URI,
            kid=KEY_ID,
            bits=DEFAULT_BITS,
        )


    def _next_unused_idx(self) -> int:
        used = {record.idx for record in self.credentials.values()}
        while True:
            idx = self._scatter.permute(self._cursor)
            self._cursor += 1
            if idx not in used:
                return idx


    def _validate_unused_idx(self, idx: int) -> None:
        if idx < 0 or idx >= len(self.statuses):
            raise ValueError(
                f"idx must be between 0 and {len(self.statuses) - 1}: {idx}"
            )
        if any(record.idx == idx for record in self.credentials.values()):
            raise KeyError(f"idx already assigned: {idx}")


def _base64url_uint(value: int, size: int) -> str:
    from status_list import base64url_encode

    return base64url_encode(value.to_bytes(size, "big"))


key_store = TestKeyStore()
issuer_state = InMemoryIssuer()


def create_credential_record(
    credential_id: str,
    idx: int | None = None,
    eudi_reference: tuple[str, int] | None = None,
) -> CredentialResponse:
    return issuer_state.create_credential(
        credential_id, idx=idx, eudi_reference=eudi_reference
    )


def revoke_credential_record(credential_id: str) -> RevokeResponse:
    return issuer_state.revoke_credential(credential_id)


def mark_credential_verification(credential_id: str, result: str) -> None:
    issuer_state.mark_verification(credential_id, result)


def credential_verification_result(credential_id: str) -> str | None:
    return issuer_state.verification_result(credential_id)


def get_credential_record(credential_id: str) -> CredentialRecord:
    return issuer_state.get_credential(credential_id)


def list_credential_records() -> list[CredentialRecord]:
    return sorted(issuer_state.credentials.values(), key=lambda record: record.idx)


def debug_status_at(idx: int) -> str:
    return issuer_state.debug_status(idx)


def generate_current_status_list_token() -> str:
    return issuer_state.status_list_token(key_store.private_pem())


def list_version() -> int:
    return issuer_state.version


def public_jwks() -> dict[str, list[dict[str, str]]]:
    return key_store.jwks()


def public_key_pem() -> str:
    return key_store.public_pem()


def reset_state() -> None:
    issuer_state.reset()
    eudi_registry.reset()


def take_eudi_reference(country: str, doctype: str, expiry_date: str):
    return eudi_registry.take(country, doctype, expiry_date)


def eudi_status_at(uri: str, idx: int) -> int:
    return eudi_registry.status_at(uri, idx)


def set_eudi_status(uri: str, idx: int, value: int = 1):
    return eudi_registry.set_status(uri, idx, value)


def eudi_list_summaries():
    return eudi_registry.list_summaries()


def build_eudi_token(uri: str, format_name: str) -> tuple[bytes | str, str, int]:
    kind, state = eudi_registry.get_by_uri(uri)
    material = material_for(state.country)
    try:
        private_pem = material.private_pem
    except FileNotFoundError:
        # Local/CI debugger runs may not have operator country keys mounted.
        # Reuse the ignored legacy test key rather than failing a public test
        # endpoint; production deployments should provide EUDI_KEY_DIR.
        private_pem = key_store.private_pem()
    certificate = material.certificate_der
    now = int(time.time())
    if kind == TOKEN_LIST_KIND:
        if format_name == "jwt":
            token = generate_status_list_token(
                state.statuses,
                private_key_pem=private_pem,
                issuer=ISSUER,
                subject=uri,
                kid=material.kid,
                certificate_der=certificate,
                include_exp=False,
            )
        else:
            compressed = zlib.compress(pack_status_values(state.statuses), level=9)
            payload = {
                2: uri,
                6: now,
                65534: 3600,
                65533: {"bits": DEFAULT_BITS, "lst": compressed},
            }
            token = encode_cwt(
                payload,
                private_pem,
                STATUS_LIST_CWT_MEDIA_TYPE,
                certificate,
            )
            return token, STATUS_LIST_CWT_MEDIA_TYPE, state.version
        return token, "application/statuslist+jwt", state.version

    if format_name == "jwt":
        token = generate_identifier_list_token(
            state.identifiers,
            private_key_pem=private_pem,
            issuer=ISSUER.rstrip("/"),
            subject=uri,
            kid=material.kid,
            certificate_der=certificate,
        )
    else:
        payload = {1: ISSUER.rstrip("/"), 2: uri, 6: now, 65533: state.identifiers}
        token = encode_cwt(
            payload,
            private_pem,
            IDENTIFIER_LIST_CWT_MEDIA_TYPE,
            certificate,
        )
        return token, IDENTIFIER_LIST_CWT_MEDIA_TYPE, state.version
    return token, "application/identifierlist+jwt", state.version


def reset_eudi_registry() -> None:
    eudi_registry.reset()
