from __future__ import annotations

import base64

import jwt
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

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


def _x5c_public_key(header: dict) -> str | None:
    """Return the PEM public key of the signer certificate in the x5c header.

    EUDI Status List JWTs advertise their signing material in ``x5c``: the first
    entry is the signer certificate. Tokens served without a configured
    certificate, and the legacy ``/status/1`` token, carry no ``x5c`` and fall
    back to the local public key.
    """

    chain = header.get("x5c")
    if not isinstance(chain, list) or not chain:
        return None
    leaf = chain[0]
    if not isinstance(leaf, str):
        raise VerificationError("x5c header must contain base64 DER certificates")
    try:
        certificate = x509.load_der_x509_certificate(
            base64.b64decode(leaf, validate=True)
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError(f"invalid x5c certificate: {exc}") from exc
    return (
        certificate.public_key()
        .public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
        .decode("ascii")
    )


def _required_claims(status_list_token: str) -> list[str]:
    """Require ``exp`` only when the token declares it.

    Country × doctype Token Status Lists are served without ``exp`` (see
    ``include_exp`` in :func:`issuer.build_eudi_token`), while the legacy mock
    list token always carries one. PyJWT validates a present ``exp`` regardless.
    """

    claims = jwt.decode(status_list_token, options={"verify_signature": False})
    required = ["sub", "iat", "status_list"]
    if "exp" in claims:
        required.append("exp")
    return required


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
            public_key or _x5c_public_key(header) or public_key_pem(),
            algorithms=["ES256"],
            options={"require": _required_claims(status_list_token)},
        )
    except VerificationError:
        raise
    except jwt.PyJWTError as exc:
        raise VerificationError(f"token verification failed: {exc}") from exc

    if payload.get("sub") != expected_subject:
        raise VerificationError("status list token subject does not match URI")
    return payload
