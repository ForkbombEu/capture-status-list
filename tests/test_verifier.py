from fastapi.testclient import TestClient

from app import app
from issuer import reset_state
from verifier import VerificationError, check_status


client = TestClient(app)


def setup_function() -> None:
    reset_state()


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
    client.post("/credentials", json={"credential_id": "cred-001"})
    client.post("/credentials/cred-001/revoke")

    response = client.post("/verify/cred-001")

    assert response.status_code == 200
    assert response.json() == {
        "credential_id": "cred-001",
        "idx": 42,
        "result": "REJECT",
        "status": "REVOKED",
    }
