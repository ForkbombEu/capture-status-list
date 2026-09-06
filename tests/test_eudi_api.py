from urllib.parse import urlparse

import jwt
from fastapi.testclient import TestClient

from app import app
from cwt_codec import decode_cwt
from issuer import public_key_pem, reset_eudi_registry, reset_state


client = TestClient(app)


def setup_function() -> None:
    reset_state()
    reset_eudi_registry()


def take() -> dict:
    response = client.post(
        "/token_status_list/take",
        headers={"X-Api-Key": "test"},
        data={
            "country": "EU",
            "doctype": "org.iso.18013.5.1.mDL",
            "expiry_date": "2099-12-31",
        },
    )
    assert response.status_code == 200
    return response.json()


def local_path(uri: str) -> str:
    return urlparse(uri).path


def test_take_creates_paired_country_doctype_references() -> None:
    reference = take()

    assert set(reference) == {"status_list", "identifier_list"}
    assert "/token_status_list/EU/org.iso.18013.5.1.mDL/" in reference["status_list"]["uri"]
    assert "/identifier_list/EU/org.iso.18013.5.1.mDL/" in reference["identifier_list"]["uri"]
    assert reference["identifier_list"]["id"] == str(reference["status_list"]["idx"])


def test_status_list_jwt_and_cwt_share_the_same_list() -> None:
    reference = take()
    path = local_path(reference["status_list"]["uri"])

    jwt_response = client.get(path, headers={"Accept": "application/statuslist+jwt"})
    cwt_response = client.get(path, headers={"Accept": "application/statuslist+cwt"})

    jwt_payload = jwt.decode(jwt_response.text, options={"verify_signature": False})
    headers, cwt_payload = decode_cwt(cwt_response.content, public_key_pem())
    assert jwt_response.headers["content-type"].startswith("application/statuslist+jwt")
    assert headers[1] == -7
    assert headers[4] == b"1"
    assert headers[16] == "application/statuslist+cwt"
    assert cwt_payload[2] == reference["status_list"]["uri"]
    assert cwt_payload[65533]["bits"] == jwt_payload["status_list"]["bits"]
    assert cwt_payload[65533]["lst"]

def test_identifier_list_jwt_and_cwt_are_iso_18013_5_shaped() -> None:
    reference = take()
    path = local_path(reference["identifier_list"]["uri"])

    jwt_response = client.get(path, headers={"Accept": "application/identifierlist+jwt"})
    cwt_response = client.get(path, headers={"Accept": "application/identifierlist+cwt"})

    jwt_payload = jwt.decode(jwt_response.text, options={"verify_signature": False})
    _, cwt_payload = decode_cwt(cwt_response.content, public_key_pem())
    assert jwt_payload["sub"] == reference["identifier_list"]["uri"]
    assert jwt_payload["identifier_list"] == {}
    assert cwt_payload[1] == "http://localhost:8000"
    assert cwt_payload[2] == reference["identifier_list"]["uri"]
    assert cwt_payload[65533] == {}


def test_set_updates_token_and_identifier_lists() -> None:
    reference = take()
    token_uri = reference["status_list"]["uri"]
    identifier_uri = reference["identifier_list"]["uri"]
    idx = str(reference["status_list"]["idx"])

    response = client.post(
        "/token_status_list/set",
        headers={"X-Api-Key": "test"},
        data={"uri": token_uri, "idx": idx, "status": "1"},
    )

    assert response.status_code == 200
    assert response.text == "Status Changed\n"
    assert client.get("/token_status_list/get", params={"uri": token_uri, "idx": idx}).text == "1"
    assert client.get("/identifier_list/get", params={"uri": identifier_uri, "id": idx}).text == "1"


def test_new_country_doctype_gets_a_distinct_uuid_list() -> None:
    first = take()
    second = client.post(
        "/token_status_list/take",
        headers={"X-Api-Key": "test"},
        data={"country": "DE", "doctype": "urn:eudi:pid:1", "expiry_date": "2099-12-31"},
    ).json()

    assert first["status_list"]["uri"] != second["status_list"]["uri"]
    summaries = client.get("/debug/status-lists").json()
    assert len(summaries) == 2
    assert {summary["country"] for summary in summaries} == {"EU", "DE"}

def test_debugger_batch_populates_and_revokes_pooled_list() -> None:
    response = client.post(
        "/credentials/random-batch",
        json={
            "count": 3,
            "prefix": "pool",
            "country": "DE",
            "doctype": "org.iso.18013.5.1.mDL",
            "expiry_date": "2099-12-31",
        },
    )
    created = response.json()["created"]
    summary = client.get("/debug/status-lists").json()[0]
    assert response.status_code == 200
    assert summary["country"] == "DE"
    assert summary["allocated"] == 3
    assert summary["revoked"] == 0

    client.post("/credentials/revoke-batch", json={"credential_ids": [item["credential_id"] for item in created]})

    assert client.get("/debug/status-lists").json()[0]["revoked"] == 3


def test_pooled_tokens_fall_back_to_local_test_key(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("EUDI_KEY_DIR", str(tmp_path))
    reference = take()
    response = client.get(
        local_path(reference["status_list"]["uri"]),
        headers={"Accept": "application/statuslist+jwt"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/statuslist+jwt")
