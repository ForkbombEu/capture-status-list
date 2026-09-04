from fastapi.testclient import TestClient

from app import app
from issuer import reset_state


client = TestClient(app)


def setup_function() -> None:
    reset_state()


def test_red_route_serves_lean_ui() -> None:
    response = client.get("/red")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Credimi TSL console" in response.text
    assert "/design-assets/assets/credimi_logo.svg" in response.text
    assert "Token Status List console" in response.text
    assert "/credentials/random-batch" in response.text
    assert "/verify-batch" in response.text


def test_credimi_logo_asset_is_served() -> None:
    response = client.get("/design-assets/assets/credimi_logo.svg")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")


def test_random_batch_create_lists_credentials() -> None:
    response = client.post(
        "/credentials/random-batch",
        json={"count": 3, "prefix": "demo"},
    )

    assert response.status_code == 200
    created = response.json()["created"]
    assert len(created) == 3
    assert [credential["idx"] for credential in created] == [42, 43, 44]
    assert all(
        credential["credential_id"].startswith("demo-") for credential in created
    )

    listed = client.get("/credentials").json()["credentials"]

    assert [credential["idx"] for credential in listed] == [42, 43, 44]
    assert {credential["status"] for credential in listed} == {"VALID"}


def test_batch_revoke_and_verify_selected_credentials() -> None:
    created = client.post(
        "/credentials/random-batch",
        json={"count": 3, "prefix": "demo"},
    ).json()["created"]
    credential_ids = [credential["credential_id"] for credential in created]

    revoked = client.post(
        "/credentials/revoke-batch",
        json={"credential_ids": credential_ids[:2] + ["missing"]},
    ).json()

    assert [item["credential_id"] for item in revoked["revoked"]] == credential_ids[:2]
    assert revoked["errors"] == [
        {"credential_id": "missing", "error": "'unknown credential: missing'"}
    ]

    verified = client.post(
        "/verify-batch",
        json={"credential_ids": credential_ids},
    ).json()["verified"]

    assert [item["result"] for item in verified] == ["REJECT", "REJECT", "ACCEPT"]
    assert [item["status"] for item in verified] == ["REVOKED", "REVOKED", "VALID"]
