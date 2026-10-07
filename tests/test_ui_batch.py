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
    assert 'id="allocation-count"' in response.text
    assert 'id="allocation-rows"' in response.text
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

    assert '<main class="page-content">\n    <div class="container">' in html
    # The console shares the brand max-width so it lines up with the header.
    assert "console-container" not in html
    assert 'class="console-grid"' in html
    assert 'class="stack console-left"' in html
    assert 'class="stack console-right"' in html
    assert html.index('id="rows"') < html.index('id="out"')
    assert html.index('id="out"') < html.index('id="token-card"')


def test_page_content_keeps_the_container_side_gutter() -> None:
    # .page-content resets horizontal padding, so it must not share an element
    # with .container: the gutter lives on a nested .container instead.
    for path in ("/", "/docs"):
        html = client.get(path).text
        assert 'class="page-content"' in html
        assert "container page-content" not in html
        assert "page-content container" not in html


def test_page_bands_share_one_fixed_gutter() -> None:
    html = client.get("/").text

    assert ":root { --page-gutter: 46px; }" in html
    assert ".topbar-inner, .hero-inner, .container, .footer-inner {" in html


def test_footer_links_to_the_repository() -> None:
    html = client.get("/").text

    repository = '<a href="https://github.com/ForkbombEu/capture-status-list"'
    assert repository in html
    assert html.index('<a href="/docs">API docs</a>') < html.index(repository)


def test_registry_previews_declare_each_token_format() -> None:
    html = client.get("/").text

    assert html.count('data-media="application/statuslist+jwt"') == 1
    assert html.count('data-media="application/statuslist+cwt"') == 1
    assert html.count('data-media="application/identifierlist+jwt"') == 1
    assert html.count('data-media="application/identifierlist+cwt"') == 1
    # Every pool can be selected as the console's working list; the raw token
    # previews stay separate so a preview never moves the context.
    assert html.count("data-work-uri=") == 1
    assert html.count("data-preview=") == 4


def test_console_declares_the_working_list_context() -> None:
    html = client.get("/").text

    assert "<h2>Working list</h2>" in html
    assert 'id="lst-select"' in html
    assert 'id="ctx-scope"' in html
    # Panels are gated on the working list: the registry is the chooser, the
    # credential panel and the allocated-entry table belong to one list each.
    assert 'id="registry-card"' in html
    assert 'id="legacy-card" hidden' in html
    assert 'id="allocation-card" hidden' in html
    assert html.index('id="legacy-card"') < html.index('id="count"')
    assert html.index('id="allocation-card"') < html.index('id="allocation-rows"')


def test_console_pages_are_not_cached() -> None:
    # The dashboard runs inline JavaScript; a cached copy would keep driving the
    # previous build against a reloaded server.
    for path in ("/", "/explorer", "/docs"):
        assert client.get(path).headers["cache-control"] == "no-store"



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
