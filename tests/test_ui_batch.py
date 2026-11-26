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
    assert "/debug/status-list" in response.text
    assert "/debug/status-lists" in response.text
    assert 'id="allocation-count"' in response.text
    assert 'id="allocation-rows"' in response.text
    assert 'id="lst-bitmap-scroll"' in response.text
    assert 'id="lst-minimap"' in response.text
    assert 'bitmap-minimap-marker' in response.text
    assert 'bitmap-minimap-row-jump' in response.text
    assert 'button[data-row]' in response.text
    assert 'id="working-tabs"' in response.text
    assert 'id="new-list-toggle"' in response.text
    assert 'id="add-entries"' in response.text



def test_console_shows_the_working_list_in_tabs() -> None:
    html = client.get("/").text

    assert '<section class="page-section" aria-labelledby="console-title">\n    <div class="container">' in html
    # The console shares the brand max-width so it lines up with the header.
    assert "console-container" not in html
    # Lists, then one working-list card whose views are tabs.
    assert html.index('id="registry-card"') < html.index('id="working-card"')
    assert html.index('id="working-card"') < html.index('id="entries-panel"')
    assert html.index('id="entries-panel"') < html.index('id="token-panel"')
    assert html.index('id="token-panel"') < html.index('id="key-panel"')
    assert 'id="token-panel" aria-labelledby="tab-token" hidden' in html
    # Failures float in one dismissible alert instead of an output panel.
    assert 'id="notice" class="notice" role="alert" hidden' in html


def test_page_sections_keep_the_container_side_gutter() -> None:
    # .page-section carries no horizontal padding, so it must not share an
    # element with .container: the gutter lives on a nested .container instead.
    for path in ("/", "/docs"):
        html = client.get(path).text
        assert 'class="page-section"' in html
        assert "container page-section" not in html
        assert "page-section container" not in html


def test_footer_links_to_the_repository() -> None:
    html = client.get("/").text

    repository = '<a href="https://github.com/ForkbombEu/capture-status-list"'
    assert repository in html
    assert html.index('<a href="/docs">API docs</a>') < html.index(repository)


def test_registry_inventory_carries_no_row_actions() -> None:
    html = client.get("/").text

    # The inventory lists the country × doctype pools; a click on a row
    # chooses it, and the raw token previews are gone with the buttons.
    assert 'data-preview=' not in html
    assert 'data-work-uri=' not in html
    assert "<th>Token formats</th>" not in html
    assert (
        "<thead><tr><th>Country</th><th>Doctype</th><th>List UUID</th>"
        "<th>Allocated</th><th>Revoked</th><th>Expiry</th><th>State</th></tr></thead>"
        in html
    )


def test_console_declares_the_working_list_context() -> None:
    html = client.get("/").text

    assert '<h3 class="subsection-heading">Country × doctype lists' in html
    assert "registryRows.onclick = chooseRow" in html
    assert 'id="ctx-scope"' in html
    # Pools are created from the primary button that opens a form on demand.
    assert 'id="new-list-toggle" class="btn btn-sm btn-primary"' in html
    assert 'id="new-list-form" class="mt-4" hidden' in html
    assert 'id="new-list" class="btn btn-md btn-primary"' in html
    # The working-list card stays hidden until a list is chosen; its Entries tab
    # tops the list up and lists the entries, whose country, doctype and URI
    # live in the card title and the Token tab rather than in every row.
    assert 'id="working-card" aria-labelledby="working-title" hidden' in html
    entries_panel = html[html.index('id="entries-panel"') : html.index('id="token-panel"')]
    assert 'id="entries-count"' in entries_panel
    assert 'id="add-entries"' in entries_panel
    assert "<th>Index</th><th>Expiry</th><th>Status</th><th>Actions</th>" in entries_panel


def test_token_tab_sets_the_encoded_jwt_beside_its_decoded_parts() -> None:
    html = client.get("/").text

    # The list URI sits above the tabs and opens the served token in a new tab.
    uri_link = 'id="lst-uri" target="_blank" rel="noreferrer"'
    assert html.index(uri_link) < html.index('id="working-tabs"')
    token_panel = html[html.index('id="token-panel"') : html.index('id="key-panel"')]
    assert 'id="lst-uri"' not in token_panel
    columns = token_panel[token_panel.index('class="jwt-columns"') :]
    assert columns.index('id="jwt"') < columns.index('id="jwt-header"') < columns.index('id="jwt-payload"')
    # Encoded and decoded start level: the colour legend sits under the JWT.
    assert columns.index('id="jwt"') < columns.index('class="jwt-legend"')


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


def test_status_list_api_links_open_the_take_operation_in_the_docs() -> None:
    html = client.get("/").text
    take = client.get("/openapi.json").json()["paths"]["/token_status_list/take"]["post"]

    # The take endpoint only accepts POST, so the topbar and footer links open
    # its entry in Swagger UI; a renamed route would break this deep link.
    assert html.count(f'href="/docs#/default/{take["operationId"]}"') == 2
    assert 'href="/token_status_list/take"' not in html
