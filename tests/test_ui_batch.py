from fastapi.testclient import TestClient

from app import app
from issuer import reset_state


client = TestClient(app)


def setup_function() -> None:
    reset_state()


def test_console_is_served_at_the_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Token status list console" in response.text
    assert "/brand/style.css" in response.text
    assert "/brand/logos/credimi_logo-transp.svg" in response.text
    assert "/credentials/random-batch" in response.text
    assert "/verify-batch" in response.text
    assert "/debug/status-list" in response.text
    assert "/debug/status-lists" in response.text
    assert "/token_status_list/take" in response.text
    assert "identifier-list" in response.text
    assert 'id="country"' in response.text
    assert 'id="doctype"' in response.text
    assert 'id="expiry-date"' in response.text
    assert 'id="lst-bitmap-scroll"' in response.text
    assert 'id="lst-minimap"' in response.text
    assert 'bitmap-minimap-marker' in response.text
    assert 'bitmap-minimap-row-jump' in response.text
    assert 'button[data-row]' in response.text
    assert 'document.querySelector("#token").onclick' in response.text
    assert 'data-preview' in response.text
    assert "application/statuslist+cwt" in response.text
    assert "application/identifierlist+cwt" in response.text
    assert "Token formats" in response.text



def test_console_renders_results_panel_before_the_token() -> None:
    html = client.get("/").text

    assert 'class="container console-container page-content"' in html
    assert 'class="console-grid"' in html
    assert 'class="stack console-left"' in html
    assert 'class="stack console-right"' in html
    assert html.index('id="rows"') < html.index('id="out"')
    assert html.index('id="out"') < html.index('id="token-card"')


def test_verify_and_revoke_reload_the_status_list_token() -> None:
    script = client.get("/").text

    for handler, endpoint in (
        ('document.querySelector("#verify").onclick', "/verify-batch"),
        ('document.querySelector("#revoke").onclick', "/credentials/revoke-batch"),
    ):
        start = script.index(handler)
        body = script[start : start + 1500]
        assert endpoint in body, handler
        assert "await refreshToken(true)" in body, handler


def test_format_previews_also_render_the_decoded_debug_token() -> None:
    html = client.get("/").text
    script_start = html.index('registryRows.querySelectorAll("button[data-preview]")')
    body = html[script_start : html.index("async function load()", script_start)]

    assert html.count('data-media="application/statuslist+jwt"') == 1
    assert html.count('data-media="application/statuslist+cwt"') == 1
    assert html.count('data-media="application/identifierlist+jwt"') == 1
    assert html.count('data-media="application/identifierlist+cwt"') == 1
    assert "write(formatPreview)" in body
    assert 'renderDecodedToken(await jsonFetch("/debug/status-list"))' in body
    assert 'tokenCard.scrollIntoView({ behavior: "smooth", block: "start" })' in body



def test_red_route_is_gone() -> None:
    assert client.get("/red").status_code == 404


def test_random_batch_create_lists_credentials() -> None:
    response = client.post(
        "/credentials/random-batch",
        json={"count": 3, "prefix": "demo"},
    )

    assert response.status_code == 200
    created = response.json()["created"]
    assert len(created) == 3
    created_idx = sorted(credential["idx"] for credential in created)
    assert len(set(created_idx)) == 3
    assert all(0 <= idx < 10_000 for idx in created_idx)
    assert all(
        credential["credential_id"].startswith("demo-") for credential in created
    )

    listed = client.get("/credentials").json()["credentials"]

    assert [credential["idx"] for credential in listed] == created_idx
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
