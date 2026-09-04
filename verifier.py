from __future__ import annotations

import jwt

from issuer import STATUS_LIST_URI, public_key_pem
from status_list import STATUS_INVALID, STATUS_VALID, read_encoded_status, status_label


class VerificationError(ValueError):
    pass


def check_status(
    idx: int,
    status_list_token: str,
    *,
    expected_subject: str = STATUS_LIST_URI,
    public_key: str | None = None,
) -> str:
    payload = decode_status_list_token(
        status_list_token,
        expected_subject=expected_subject,
        public_key=public_key,
    )
    status_list = payload.get("status_list")
    if not isinstance(status_list, dict):
        raise VerificationError("missing status_list claim")

    bits = status_list.get("bits")
    encoded_list = status_list.get("lst")
    if not isinstance(bits, int) or not isinstance(encoded_list, str):
        raise VerificationError("invalid status_list claim")

    value = read_encoded_status(encoded_list, idx, bits=bits)
    if value not in {STATUS_VALID, STATUS_INVALID}:
        raise VerificationError(f"unsupported EUDI status value: {value}")
    return status_label(value)


def decode_status_list_token(
    status_list_token: str,
    *,
    expected_subject: str = STATUS_LIST_URI,
    public_key: str | None = None,
) -> dict:
    try:
        header = jwt.get_unverified_header(status_list_token)
        if header.get("typ") != "statuslist+jwt":
            raise VerificationError("JWT typ must be statuslist+jwt")

        payload = jwt.decode(
            status_list_token,
            public_key or public_key_pem(),
            algorithms=["ES256"],
            options={"require": ["sub", "iat", "exp", "status_list"]},
        )
    except VerificationError:
        raise
    except jwt.PyJWTError as exc:
        raise VerificationError(f"status list token verification failed: {exc}") from exc

    if payload.get("sub") != expected_subject:
        raise VerificationError("status list token subject does not match URI")
    return payload
