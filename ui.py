"""Credimi-branded HTML shells.

Every HTML page in this application, the API documentation included, is
rendered through `page()` so that it carries the same chrome: the Credimi
Extras top strip, the topbar wordmark, the deep-indigo footer with the
ForkBomb sub-bar, and the Credimi Extras bottom strip.

`.puria/design/DESIGN.md` is the design source. The brand stylesheet at
`brand/style.css` loads first and application CSS loads after it; only
layouts and behaviours absent from the brand foundation are declared here.
"""

BRAND_ROOT = "/brand"
STYLE_HREF = f"{BRAND_ROOT}/style.css"
LOGO_MARK = f"{BRAND_ROOT}/logos/credimi_logo.svg"
LOGO_WORDMARK_WHITE = f"{BRAND_ROOT}/logos/credimi_logo-transp_white.svg"
CREDIMI_URL = "https://credimi.io"
# `POST /token_status_list/take` answers a browser GET with 405, so its links
# open the operation in the API docs (Swagger UI deep link: untagged routes sit
# under "default", addressed by FastAPI's generated operationId).
TAKE_DOCS_HREF = "/docs#/default/take_status_list_token_status_list_take_post"

APP_CSS = """
    /* Application layer — loaded after the brand stylesheet.
       Only what the brand foundation does not already provide. */

    .extras-strip {
      background: var(--brand-secondary);
      color: var(--brand-primary);
      border-bottom: 1px solid var(--border);
      font-size: var(--fs-xs);
      font-weight: 500;
      text-align: center;
      padding: var(--space-2) var(--space-4);
    }
    .extras-strip-inner {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-2);
      flex-wrap: wrap;
      max-width: var(--max-width);
      margin: 0 auto;
    }
    .extras-strip img { height: 16px; width: auto; display: block; }
    .extras-strip a { color: var(--brand-primary); }
    .extras-bottom {
      background: rgba(0, 0, 0, 0.3);
      color: rgba(255, 255, 255, 0.7);
      font-size: var(--fs-xs);
      font-weight: 500;
      text-align: center;
      padding: var(--space-3) var(--space-4);
    }
    .extras-bottom-inner {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-2);
      flex-wrap: wrap;
    }
    .extras-bottom img { height: 16px; width: auto; display: block; }
    .extras-strip a:focus-visible,
    .extras-bottom a:focus-visible {
      outline: 2px solid var(--ring);
      outline-offset: 2px;
    }

    /* Page shell: the Credimi Extras top strip stays the first element in the
       body, and the footer stays at the bottom on short pages. */
    body {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      background: var(--brand-secondary);
    }
    /* Flex children with `margin: 0 auto` (every .container) would otherwise
       shrink to fit their content instead of stretching. */
    body > * { width: 100%; }
    body > main { flex: 1; }

    .footer-brand h5 { color: var(--fg-on-primary); margin-bottom: var(--space-2); }

    /* Topbar lockup: the Credimi mark at its 32px minimum (DESIGN.md §4), then
       the service name. Logo links carry no underline: the brand rule
       underlines every anchor. */
    .topbar-logo {
      display: flex;
      align-items: center;
      gap: var(--space-3);
      height: auto;
      color: var(--fg);
      text-decoration: none;
    }
    .topbar-logo img { width: 32px; height: 32px; }
    .topbar-title {
      font: 700 var(--fs-md)/1 var(--font-display);
      letter-spacing: -0.01em;
      white-space: nowrap;
    }
    /* Below 480px the name and the nav no longer fit the 56px bar side by side;
       the mark alone stays as the home link. */
    @media (max-width: 480px) {
      .topbar-title { display: none; }
    }
    .extras-bottom a { text-decoration: none; }

    /* Grid items default to min-width:auto, so the table's own min-width would
       widen the whole page instead of scrolling inside its wrapper. */
    .stack { display: grid; gap: var(--space-6); }
    .stack > *, .card-grid > * { min-width: 0; }
    .test-table-wrap { max-width: 100%; }

    /* Tables are the brand's Scoreboard pattern (`.test-table`, DESIGN.md §11
       Tables); the console only adds the registry's two-line first cell. */
    /* The list's name opens its Status List Token URI in a new tab; like the
       topbar links it is underlined only under the pointer. */
    .list-name {
      display: inline-block;
      color: var(--brand-primary);
      font-size: var(--fs-base);
      font-weight: 600;
      text-decoration: none;
    }
    .list-name:hover { text-decoration: underline; }
    .list-name:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
    .list-meta {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: var(--space-2);
      margin-top: var(--space-1);
      color: var(--fg-muted);
      font-size: var(--fs-xs);
    }
    .list-meta .status-chip { height: 20px; padding: 0 var(--space-2); }
    /* The entries table scrolls under its sticky 40px header band (brand
       `.test-table th`), so its scrollbar track starts below the band, and the
       box's top 40px take the band's lavender to fill the gutter beside it: a
       flat fill with a hard stop, not a visible gradient. Firefox has no track
       margin; there the thin bar runs alongside the header. */
    .entries-scroll {
      max-height: 420px;
      overflow: auto;
      border-radius: var(--radius);
      background: linear-gradient(var(--brand-secondary-strong) 40px, var(--bg) 40px);
    }
    .entries-scroll::-webkit-scrollbar-track { margin-top: 40px; }
    .entries-scroll .test-table-wrap { overflow: visible; }

    .btn-secondary {
      background: var(--brand-secondary-deep);
      color: var(--brand-primary);
    }
    .btn-secondary:hover { background: var(--brand-secondary-strong); }
    /* A disabled action keeps its label and turns muted: a revoked entry still
       reads "Revoke", greyed out. */
    .btn:disabled,
    .btn:disabled:hover {
      background: var(--bg-muted);
      color: var(--fg-muted);
      cursor: not-allowed;
    }
    .btn-row { display: flex; flex-wrap: wrap; gap: var(--space-2); }
    .btn-row .btn { justify-content: center; }

    .metric-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: var(--space-4);
    }
    .metric-value {
      display: block;
      font: 700 var(--fs-3xl)/1 var(--font-display);
      letter-spacing: -0.007em;
      color: var(--brand-primary);
      margin-bottom: var(--space-2);
    }

    .test-table { min-width: 680px; }
    .test-table td { vertical-align: middle; }
    .test-table td.cell-mono {
      font-family: var(--font-mono);
      font-size: var(--fs-xs);
      white-space: nowrap;
    }
    .test-table tr.revoked td { background: var(--destructive-bg); }
    .test-table .empty-row td {
      color: var(--fg-subtle);
      padding: var(--space-5) var(--space-3);
    }

    .status-valid { background: var(--success-bg); color: var(--success); }
    .status-valid::before { background: var(--success); }
    .status-revoked { background: var(--destructive-bg); color: var(--destructive); }
    .status-revoked::before { background: var(--destructive); }
    .status-reject { background: var(--destructive-bg); color: var(--destructive); }
    .status-reject::before { background: var(--destructive); }

    .output {
      min-height: 96px;
      white-space: pre-wrap;
      word-break: break-word;
      margin: 0;
    }

    /* Status list token: the three JWT segments, each on its own brand
       colour. The Token tab sets the encoded JWT beside its decoded header and
       payload, as jwt.io does; narrow screens stack them. */
    .jwt-columns {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: var(--space-6);
      align-items: start;
    }
    .jwt-columns > * { min-width: 0; }
    .jwt-decoded pre { max-height: 360px; overflow: auto; }
    @media (max-width: 900px) {
      .jwt-columns { grid-template-columns: 1fr; }
    }
    .jwt { font-size: var(--fs-sm); }
    .jwt-header { color: var(--brand-primary); font-weight: 600; }
    .jwt-payload { color: var(--brand-accent-vivid); font-weight: 600; }
    .jwt-signature { color: var(--credential); font-weight: 600; }
    .jwt-dot { color: var(--fg-muted); }
    .jwt-legend {
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-2);
    }
    .jwt-legend .badge { background: var(--bg-muted); }
    .jwt-legend .badge-dot { width: 8px; height: 8px; }
    /* Icons in buttons (refresh, new) follow the label colour. */
    .btn svg {
      flex: 0 0 auto;
      width: 14px;
      height: 14px;
      fill: none;
      stroke: currentColor;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
    .btn-lg svg { width: 16px; height: 16px; }
    .legend-header { background: var(--brand-primary); }
    .legend-payload { background: var(--brand-accent-vivid); }
    .legend-signature { background: var(--credential); }

    .bitmap-shell {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 48px;
      gap: var(--space-2);
      min-width: 0;
    }
    .bitmap-scroll,
    .bitmap-minimap-scroll {
      /* Ten visible rows; the full spectrum remains vertically scrollable. */
      height: calc(10 * 1.6rem + 2 * var(--space-4));
      overflow: auto;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--bg-muted);
    }
    .bitmap-minimap-scroll {
      overflow: hidden;
      position: relative;
    }
    .bitmap-scroll:focus-visible,
    .bitmap-minimap-scroll:focus-visible {
      outline: 3px solid var(--brand-accent);
      outline-offset: 2px;
    }
    .bitmap-minimap {
      display: flex;
      flex-direction: column;
      height: 100%;
      min-height: 0;
      padding: var(--space-2);
      font-family: var(--font-mono);
      position: relative;
    }
    .bitmap-minimap-line {
      display: flex;
      flex: 1 1 0;
      align-items: center;
      min-height: 1px;
    }
    .bitmap-minimap-marker {
      width: 100%;
      height: 100%;
      min-height: 2px;
      padding: 0;
      border: 0;
      border-radius: 1px;
      background: var(--destructive);
      color: transparent;
      cursor: pointer;
      font-size: 0;
      line-height: 1;
    }
    .bitmap-minimap-marker:hover,
    .bitmap-minimap-marker:focus-visible {
      background: var(--destructive);
      outline: 2px solid var(--destructive);
      outline-offset: 1px;
    }
    .bitmap-minimap-row-jump {
      width: 100%;
      height: 100%;
      min-height: 2px;
      padding: 0;
      border: 0;
      border-radius: 1px;
      background: transparent;
      color: transparent;
      cursor: pointer;
      font-size: 0;
      line-height: 1;
    }
    .bitmap-minimap-row-jump:hover,
    .bitmap-minimap-row-jump:focus-visible {
      background: var(--brand-secondary-strong);
      outline: 2px solid var(--brand-accent);
      outline-offset: 1px;
    }
    .bitmap-minimap-viewport {
      position: absolute;
      inset-inline: 0;
      border: 2px solid var(--brand-accent);
      background: var(--brand-secondary-strong);
      opacity: 0.35;
      cursor: grab;
      touch-action: none;
      z-index: 1;
    }
    .bitmap-minimap-viewport:active,
    .bitmap-minimap-viewport.dragging {
      cursor: grabbing;
      opacity: 0.5;
    }
    .bitmap-minimap-empty {
      display: block;
      padding: var(--space-2) 0;
      color: var(--fg-muted);
      font-size: var(--fs-xs);
      line-height: 1.2;
      text-align: center;
      writing-mode: vertical-rl;
    }
    /* Inflated `lst`: one character per entry, 64 per row, with the row's
       first index in the gutter. */
    .bitmap {
      display: grid;
      grid-template-columns: max-content 1fr;
      gap: var(--space-1) var(--space-4);
      overflow-x: auto;
      padding: var(--space-4);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--bg-muted);
      font-family: var(--font-mono);
      font-size: var(--fs-sm);
      line-height: 1.6;
    }
    .bitmap-index { color: var(--fg-muted); white-space: nowrap; }
    .bitmap-row { color: var(--fg-subtle); white-space: pre; }
    .bitmap-row b {
      color: var(--fg-on-primary);
      background: var(--destructive);
      border-radius: var(--radius-sm);
      font-weight: 700;
      padding-inline: 1px;
    }
    .bitmap-caption {
      margin-top: var(--space-2);
      color: var(--fg-subtle);
      font-size: var(--fs-sm);
    }
    .lst-note {
      margin-top: var(--space-2);
      color: var(--fg-subtle);
      font-size: var(--fs-sm);
    }

    .index-list {
      font-family: var(--font-mono);
      font-size: var(--fs-sm);
      color: var(--fg-subtle);
      word-break: break-word;
    }
    .index-group + .index-group { margin-top: var(--space-3); }
    .index-group-name {
      margin-bottom: var(--space-1);
      font-size: var(--fs-sm);
      font-weight: 600;
    }

    /* Explorer: the brand styles the payload textarea as a form-field control;
       here it is taller and set in monospace for tokens. */
    .form-field .payload-input {
      min-height: 160px;
      font: var(--fs-sm)/1.5 var(--font-mono);
      word-break: break-all;
    }
    .disclosure-body { padding: var(--space-4); }
    .bits-segmented { max-width: 320px; }
    /* A token without an encoded form to show (CWT, JSON) keeps one column. */
    .jwt-columns-single { grid-template-columns: 1fr; }
    /* The registry is the chooser: clicking a row opens that list's panel under
       it. Rows top-align like the scoreboard and stay white; the chevron marks
       the open one, and the usual hairline separates it from its panel. */
    .registry-row { cursor: pointer; }
    .registry-row td { vertical-align: top; }
    .registry-row td.cell-mono { line-height: 20px; }
    .registry-row:hover td { background: var(--bg-muted); }
    .registry-row:focus-visible { outline: 2px solid var(--ring); outline-offset: -2px; }
    /* The working-list panel opens as a detail row under the chosen list, the
       way the scoreboard expands a pipeline, with no card of its own. Fixed
       columns keep a long JWT or JSON line in it from stretching the table. */
    .registry-table { table-layout: fixed; --toggle-col: 44px; }
    .registry-table .col-toggle { width: var(--toggle-col); }
    .registry-table .col-uuid { width: 330px; }
    .registry-table .col-expiry { width: 120px; }
    .registry-chevron {
      display: block;
      width: 16px;
      height: 16px;
      margin-top: 2px;
      fill: none;
      stroke: var(--brand-primary);
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
      transition: transform 150ms ease-out;
    }
    .registry-row[aria-expanded="true"] .registry-chevron { transform: rotate(180deg); }
    /* The brand row hover (`.test-table tr:hover td`) would paint every cell of
       the panel's own table while the pointer is over the detail row; the panel
       stays white, its rows keep their own hover and revoked tint. The panel is
       indented to line up with the List column. */
    .test-table .registry-detail:hover td { background: transparent; }
    .test-table .registry-detail > td,
    .test-table .registry-detail:hover > td {
      padding: var(--space-4) var(--space-3) var(--space-5) calc(var(--toggle-col) + var(--space-3));
      background: var(--bg);
    }
    .registry-detail .test-table tr:hover td { background: var(--bg-muted); }
    .registry-detail .test-table tr.revoked td { background: var(--destructive-bg); }
    @media (prefers-reduced-motion: reduce) {
      .registry-chevron { transition: none; }
    }
    /* The explorer's index check answers as you type, its chip beside the field. */
    .index-check-status { display: inline-flex; align-items: center; min-height: 44px; }
    .status-suspended { background: var(--warning-bg); color: var(--fg); }
    .status-suspended::before { background: var(--warning); }

    /* Swagger UI ships its own reset; keep it inside the branded card and on
       the brand families. */
    .docs-frame {
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: var(--space-5);
    }
    .docs-frame .swagger-ui .topbar { display: none; }
    .docs-frame .swagger-ui,
    .docs-frame .swagger-ui .info .title,
    .docs-frame .swagger-ui .opblock-tag,
    .docs-frame .swagger-ui .btn {
      font-family: var(--font-sans);
      color: var(--fg);
    }
    .docs-frame .swagger-ui .info .title { font-weight: 700; }
    .docs-frame .swagger-ui .opblock .opblock-summary-path,
    .docs-frame .swagger-ui .microlight { font-family: var(--font-mono); }
    .docs-frame .swagger-ui .wrapper { max-width: none; padding: 0; }
    /* Undo the brand's bare-element rules where Swagger styles the element
       itself; the brand hairline box turns its code blocks unreadable. */
    .docs-frame .swagger-ui pre {
      background: none;
      border: 0;
      padding: 0;
      font-size: var(--fs-sm);
    }
    .docs-frame .swagger-ui .highlight-code > .microlight {
      padding: var(--space-4);
      border-radius: var(--radius);
    }
    .docs-frame .swagger-ui input[type="text"] {
      height: auto;
      width: auto;
      border-radius: var(--radius);
      font-size: var(--fs-sm);
    }
    .docs-frame .swagger-ui h1,
    .docs-frame .swagger-ui h2,
    .docs-frame .swagger-ui h3,
    .docs-frame .swagger-ui h4,
    .docs-frame .swagger-ui h5 { letter-spacing: normal; }

    @media (max-width: 768px) {
      .metric-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
"""

_EXTRAS_TOP = f"""  <div class="extras-strip">
    <div class="extras-strip-inner">
      <img src="{LOGO_MARK}" alt="" aria-hidden="true">
      <span>This app is part of Credimi Extras. Automate all your EUDI testing with
        <a href="{CREDIMI_URL}" target="_blank" rel="noopener">Credimi</a></span>
    </div>
  </div>"""

_EXTRAS_BOTTOM = f"""    <div class="extras-bottom">
      <div class="extras-bottom-inner">
        <span>This app is part of Credimi Extras. Automate all your EUDI testing with</span>
        <a href="{CREDIMI_URL}" target="_blank" rel="noopener">
          <img src="{LOGO_WORDMARK_WHITE}" alt="Credimi">
        </a>
      </div>
    </div>"""


def _topbar(active: str) -> str:
    links = (
        ("Console", "/"),
        ("Explorer", "/explorer"),
        ("API docs", "/docs"),
        ("TSL JWKS", "/.well-known/jwks.json"),
    )
    items = "\n".join(
        '        <li><a href="{href}"{current}>{label}</a></li>'.format(
            href=href,
            label=label,
            # The brand stylesheet marks the current page with `.nav-active`.
            current=' class="nav-active" aria-current="page"' if label == active else "",
        )
        for label, href in links
    )
    return f"""  <nav class="topbar">
    <div class="topbar-inner">
      <a class="topbar-logo" href="/"><img src="{LOGO_MARK}" alt="Credimi"><span class="topbar-title">Token status list</span></a>
      <ul class="topbar-nav">
{items}
      </ul>
    </div>
  </nav>"""


_FOOTER = f"""  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-content">
        <div class="footer-brand">
          <h5>Mock Token Status List server</h5>
          <p>A Credimi Extra: local test infrastructure for EUDI Wallet Functional
            Conformance Assessment experiments. Not a certification service.</p>
        </div>
        <div class="footer-links">
          <div class="footer-col">
            <a href="{TAKE_DOCS_HREF}">Status list API</a>
            <a href="/status/1">Legacy status list token</a>
            <a href="/token_status_list/aggregation">Status list aggregation</a>
            <a href="/.well-known/jwks.json">TSL JWKS</a>
            <a href="/docs">API docs</a>
            <a href="https://github.com/ForkbombEu/capture-status-list"
               target="_blank" rel="noopener">Repository</a>
          </div>
          <div class="footer-col">
            <h5>Standards</h5>
            <a href="https://datatracker.ietf.org/doc/draft-ietf-oauth-status-list/"
               target="_blank" rel="noopener">IETF Token Status List</a>
            <a href="https://www.rfc-editor.org/rfc/rfc7519" target="_blank" rel="noopener">JWT · RFC 7519</a>
            <a href="https://www.rfc-editor.org/rfc/rfc7515" target="_blank" rel="noopener">JWS · RFC 7515</a>
          </div>
        </div>
      </div>
    </div>
    <div class="footer-sub-bar">Proudly developed by ForkBomb BV</div>
{_EXTRAS_BOTTOM}
  </footer>"""


def page(
    *,
    title: str,
    active: str,
    body: str,
    head: str = "",
    scripts: str = "",
) -> str:
    """Render a full branded HTML page around `body`."""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="stylesheet" href="{STYLE_HREF}">
{head}  <style>{APP_CSS}  </style>
</head>
<body>
{_EXTRAS_TOP}
{_topbar(active)}
{body}
{_FOOTER}
{scripts}
</body>
</html>"""


def _section_intro(level: int, title_id: str, title: str, description: str = "") -> str:
    """A section intro (DESIGN.md §8): the title row, then an optional description."""
    paragraph = (
        f"""
      <div class="section-intro-description"><p>{description}</p></div>"""
        if description
        else ""
    )
    return f"""    <header class="section-intro">
      <div class="section-intro-heading">
        <h{level} class="section-intro-title" id="{title_id}">{title}</h{level}>
      </div>{paragraph}
    </header>"""


def _hero_band(title: str, description: str) -> str:
    """The indigo band every page opens with (DESIGN.md §8), titled `#page-title`."""
    return f"""  <section class="hero-band" aria-labelledby="page-title">
    <div class="hero-inner">
{_section_intro(1, "page-title", title, description)}
    </div>
  </section>"""


# The one alert every page reports failures and hints in (DESIGN.md §11
# Alerts); the shared script's notify() fills and shows it.
_NOTICE = """
      <div id="notice" class="alert alert-floating" role="alert" hidden>
        <svg class="alert-icon" data-kind="destructive" viewBox="0 0 24 24" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
        <svg class="alert-icon" data-kind="info" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
        <div>
          <p class="alert-title" id="notice-title"></p>
          <p class="alert-body" id="notice-body"></p>
        </div>
        <button id="notice-dismiss" class="btn btn-sm btn-ghost" type="button">Dismiss</button>
      </div>
"""


_CONSOLE_BODY = (
    _hero_band(
        "Token status list console",
        "A test server for EUDI Wallet conformance: IETF Token Status Lists per country"
        " and doctype, in JWT and CWT, each paired with an ISO 18013-5 identifier list.",
    )
    + """
  <main>
    <section class="page-section" aria-labelledby="console-title">
    <div class="container">
"""
    + _section_intro(
        2,
        "console-title",
        "Browse the status lists",
        "Pick a list to add or revoke entries, read its signed token, and check the key"
        " that signs it.",
    )
    + """
    <div class="stack">
      <div id="registry">
        <div class="test-table-wrap">
          <table class="test-table registry-table">
            <thead><tr><th class="col-toggle"></th><th>List</th><th class="col-uuid">List UUID</th><th class="col-expiry">Expiry</th></tr></thead>
            <tbody id="registry-rows"></tbody>
          </table>
        </div>
        <div class="btn-row mt-4">
          <button id="registry-refresh" class="btn btn-lg btn-outline"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>Refresh lists</button>
          <button id="new-list-toggle" class="btn btn-lg btn-primary" aria-expanded="false" aria-controls="new-list-form"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="M12 5v14"/></svg>New status list</button>
        </div>
        <div id="new-list-form" class="mt-4" hidden>
          <div class="form-row">
            <label class="form-field form-field-sm">
              <span class="subsection-heading">Country</span>
              <input id="new-country" type="text" value="EU" maxlength="16">
            </label>
            <label class="form-field form-field-grow">
              <span class="subsection-heading">Doctype</span>
              <input id="new-doctype" type="text" value="org.iso.18013.5.1.mDL" maxlength="128">
            </label>
            <label class="form-field form-field-md">
              <span class="subsection-heading">List expiry</span>
              <input id="new-expiry" type="date" value="2099-12-31">
            </label>
            <button id="new-list-cancel" class="btn btn-lg btn-outline" type="button">Cancel</button>
            <button id="new-list" class="btn btn-lg btn-primary" type="button">Create</button>
          </div>
        </div>
      </div>

      <section id="working-card" aria-label="Selected status list" hidden>
        <div class="tabs" role="tablist" id="working-tabs" aria-label="Working list views">
          <button class="tab-btn active" type="button" role="tab" id="tab-entries" data-tab="entries" aria-selected="true" aria-controls="entries-panel">Entries <span id="allocation-count" class="count-chip">0</span></button>
          <button class="tab-btn" type="button" role="tab" id="tab-token" data-tab="token" aria-selected="false" aria-controls="token-panel" tabindex="-1">Token</button>
          <button class="tab-btn" type="button" role="tab" id="tab-decoded" data-tab="decoded" aria-selected="false" aria-controls="decoded-panel" tabindex="-1">Decoded status list</button>
        </div>

        <div role="tabpanel" id="entries-panel" aria-labelledby="tab-entries">
          <div class="entries-scroll">
            <div class="test-table-wrap">
              <table class="test-table">
                <thead><tr><th>Index</th><th>Expiry</th><th>Status</th><th>Actions</th></tr></thead>
                <tbody id="allocation-rows"></tbody>
              </table>
            </div>
          </div>
          <div class="btn-row mt-4">
            <button id="add-entries-toggle" class="btn btn-lg btn-outline" type="button" aria-expanded="false" aria-controls="add-entries-form"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="M12 5v14"/></svg>Add entries</button>
          </div>
          <div id="add-entries-form" class="mt-4" hidden>
            <div class="form-row">
              <label class="form-field form-field-sm">
                <span class="subsection-heading">Count</span>
                <input id="entries-count" type="number" min="1" max="500" value="10">
              </label>
              <label class="form-field form-field-md">
                <span class="subsection-heading">Entry expiry</span>
                <input id="entries-expiry" type="date" value="2099-12-31">
              </label>
              <button id="add-entries-cancel" class="btn btn-lg btn-outline" type="button">Cancel</button>
              <button id="add-entries" class="btn btn-lg btn-primary" type="button">Add</button>
            </div>
          </div>
        </div>

        <div role="tabpanel" id="token-panel" aria-labelledby="tab-token" hidden>
          <div class="jwt-columns">
            <div>
              <p class="eyebrow">Encoded</p>
              <pre class="output jwt" id="jwt"></pre>
              <div class="flex-between gap-3 mt-4">
                <p class="jwt-legend">
                  <span class="badge"><span class="badge-dot legend-header"></span>Header</span>
                  <span class="badge"><span class="badge-dot legend-payload"></span>Payload</span>
                  <span class="badge"><span class="badge-dot legend-signature"></span>Signature</span>
                </p>
                <button id="copy-token" class="btn btn-sm btn-outline">Copy the JWT</button>
              </div>
            </div>
            <div class="jwt-decoded">
              <p class="eyebrow">Decoded header</p>
              <pre id="jwt-header"></pre>
              <p class="eyebrow mt-4">Decoded payload</p>
              <pre id="jwt-payload"></pre>
              <p class="lst-note" id="lst-note"></p>
            </div>
          </div>
        </div>

        <div role="tabpanel" id="decoded-panel" aria-labelledby="tab-decoded" hidden>
          <div class="metric-grid">
            <div class="card">
              <strong class="metric-value" id="lst-bits">0</strong>
              <span class="eyebrow">Bits per entry</span>
            </div>
            <div class="card">
              <strong class="metric-value" id="lst-size">0</strong>
              <span class="eyebrow">Entries</span>
            </div>
            <div class="card">
              <strong class="metric-value" id="lst-valid">0</strong>
              <span class="eyebrow">Valid</span>
            </div>
            <div class="card">
              <strong class="metric-value" id="lst-revoked">0</strong>
              <span class="eyebrow">Revoked</span>
            </div>
          </div>
          <p class="eyebrow mt-4">Inflated lst spectrum</p>
          <div class="bitmap-shell">
            <div class="bitmap-scroll" id="lst-bitmap-scroll" tabindex="0" aria-label="Full inflated status list">
              <div class="bitmap" id="lst-bitmap"></div>
            </div>
            <div class="bitmap-minimap-scroll" id="lst-minimap-scroll" tabindex="0" aria-label="Revoked-entry minimap">
              <div class="bitmap-minimap" id="lst-minimap"></div>
            </div>
          </div>
          <p class="bitmap-caption" id="lst-caption"></p>
          <p class="eyebrow mt-4">Revoked indices</p>
          <p class="index-list" id="lst-indices">None</p>
        </div>
      </section>

"""
    + _NOTICE
    + """

    </div>
    </div>
    </section>
  </main>"""
)


# Helpers shared by the console and the explorer: HTML escaping, the styled
# console signature, and the inflated-lst spectrum renderer.
_SHARED_SCRIPT = """<script>
    console.log(
      "%c Credimi %c Token status list · ForkBomb BV ",
      "background:#220E7E;color:#FAFAFA;font-weight:700;padding:2px 6px;border-radius:4px 0 0 4px",
      "background:#EEEAFE;color:#220E7E;font-weight:600;padding:2px 6px;border-radius:0 4px 4px 0",
    );

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }

    // Status values arrive in caps (VALID, REVOKED); chips show them in sentence
    // case, since DESIGN.md §3 keeps uppercase for eyebrow labels only.
    function statusLabel(value) {
      return value.charAt(0) + value.slice(1).toLowerCase();
    }

    // Failures and hints float in the page's one alert until dismissed or until
    // the next action starts; successful actions show their result in the page.
    const notice = document.querySelector("#notice");

    function describe(value) {
      if (typeof value === "string") return value;
      if (value instanceof Error) return value.message;
      if (value && typeof value.detail === "string") return value.detail;
      return JSON.stringify(value, null, 2);
    }

    function notify(value, kind = "destructive", title = kind === "info" ? "Nothing selected" : "The action failed") {
      notice.className = `alert alert-floating alert-${kind}`;
      // Only this kind's icon shows; SVG elements have no .hidden property.
      notice.querySelectorAll(".alert-icon").forEach((icon) => icon.toggleAttribute("hidden", icon.dataset.kind !== kind));
      document.querySelector("#notice-title").textContent = title;
      document.querySelector("#notice-body").textContent = describe(value);
      notice.hidden = false;
    }
    document.querySelector("#notice-dismiss").onclick = () => { notice.hidden = true; };

    // Every action reports failures in the alert: an unhandled rejection would
    // leave the page stale with no explanation.
    async function guard(action) {
      notice.hidden = true;
      try {
        await action();
      } catch (error) {
        notify(error);
      }
    }

    async function jsonFetch(url, options = {}) {
      const response = await fetch(url, {
        cache: "no-store",
        headers: { "content-type": "application/json", ...(options.headers || {}) },
        ...options,
      });
      const type = response.headers.get("content-type") || "";
      const body = type.includes("application/json") ? await response.json() : await response.text();
      if (!response.ok) throw body;
      return body;
    }

    // Tabs (the WAI-ARIA pattern): one panel shows at a time and arrow keys move
    // between tabs. Returns the function that shows a tab by its data-tab name.
    function setupTabs(tablist) {
      const tabs = [...tablist.querySelectorAll("[role=tab]")];
      function showTab(name) {
        for (const tab of tabs) {
          const active = tab.dataset.tab === name;
          tab.classList.toggle("active", active);
          tab.setAttribute("aria-selected", String(active));
          tab.tabIndex = active ? 0 : -1;
          const panel = document.getElementById(tab.getAttribute("aria-controls"));
          panel.hidden = !active;
          // A bitmap laid out while its tab was hidden measured nothing; a
          // scroll event makes it re-measure its minimap viewport now it shows.
          if (active) {
            panel.querySelectorAll(".bitmap-scroll").forEach((scroll) => scroll.dispatchEvent(new Event("scroll")));
          }
        }
      }
      tabs.forEach((tab) => { tab.onclick = () => showTab(tab.dataset.tab); });
      tablist.onkeydown = (event) => {
        const step = { ArrowRight: 1, ArrowLeft: -1 }[event.key];
        if (!step) return;
        const visible = tabs.filter((tab) => !tab.hidden);
        const index = visible.findIndex((tab) => tab.getAttribute("aria-selected") === "true");
        const next = visible[(index + step + visible.length) % visible.length];
        showTab(next.dataset.tab);
        next.focus();
      };
      return showTab;
    }

    // A JWT as its three segments, each in its own brand colour.
    function renderJwt(target, token) {
      const [header, payload, signature] = token.split(".");
      target.innerHTML =
        `<span class="jwt-header">${escapeHtml(header)}</span>` +
        `<span class="jwt-dot">.</span>` +
        `<span class="jwt-payload">${escapeHtml(payload)}</span>` +
        `<span class="jwt-dot">.</span>` +
        `<span class="jwt-signature">${escapeHtml(signature)}</span>`;
    }

    const ROW_ENTRIES = 64;

    // One character per entry (two when bits is 8), 64 entries to a row, with
    // every non-zero — that is, not VALID — entry marked. `prefix` selects the
    // #<prefix>-bitmap, -bitmap-scroll, -minimap and -caption elements.
    function renderBitmap(prefix, lst, markedIndices) {
      const bitmapScroll = document.querySelector(`#${prefix}-bitmap-scroll`);
      const bitmap = document.querySelector(`#${prefix}-bitmap`);
      const minimap = document.querySelector(`#${prefix}-minimap`);
      const full = lst.full || lst.window;
      const width = ROW_ENTRIES * lst.chars_per_entry;
      let html = "";
      let minimapHtml = "";

      for (let offset = 0, rowNumber = 0; offset < full.length; offset += width, rowNumber += 1) {
        const row = full.slice(offset, offset + width);
        const index = offset / lst.chars_per_entry;
        const rowMarked = markedIndices.filter((entry) => entry >= index && entry < index + row.length / lst.chars_per_entry);
        const marked = [...row]
          .map((char, position) => {
            const spacer = position > 0 && position % (8 * lst.chars_per_entry) === 0 ? " " : "";
            return spacer + (char === "0" ? char : `<b>${escapeHtml(char)}</b>`);
          })
          .join("");
        html += `<span class="bitmap-index" data-row="${rowNumber}">${index}</span><span class="bitmap-row" data-row="${rowNumber}">${marked}</span>`;
        const marker = rowMarked.length
          ? `<button class="bitmap-minimap-marker" type="button" data-row="${rowNumber}" aria-label="Jump to entries ${escapeHtml(rowMarked.join(", "))}" title="Not valid: ${escapeHtml(rowMarked.join(", "))}"></button>`
          : `<button class="bitmap-minimap-row-jump" type="button" data-row="${rowNumber}" aria-label="Jump to entries starting at ${index}" title="Entries ${index} to ${index + ROW_ENTRIES - 1}"></button>`;
        minimapHtml += `<div class="bitmap-minimap-line">${marker}</div>`;
      }

      bitmap.innerHTML = html;
      minimap.innerHTML = `<div class="bitmap-minimap-viewport" role="slider" tabindex="0" aria-label="Spectrum scroll position" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"></div>` +
        (minimapHtml || `<span class="bitmap-minimap-empty">No revoked entries</span>`);
      const totalRows = Math.ceil(full.length / width);
      minimap.querySelectorAll("button[data-row]").forEach((marker) => {
        marker.onclick = (event) => {
          event.preventDefault();
          event.stopPropagation();
          const rowNumber = Number(marker.dataset.row);
          const maxScroll = Math.max(0, bitmapScroll.scrollHeight - bitmapScroll.clientHeight);
          const target = totalRows <= 1 ? 0 : rowNumber / (totalRows - 1) * maxScroll;
          bitmapScroll.scrollTo({ top: target, behavior: "auto" });
        };
      });

      const viewport = minimap.querySelector(".bitmap-minimap-viewport");
      const syncViewport = () => {
        const contentHeight = Math.max(1, bitmapScroll.scrollHeight);
        const progress = bitmapScroll.scrollTop / Math.max(1, bitmapScroll.scrollHeight - bitmapScroll.clientHeight);
        viewport.style.top = `${bitmapScroll.scrollTop / contentHeight * 100}%`;
        viewport.style.height = `${bitmapScroll.clientHeight / contentHeight * 100}%`;
        viewport.setAttribute("aria-valuenow", String(Math.round(progress * 100)));
      };
      let dragStartY = null;
      let dragStartScroll = 0;
      viewport.addEventListener("pointerdown", (event) => {
        dragStartY = event.clientY;
        dragStartScroll = bitmapScroll.scrollTop;
        viewport.classList.add("dragging");
        viewport.setPointerCapture(event.pointerId);
        event.preventDefault();
      });
      viewport.addEventListener("pointermove", (event) => {
        if (dragStartY === null) return;
        const track = Math.max(1, minimap.clientHeight - viewport.offsetHeight);
        const maxScroll = Math.max(0, bitmapScroll.scrollHeight - bitmapScroll.clientHeight);
        bitmapScroll.scrollTop = dragStartScroll + (event.clientY - dragStartY) / track * maxScroll;
      });
      const stopDrag = (event) => {
        if (dragStartY === null) return;
        dragStartY = null;
        viewport.classList.remove("dragging");
        if (viewport.hasPointerCapture(event.pointerId)) viewport.releasePointerCapture(event.pointerId);
      };
      viewport.addEventListener("pointerup", stopDrag);
      viewport.addEventListener("pointercancel", stopDrag);
      viewport.addEventListener("keydown", (event) => {
        if (event.key !== "ArrowUp" && event.key !== "ArrowDown") return;
        bitmapScroll.scrollTop += event.key === "ArrowDown" ? bitmapScroll.clientHeight / 5 : -bitmapScroll.clientHeight / 5;
        event.preventDefault();
      });
      bitmapScroll.onscroll = syncViewport;
      syncViewport();
      const last = lst.entries - 1;
      document.querySelector(`#${prefix}-caption`).textContent =
        `Entries 0 to ${last} of ${lst.entries}. Red bars mark rows with non-valid entries; click a bar to jump there.`;
    }
  </script>"""


_CONSOLE_SCRIPT = """<script>
    const registryRows = document.querySelector("#registry-rows");
    const allocationRows = document.querySelector("#allocation-rows");
    const allocationCount = document.querySelector("#allocation-count");
    const workingCard = document.querySelector("#working-card");
    // Where the panel rests while no list is open; re-rendering the rows parks
    // it here first, so it is never detached from the document.
    const workingCardHome = workingCard.parentElement;
    const jwtBox = document.querySelector("#jwt");
    const copyButton = document.querySelector("#copy-token");
    let allocations = [];
    let registry = [];
    let currentToken = "";
    // The working list the whole console is scoped to: null until the
    // operator clicks a list in the registry.
    let activeListUri = null;

    function workingPool() {
      return registry.find((item) => item.status_list_uri === activeListUri) || null;
    }

    // Dates read DD/MM/YYYY (DESIGN.md §15).
    function formatDate(iso) {
      return iso ? iso.split("-").reverse().join("/") : "—";
    }

    // The Entries tab is the working list's own inventory.
    function renderAllocations() {
      const entries = allocations.filter((item) => item.status_list_uri === activeListUri);
      allocationCount.textContent = entries.length;
      allocationRows.innerHTML = entries.length
        ? entries.map((item) => {
            const state = escapeHtml(item.status.toLowerCase());
            const revoked = item.status === "REVOKED";
            return `<tr class="${state}">
              <td class="cell-mono">${item.idx}</td>
              <td class="cell-mono">${escapeHtml(formatDate(item.expiry_date))}</td>
              <td><span class="status-chip status-${state}">${escapeHtml(statusLabel(item.status))}</span></td>
              <td>
                <button class="btn btn-sm btn-destructive" type="button" data-allocation-uri="${escapeHtml(item.status_list_uri)}" data-allocation-idx="${item.idx}" aria-label="Revoke entry ${item.idx}" ${revoked ? "disabled" : ""}>Revoke</button>
              </td>
            </tr>`;
          }).join("")
        : `<tr class="empty-row"><td colspan="4">No entry of this list is allocated yet. Entries appear here as the status-list API hands them out.</td></tr>`;
      allocationRows.querySelectorAll("button[data-allocation-uri]").forEach((button) => {
        button.onclick = () => guard(async () => {
          await jsonFetch("/dashboard/allocated-entries/revoke", {
            method: "POST",
            body: JSON.stringify({
              status_list_uri: button.dataset.allocationUri,
              idx: Number(button.dataset.allocationIdx),
            }),
          });
          await load();
          await refreshCard();
        });
      });
    }

    // The registry is both the inventory and the chooser: clicking a row opens
    // that list's panel underneath it; clicking the open row closes it.
    function renderRegistry() {
      workingCardHome.append(workingCard);
      registryRows.innerHTML = registry.length
        ? registry.map((item) => {
            const open = item.status_list_uri === activeListUri;
            return `<tr class="registry-row" tabindex="0" data-list="${escapeHtml(item.status_list_uri)}" aria-expanded="${open}"${open ? ' aria-current="true"' : ""}>
            <td><svg class="registry-chevron" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></td>
            <td>
              <a class="list-name" href="${escapeHtml(item.status_list_uri)}" target="_blank" rel="noreferrer" title="Open this list's token in a new tab">${escapeHtml(item.country)} · ${escapeHtml(item.doctype)}</a>
              <span class="list-meta"><span class="status-chip status-${item.expired ? "revoked" : "valid"}">${item.expired ? "Expired" : "Active"}</span><span class="font-mono">${item.allocated} allocated · ${item.revoked} revoked</span></span>
            </td>
            <td class="cell-mono">${escapeHtml(item.list_id)}</td>
            <td class="cell-mono">${escapeHtml(formatDate(item.expires))}</td>
          </tr>`;
          }).join("")
        : `<tr class="empty-row"><td colspan="4">No country × doctype list allocated yet.</td></tr>`;
      const openRow = registryRows.querySelector('tr[aria-current="true"]');
      if (!openRow) return;
      const detail = document.createElement("tr");
      detail.className = "registry-detail";
      const cell = document.createElement("td");
      cell.colSpan = 4;
      cell.append(workingCard);
      detail.append(cell);
      openRow.after(detail);
    }

    // The working-list panel follows the chosen list.
    function renderContext() {
      const pool = workingPool();
      workingCard.hidden = !pool;
      renderRegistry();
      renderAllocations();
    }

    async function load() {
      const [data, summaries] = await Promise.all([
        jsonFetch("/credentials"),
        jsonFetch("/debug/status-lists"),
      ]);
      allocations = data.allocated_entries;
      registry = summaries;
      // A list that disappears (state reset, server restart) drops the console
      // back to the unselected view.
      if (activeListUri && !workingPool()) activeListUri = null;
      renderContext();
    }

    async function showCard(uri) {
      renderDecodedToken(await jsonFetch(`/debug/status-list?${new URLSearchParams({ uri })}`));
    }

    async function refreshCard() {
      if (activeListUri) await showCard(activeListUri);
    }

    // The single context switch: pick a list, then read its signed token.
    async function selectList(uri) {
      if (uri !== activeListUri) {
        showTab("entries");
        showAddEntriesForm(false);
      }
      activeListUri = uri;
      renderContext();
      await showCard(uri);
    }

    // The working-list views: one tab visible at a time keeps the page short.
    const showTab = setupTabs(document.querySelector("#working-tabs"));

    function chooseRow(event) {
      if (event.target.closest("a")) return;  // the list name opens its URI instead
      const row = event.target.closest("tr[data-list]");
      if (!row) return;
      const uri = row.dataset.list;
      guard(async () => {
        if (uri === activeListUri) {
          activeListUri = null;      // the open row closes its panel
          renderContext();
        } else {
          await selectList(uri);
        }
        // Re-rendering the registry drops focus; keyboard users keep their row.
        if (event.type === "keydown") registryRows.querySelector(`tr[data-list="${CSS.escape(uri)}"]`)?.focus();
      });
    }
    registryRows.onclick = chooseRow;
    // Only a focused row reacts to Enter and Space: the open panel lives in the
    // same table body, and its inputs and buttons keep their own keys.
    registryRows.onkeydown = (event) => {
      if (!event.target.matches("tr[data-list]")) return;
      if (event.key !== "Enter" && event.key !== " ") return;
      event.preventDefault();
      chooseRow(event);
    };

    // A button that opens the form under it on demand, so the tables come
    // first: `New status list` under the lists, `Add entries` under the entries.
    function revealer(toggle, form, firstField) {
      const show = (visible) => {
        form.hidden = !visible;
        toggle.setAttribute("aria-expanded", String(visible));
        if (visible) firstField.focus();
      };
      toggle.onclick = () => show(form.hidden);
      return show;
    }

    const showAddEntriesForm = revealer(
      document.querySelector("#add-entries-toggle"),
      document.querySelector("#add-entries-form"),
      document.querySelector("#entries-count"),
    );
    document.querySelector("#add-entries-cancel").onclick = () => showAddEntriesForm(false);

    // Top-up of the working list: entries land in this list only, or the
    // server refuses them (a full list is never rolled over into another).
    document.querySelector("#add-entries").onclick = () => guard(async () => {
      const pool = workingPool();
      if (!pool) return notify("Click a country × doctype list first.", "info");
      await jsonFetch("/dashboard/status-lists/entries", {
        method: "POST",
        body: JSON.stringify({
          status_list_uri: pool.status_list_uri,
          expiry_date: document.querySelector("#entries-expiry").value || pool.expires,
          count: Number(document.querySelector("#entries-count").value || 10),
        }),
      });
      showAddEntriesForm(false);
      await load();
      await refreshCard();
    });

    const showNewListForm = revealer(
      document.querySelector("#new-list-toggle"),
      document.querySelector("#new-list-form"),
      document.querySelector("#new-country"),
    );
    document.querySelector("#new-list-cancel").onclick = () => showNewListForm(false);

    document.querySelector("#new-list").onclick = () => guard(async () => {
      const data = await jsonFetch("/dashboard/status-lists", {
        method: "POST",
        body: JSON.stringify({
          country: document.querySelector("#new-country").value || "EU",
          doctype: document.querySelector("#new-doctype").value || "org.iso.18013.5.1.mDL",
          expiry_date: document.querySelector("#new-expiry").value || "2099-12-31",
          count: 1,
        }),
      });
      showNewListForm(false);
      await load();
      await selectList(data.status_list_uri);
    });

    document.querySelector("#registry-refresh").onclick = () => guard(load);

    function renderDecodedToken(data) {
      currentToken = data.token;
      renderJwt(jwtBox, data.token);
      document.querySelector("#jwt-header").textContent = JSON.stringify(data.header, null, 2);
      document.querySelector("#jwt-payload").textContent = JSON.stringify(data.payload, null, 2);
      document.querySelector("#lst-bits").textContent = data.bits;
      document.querySelector("#lst-size").textContent = data.size;
      document.querySelector("#lst-valid").textContent = data.valid;
      document.querySelector("#lst-revoked").textContent = data.revoked;
      renderBitmap("lst", data.lst, data.revoked_indices);
      document.querySelector("#lst-note").textContent =
        `"lst" is ${data.lst.compressed_bytes} compressed bytes; it inflates to ` +
        `${data.lst.inflated_bytes} bytes holding ${data.lst.entries} entries at ` +
        `${data.bits} bit per entry. The Decoded status list tab shows the inflated entries.`;

      const shown = data.revoked_indices.slice(0, 200);
      const rest = data.revoked_indices.length - shown.length;
      document.querySelector("#lst-indices").textContent = shown.length
        ? shown.join(", ") + (rest > 0 ? `, and ${rest} more` : "")
        : "None";
    }

    copyButton.onclick = async () => {
      if (!currentToken) return;
      try {
        await navigator.clipboard.writeText(currentToken);
        copyButton.textContent = "Copied";
      } catch (error) {
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(jwtBox);
        selection.removeAllRanges();
        selection.addRange(range);
        copyButton.textContent = "Press ctrl+c";
      }
      setTimeout(() => { copyButton.textContent = "Copy the JWT"; }, 2000);
    };

    load().catch(notify);
  </script>"""


def console_html() -> str:
    """The credential console."""
    return page(
        title="Token status list console · Credimi",
        active="Console",
        body=_CONSOLE_BODY,
        scripts=_SHARED_SCRIPT + "\n" + _CONSOLE_SCRIPT,
    )


_EXPLORER_BODY = (
    _hero_band(
        "Status list explorer",
        "Paste a Token Status List from any issuer and inspect it: the decoded header and"
        ' payload, the inflated <span class="mono">lst</span>, every revoked index, and the'
        " status of a single index.",
    )
    + """
  <main>
    <section class="page-section" aria-labelledby="payload-title">
    <div class="container">
"""
    + _section_intro(
        2,
        "payload-title",
        "Inspect a status list",
        'Paste a JWT, a CWT as hex or base64, the JSON payload or the bare <span class="mono">lst</span>'
        " value, load a file, or pick one of this server's lists. Signatures are not verified.",
    )
    + """
      <label class="form-field">
        <span class="subsection-heading">Payload</span>
        <textarea id="explore-payload" class="payload-input" spellcheck="false"
          placeholder="eyJhbGciOiJFUzI1NiIs… · d28450a3… · {&quot;bits&quot;:1,&quot;lst&quot;:&quot;eNrb…&quot;} · eNrb…"></textarea>
      </label>
      <details class="disclosure mt-4">
        <summary>Advanced</summary>
        <div class="disclosure-body">
          <div class="form-field">
            <span class="subsection-heading" id="explore-bits-label">Bits per entry</span>
            <div class="segmented bits-segmented" role="radiogroup" aria-labelledby="explore-bits-label">
              <label><input type="radio" name="explore-bits" value="1" checked><span>1</span></label>
              <label><input type="radio" name="explore-bits" value="2"><span>2</span></label>
              <label><input type="radio" name="explore-bits" value="4"><span>4</span></label>
              <label><input type="radio" name="explore-bits" value="8"><span>8</span></label>
            </div>
            <p class="text-sm text-muted">Read only for a bare <span class="mono">lst</span> value; tokens and JSON carry their own.</p>
          </div>
        </div>
      </details>
      <div class="form-row mt-4">
        <label class="form-field form-field-grow">
          <span class="subsection-heading">Load from this server</span>
          <select id="explore-server"><option value="">Choose a list…</option></select>
        </label>
        <label class="btn btn-lg btn-outline btn-file"><input id="explore-file" type="file">Load a file</label>
        <button id="explore" class="btn btn-lg btn-primary" type="button">Inspect</button>
      </div>
    </div>
    </section>

    <section class="page-section page-section-white" id="explore-card" aria-labelledby="decoded-title" hidden>
    <div class="container">
"""
    + _section_intro(2, "decoded-title", "Inspection result", '<span id="explore-summary"></span>')
    + """
      <div class="tabs" role="tablist" id="explore-tabs" aria-label="Inspection views">
        <button class="tab-btn active" type="button" role="tab" id="explore-tab-decoded" data-tab="decoded" aria-selected="true" aria-controls="explore-decoded-panel">Decoded status list</button>
        <button class="tab-btn" type="button" role="tab" id="explore-tab-token" data-tab="token" aria-selected="false" aria-controls="explore-token-panel" tabindex="-1">Token</button>
      </div>

      <div role="tabpanel" id="explore-decoded-panel" aria-labelledby="explore-tab-decoded">
        <div class="form-row">
          <label class="form-field form-field-md">
            <span class="subsection-heading">Check an index</span>
            <input id="explore-index" type="number" min="0" value="0">
          </label>
          <span id="explore-index-status" class="index-check-status" aria-live="polite"></span>
        </div>
        <div class="metric-grid mt-4">
          <div class="card">
            <strong class="metric-value" id="explore-bits-value">0</strong>
            <span class="eyebrow">Bits per entry</span>
          </div>
          <div class="card">
            <strong class="metric-value" id="explore-size">0</strong>
            <span class="eyebrow">Entries</span>
          </div>
          <div class="card">
            <strong class="metric-value" id="explore-valid">0</strong>
            <span class="eyebrow">Valid</span>
          </div>
          <div class="card">
            <strong class="metric-value" id="explore-not-valid">0</strong>
            <span class="eyebrow">Not valid</span>
          </div>
        </div>
        <p class="lst-note" id="explore-note"></p>
        <p class="eyebrow mt-4">Inflated lst spectrum</p>
        <div class="bitmap-shell">
          <div class="bitmap-scroll" id="explore-bitmap-scroll" tabindex="0" aria-label="Full inflated status list">
            <div class="bitmap" id="explore-bitmap"></div>
          </div>
          <div class="bitmap-minimap-scroll" id="explore-minimap-scroll" tabindex="0" aria-label="Non-valid entry minimap">
            <div class="bitmap-minimap" id="explore-minimap"></div>
          </div>
        </div>
        <p class="bitmap-caption" id="explore-caption"></p>
        <p class="eyebrow mt-4">Non-valid indices</p>
        <div id="explore-indices"></div>
        <div class="btn-row mt-4" id="explore-copy-row">
          <button id="explore-copy-indices" class="btn btn-sm btn-outline" type="button">Copy the indices</button>
        </div>
      </div>

      <div role="tabpanel" id="explore-token-panel" aria-labelledby="explore-tab-token" hidden>
        <div class="jwt-columns" id="explore-columns">
          <div id="explore-encoded">
            <p class="eyebrow">Encoded</p>
            <pre class="output jwt" id="explore-jwt"></pre>
            <div class="flex-between gap-3 mt-4">
              <p class="jwt-legend">
                <span class="badge"><span class="badge-dot legend-header"></span>Header</span>
                <span class="badge"><span class="badge-dot legend-payload"></span>Payload</span>
                <span class="badge"><span class="badge-dot legend-signature"></span>Signature</span>
              </p>
            </div>
          </div>
          <div class="jwt-decoded">
            <div id="explore-header-block">
              <p class="eyebrow">Decoded header</p>
              <pre id="explore-header"></pre>
            </div>
            <p class="eyebrow mt-4">Decoded payload</p>
            <pre id="explore-payload-json"></pre>
          </div>
        </div>
      </div>
    </div>
    </section>
"""
    + _NOTICE
    + """
  </main>"""
)


_EXPLORER_SCRIPT = """<script>
    const STATUS_NAMES = { 0: "VALID", 1: "REVOKED", 2: "SUSPENDED" };
    const FORMAT_NAMES = { jwt: "a JWT", cwt: "a CWT", json: "a JSON payload", lst: "a bare lst" };
    const payloadInput = document.querySelector("#explore-payload");
    const resultSection = document.querySelector("#explore-card");
    const serverLists = document.querySelector("#explore-server");
    const showTab = setupTabs(document.querySelector("#explore-tabs"));
    let explored = null;

    function statusName(value) {
      return STATUS_NAMES[value] || `UNKNOWN(${value})`;
    }

    function statusAt(lst, index) {
      const width = lst.chars_per_entry;
      return parseInt(lst.full.slice(index * width, (index + 1) * width), 16);
    }

    function groupedIndices(data) {
      const groups = {};
      for (const index of data.non_valid_indices) {
        const name = statusName(statusAt(data.lst, index));
        (groups[name] ||= []).push(index);
      }
      return groups;
    }

    function renderIndices(data) {
      const groups = groupedIndices(data);
      const names = Object.keys(groups);
      document.querySelector("#explore-indices").innerHTML = names.length
        ? names.map((name) => {
            const indices = groups[name];
            const shown = indices.slice(0, 500);
            const rest = indices.length - shown.length;
            return `<div class="index-group"><p class="index-group-name">${escapeHtml(statusLabel(name))} · ${indices.length}</p>` +
              `<p class="index-list">${shown.join(", ")}${rest > 0 ? `, and ${rest} more` : ""}</p></div>`;
          }).join("")
        : `<p class="index-list">None: every entry is valid.</p>`;
      document.querySelector("#explore-copy-row").hidden = !names.length;
    }

    // The index check answers as you type; an empty field shows nothing.
    function lookupIndex() {
      const target = document.querySelector("#explore-index-status");
      const raw = document.querySelector("#explore-index").value;
      if (!explored || raw === "") {
        target.innerHTML = "";
        return;
      }
      const index = Number(raw);
      if (!Number.isInteger(index) || index < 0 || index >= explored.size) {
        target.innerHTML = `<span class="status-chip status-reject">Out of range: 0 to ${explored.size - 1}</span>`;
        return;
      }
      const name = statusName(statusAt(explored.lst, index));
      target.innerHTML = `<span class="status-chip status-${escapeHtml(name.toLowerCase())}">${escapeHtml(statusLabel(name))}</span>`;
    }

    // The Token tab: a JWT shows encoded beside decoded, a CWT or JSON payload
    // its decoded parts only, and a bare lst has no token to show.
    function renderToken(data, payload) {
      const jwt = data.format === "jwt";
      document.querySelector("#explore-tab-token").hidden = data.format === "lst";
      document.querySelector("#explore-encoded").hidden = !jwt;
      document.querySelector("#explore-columns").classList.toggle("jwt-columns-single", !jwt);
      if (jwt) renderJwt(document.querySelector("#explore-jwt"), payload);
      document.querySelector("#explore-header-block").hidden = !Object.keys(data.header).length;
      document.querySelector("#explore-header").textContent = JSON.stringify(data.header, null, 2);
      document.querySelector("#explore-payload-json").textContent = JSON.stringify(data.payload, null, 2);
    }

    function renderExplored(data, payload) {
      explored = data;
      const signed = data.format === "jwt" || data.format === "cwt";
      document.querySelector("#explore-summary").textContent =
        `Decoded from ${FORMAT_NAMES[data.format] || data.format}: ${data.size} entries at ` +
        `${data.bits} bit${data.bits === 1 ? "" : "s"} per entry.` +
        (signed ? " The signature was not verified." : "");
      document.querySelector("#explore-bits-value").textContent = data.bits;
      document.querySelector("#explore-size").textContent = data.size;
      document.querySelector("#explore-valid").textContent = data.counts.VALID || 0;
      document.querySelector("#explore-not-valid").textContent = data.non_valid_indices.length;
      const counts = Object.entries(data.counts)
        .map(([name, count]) => `${count} ${statusLabel(name).toLowerCase()}`)
        .join(", ");
      document.querySelector("#explore-note").textContent =
        `"lst" is ${data.lst.compressed_bytes} compressed bytes; it inflates to ` +
        `${data.lst.inflated_bytes} bytes: ${counts}.`;
      renderIndices(data);
      renderToken(data, payload);
      resultSection.hidden = false;
      showTab("decoded");
      renderBitmap("explore", data.lst, data.non_valid_indices);
      lookupIndex();
    }

    async function inspect() {
      const payload = payloadInput.value.trim();
      if (!payload) {
        return notify("Paste a payload, load a file, or pick one of this server's lists.", "info", "Nothing to inspect");
      }
      const bits = Number(document.querySelector('input[name="explore-bits"]:checked').value);
      let data;
      try {
        data = await jsonFetch("/debug/status-list/explore", {
          method: "POST",
          body: JSON.stringify({ payload, bits }),
        });
      } catch (error) {
        resultSection.hidden = true;  // no stale result under a failed payload
        explored = null;
        throw error;
      }
      renderExplored(data, payload);
      resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    // This server's lists, the legacy one first; picking one inspects its JWT.
    async function loadServerLists() {
      const summaries = await jsonFetch("/debug/status-lists");
      const chosen = serverLists.value;
      serverLists.innerHTML =
        '<option value="">Choose a list…</option>' +
        '<option value="/status/1">Legacy credential list · /status/1</option>' +
        summaries.map((item) => {
          const path = new URL(item.status_list_uri).pathname;
          return `<option value="${escapeHtml(path)}">${escapeHtml(item.country)} · ${escapeHtml(item.doctype)} · ${escapeHtml(item.list_id.slice(0, 8))}</option>`;
        }).join("");
      serverLists.value = chosen;
    }
    serverLists.onfocus = () => guard(loadServerLists);
    serverLists.onchange = () => guard(async () => {
      if (!serverLists.value) return;
      const response = await fetch(serverLists.value, {
        cache: "no-store",
        headers: { accept: "application/statuslist+jwt" },
      });
      if (!response.ok) throw await response.text();
      payloadInput.value = (await response.text()).trim();
      await inspect();
    });

    // Binary CWT files become base64; text files (JWT, JSON, hex) load as-is.
    document.querySelector("#explore-file").onchange = (event) => guard(async () => {
      const file = event.target.files[0];
      if (!file) return;
      const bytes = new Uint8Array(await file.arrayBuffer());
      event.target.value = "";  // picking the same file again still loads it
      let text = null;
      try { text = new TextDecoder("utf-8", { fatal: true }).decode(bytes); } catch (error) { text = null; }
      if (text === null || bytes[0] === 0xd2 || bytes[0] === 0xd8 || bytes[0] === 0x84) {
        let binary = "";
        for (const byte of bytes) binary += String.fromCharCode(byte);
        payloadInput.value = btoa(binary);
      } else {
        payloadInput.value = text.trim();
      }
      await inspect();
    });

    document.querySelector("#explore").onclick = () => guard(inspect);
    document.querySelector("#explore-index").oninput = lookupIndex;
    document.querySelector("#explore-copy-indices").onclick = async (event) => {
      if (!explored) return;
      await navigator.clipboard.writeText(explored.non_valid_indices.join(","));
      event.target.textContent = "Copied";
      setTimeout(() => { event.target.textContent = "Copy the indices"; }, 2000);
    };

    guard(loadServerLists);
  </script>"""


def explorer_html() -> str:
    """Paste-and-inspect explorer for status lists from any issuer."""
    return page(
        title="Status list explorer · Credimi",
        active="Explorer",
        body=_EXPLORER_BODY,
        scripts=_SHARED_SCRIPT + "\n" + _EXPLORER_SCRIPT,
    )


SWAGGER_CSS = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css"
SWAGGER_JS = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"


def docs_html(openapi_url: str) -> str:
    """Swagger UI inside the same branded shell as the rest of the app."""
    body = (
        _hero_band("API documentation", "Every endpoint of the mock Token Status List server.")
        + """
  <main>
    <section class="page-section" aria-labelledby="endpoints-title">
    <div class="container">
"""
        + _section_intro(
            2,
            "endpoints-title",
            "Endpoints",
            'Generated from the OpenAPI document at <span class="mono">/openapi.json</span>.',
        )
        + """
      <div class="docs-frame"><div id="swagger-ui"></div></div>
    </div>
    </section>
  </main>"""
    )
    return page(
        title="API documentation · Credimi",
        active="API docs",
        body=body,
        head=f'  <link rel="stylesheet" href="{SWAGGER_CSS}">\n',
        scripts=f"""<script src="{SWAGGER_JS}"></script>
  <script>
    window.ui = SwaggerUIBundle({{
      url: "{openapi_url}",
      dom_id: "#swagger-ui",
      deepLinking: true,
      layout: "BaseLayout",
    }});
  </script>""",
    )
