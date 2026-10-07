import json
import os
import subprocess
import sys
from urllib.parse import urlparse

import jwt
from fastapi.testclient import TestClient

from app import app
from cwt_codec import decode_cwt
from issuer import public_key_pem, reset_eudi_registry, reset_state
from verifier import check_status


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

def test_take_replays_same_allocation_id_without_consuming_an_index() -> None:
    first = client.post(
        "/token_status_list/take",
        headers={"X-Api-Key": "test"},
        data={
            "country": "EU",
            "doctype": "urn:eudi:pid:1",
            "expiry_date": "2099-12-31",
            "allocation_id": "retry-1",
        },
    )
    replay = client.post(
        "/token_status_list/take",
        headers={"X-Api-Key": "test"},
        data={
            "country": "EU",
            "doctype": "urn:eudi:pid:1",
            "expiry_date": "2099-12-31",
            "allocation_id": "retry-1",
        },
    )

    assert first.status_code == 200
    assert replay.status_code == 200
    assert replay.json() == first.json()
    assert client.get("/debug/status-lists").json()[0]["allocated"] == 1

    conflict = client.post(
        "/token_status_list/take",
        headers={"X-Api-Key": "test"},
        data={
            "country": "EU",
            "doctype": "urn:eudi:pid:1",
            "expiry_date": "2030-01-01",
            "allocation_id": "retry-1",
        },
    )
    assert conflict.status_code == 400
    assert "different parameters" in conflict.json()["detail"]

def test_take_is_documented_as_an_api_key_protected_form_operation() -> None:
    operation = client.get("/openapi.json").json()["paths"]["/token_status_list/take"]["post"]

    assert operation["security"] == [{"ApiKeyAuth": []}]
    assert operation["requestBody"]["required"] is True
    schema = operation["requestBody"]["content"]["application/x-www-form-urlencoded"]["schema"]
    assert schema["required"] == ["country", "doctype", "expiry_date"]
    assert set(schema["properties"]) == {"country", "doctype", "expiry_date"}

    security_scheme = client.get("/openapi.json").json()["components"]["securitySchemes"]["ApiKeyAuth"]
    assert security_scheme == {"type": "apiKey", "in": "header", "name": "X-Api-Key"}


def test_take_exposes_allocated_entries_in_the_credentials_data() -> None:
    reference = take()

    allocations = client.get("/credentials").json()["allocated_entries"]

    assert allocations == [
        {
            "country": "EU",
            "doctype": "org.iso.18013.5.1.mDL",
            "status_list_uri": reference["status_list"]["uri"],
            "identifier_list_uri": reference["identifier_list"]["uri"],
            "idx": reference["status_list"]["idx"],
            "expiry_date": "2099-12-31",
            "status": "VALID",
        }
    ]


def test_take_uses_configured_public_url() -> None:
    script = '''
import json
from fastapi.testclient import TestClient
from app import app
from urllib.parse import urlparse

client = TestClient(app)
response = client.post(
    "/token_status_list/take",
    headers={"X-Api-Key": "test"},
    data={
        "country": "EU",
        "doctype": "org.iso.18013.5.1.mDL",
        "expiry_date": "2099-12-31",
    },
)
reference = response.json()
path = urlparse(reference["status_list"]["uri"]).path
print(json.dumps({"reference": reference, "status_code": client.get(path).status_code}))
'''
    environment = os.environ | {
        "STATUS_LIST_PUBLIC_URL": "https://status.example.test/"
    }
    result = subprocess.run(
        [sys.executable, "-c", script],
        check=True,
        capture_output=True,
        env=environment,
        text=True,
    )
    output = json.loads(result.stdout)
    reference = output["reference"]

    assert reference["status_list"]["uri"].startswith(
        "https://status.example.test/token_status_list/"
    )
    assert reference["identifier_list"]["uri"].startswith(
        "https://status.example.test/identifier_list/"
    )
    assert output["status_code"] == 200


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


def test_dashboard_revokes_allocated_entry_without_an_api_key() -> None:
    reference = take()
    token_uri = reference["status_list"]["uri"]
    identifier_uri = reference["identifier_list"]["uri"]
    idx = reference["status_list"]["idx"]

    response = client.post(
        "/dashboard/allocated-entries/revoke",
        json={"status_list_uri": token_uri, "idx": idx},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status_list_uri": token_uri,
        "idx": idx,
        "status": "REVOKED",
    }
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



def test_local_mode_tokens_carry_x5c_and_verify_end_to_end(monkeypatch) -> None:
    monkeypatch.delenv("EUDI_KEY_DIR", raising=False)
    reference = take()
    uri = reference["status_list"]["uri"]
    idx = reference["status_list"]["idx"]

    token = client.get(
        local_path(uri), headers={"Accept": "application/statuslist+jwt"}
    ).text
    header = jwt.get_unverified_header(token)
    assert header["kid"] == "EU-status-list"
    assert header["x5c"]

    assert check_status(idx, token, expected_subject=uri) == "VALID"

    client.post(
        "/token_status_list/set",
        headers={"X-Api-Key": "test"},
        data={"uri": uri, "idx": str(idx), "status": "1"},
    )
    revoked = client.get(
        local_path(uri), headers={"Accept": "application/statuslist+jwt"}
    ).text
    assert check_status(idx, revoked, expected_subject=uri) == "REVOKED"


def test_debug_status_list_decodes_the_allocated_list_with_uri() -> None:
    reference = take()
    uri = reference["status_list"]["uri"]
    idx = reference["status_list"]["idx"]
    client.post(
        "/dashboard/allocated-entries/revoke",
        json={"status_list_uri": uri, "idx": idx},
    )

    decoded = client.get("/debug/status-list", params={"uri": uri}).json()

    assert decoded["list_uri"] == uri
    assert decoded["payload"]["sub"] == uri
    assert decoded["size"] == 10_000
    assert decoded["revoked"] == 1
    assert decoded["revoked_indices"] == [idx]
    # Allocations carry no credential identifier, so the console shows the
    # allocated-entry table instead of credential assignments.
    assert decoded["assignments"] == []
    assert decoded["assignment_total"] == 0
    assert decoded["jwks"]["keys"][0]["kid"] == decoded["header"]["kid"]


def test_debug_status_list_without_uri_still_decodes_the_legacy_list() -> None:
    created = client.post(
        "/credentials", json={"credential_id": "cred-001"}
    ).json()
    client.post("/credentials/cred-001/revoke")

    decoded = client.get("/debug/status-list").json()

    assert decoded["list_uri"].endswith("/status/1")
    assert decoded["payload"]["sub"] == decoded["list_uri"]
    assert decoded["revoked_indices"] == [created["idx"]]
    assert {item["credential_id"] for item in decoded["assignments"]} == {"cred-001"}


def test_debug_status_list_rejects_unknown_and_identifier_lists() -> None:
    reference = take()
    missing = "00000000-0000-0000-0000-000000000000"
    unknown_uri = reference["status_list"]["uri"].rsplit("/", 1)[0] + f"/{missing}"

    assert (
        client.get("/debug/status-list", params={"uri": unknown_uri}).status_code == 404
    )
    assert (
        client.get(
            "/debug/status-list", params={"uri": reference["identifier_list"]["uri"]}
        ).status_code
        == 400
    )
    assert (
        client.get(
            "/debug/status-list",
            params={"uri": "https://other.example/token_status_list/EU/mDL/x"},
        ).status_code
        == 400
    )


def _issuer_base(reference: dict) -> str:
    return reference["status_list"]["uri"].rsplit("/token_status_list/", 1)[0]


def test_status_list_aggregation_lists_every_status_list_token() -> None:
    reference = take()

    aggregation = client.get("/token_status_list/aggregation")

    assert aggregation.status_code == 200
    assert aggregation.headers["content-type"].startswith("application/json")
    assert aggregation.headers["cache-control"] == "no-store"
    assert aggregation.json() == {
        "status_lists": [
            f"{_issuer_base(reference)}/status/1",
            reference["status_list"]["uri"],
        ]
    }
    # Identifier lists are not Status List Tokens and must not be advertised.
    assert reference["identifier_list"]["uri"] not in aggregation.json()["status_lists"]
    # Every advertised URI has to resolve to a Status List Token.
    for uri in aggregation.json()["status_lists"]:
        assert (
            client.get(
                local_path(uri), headers={"accept": "application/statuslist+jwt"}
            ).status_code
            == 200
        )


def test_status_list_tokens_advertise_the_aggregation_uri() -> None:
    reference = take()
    aggregation_uri = f"{_issuer_base(reference)}/token_status_list/aggregation"

    legacy = jwt.decode(
        client.get(
            "/status/1", headers={"accept": "application/statuslist+jwt"}
        ).text,
        options={"verify_signature": False},
    )
    pool = jwt.decode(
        client.get(
            local_path(reference["status_list"]["uri"]),
            headers={"accept": "application/statuslist+jwt"},
        ).text,
        options={"verify_signature": False},
    )
    for payload in (legacy, pool):
        assert payload["status_list"]["aggregation_uri"] == aggregation_uri

    cwt = client.get(
        local_path(reference["status_list"]["uri"]),
        headers={"accept": "application/statuslist+cwt"},
    ).content
    _, cwt_payload = decode_cwt(cwt, public_key_pem())
    assert cwt_payload[65533]["aggregation_uri"] == aggregation_uri

    identifier_list = jwt.decode(
        client.get(
            local_path(reference["identifier_list"]["uri"]),
            headers={"accept": "application/identifierlist+jwt"},
        ).text,
        options={"verify_signature": False},
    )
    assert "aggregation_uri" not in identifier_list["identifier_list"]
