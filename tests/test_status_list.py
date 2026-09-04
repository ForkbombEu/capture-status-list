import jwt
from fastapi.testclient import TestClient

from app import app
from issuer import STATUS_LIST_URI, public_key_pem, reset_state
from status_list import (
    InvalidStatusListIndex,
    decode_status_list,
    encode_status_list,
    pack_status_values,
)
from verifier import check_status, decode_status_list_token


client = TestClient(app)


def setup_function() -> None:
    reset_state()


def test_tsl_001_valid_credential() -> None:
    created = client.post("/credentials", json={"credential_id": "cred-001"}).json()

    token = client.get("/status/1").text

    assert created["idx"] == 42
    assert check_status(created["idx"], token) == "VALID"


def test_tsl_003_only_one_credential_revoked() -> None:
    client.post("/credentials", json={"credential_id": "cred-A", "idx": 10})
    client.post("/credentials", json={"credential_id": "cred-B", "idx": 11})
    client.post("/credentials/cred-A/revoke")

    token = client.get("/status/1").text

    assert check_status(10, token) == "REVOKED"
    assert check_status(11, token) == "VALID"


def test_tsl_005_invalid_index() -> None:
    token = client.get("/status/1").text

    try:
        check_status(10_000, token)
    except InvalidStatusListIndex as exc:
        assert exc.idx == 10_000
    else:
        raise AssertionError("expected invalid index")


def test_tsl_006_status_list_compression_decompression() -> None:
    values = [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1]

    encoded = encode_status_list(values)
    decoded = decode_status_list(encoded, size=len(values))

    assert decoded == values
    assert pack_status_values(values) == bytes([0x9A, 0xA5])


def test_tsl_007_status_list_retrieval() -> None:
    response = client.get("/status/1")
    token = response.text

    payload = decode_status_list_token(token)

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/statuslist+jwt")
    assert jwt.get_unverified_header(token)["typ"] == "statuslist+jwt"
    assert payload["sub"] == STATUS_LIST_URI
    assert payload["status_list"]["bits"] == 1
    assert isinstance(payload["status_list"]["lst"], str)
    jwt.decode(token, public_key_pem(), algorithms=["ES256"])


def test_status_list_has_no_personal_identifiers() -> None:
    client.post("/credentials", json={"credential_id": "cred-private", "idx": 7})
    token = client.get("/status/1").text
    payload = decode_status_list_token(token)

    status_list = payload["status_list"]
    serialized_status_list = str(status_list).lower()

    assert set(status_list) == {"bits", "lst"}
    assert "name" not in serialized_status_list
    assert "email" not in serialized_status_list
    assert "date_of_birth" not in serialized_status_list
    assert "holder" not in serialized_status_list
    assert "cred-private" not in serialized_status_list


def test_status_indexes_are_not_global_user_identifiers() -> None:
    first = client.post(
        "/credentials",
        json={"credential_id": "cred-A", "idx": 20},
    ).json()
    second = client.post(
        "/credentials",
        json={"credential_id": "cred-B", "idx": 21},
    ).json()

    assert first["referenced_token_status"] != second["referenced_token_status"]
    assert set(first["referenced_token_status"]["status_list"]) == {"idx", "uri"}
    assert set(second["referenced_token_status"]["status_list"]) == {"idx", "uri"}
