import json
import os
import subprocess
import sys
import zlib
from urllib.parse import urlparse

import jwt
import pytest
from fastapi.testclient import TestClient

import app as server
from cwt_codec import decode_cwt
from issuer import public_key_pem, reset_state
from status_list import TOKEN_TTL_SECONDS, read_encoded_status, read_packed_status


client = TestClient(server.app)

T0 = 1_800_000_000
STATUS_JWT = "application/statuslist+jwt"
STATUS_CWT = "application/statuslist+cwt"
IDENTIFIER_JWT = "application/identifierlist+jwt"
IDENTIFIER_CWT = "application/identifierlist+cwt"


def setup_function() -> None:
    reset_state()


@pytest.fixture
def clock(monkeypatch) -> list[int]:
    now = [T0]
    monkeypatch.setattr(server, "_unix_now", lambda: now[0])
    return now


def _take() -> dict:
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


def _path(list_key: str | None) -> str:
    if list_key is None:
        return "/status/1"
    return urlparse(_take()[list_key]["uri"]).path


def _payload(response) -> dict:
    if "+cwt" in response.headers["content-type"]:
        _, payload = decode_cwt(response.content, public_key_pem())
        return payload
    return jwt.decode(response.text, options={"verify_signature": False})


def _lifetime(response) -> tuple[int, int, int]:
    """Return (iat, exp, ttl) for a JWT or CWT list token."""
    payload = _payload(response)
    if "+cwt" in response.headers["content-type"]:
        return payload[6], payload[4], payload[65534]
    return payload["iat"], payload["exp"], payload["ttl"]


def _status(response, idx: int) -> int:
    payload = _payload(response)
    if "+cwt" in response.headers["content-type"]:
        status_list = payload[65533]
        packed = zlib.decompress(status_list["lst"])
        return read_packed_status(packed, idx, bits=status_list["bits"])
    status_list = payload["status_list"]
    return read_encoded_status(status_list["lst"], idx, bits=status_list["bits"])


@pytest.mark.parametrize(
    ("list_key", "accept"),
    [
        (None, STATUS_JWT),
        ("status_list", STATUS_JWT),
        ("status_list", STATUS_CWT),
        ("identifier_list", IDENTIFIER_JWT),
        ("identifier_list", IDENTIFIER_CWT),
    ],
)
def test_every_freshness_signal_ends_at_exp(clock, list_key, accept) -> None:
    response = client.get(_path(list_key), headers={"Accept": accept})

    assert response.status_code == 200
    assert _lifetime(response) == (T0, T0 + TOKEN_TTL_SECONDS, TOKEN_TTL_SECONDS)
    assert response.headers["cache-control"] == f"max-age={TOKEN_TTL_SECONDS}"


@pytest.mark.parametrize(
    ("list_key", "accept"),
    [(None, STATUS_JWT), ("status_list", STATUS_JWT), ("status_list", STATUS_CWT)],
)
def test_revalidation_confirms_a_cached_token_only_until_its_exp(
    clock, list_key, accept
) -> None:
    path = _path(list_key)
    etag = client.get(path, headers={"Accept": accept}).headers["etag"]

    clock[0] = T0 + TOKEN_TTL_SECONDS - 1
    confirmed = client.get(path, headers={"Accept": accept, "If-None-Match": etag})

    assert confirmed.status_code == 304
    assert confirmed.headers["etag"] == etag
    assert confirmed.headers["cache-control"] == "max-age=1"

    clock[0] = T0 + TOKEN_TTL_SECONDS
    refreshed = client.get(path, headers={"Accept": accept, "If-None-Match": etag})

    assert refreshed.status_code == 200
    assert _lifetime(refreshed)[1] == T0 + 2 * TOKEN_TTL_SECONDS


@pytest.mark.parametrize("accept", [STATUS_JWT, STATUS_CWT])
def test_revocation_reaches_a_consumer_that_cached_the_list_before_it(
    clock, accept
) -> None:
    reference = _take()
    uri = reference["status_list"]["uri"]
    idx = reference["status_list"]["idx"]
    path = urlparse(uri).path
    before = client.get(path, headers={"Accept": accept})
    assert _status(before, idx) == 0

    clock[0] = T0 + 1
    client.post(
        "/token_status_list/set",
        headers={"X-Api-Key": "test"},
        data={"uri": uri, "idx": str(idx), "status": "1"},
    )
    after = client.get(
        path, headers={"Accept": accept, "If-None-Match": before.headers["etag"]}
    )

    assert after.status_code == 200
    assert _status(after, idx) == 1


def test_a_cached_jwt_does_not_revalidate_the_cwt_representation(clock) -> None:
    path = _path("status_list")
    jwt_etag = client.get(path, headers={"Accept": STATUS_JWT}).headers["etag"]

    cwt = client.get(path, headers={"Accept": STATUS_CWT, "If-None-Match": jwt_etag})

    assert cwt.status_code == 200
    assert cwt.headers["content-type"].startswith(STATUS_CWT)


def test_status_list_ttl_seconds_sets_the_token_lifetime() -> None:
    script = '''
import json
import jwt
from fastapi.testclient import TestClient
from app import app

response = TestClient(app).get("/status/1")
payload = jwt.decode(response.text, options={"verify_signature": False})
print(json.dumps({
    "lifetime": payload["exp"] - payload["iat"],
    "ttl": payload["ttl"],
    "cache_control": response.headers["cache-control"],
}))
'''
    result = subprocess.run(
        [sys.executable, "-c", script],
        check=True,
        capture_output=True,
        env=os.environ | {"STATUS_LIST_TTL_SECONDS": "120"},
        text=True,
    )

    assert json.loads(result.stdout) == {
        "lifetime": 120,
        "ttl": 120,
        "cache_control": "max-age=120",
    }


@pytest.mark.parametrize("value", ["0", "-5", "2m"])
def test_invalid_status_list_ttl_seconds_stops_startup(value) -> None:
    result = subprocess.run(
        [sys.executable, "-c", "import app"],
        capture_output=True,
        env=os.environ | {"STATUS_LIST_TTL_SECONDS": value},
        text=True,
    )

    assert result.returncode != 0
    assert "STATUS_LIST_TTL_SECONDS must be a positive integer" in result.stderr
