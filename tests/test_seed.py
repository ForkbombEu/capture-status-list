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
    statuses = [c["status"] for c in listed]
    assert statuses.count("REVOKED") == 3
    assert statuses.count("VALID") == 5
