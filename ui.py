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
LOGO_WORDMARK = f"{BRAND_ROOT}/logos/credimi_logo-transp.svg"
LOGO_WORDMARK_WHITE = f"{BRAND_ROOT}/logos/credimi_logo-transp_white.svg"
CREDIMI_URL = "https://credimi.io"

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

    /* Logo links carry no underline: the brand rule underlines every anchor. */
    .topbar-logo { display: block; text-decoration: none; }
    .extras-bottom a { text-decoration: none; }

    /* Grid items default to min-width:auto, so the table's own min-width would
       widen the whole page instead of scrolling inside its wrapper. */
    .stack { display: grid; gap: var(--space-6); }
    .stack > *, .card-grid > * { min-width: 0; }
    .batch-card { max-width: none; }
    /* Page gutter: the topbar, hero, content and footer share one fixed side
       gutter so their edges line up, and they grow with the window instead of
       stopping at the brand max-width. Small screens keep the brand gutter. */
    :root { --page-gutter: 46px; }
    .topbar-inner, .hero-inner, .container, .footer-inner {
      max-width: none;
      padding-left: var(--page-gutter);
      padding-right: var(--page-gutter);
    }
    @media (max-width: 768px) {
      :root { --page-gutter: var(--space-4); }
    }
    /* Console layout: a two-column dashboard inside the page gutter —
       forms and info on the left, results on the right, so every CTA
       produces feedback the user can see without scrolling away. */
    .console-grid {
      display: grid;
      grid-template-columns: minmax(0, 3fr) minmax(0, 2fr);
      align-items: start;
      gap: var(--space-6);
    }
    .console-right {
      position: sticky;
      top: calc(var(--topbar-height) + var(--space-4));
      max-height: calc(100vh - var(--topbar-height) - 2 * var(--space-4));
      overflow-y: auto;
    }
    @media (max-width: 1100px) {
      .console-grid { grid-template-columns: 1fr; }
      .console-right {
        position: static;
        max-height: none;
        overflow-y: visible;
      }
    }
    .batch-fields {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 0 var(--space-3);
    }
    .batch-fields .field-label { margin-top: var(--space-3); }
    @media (max-width: 900px) {
      .batch-fields { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 560px) {
      .batch-fields { grid-template-columns: 1fr; }
    }
    .test-table-wrap { max-width: 100%; }
    .field-label {
      display: block;
      margin: var(--space-3) 0 var(--space-2);
      font-size: var(--fs-sm);
      font-weight: 500;
    }
    input[type="number"] {
      font-family: var(--font-sans);
      font-size: var(--fs-base);
      height: 36px;
      padding: 0 var(--space-4);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      background: var(--bg);
      color: var(--fg);
      width: 100%;
      transition: border-color 200ms ease-out, box-shadow 200ms ease-out;
    }

    .credential-scroll {
      max-height: 420px;
      overflow: auto;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--bg);
    }
    .credential-scroll .test-table-wrap { overflow: visible; }
    .decoded-credentials-scroll {
      max-height: 420px;
      overflow: auto;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--bg);
    }
    .decoded-credentials-scroll .test-table-wrap { overflow: visible; }
    input[type="number"]:focus {
      outline: none;
      border-color: var(--brand-primary);
      box-shadow: 0 0 0 3px oklch(0.2955 0.1659 277.31 / 0.18);
    }

    .btn-secondary {
      background: var(--brand-secondary-deep);
      color: var(--brand-primary);
    }
    .btn-secondary:hover { background: var(--brand-secondary-strong); }
    .btn-success {
      background: var(--success);
      color: var(--fg-on-primary);
    }
    .btn-success:hover { background: var(--success-border); }
    .btn-row { display: flex; flex-wrap: wrap; gap: var(--space-2); }
    .btn-stack { display: grid; gap: var(--space-2); margin-top: var(--space-3); }
    .btn-row .btn, .btn-stack .btn { justify-content: center; }

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
    .test-table input[type="checkbox"] {
      accent-color: var(--brand-primary);
      width: 16px;
      height: 16px;
    }
    .test-table td.cell-mono {
      font-family: var(--font-mono);
      font-size: var(--fs-xs);
      white-space: nowrap;
    }
    .test-table td.cell-select { width: 32px; }
    .test-table tr.revoked td { background: var(--destructive-bg); }
    .test-table .empty-row td {
      color: var(--fg-subtle);
      padding: var(--space-5) var(--space-3);
    }

    .status-valid { background: var(--success-bg); color: var(--success); }
    .status-valid::before { background: var(--success); }
    .status-revoked { background: var(--destructive-bg); color: var(--destructive); }
    .status-revoked::before { background: var(--destructive); }
    .status-accept { background: var(--success-bg); color: var(--success); }
    .status-accept::before { background: var(--success); }
    .status-reject { background: var(--destructive-bg); color: var(--destructive); }
    .status-reject::before { background: var(--destructive); }
    .status-unchecked { background: var(--bg-muted); color: var(--fg-subtle); }
    .status-unchecked::before { background: var(--fg-muted); }

    .output {
      min-height: 96px;
      white-space: pre-wrap;
      word-break: break-word;
      margin: 0;
    }

    /* Status list token: the three JWT segments, each on its own brand
       colour, plus the decoded views underneath. */
    #token-card { scroll-margin-top: calc(var(--topbar-height) + var(--space-4)); }
    .jwt { font-size: var(--fs-sm); }
    .jwt-header { color: var(--brand-primary); font-weight: 600; }
    .jwt-payload { color: var(--brand-accent-vivid); font-weight: 600; }
    .jwt-signature { color: var(--credential); font-weight: 600; }
    .jwt-dot { color: var(--fg-muted); }
    .jwt-legend {
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-2);
      margin-bottom: var(--space-3);
    }
    .jwt-legend .badge { background: var(--bg-muted); }
    .jwt-legend .badge-dot { width: 8px; height: 8px; }
    .legend-header { background: var(--brand-primary); }
    .legend-payload { background: var(--brand-accent-vivid); }
    .legend-signature { background: var(--credential); }

    .subhead {
      margin: var(--space-6) 0 var(--space-3);
      padding-bottom: var(--space-2);
      border-bottom: 1px solid var(--border);
      font: 700 var(--fs-xl)/var(--lh-xl) var(--font-sans);
      letter-spacing: -0.005em;
    }
    .subhead::after { content: ':'; }
    .decoded-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: var(--space-4);
    }
    .decoded-grid > * { min-width: 0; }
    .decoded-grid pre { max-height: 320px; overflow: auto; }
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
    .index-groups .eyebrow { margin-top: var(--space-3); }
    .index-groups .eyebrow:first-child { margin-top: 0; }

    /* Explorer: the pasted payload, its options, and the single-index lookup. */
    .payload-input {
      display: block;
      width: 100%;
      min-height: 160px;
      padding: var(--space-3) var(--space-4);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      background: var(--bg);
      color: var(--fg);
      font: var(--fs-sm)/1.5 var(--font-mono);
      resize: vertical;
      word-break: break-all;
    }
    .payload-input:focus,
    .explorer-select:focus {
      outline: none;
      border-color: var(--brand-primary);
      box-shadow: 0 0 0 3px oklch(0.2955 0.1659 277.31 / 0.18);
    }
    .explorer-fields {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 0 var(--space-3);
    }
    @media (max-width: 560px) {
      .explorer-fields { grid-template-columns: 1fr; }
    }
    .explorer-select {
      width: 100%;
      height: 36px;
      padding: 0 var(--space-4);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      background: var(--bg);
      color: var(--fg);
      font: var(--fs-base) var(--font-sans);
    }
    /* The status-list card decodes one list at a time: the picker names the
       legacy credential list and every allocated country × doctype pool. */
    .list-picker { display: flex; align-items: center; gap: var(--space-3); }
    #lst-select {
      height: 36px;
      max-width: 340px;
      padding: 0 var(--space-4);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      background: var(--bg);
      color: var(--fg);
      font: var(--fs-sm) var(--font-sans);
    }
    .explorer-file { font: var(--fs-sm) var(--font-sans); padding-top: var(--space-2); }
    .index-lookup {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: var(--space-3);
    }
    .index-lookup input[type="number"] { width: 160px; }
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
      .decoded-grid { grid-template-columns: 1fr; }
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
        ("Status list API", "/token_status_list/take"),
    )
    items = "\n".join(
        '        <li><a href="{href}"{current}>{label}</a></li>'.format(
            href=href,
            label=label,
            current=' aria-current="page"' if label == active else "",
        )
        for label, href in links
    )
    return f"""  <nav class="topbar">
    <div class="topbar-inner">
      <a class="topbar-logo" href="/"><img src="{LOGO_WORDMARK}" alt="Credimi"></a>
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
            <a href="/token_status_list/take">Status list API</a>
            <a href="/status/1">Legacy status list token</a>
            <a href="/token_status_list/aggregation">Status list aggregation</a>
            <a href="/.well-known/jwks.json">JWKS</a>
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


_CONSOLE_BODY = """  <header class="hero">
    <div class="hero-inner">
      <p class="eyebrow">EUDI conformance utility</p>
      <h1>Token status list console</h1>
        <p>Create test credentials, revoke selected entries, and verify them against the
        signed Status List Token. The registry debugger below exposes paired country × doctype
        Token Status Lists and ISO 18013-5 identifier lists in JWT and CWT forms.</p>
    </div>
  </header>
  <main class="page-content">
    <div class="container">
    <div class="console-grid">
      <div class="stack console-left">
      <section class="card" id="registry-card">
        <div class="section-header">
          <h2>Country × doctype lists <span id="registry-count" class="count-chip">0</span></h2>
          <button id="registry-refresh" class="btn btn-sm btn-outline">Refresh lists</button>
        </div>
        <p class="text-sm text-muted">Paired Token Status List and ISO 18013-5 identifier-list resources. Choose the list to operate on: every panel below then belongs to that list, and the console never mixes the legacy <span class="mono">/status/1</span> credential list with an allocated country × doctype pool.</p>
        <div class="list-picker mt-4">
          <label class="field-label" for="lst-select">Operate on</label>
          <select id="lst-select" aria-label="Status list to operate on"></select>
          <button id="new-list-toggle" class="btn btn-sm btn-success" aria-expanded="false" aria-controls="new-list-form">New status list</button>
        </div>
        <p class="text-sm text-muted mt-4" id="ctx-scope"></p>
        <div id="new-list-form" class="mt-4" hidden>
          <div class="batch-fields">
            <div>
              <label class="field-label" for="new-country">Country</label>
              <input id="new-country" type="text" value="EU" maxlength="16">
            </div>
            <div>
              <label class="field-label" for="new-doctype">Doctype</label>
              <input id="new-doctype" type="text" value="org.iso.18013.5.1.mDL" maxlength="128">
            </div>
            <div>
              <label class="field-label" for="new-expiry">List expiry</label>
              <input id="new-expiry" type="date" value="2099-12-31">
            </div>
          </div>
          <div class="btn-row mt-4">
            <button id="new-list" class="btn btn-md btn-success">Create status list</button>
            <button id="new-list-cancel" class="btn btn-md btn-outline">Cancel</button>
          </div>
        </div>
        <div class="test-table-wrap mt-4">
          <table class="test-table">
            <thead><tr><th>Country</th><th>Doctype</th><th>List UUID</th><th>Allocated</th><th>Revoked</th><th>Expiry</th><th>State</th></tr></thead>
            <tbody id="registry-rows"></tbody>
          </table>
        </div>
      </section>

      <section class="card batch-card" id="legacy-card" hidden>
        <div class="section-header">
          <h2>Credentials <span id="row-count" class="count-chip">0</span></h2>
          <div class="btn-row">
            <button id="refresh" class="btn btn-sm btn-outline">Refresh</button>
            <button id="reset" class="btn btn-sm btn-outline">Reset state</button>
            <button id="token" class="btn btn-sm btn-outline">Fetch status list token</button>
          </div>
        </div>
        <p class="text-sm text-muted">Credentials and their verification belong to the legacy <span class="mono">/status/1</span> list. A batch adds credentials here and allocates each one a paired country × doctype entry.</p>
        <div class="batch-fields">
          <div>
            <label class="field-label" for="count">Count</label>
            <input id="count" type="number" min="1" max="500" value="10">
          </div>
          <div>
            <label class="field-label" for="prefix">Credential prefix</label>
            <input id="prefix" type="text" value="cred">
          </div>
          <div>
            <label class="field-label" for="country">Country</label>
            <input id="country" type="text" value="EU" maxlength="16">
          </div>
          <div>
            <label class="field-label" for="doctype">Doctype</label>
            <input id="doctype" type="text" value="org.iso.18013.5.1.mDL" maxlength="128">
          </div>
          <div>
            <label class="field-label" for="expiry-date">List expiry</label>
            <input id="expiry-date" type="date" value="2099-12-31">
          </div>
        </div>
        <div class="btn-row mt-4 mb-4">
          <button id="create" class="btn btn-md btn-primary">Create random batch</button>
        </div>
        <div class="btn-row mb-4">
          <button id="all" class="btn btn-sm btn-outline">Select all</button>
          <button id="none" class="btn btn-sm btn-outline">Select none</button>
          <button id="verify" class="btn btn-sm btn-secondary">Verify selected</button>
          <button id="revoke" class="btn btn-sm btn-destructive">Revoke selected</button>
        </div>
        <div class="credential-scroll">
          <div class="test-table-wrap">
            <table class="test-table">
              <thead>
                <tr>
                  <th><span class="text-xs">Pick</span></th>
                  <th>Credential</th>
                  <th>Index</th>
                  <th>Status</th>
                  <th>Verification</th>
                </tr>
              </thead>
              <tbody id="rows"></tbody>
            </table>
          </div>
        </div>
      </section>

      <section class="card" id="allocation-card" hidden>
        <div class="section-header">
          <h2>Known allocated status-list entries <span id="allocation-count" class="count-chip">0</span></h2>
        </div>
        <p class="text-sm text-muted">Entries of the working list. They identify a country, doctype, list and index, but carry no credential identifier: these pools are allocated through the status-list API, not through the credential console.</p>
        <div class="batch-fields">
          <div>
            <label class="field-label" for="entries-count">Count</label>
            <input id="entries-count" type="number" min="1" max="500" value="10">
          </div>
          <div>
            <label class="field-label" for="entries-expiry">List expiry</label>
            <input id="entries-expiry" type="date" value="2099-12-31">
          </div>
        </div>
        <div class="btn-row mt-4 mb-4">
          <button id="add-entries" class="btn btn-md btn-secondary">Add entries to this list</button>
        </div>
        <div class="credential-scroll">
          <div class="test-table-wrap">
            <table class="test-table">
              <thead><tr><th>Country</th><th>Doctype</th><th>Index</th><th>Expiry</th><th>Status</th><th>Status list URI</th><th>Actions</th></tr></thead>
              <tbody id="allocation-rows"></tbody>
            </table>
          </div>
        </div>
      </section>

      </div>

      <aside class="stack console-right" aria-label="Results panel">
        <section class="card">
          <div class="section-header"><h2>Output</h2></div>
          <pre class="output" id="out">Ready</pre>
        </section>

      <section class="card" id="token-card" hidden>
        <div class="section-header">
          <h2>Status list token</h2>
          <button id="copy-token" class="btn btn-sm btn-outline">Copy the JWT</button>
        </div>
        <p class="text-sm text-muted" id="lst-scope"></p>
        <p class="jwt-legend">
          <span class="badge"><span class="badge-dot legend-header"></span>Header</span>
          <span class="badge"><span class="badge-dot legend-payload"></span>Payload</span>
          <span class="badge"><span class="badge-dot legend-signature"></span>Signature</span>
        </p>
        <pre class="output jwt" id="jwt"></pre>

        <h3 class="subhead">Decoded token</h3>
        <div class="decoded-grid">
          <div>
            <p class="eyebrow">Header</p>
            <pre id="jwt-header"></pre>
          </div>
          <div>
            <p class="eyebrow">Payload</p>
            <pre id="jwt-payload"></pre>
            <p class="lst-note" id="lst-note"></p>
          </div>
        </div>

        <h3 class="subhead">Status list</h3>
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
        <div class="decoded-credentials-scroll">
          <div class="test-table-wrap">
            <table class="test-table">
              <thead>
                <tr>
                  <th>Credential</th>
                  <th>Index</th>
                  <th>Decoded status</th>
                </tr>
              </thead>
              <tbody id="lst-rows"></tbody>
            </table>
          </div>
        </div>
        <div class="btn-row mt-4" id="assignment-pagination"></div>

        <h3 class="subhead">Signing key</h3>
        <p class="eyebrow" id="jwks-label">JWKS · /.well-known/jwks.json</p>
        <pre id="jwks"></pre>
      </section>

      </aside>
    </div>
    </div>
  </main>"""


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
    const rows = document.querySelector("#rows");
    const registryRows = document.querySelector("#registry-rows");
    const registryCount = document.querySelector("#registry-count");
    const allocationRows = document.querySelector("#allocation-rows");
    const allocationCount = document.querySelector("#allocation-count");
    const out = document.querySelector("#out");
    const rowCount = document.querySelector("#row-count");
    let credentials = [];
    let verification = {};
    let allocations = [];
    let registry = [];

    function selectedIds() {
      return [...document.querySelectorAll("tbody input:checked")]
        .map((box) => credentials[Number(box.value)]?.credential_id)
        .filter(Boolean);
    }

    function write(value) {
      out.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
    }

    // Every dashboard fetch reports failures in Output: an unhandled rejection
    // would leave the operator with a stale table and no explanation.
    async function guard(action) {
      try {
        await action();
      } catch (error) {
        write(error);
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

    let visibleRows = 100;

    function render() {
      const selectedIndexes = new Set([...document.querySelectorAll("tbody input:checked")].map((box) => box.value));
      rowCount.textContent = credentials.length;

      if (!credentials.length) {
        rows.innerHTML = `<tr class="empty-row"><td colspan="5">No credentials yet. Create a random batch to start.</td></tr>`;
        return;
      }

      const shown = credentials.slice(0, visibleRows);
      rows.innerHTML = shown.map((item, index) => {
        const safeCredentialId = escapeHtml(item.credential_id);
        const checked = selectedIndexes.has(String(index)) ? "checked" : "";
        const key = item.credential_id;
        const state = item.status.toLowerCase();
        const result = verification[key]
          ? `<span class="status-chip status-${escapeHtml(verification[key].result.toLowerCase())}">${escapeHtml(verification[key].result)} · ${escapeHtml(verification[key].status)}</span>`
          : `<span class="status-chip status-unchecked">Not verified</span>`;
        return `<tr class="${state}">
          <td class="cell-select"><input type="checkbox" value="${index}" ${checked} aria-label="Select ${safeCredentialId}"></td>
          <td class="cell-mono">${safeCredentialId}</td>
          <td class="cell-mono">${item.idx}</td>
          <td><span class="status-chip status-${state}">${escapeHtml(item.status)}</span></td>
          <td>${result}</td>
        </tr>`;
      }).join("") + (visibleRows < credentials.length
        ? `<tr class="show-more-row"><td colspan="5">
            <button id="show-more" class="btn btn-sm btn-outline" type="button">Show more (${visibleRows} of ${credentials.length})</button>
          </td></tr>`
        : "");
      const showMore = document.querySelector("#show-more");
      if (showMore) showMore.onclick = () => {
        visibleRows = Math.min(credentials.length, visibleRows + 200);
        render();
      };
    }

    function renderAllocations() {
      // The table is the working list's own inventory: a legacy context has no
      // allocated entries, a pool context shows exactly that pool's entries.
      const entries = activeListUri
        ? allocations.filter((item) => item.status_list_uri === activeListUri)
        : [];
      allocationCount.textContent = entries.length;
      allocationRows.innerHTML = entries.length
        ? entries.map((item) => {
            const status = escapeHtml(item.status);
            const revoked = item.status === "REVOKED";
            return `<tr class="${escapeHtml(item.status.toLowerCase())}">
              <td class="cell-mono">${escapeHtml(item.country)}</td>
              <td class="cell-mono">${escapeHtml(item.doctype)}</td>
              <td class="cell-mono">${item.idx}</td>
              <td class="cell-mono">${escapeHtml(item.expiry_date)}</td>
              <td><span class="status-chip status-${escapeHtml(item.status.toLowerCase())}">${status}</span></td>
              <td class="cell-mono">${escapeHtml(item.status_list_uri)}</td>
              <td>
                <div class="btn-row">
                  <button class="btn btn-sm btn-destructive" type="button" data-allocation-uri="${escapeHtml(item.status_list_uri)}" data-allocation-idx="${item.idx}" aria-label="Revoke ${escapeHtml(item.country)} ${escapeHtml(item.doctype)} entry ${item.idx}" ${revoked ? "disabled" : ""}>${revoked ? "Revoked" : "Revoke"}</button>
                </div>
              </td>
            </tr>`;
          }).join("")
        : `<tr class="empty-row"><td colspan="7">No entry of this list is allocated yet. Entries appear here as the status-list API hands them out.</td></tr>`;
      allocationRows.querySelectorAll("button[data-allocation-uri]").forEach((button) => {
        button.onclick = () => guard(async () => {
          const data = await jsonFetch("/dashboard/allocated-entries/revoke", {
            method: "POST",
            body: JSON.stringify({
              status_list_uri: button.dataset.allocationUri,
              idx: Number(button.dataset.allocationIdx),
            }),
          });
          write(data);
          await load();
          await refreshCard();
        });
      });
    }

    // The registry renders the list summaries: inventory only, the picker chooses.

    function renderRegistry(summaries) {
      registryCount.textContent = summaries.length;
      // Pure inventory: the picker above chooses the list to operate on.
      registryRows.innerHTML = summaries.length
        ? summaries.map((item) => `<tr>
            <td class="cell-mono">${escapeHtml(item.country)}</td>
            <td class="cell-mono">${escapeHtml(item.doctype)}</td>
            <td class="cell-mono">${escapeHtml(item.list_id)}</td>
            <td>${item.allocated}</td><td>${item.revoked}</td>
            <td class="cell-mono">${escapeHtml(item.expires || "—")}</td>
            <td><span class="status-chip status-${item.expired ? "revoked" : "valid"}">${item.expired ? "EXPIRED" : "ACTIVE"}</span></td>
          </tr>`).join("")
        : `<tr class="empty-row"><td colspan="7">No country × doctype list allocated yet.</td></tr>`;
    }

    async function load() {
      const [data, summaries] = await Promise.all([
        jsonFetch("/credentials"),
        jsonFetch("/debug/status-lists"),
      ]);
      credentials = data.credentials;
      allocations = data.allocated_entries;
      registry = summaries;
      verification = Object.fromEntries(
        credentials
          .filter((item) => item.verification_result)
          .map((item) => [item.credential_id, { result: item.verification_result, status: item.status }])
      );
      renderRegistry(registry);
      renderListOptions(registry);
      if (
        contextChosen &&
        activeListUri &&
        !registry.some((item) => item.status_list_uri === activeListUri)
      ) {
        clearList();           // the pool is gone: state was reset or the server reloaded
        return;
      }
      listSelect.value = contextChosen ? activeListUri || "legacy" : "none";
      renderPanels();
      renderContext();
      render();
    }

    // The credentials panel owns the credential batch: /status/1 credentials,
    // each one paired with an entry in the country × doctype pool of the form.
    document.querySelector("#create").onclick = () => guard(async () => {
      const data = await jsonFetch("/credentials/random-batch", {
        method: "POST",
        body: JSON.stringify({
          count: Number(document.querySelector("#count").value || 10),
          prefix: document.querySelector("#prefix").value || "cred",
          country: document.querySelector("#country").value || "EU",
          doctype: document.querySelector("#doctype").value || "org.iso.18013.5.1.mDL",
          expiry_date: document.querySelector("#expiry-date").value || "2099-12-31",
        }),
      });
      write(data);
      await load();
      await refreshCard();
    });

    // The allocated-entry panel owns its pool's top-up: entries only.
    document.querySelector("#add-entries").onclick = () => guard(async () => {
      const pool = workingPool();
      if (!pool) return write("Operate on an allocated pool first.");
      const data = await jsonFetch("/dashboard/status-lists", {
        method: "POST",
        body: JSON.stringify({
          country: pool.country,
          doctype: pool.doctype,
          expiry_date: document.querySelector("#entries-expiry").value || pool.expires,
          count: Number(document.querySelector("#entries-count").value || 10),
        }),
      });
      write(data);
      await load();
      await refreshCard();
    });

    const newListForm = document.querySelector("#new-list-form");
    const newListToggle = document.querySelector("#new-list-toggle");
    function showNewListForm(visible) {
      newListForm.hidden = !visible;
      newListToggle.setAttribute("aria-expanded", String(visible));
      if (visible) document.querySelector("#new-country").focus();
    }

    newListToggle.onclick = () => showNewListForm(newListForm.hidden);
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
      write(data);
      showNewListForm(false);
      await load();
      await selectList(data.status_list_uri);
    });

    document.querySelector("#revoke").onclick = () => guard(async () => {
      const ids = selectedIds();
      if (!ids.length) return write("Select credentials first.");
      const data = await jsonFetch("/credentials/revoke-batch", {
        method: "POST",
        body: JSON.stringify({ credential_ids: ids }),
      });
      write(data);
      await load();
      await refreshCard();
    });

    document.querySelector("#verify").onclick = () => guard(async () => {
      const ids = selectedIds();
      if (!ids.length) return write("Select credentials first.");
      const data = await jsonFetch("/verify-batch", {
        method: "POST",
        body: JSON.stringify({ credential_ids: ids }),
      });
      for (const item of data.verified || []) {
        verification[item.credential_id] = { result: item.result, status: item.status };
      }
      write(data);
      render();
      await refreshCard();
    });

    document.querySelector("#refresh").onclick = () => guard(load);
    document.querySelector("#registry-refresh").onclick = () => guard(load);
    document.querySelector("#all").onclick = () => {
      visibleRows = credentials.length;
      render();
      document.querySelectorAll("tbody input").forEach((box) => { box.checked = true; });
    };
    document.querySelector("#none").onclick = () => {
      document.querySelectorAll("tbody input").forEach((box) => { box.checked = false; });
    };
    const tokenCard = document.querySelector("#token-card");
    const registryCard = document.querySelector("#registry-card");
    const legacyCard = document.querySelector("#legacy-card");
    const allocationCard = document.querySelector("#allocation-card");
    const jwtBox = document.querySelector("#jwt");
    const copyButton = document.querySelector("#copy-token");
    const listSelect = document.querySelector("#lst-select");
    let currentToken = "";

    // The working list the whole console is scoped to. Nothing is selected
    // until the operator picks one; null then means the legacy /status/1 list.
    let activeListUri = null;
    let contextChosen = false;

    // Option labels carry the revoked count: the operator sees at a glance
    // which of the registered lists the revocation landed in.
    function renderListOptions(summaries) {
      listSelect.innerHTML = [
        '<option value="none">Pick a status list…</option>',
        '<option value="legacy">Legacy /status/1 · credential list</option>',
        ...summaries.map((item) => `<option value="${escapeHtml(item.status_list_uri)}">` +
          `${escapeHtml(item.country)} · ${escapeHtml(item.doctype)} · ` +
          `${escapeHtml(item.list_id.slice(0, 8))} · ${item.revoked} revoked</option>`),
      ].join("");
    }

    function statusListUrl(uri, offset, limit) {
      const params = new URLSearchParams({
        assignment_offset: String(offset),
        assignment_limit: String(limit),
      });
      if (uri) params.set("uri", uri);
      return `/debug/status-list?${params}`;
    }

    // Decoding never changes the working list: the card always shows it.
    async function showCard(uri, offset = 0, limit = 100) {
      const data = await jsonFetch(statusListUrl(uri, offset, limit));
      renderDecodedToken(data);
      return data;
    }

    async function refreshCard() {
      if (!contextChosen || tokenCard.hidden) return;
      await showCard(activeListUri);
    }

    function contextLabel() {
      return activeListUri || "the legacy /status/1 list";
    }

    // The registry stays on screen: it is both the inventory and the chooser.
    // The other panels follow the chosen list, one kind at a time.
    function renderPanels() {
      const pool = Boolean(activeListUri);
      legacyCard.hidden = !contextChosen || pool;
      allocationCard.hidden = !contextChosen || !pool;
    }

    function workingPool() {
      return registry.find((item) => item.status_list_uri === activeListUri) || null;
    }

    function renderContext() {
      const pool = registry.find((item) => item.status_list_uri === activeListUri);
      document.querySelector("#ctx-scope").textContent = !contextChosen
        ? "No list selected yet: choose one above to operate on it."
        : activeListUri
          ? `Working on ${activeListUri} — ${pool.allocated} allocated, ${pool.revoked} revoked, ${pool.expired ? "expired" : "active"}.`
          : "Working on the legacy /status/1 credential list.";
      renderAllocations();
    }

    // The single context switch: pick a list, then read its signed token.
    async function selectList(uri) {
      contextChosen = true;
      activeListUri = uri;
      listSelect.value = uri || "legacy";
      renderPanels();
      renderContext();
      await showCard(uri);
    }

    function clearList() {
      contextChosen = false;
      activeListUri = null;
      listSelect.value = "none";
      tokenCard.hidden = true;
      renderPanels();
      renderContext();
    }

    listSelect.onchange = () => guard(async () => {
      const value = listSelect.value;
      if (!value || value === "none") return clearList();
      await selectList(value === "legacy" ? null : value);
    });

    function renderJwt(token) {
      const [header, payload, signature] = token.split(".");
      jwtBox.innerHTML =
        `<span class="jwt-header">${escapeHtml(header)}</span>` +
        `<span class="jwt-dot">.</span>` +
        `<span class="jwt-payload">${escapeHtml(payload)}</span>` +
        `<span class="jwt-dot">.</span>` +
        `<span class="jwt-signature">${escapeHtml(signature)}</span>`;
    }

    function renderAssignments(data) {
      const rows = document.querySelector("#lst-rows");
      rows.innerHTML = data.assignments.length
        ? data.assignments.map((item) => `<tr>
            <td class="cell-mono">${escapeHtml(item.credential_id)}</td>
            <td class="cell-mono">${item.idx}</td>
            <td><span class="status-chip status-${escapeHtml(item.status.toLowerCase())}">${escapeHtml(item.status)}</span></td>
          </tr>`).join("")
        : `<tr class="empty-row"><td colspan="3">${activeListUri ? "This list is allocated through the status-list API; its entries carry no credential identifier." : "No credential is assigned to an index yet."}</td></tr>`;
      const pagination = document.querySelector("#assignment-pagination");
      pagination.innerHTML = "";
      if (data.assignment_total <= data.assignment_limit) return;
      const start = data.assignment_offset + 1;
      const end = Math.min(data.assignment_total, data.assignment_offset + data.assignment_limit);
      const label = document.createElement("span");
      label.className = "text-sm text-muted";
      label.textContent = `Showing ${start}–${end} of ${data.assignment_total}`;
      pagination.append(label);
      const previous = document.createElement("button");
      previous.className = "btn btn-sm btn-outline";
      previous.type = "button";
      previous.textContent = "Previous";
      previous.disabled = data.assignment_offset === 0;
      previous.onclick = () => guard(() => showCard(
        activeListUri,
        Math.max(0, data.assignment_offset - data.assignment_limit),
        data.assignment_limit,
      ));
      const next = document.createElement("button");
      next.className = "btn btn-sm btn-outline";
      next.type = "button";
      next.textContent = "Next";
      next.disabled = end >= data.assignment_total;
      next.onclick = () => guard(() => showCard(
        activeListUri,
        data.assignment_offset + data.assignment_limit,
        data.assignment_limit,
      ));
      pagination.append(previous, next);

    }
    function renderDecodedToken(data) {
      currentToken = data.token;
      renderJwt(data.token);
      document.querySelector("#lst-scope").textContent =
        `Working list: ${data.list_uri}`;
      document.querySelector("#jwks-label").textContent = activeListUri
        ? "JWKS · list signer certificate"
        : "JWKS · /.well-known/jwks.json";
      document.querySelector("#jwt-header").textContent = JSON.stringify(data.header, null, 2);
      document.querySelector("#jwt-payload").textContent = JSON.stringify(data.payload, null, 2);
      document.querySelector("#jwks").textContent = JSON.stringify(data.jwks, null, 2);
      document.querySelector("#lst-bits").textContent = data.bits;
      document.querySelector("#lst-size").textContent = data.size;
      document.querySelector("#lst-valid").textContent = data.valid;
      document.querySelector("#lst-revoked").textContent = data.revoked;
      renderBitmap("lst", data.lst, data.revoked_indices);
      document.querySelector("#lst-note").textContent =
        `"lst" is ${data.lst.compressed_bytes} compressed bytes; it inflates to ` +
        `${data.lst.inflated_bytes} bytes holding ${data.lst.entries} entries at ` +
        `${data.bits} bit per entry. The inflated entries are shown below.`;

      const shown = data.revoked_indices.slice(0, 200);
      const rest = data.revoked_indices.length - shown.length;
      document.querySelector("#lst-indices").textContent = shown.length
        ? shown.join(", ") + (rest > 0 ? `, and ${rest} more` : "")
        : "None";

      renderAssignments(data);

      tokenCard.hidden = false;
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
    document.querySelector("#token").onclick = () => guard(async () => {
      await showCard(activeListUri);
      write(
        `Status list token fetched for ${contextLabel()}. ` +
        "The decoded token, status list and signing key are shown below the output.",
      );
      tokenCard.scrollIntoView({ behavior: "smooth", block: "start" });
    });

    document.querySelector("#reset").onclick = () => guard(async () => {
      const data = await jsonFetch("/reset", { method: "POST" });
      verification = {};
      write(data);
      await load();          // every pool is gone: the context falls back
      await refreshCard();
    });

    load().catch(write);
  </script>"""


def console_html() -> str:
    """The credential console."""
    return page(
        title="Token status list console · Credimi",
        active="Console",
        body=_CONSOLE_BODY,
        scripts=_SHARED_SCRIPT + "\n" + _CONSOLE_SCRIPT,
    )


_EXPLORER_BODY = """  <header class="hero">
    <div class="hero-inner">
      <p class="eyebrow">EUDI conformance utility</p>
      <h1>Status list explorer</h1>
      <p>Paste a Token Status List from any issuer and inspect it: the decoded header and
        payload, the inflated <span class="mono">lst</span>, every revoked index, and the status
        of a single index. Accepts a JWT, a CWT as hex or base64, the JSON payload, or the
        bare <span class="mono">lst</span> value. Signatures are not verified.</p>
    </div>
  </header>
  <main class="page-content">
    <div class="container">
    <div class="stack">
      <section class="card">
        <div class="section-header"><h2>Payload</h2></div>
        <label class="field-label" for="explore-payload">Status list JWT, CWT, JSON payload or lst</label>
        <textarea id="explore-payload" class="payload-input" spellcheck="false"
          placeholder="eyJhbGciOiJFUzI1NiIs… · d28450a3… · {&quot;bits&quot;:1,&quot;lst&quot;:&quot;eNrb…&quot;} · eNrb…"></textarea>
        <div class="explorer-fields">
          <div>
            <label class="field-label" for="explore-bits">Bits per entry, for a bare lst</label>
            <select id="explore-bits" class="explorer-select">
              <option value="1" selected>1</option>
              <option value="2">2</option>
              <option value="4">4</option>
              <option value="8">8</option>
            </select>
          </div>
          <div>
            <label class="field-label" for="explore-file">Or load a file</label>
            <input id="explore-file" type="file" class="explorer-file">
          </div>
        </div>
        <div class="btn-row mt-4">
          <button id="explore" class="btn btn-md btn-primary">Inspect payload</button>
          <button id="explore-current" class="btn btn-md btn-outline">Load this server's status list</button>
        </div>
        <pre class="output mt-4" id="explore-out">Paste a payload, then inspect it.</pre>
      </section>

      <section class="card" id="explore-card" hidden>
        <div class="section-header"><h2>Decoded status list</h2></div>
        <div class="metric-grid">
          <div class="card">
            <strong class="metric-value" id="explore-format">—</strong>
            <span class="eyebrow">Format</span>
          </div>
          <div class="card">
            <strong class="metric-value" id="explore-bits-value">0</strong>
            <span class="eyebrow">Bits per entry</span>
          </div>
          <div class="card">
            <strong class="metric-value" id="explore-size">0</strong>
            <span class="eyebrow">Entries</span>
          </div>
          <div class="card">
            <strong class="metric-value" id="explore-revoked">0</strong>
            <span class="eyebrow">Revoked</span>
          </div>
        </div>
        <p class="lst-note" id="explore-note"></p>

        <h3 class="subhead">Check an index</h3>
        <div class="index-lookup">
          <input id="explore-index" type="number" min="0" value="0" aria-label="Index">
          <button id="explore-lookup" class="btn btn-sm btn-secondary">Check index</button>
          <span id="explore-index-status"></span>
        </div>

        <h3 class="subhead">Non-valid indices</h3>
        <div id="explore-indices" class="index-groups"></div>
        <div class="btn-row mt-4">
          <button id="explore-copy-indices" class="btn btn-sm btn-outline">Copy the indices</button>
        </div>

        <h3 class="subhead">Inflated lst spectrum</h3>
        <div class="bitmap-shell">
          <div class="bitmap-scroll" id="explore-bitmap-scroll" tabindex="0" aria-label="Full inflated status list">
            <div class="bitmap" id="explore-bitmap"></div>
          </div>
          <div class="bitmap-minimap-scroll" id="explore-minimap-scroll" tabindex="0" aria-label="Non-valid entry minimap">
            <div class="bitmap-minimap" id="explore-minimap"></div>
          </div>
        </div>
        <p class="bitmap-caption" id="explore-caption"></p>

        <h3 class="subhead">Decoded token</h3>
        <div class="decoded-grid">
          <div>
            <p class="eyebrow">Header</p>
            <pre id="explore-header"></pre>
          </div>
          <div>
            <p class="eyebrow">Payload</p>
            <pre id="explore-payload-json"></pre>
          </div>
        </div>
      </section>
    </div>
    </div>
  </main>"""


_EXPLORER_SCRIPT = """<script>
    const STATUS_NAMES = { 0: "VALID", 1: "REVOKED", 2: "SUSPENDED" };
    const payloadInput = document.querySelector("#explore-payload");
    const explorerOut = document.querySelector("#explore-out");
    const exploreCard = document.querySelector("#explore-card");
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
            return `<p class="eyebrow">${escapeHtml(name)} · ${indices.length}</p>` +
              `<p class="index-list">${shown.join(", ")}${rest > 0 ? `, and ${rest} more` : ""}</p>`;
          }).join("")
        : `<p class="index-list">None. Every entry is VALID.</p>`;
    }

    function lookupIndex() {
      if (!explored) return;
      const target = document.querySelector("#explore-index-status");
      const index = Number(document.querySelector("#explore-index").value);
      if (!Number.isInteger(index) || index < 0 || index >= explored.size) {
        target.innerHTML = `<span class="status-chip status-reject">Out of range: 0 to ${explored.size - 1}</span>`;
        return;
      }
      const name = statusName(statusAt(explored.lst, index));
      target.innerHTML = `<span class="status-chip status-${escapeHtml(name.toLowerCase())}">${escapeHtml(name)}</span>`;
    }

    function renderExplored(data) {
      explored = data;
      document.querySelector("#explore-format").textContent = data.format.toUpperCase();
      document.querySelector("#explore-bits-value").textContent = data.bits;
      document.querySelector("#explore-size").textContent = data.size;
      document.querySelector("#explore-revoked").textContent = data.counts.REVOKED || 0;
      const counts = Object.entries(data.counts).map(([name, count]) => `${count} ${name}`).join(", ");
      document.querySelector("#explore-note").textContent =
        `"lst" is ${data.lst.compressed_bytes} compressed bytes; it inflates to ` +
        `${data.lst.inflated_bytes} bytes holding ${data.size} entries at ${data.bits} ` +
        `bit${data.bits === 1 ? "" : "s"} per entry: ${counts}.`;
      document.querySelector("#explore-header").textContent = JSON.stringify(data.header, null, 2);
      document.querySelector("#explore-payload-json").textContent = JSON.stringify(data.payload, null, 2);
      renderIndices(data);
      renderBitmap("explore", data.lst, data.non_valid_indices);
      exploreCard.hidden = false;
      lookupIndex();
    }

    async function inspect() {
      const payload = payloadInput.value.trim();
      if (!payload) return void (explorerOut.textContent = "Paste a payload first.");
      let response;
      try {
        response = await fetch("/debug/status-list/explore", {
          method: "POST",
          cache: "no-store",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ payload, bits: Number(document.querySelector("#explore-bits").value) }),
        });
      } catch (error) {
        explorerOut.textContent = String(error);
        return;
      }
      const body = await response.json();
      if (!response.ok) {
        exploreCard.hidden = true;
        explored = null;
        explorerOut.textContent = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail, null, 2);
        return;
      }
      renderExplored(body);
      explorerOut.textContent = `Decoded a ${body.format.toUpperCase()} status list: ${body.size} entries, ${body.non_valid_indices.length} not VALID.`;
    }

    // Binary CWT files become base64; text files (JWT, JSON, hex) load as-is.
    document.querySelector("#explore-file").onchange = async (event) => {
      const file = event.target.files[0];
      if (!file) return;
      const bytes = new Uint8Array(await file.arrayBuffer());
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
    };

    document.querySelector("#explore-current").onclick = async () => {
      let response;
      try {
        response = await fetch("/status/1", { cache: "no-store", headers: { accept: "application/statuslist+jwt" } });
      } catch (error) {
        explorerOut.textContent = String(error);
        return;
      }
      payloadInput.value = await response.text();
      await inspect();
    };

    document.querySelector("#explore").onclick = inspect;
    document.querySelector("#explore-lookup").onclick = lookupIndex;
    document.querySelector("#explore-index").onkeydown = (event) => {
      if (event.key === "Enter") lookupIndex();
    };
    document.querySelector("#explore-copy-indices").onclick = async (event) => {
      if (!explored) return;
      await navigator.clipboard.writeText(explored.non_valid_indices.join(","));
      event.target.textContent = "Copied";
      setTimeout(() => { event.target.textContent = "Copy the indices"; }, 2000);
    };
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
    body = """  <header class="hero">
    <div class="hero-inner">
      <p class="eyebrow">EUDI conformance utility</p>
      <h1>API documentation</h1>
      <p>Every endpoint of the mock Token Status List server, generated from the
        OpenAPI document at <span class="mono">/openapi.json</span>.</p>
    </div>
  </header>
  <main class="page-content">
    <div class="container">
      <div class="docs-frame"><div id="swagger-ui"></div></div>
    </div>
  </main>"""
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
