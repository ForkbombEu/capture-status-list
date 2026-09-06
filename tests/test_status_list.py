import jwt
from fastapi.testclient import TestClient

from app import app
from issuer import STATUS_LIST_URI, public_key_pem, reset_state
from status_list import (
    TOKEN_TTL_SECONDS,
    IndexScatter,
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

    assert 0 <= created["idx"] < 10_000
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


def test_debug_status_list_decodes_token_header_payload_and_lst() -> None:
    import jwt
    from fastapi.testclient import TestClient

    from app import app
    from issuer import reset_state

    client = TestClient(app)
    reset_state()
    client.post("/credentials", json={"credential_id": "cred-001", "idx": 5})
    client.post("/credentials", json={"credential_id": "cred-002", "idx": 6})
    client.post("/credentials/cred-001/revoke")
    decoded = client.get("/debug/status-list").json()

    assert decoded["warning"] == "TEST/DEBUG ONLY"
    assert decoded["token"].count(".") == 2
    assert decoded["header"] == {
        "alg": "ES256",
        "kid": "mock-eudi-status-list-1",
        "typ": "statuslist+jwt",
    }
    assert decoded["payload"]["sub"] == "http://localhost:8000/status/1"
    assert decoded["payload"]["status_list"]["bits"] == 1
    assert decoded["bits"] == 1
    assert decoded["size"] == 10000
    assert decoded["revoked"] == 1
    assert decoded["valid"] == 9999
    assignments = decoded["assignments"]
    revoked = next(a for a in assignments if a["status"] == "REVOKED")
    valid = next(a for a in assignments if a["status"] == "VALID")
    assert decoded["revoked_indices"] == [revoked["idx"]]
    assert {a["credential_id"] for a in assignments} == {"cred-001", "cred-002"}
    assert revoked["credential_id"] == "cred-001"
    lst = decoded["lst"]
    assert lst["entries"] == 10000
    assert lst["inflated_bytes"] == 1250
    assert lst["compressed_bytes"] < lst["inflated_bytes"]
    assert lst["chars_per_entry"] == 1
    assert lst["window_size"] == 256
    assert len(lst["window"]) == 256
    start = lst["window_start"]
    assert start == 0
    assert lst["window"][revoked["idx"] - start] == "1"
    assert lst["window"][valid["idx"] - start] == "0"
    assert set(lst["window"]) == {"0", "1"}

    assert decoded["jwks"]["keys"][0]["kid"] == "mock-eudi-status-list-1"
    # ES256 signatures are randomized and each call re-issues the token, so
    # compare the encoded list rather than the token bytes.
    served = client.get(
        "/status/1", headers={"accept": "application/statuslist+jwt"}
    ).text.strip('"')
    served_payload = jwt.decode(served, options={"verify_signature": False})
    assert served_payload["status_list"] == decoded["payload"]["status_list"]


def test_index_scatter_is_bijective_deterministic_and_nonsequential() -> None:
    size = 1_000
    scatter = IndexScatter(size, seed=b"k" * 32)
    permuted = [scatter.permute(i) for i in range(size)]

    assert sorted(permuted) == list(range(size))
    assert permuted != list(range(size))
    again = IndexScatter(size, seed=b"k" * 32)
    assert [again.permute(i) for i in range(size)] == permuted


def test_index_scatter_varies_with_seed() -> None:
    first = IndexScatter(1_000, seed=b"a" * 32)
    second = IndexScatter(1_000, seed=b"b" * 32)

    assert [first.permute(i) for i in range(32)] != [
        second.permute(i) for i in range(32)
    ]


def test_index_scatter_rejects_out_of_domain_cursor() -> None:
    scatter = IndexScatter(1_000, seed=b"c" * 32)

    try:
        scatter.permute(1_000)
    except InvalidStatusListIndex:
        pass
    else:
        raise AssertionError("expected out-of-domain cursor to fail")


def test_status_list_token_sends_cache_headers() -> None:
    response = client.get("/status/1")

    assert response.status_code == 200
    assert response.headers["cache-control"] == f"max-age={TOKEN_TTL_SECONDS}"
    assert response.headers["etag"].startswith("W/")


def test_status_list_revalidates_with_etag() -> None:
    first = client.get("/status/1")

    cached = client.get("/status/1", headers={"If-None-Match": first.headers["etag"]})

    assert cached.status_code == 304
    assert cached.headers["etag"] == first.headers["etag"]


def test_status_list_etag_changes_on_revocation() -> None:
    client.post("/credentials", json={"credential_id": "cred-001"})
    first = client.get("/status/1")

    client.post("/credentials/cred-001/revoke")
    revalidated = client.get(
        "/status/1", headers={"If-None-Match": first.headers["etag"]}
    )

    assert revalidated.status_code == 200
    assert revalidated.headers["etag"] != first.headers["etag"]
