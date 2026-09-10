import datetime
from urllib.parse import urlparse

import jwt
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID
from fastapi.testclient import TestClient

from app import app
from issuer import reset_eudi_registry, reset_state
from status_list import generate_status_list_token
from verifier import VerificationError, check_status


client = TestClient(app)


def setup_function() -> None:
    reset_state()
    reset_eudi_registry()


def test_tsl_002_revoked_credential() -> None:
    created = client.post("/credentials", json={"credential_id": "cred-001"}).json()
    client.post("/credentials/cred-001/revoke")

    token = client.get("/status/1").text

    assert check_status(created["idx"], token) == "REVOKED"


def test_tsl_004_jwt_signature_validation() -> None:
    token = client.get("/status/1").text
    header, payload, signature = token.split(".")
    replacement = "A" if payload[-1] != "A" else "B"
    tampered = f"{header}.{payload[:-1]}{replacement}.{signature}"

    try:
        check_status(42, tampered)
    except VerificationError:
        pass
    else:
        raise AssertionError("expected signature verification to fail")


def test_tsl_008_revocation_propagation() -> None:
    created = client.post("/credentials", json={"credential_id": "cred-001"}).json()
    before_token = client.get("/status/1").text

    client.post("/credentials/cred-001/revoke")
    after_token = client.get("/status/1").text

    assert check_status(created["idx"], before_token) == "VALID"
    assert check_status(created["idx"], after_token) == "REVOKED"


def test_verify_endpoint_rejects_revoked_credential() -> None:
    created = client.post("/credentials", json={"credential_id": "cred-001"}).json()
    client.post("/credentials/cred-001/revoke")

    response = client.post("/verify/cred-001")

    assert response.status_code == 200
    assert response.json() == {
        "credential_id": "cred-001",
        "idx": created["idx"],
        "result": "REJECT",
        "status": "REVOKED",
    }


def _write_country_material(key_dir, country: str) -> tuple[str, bytes]:
    """Write a self-signed signer certificate; return (key PEM, cert DER)."""

    key = ec.generate_private_key(ec.SECP256R1())
    subject = x509.Name(
        [x509.NameAttribute(NameOID.COMMON_NAME, f"{country} status list")]
    )
    now = datetime.datetime.now(datetime.timezone.utc)
    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=30))
        .sign(key, hashes.SHA256())
    )
    key_pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode("ascii")
    certificate_der = certificate.public_bytes(serialization.Encoding.DER)
    (key_dir / f"{country}.key.pem").write_text(key_pem, encoding="ascii")
    (key_dir / f"{country}.cert.der").write_bytes(certificate_der)
    return key_pem, certificate_der


def test_eudi_status_list_token_verifies_with_its_x5c_certificate(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("EUDI_KEY_DIR", str(tmp_path))
    _write_country_material(tmp_path, "EU")

    reference = client.post(
        "/token_status_list/take",
        headers={"X-Api-Key": "test"},
        data={
            "country": "EU",
            "doctype": "org.iso.18013.5.1.mDL",
            "expiry_date": "2099-12-31",
        },
    ).json()
    uri = reference["status_list"]["uri"]
    idx = reference["status_list"]["idx"]
    token = client.get(
        urlparse(uri).path, headers={"Accept": "application/statuslist+jwt"}
    ).text

    header = jwt.get_unverified_header(token)
    assert header["kid"] == "EU-status-list"
    assert header["x5c"]
    # EUDI lists are served without exp; the verifier must not require it.
    assert "exp" not in jwt.decode(token, options={"verify_signature": False})

    assert check_status(idx, token, expected_subject=uri) == "VALID"

    client.post(
        "/token_status_list/set",
        headers={"X-Api-Key": "test"},
        data={"uri": uri, "idx": str(idx), "status": "1"},
    )
    revoked = client.get(
        urlparse(uri).path, headers={"Accept": "application/statuslist+jwt"}
    ).text
    assert check_status(idx, revoked, expected_subject=uri) == "REVOKED"


def test_token_signed_by_a_key_absent_from_x5c_is_rejected(tmp_path) -> None:
    signing_pem, _ = _write_country_material(tmp_path, "AA")
    _, foreign_certificate_der = _write_country_material(tmp_path, "BB")
    subject = (
        "http://localhost:8000/token_status_list/AA/mDL/"
        "00000000-0000-0000-0000-000000000000"
    )
    token = generate_status_list_token(
        [0] * 16,
        private_key_pem=signing_pem,
        issuer="http://localhost:8000",
        subject=subject,
        kid="AA-status-list",
        certificate_der=foreign_certificate_der,
    )

    try:
        check_status(0, token, expected_subject=subject)
    except VerificationError:
        pass
    else:
        raise AssertionError("expected signature verification to fail")


def test_malformed_x5c_header_is_rejected(tmp_path) -> None:
    signing_pem, _ = _write_country_material(tmp_path, "XX")
    token = generate_status_list_token(
        [0] * 16,
        private_key_pem=signing_pem,
        issuer="http://localhost:8000",
        subject="http://localhost:8000/status/1",
        kid="XX-status-list",
        certificate_der=b"not-a-der-certificate",
    )

    try:
        check_status(0, token)
    except VerificationError:
        pass
    else:
        raise AssertionError("expected malformed x5c to be rejected")
