"""Brand-asset integrity and page-chrome tests.

The four logo SVGs are frozen: `.puria/design/DESIGN.md` §1 pins their
SHA-256 digests, and the runtime copies under `brand/logos/` must stay
byte-for-byte identical to those pins.
"""

import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)

BRAND_DIR = Path(__file__).resolve().parent.parent / "brand"

FROZEN_LOGOS = {
    "credimi_logo.svg": "031885760a9165e9d8d49eab45baca30ba5ed8dd1fbf0b4699fba2de5dc4feac",
    "credimi_logo_negative.svg": "32df33f9f5ffa696d452e1f65f5d6738b920415c5114db4b010af1f997a8cb3a",
    "credimi_logo-transp.svg": "8407a3ed0beddc137599f71498f1ca8e68766a2684dba80093ea25e17173eef7",
    "credimi_logo-transp_white.svg": "196017744fca7d3836720995aca8c55c8531908e8dcdafc5ca5e7b48ef8f7e10",
}

HTML_PAGES = ("/", "/docs")


def test_frozen_logos_match_their_pinned_digests() -> None:
    for name, digest in FROZEN_LOGOS.items():
        payload = (BRAND_DIR / "logos" / name).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == digest, name


def test_fonts_are_vendored_next_to_the_stylesheet() -> None:
    assert (BRAND_DIR / "style.css").is_file()
    for name in (
        "InterVariable.ttf",
        "InterVariable.OFL.txt",
        "SourceCodeProVariable.ttf",
        "SourceCodeProVariable.OFL.txt",
    ):
        assert (BRAND_DIR / "fonts" / name).is_file(), name


def test_stylesheet_declares_no_third_party_font_source() -> None:
    stylesheet = (BRAND_DIR / "style.css").read_text(encoding="utf-8")

    assert "fonts.googleapis.com" not in stylesheet
    assert "fonts.gstatic.com" not in stylesheet


def test_brand_assets_are_served() -> None:
    stylesheet = client.get("/brand/style.css")
    assert stylesheet.status_code == 200
    assert stylesheet.headers["content-type"].startswith("text/css")

    font = client.get("/brand/fonts/InterVariable.ttf")
    assert font.status_code == 200

    for name, digest in FROZEN_LOGOS.items():
        served = client.get(f"/brand/logos/{name}")
        assert served.status_code == 200
        assert served.headers["content-type"].startswith("image/svg+xml")
        assert hashlib.sha256(served.content).hexdigest() == digest, name


def test_favicon_is_the_credimi_mark() -> None:
    response = client.get("/favicon.svg")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")
    assert response.content == (BRAND_DIR / "logos" / "credimi_logo.svg").read_bytes()


def test_every_html_page_carries_the_brand_chrome() -> None:
    for path in HTML_PAGES:
        page = client.get(path)

        assert page.status_code == 200, path
        assert page.headers["content-type"].startswith("text/html"), path
        assert '<link rel="stylesheet" href="/brand/style.css">' in page.text, path
        assert '<link rel="icon" type="image/svg+xml" href="/favicon.svg">' in page.text, path
        assert '<img src="/brand/logos/credimi_logo-transp.svg" alt="Credimi">' in page.text, path
        assert "Proudly developed by ForkBomb BV" in page.text, path


def test_every_html_page_carries_both_credimi_extras_strips() -> None:
    sentence = (
        "This app is part of Credimi Extras. Automate all your EUDI testing with"
    )

    for path in HTML_PAGES:
        page = client.get(path)

        assert page.text.count(sentence) == 2, path
        assert page.text.count('href="https://credimi.io" target="_blank" rel="noopener"') == 2, path
        assert '/brand/logos/credimi_logo.svg' in page.text, path
        assert '/brand/logos/credimi_logo-transp_white.svg' in page.text, path


def test_api_documentation_is_branded_and_reachable() -> None:
    docs = client.get("/docs")

    assert docs.status_code == 200
    assert "API documentation" in docs.text
    assert "swagger-ui" in docs.text
    assert client.get("/openapi.json").status_code == 200
