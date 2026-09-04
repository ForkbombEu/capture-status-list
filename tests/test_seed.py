from fastapi.testclient import TestClient

from app import app
from issuer import reset_state
from seed import seed_server


client = TestClient(app)


def setup_function() -> None:
    reset_state()


def test_seed_server_creates_revokes_and_verifies_demo_data() -> None:
    result = seed_server(
        client,
        base_url="",
        count=8,
        prefix="seed",
        revoke_count=3,
    )

    assert result == {
        "created": 8,
        "revoked": 3,
        "accepted": 5,
        "rejected": 3,
    }

    listed = client.get("/credentials").json()["credentials"]

    assert len(listed) == 8
    assert [credential["status"] for credential in listed[:3]] == [
        "REVOKED",
        "REVOKED",
        "REVOKED",
    ]
    assert {credential["status"] for credential in listed[3:]} == {"VALID"}
