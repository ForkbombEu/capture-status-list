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


def test_rich_seed_creates_mixed_pools_and_verification_states() -> None:
    result = seed_server(client, base_url="", prefix="rich", rich=True)

    assert result == {
        "created": 24,
        "revoked": 4,
        "accepted": 6,
        "rejected": 2,
    }
    summaries = client.get("/debug/status-lists").json()
    assert {summary["country"] for summary in summaries} == {"EU", "DE", "PT", "NL"}
    assert any(summary["expired"] for summary in summaries)
    assert any(not summary["expired"] for summary in summaries)
    credentials = client.get("/credentials").json()["credentials"]
    assert any(item["verification_result"] == "ACCEPT" for item in credentials)
    assert any(item["verification_result"] == "REJECT" for item in credentials)
    assert any(item["verification_result"] is None for item in credentials)
