import base64
import json
import zlib
from urllib.parse import urlparse

import jwt
from fastapi.testclient import TestClient

from app import app
from issuer import reset_eudi_registry, reset_state
from status_list import encode_status_list
from status_list_explorer import MAX_INFLATED_BYTES


client = TestClient(app)


def setup_function() -> None:
    reset_state()
    reset_eudi_registry()


def explore(payload: str, bits: int = 1):
    return client.post("/debug/status-list/explore", json={"payload": payload, "bits": bits})


def take_and_revoke(indices_to_revoke: int) -> tuple[str, list[int]]:
    revoked = []
    uri = ""
    for position in range(indices_to_revoke + 2):
        reference = client.post(
            "/token_status_list/take",
            headers={"X-Api-Key": "test"},
            data={"country": "EU", "doctype": "org.iso.18013.5.1.mDL", "expiry_date": "2099-12-31"},
        ).json()["status_list"]
        uri = reference["uri"]
        if position < indices_to_revoke:
            client.post(
                "/token_status_list/set",
                headers={"X-Api-Key": "test"},
                data={"uri": uri, "idx": reference["idx"], "status": 1},
            )
            revoked.append(reference["idx"])
    return uri, sorted(revoked)


def test_server_jwt_reports_exactly_the_revoked_indices() -> None:
    uri, revoked = take_and_revoke(3)
    token = client.get(urlparse(uri).path, headers={"accept": "application/statuslist+jwt"}).text

    data = explore(token).json()

    assert data["format"] == "jwt"
    assert data["header"]["typ"] == "statuslist+jwt"
    assert data["payload"]["sub"] == uri
    assert data["non_valid_indices"] == revoked
    assert data["counts"] == {"VALID": data["size"] - 3, "REVOKED": 3}


def test_server_cwt_in_hex_and_base64_matches_the_jwt() -> None:
    uri, revoked = take_and_revoke(2)
    path = urlparse(uri).path
    raw = client.get(path, headers={"accept": "application/statuslist+cwt"}).content

    as_hex = explore(raw.hex()).json()
    as_base64 = explore(base64.b64encode(raw).decode()).json()
    as_base64url = explore(base64.urlsafe_b64encode(raw).decode().rstrip("=")).json()

    for data in (as_hex, as_base64, as_base64url):
        assert data["format"] == "cwt"
        assert data["non_valid_indices"] == revoked
        assert data["payload"]["2"] == uri
    assert as_hex["header"]["1"] == -7


def test_json_payload_and_bare_claim_decode() -> None:
    lst = encode_status_list([0, 1, 0, 0, 1, 0, 0, 0])

    claim = explore(json.dumps({"bits": 1, "lst": lst})).json()
    payload = explore(json.dumps({"sub": "x", "status_list": {"bits": 1, "lst": lst}})).json()

    assert claim["non_valid_indices"] == payload["non_valid_indices"] == [1, 4]
    assert payload["payload"]["sub"] == "x"


def test_bare_lst_uses_the_supplied_bits() -> None:
    lst = encode_status_list([0, 2, 1, 0], bits=2)

    data = explore(lst, bits=2).json()

    assert data["format"] == "lst"
    assert data["bits"] == 2
    assert data["non_valid_indices"] == [1, 2]
    assert data["counts"] == {"VALID": 2, "SUSPENDED": 1, "REVOKED": 1}
    assert data["lst"]["full"] == "0210"


def test_foreign_issuer_jwt_decodes_without_its_key() -> None:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ec

    foreign_key = ec.generate_private_key(ec.SECP256R1()).private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    token = jwt.encode(
        {"sub": "https://other.example/1", "status_list": {"bits": 1, "lst": encode_status_list([1, 0, 1])}},
        foreign_key,
        algorithm="ES256",
        headers={"typ": "statuslist+jwt"},
    )

    data = explore(token).json()

    assert data["non_valid_indices"] == [0, 2]


def test_rejects_unusable_payloads() -> None:
    no_claim = jwt.encode({"sub": "x"}, "k" * 32, algorithm="HS256")
    cases = {
        "not json": "{not json",
        "no claim": json.dumps({"sub": "x"}),
        "jwt without claim": no_claim,
        "not zlib": base64.urlsafe_b64encode(b"plain bytes").decode(),
        "bad bits": json.dumps({"bits": 3, "lst": encode_status_list([0])}),
        "truncated": base64.urlsafe_b64encode(zlib.compress(b"\x00" * 64)[:-4]).decode(),
    }
    for name, payload in cases.items():
        response = explore(payload)
        assert response.status_code == 400, name
        assert response.json()["detail"], name


def test_rejects_decompression_bombs() -> None:
    bomb = base64.urlsafe_b64encode(zlib.compress(b"\x00" * (MAX_INFLATED_BYTES + 1))).decode()

    response = explore(bomb)

    assert response.status_code == 400
    assert "inflates beyond" in response.json()["detail"]


def test_explorer_page_is_reachable_from_the_topbar() -> None:
    response = client.get("/explorer")

    assert response.status_code == 200
    assert '<a href="/explorer" aria-current="page">Explorer</a>' in response.text
    assert '<a href="/explorer">Explorer</a>' in client.get("/").text


def test_packed_bit_order_is_lsb_first() -> None:
    # TSL §4.1: index 0 is the least significant bit of the first byte.
    lst = base64.urlsafe_b64encode(zlib.compress(bytes([0x80, 0x01]))).decode()

    assert explore(lst).json()["non_valid_indices"] == [7, 8]
