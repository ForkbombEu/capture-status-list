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
    /* Console layout: the page runs full width as a two-column dashboard —
       forms and info on the left, results on the right, so every CTA
       produces feedback the user can see without scrolling away. */
    .console-container { max-width: none; }
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
    links = (("Console", "/"), ("API docs", "/docs"), ("Status list API", "/token_status_list/take"))
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
            <a href="/.well-known/jwks.json">JWKS</a>
            <a href="/docs">API docs</a>
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
  <main class="container console-container page-content">
    <div class="console-grid">
      <div class="stack console-left">
      <section class="card batch-card">
        <div class="section-header"><h2>Add batch</h2></div>
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
        <div class="btn-row mt-4">
          <button id="create" class="btn btn-md btn-primary">Create random batch</button>
        </div>
      </section>

      <section class="card">
        <div class="section-header">
          <h2>Country × doctype lists <span id="registry-count" class="count-chip">0</span></h2>
          <button id="registry-refresh" class="btn btn-sm btn-outline">Refresh lists</button>
        </div>
        <p class="text-sm text-muted">Paired Token Status List and ISO 18013-5 identifier-list resources. Token endpoints negotiate JWT or CWT with <span class="mono">Accept</span>.</p>
        <div class="test-table-wrap">
          <table class="test-table">
            <thead><tr><th>Country</th><th>Doctype</th><th>List UUID</th><th>Allocated</th><th>Revoked</th><th>Expiry</th><th>State</th><th>Token formats</th></tr></thead>
            <tbody id="registry-rows"></tbody>
          </table>
        </div>
      </section>

      <section class="card">
        <div class="section-header">
          <h2>Credentials <span id="row-count" class="count-chip">0</span></h2>
          <div class="btn-row">
            <button id="refresh" class="btn btn-sm btn-outline">Refresh</button>
            <button id="reset" class="btn btn-sm btn-outline">Reset state</button>
            <button id="token" class="btn btn-sm btn-outline">Fetch status list token</button>
          </div>
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

        <div class="section-header mt-4">
          <h3>Known allocated status-list entries <span id="allocation-count" class="count-chip">0</span></h3>
        </div>
        <p class="text-sm text-muted">These entries are allocated by the status-list service. They identify a country, doctype, list and index, but do not include a credential identifier.</p>
        <div class="credential-scroll">
          <div class="test-table-wrap">
            <table class="test-table">
              <thead><tr><th>Country</th><th>Doctype</th><th>Index</th><th>Expiry</th><th>Status</th><th>Status list URI</th></tr></thead>
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
        <p class="eyebrow">JWKS · /.well-known/jwks.json</p>
        <pre id="jwks"></pre>
      </section>

      </aside>
    </div>
  </main>"""


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

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }

    function selectedIds() {
      return [...document.querySelectorAll("tbody input:checked")]
        .map((box) => credentials[Number(box.value)]?.credential_id)
        .filter(Boolean);
    }

    function write(value) {
      out.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
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

    function renderAllocations(entries) {
      allocationCount.textContent = entries.length;
      allocationRows.innerHTML = entries.length
        ? entries.map((item) => `<tr class="${escapeHtml(item.status.toLowerCase())}">
            <td class="cell-mono">${escapeHtml(item.country)}</td>
            <td class="cell-mono">${escapeHtml(item.doctype)}</td>
            <td class="cell-mono">${item.idx}</td>
            <td class="cell-mono">${escapeHtml(item.expiry_date)}</td>
            <td><span class="status-chip status-${escapeHtml(item.status.toLowerCase())}">${escapeHtml(item.status)}</span></td>
            <td class="cell-mono">${escapeHtml(item.status_list_uri)}</td>
          </tr>`).join("")
        : `<tr class="empty-row"><td colspan="6">No status-list entries allocated yet.</td></tr>`;
    }

    let formatPreview = null;

    function renderRegistry(lists) {
      registryCount.textContent = lists.length;
      const sameOrigin = (uri) => uri.replace(/^https?:\\/\\/[^/]+/, window.location.origin);
      registryRows.innerHTML = lists.length
        ? lists.map((item) => {
            const tokenUri = sameOrigin(item.status_list_uri);
            const identifierUri = sameOrigin(item.identifier_list_uri);
            return `<tr>
            <td class="cell-mono">${escapeHtml(item.country)}</td>
            <td class="cell-mono">${escapeHtml(item.doctype)}</td>
            <td class="cell-mono">${escapeHtml(item.list_id)}</td>
            <td>${item.allocated}</td><td>${item.revoked}</td>
            <td class="cell-mono">${escapeHtml(item.expires || "—")}</td>
            <td><span class="status-chip status-${item.expired ? "revoked" : "valid"}">${item.expired ? "EXPIRED" : "ACTIVE"}</span></td>
            <td>
              <div class="btn-row">
                <button class="btn btn-sm btn-outline" type="button" data-preview="${escapeHtml(tokenUri)}" data-media="application/statuslist+jwt">TSL · JWT</button>
                <button class="btn btn-sm btn-outline" type="button" data-preview="${escapeHtml(tokenUri)}" data-media="application/statuslist+cwt">TSL · CWT</button>
                <button class="btn btn-sm btn-outline" type="button" data-preview="${escapeHtml(identifierUri)}" data-media="application/identifierlist+jwt">ARL · JWT</button>
                <button class="btn btn-sm btn-outline" type="button" data-preview="${escapeHtml(identifierUri)}" data-media="application/identifierlist+cwt">ARL · CWT</button>
              </div>
            </td>
          </tr>`;
          }).join("")
        : `<tr class="empty-row"><td colspan="8">No country × doctype lists allocated yet.</td></tr>`;
      registryRows.querySelectorAll("button[data-preview]").forEach((button) => {
        button.onclick = async () => {
          const response = await fetch(button.dataset.preview, {
            cache: "no-store",
            headers: { Accept: button.dataset.media },
          });
          if (!response.ok) {
            write(`Token fetch failed: ${response.status}`);
            return;
          }
          const type = response.headers.get("content-type") || "";
          const body = type.includes("cwt")
            ? [...new Uint8Array(await response.arrayBuffer())]
            : await response.text();
          formatPreview = { uri: button.dataset.preview, media: button.dataset.media, body };
          write(formatPreview);
          // Keep the selected format in Output, while showing the same decoded
          // status-list dissertation as the credentials token action.
          renderDecodedToken(await jsonFetch("/debug/status-list"));
          tokenCard.scrollIntoView({ behavior: "smooth", block: "start" });
        };
      });
    }

    async function load() {
      const [data, lists] = await Promise.all([
        jsonFetch("/credentials"),
        jsonFetch("/debug/status-lists"),
      ]);
      credentials = data.credentials;
      renderAllocations(data.allocated_entries);
      verification = Object.fromEntries(
        credentials
          .filter((item) => item.verification_result)
          .map((item) => [item.credential_id, { result: item.verification_result, status: item.status }])
      );
      renderRegistry(lists);
      render();
    }

    document.querySelector("#create").onclick = async () => {
      const body = {
        count: Number(document.querySelector("#count").value || 10),
        prefix: document.querySelector("#prefix").value || "cred",
        country: document.querySelector("#country").value || "EU",
        doctype: document.querySelector("#doctype").value || "org.iso.18013.5.1.mDL",
        expiry_date: document.querySelector("#expiry-date").value || "2099-12-31",
      };
      const data = await jsonFetch("/credentials/random-batch", {
        method: "POST",
        body: JSON.stringify(body),
      });
      write(data);
      await load();
      await refreshToken(true);
    };

    document.querySelector("#revoke").onclick = async () => {
      const ids = selectedIds();
      if (!ids.length) return write("Select credentials first.");
      const data = await jsonFetch("/credentials/revoke-batch", {
        method: "POST",
        body: JSON.stringify({ credential_ids: ids }),
      });
      write(data);
      await load();
      await refreshToken(true);
    };

    document.querySelector("#verify").onclick = async () => {
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
      await refreshToken(true);
    };

    document.querySelector("#refresh").onclick = load;
    document.querySelector("#registry-refresh").onclick = load;
    document.querySelector("#all").onclick = () => {
      visibleRows = credentials.length;
      render();
      document.querySelectorAll("tbody input").forEach((box) => { box.checked = true; });
    };
    document.querySelector("#none").onclick = () => {
      document.querySelectorAll("tbody input").forEach((box) => { box.checked = false; });
    };
    const tokenCard = document.querySelector("#token-card");
    const jwtBox = document.querySelector("#jwt");
    const copyButton = document.querySelector("#copy-token");
    let currentToken = "";

    function renderJwt(token) {
      const [header, payload, signature] = token.split(".");
      jwtBox.innerHTML =
        `<span class="jwt-header">${escapeHtml(header)}</span>` +
        `<span class="jwt-dot">.</span>` +
        `<span class="jwt-payload">${escapeHtml(payload)}</span>` +
        `<span class="jwt-dot">.</span>` +
        `<span class="jwt-signature">${escapeHtml(signature)}</span>`;
    }

    const ROW_ENTRIES = 64;

    // One character per entry (two when bits is 8), 64 entries to a row, with
    // every non-zero — that is, revoked — entry marked.
    function renderBitmap(lst, revokedIndices) {
      const bitmapScroll = document.querySelector("#lst-bitmap-scroll");
      const bitmap = document.querySelector("#lst-bitmap");
      const minimap = document.querySelector("#lst-minimap");
      const full = lst.full || lst.window;
      const width = ROW_ENTRIES * lst.chars_per_entry;
      let html = "";
      let minimapHtml = "";

      for (let offset = 0, rowNumber = 0; offset < full.length; offset += width, rowNumber += 1) {
        const row = full.slice(offset, offset + width);
        const index = offset / lst.chars_per_entry;
        const rowRevoked = revokedIndices.filter((entry) => entry >= index && entry < index + row.length / lst.chars_per_entry);
        const marked = [...row]
          .map((char, position) => {
            const spacer = position > 0 && position % (8 * lst.chars_per_entry) === 0 ? " " : "";
            return spacer + (char === "0" ? char : `<b>${escapeHtml(char)}</b>`);
          })
          .join("");
        html += `<span class="bitmap-index" data-row="${rowNumber}">${index}</span><span class="bitmap-row" data-row="${rowNumber}">${marked}</span>`;
        const marker = rowRevoked.length
          ? `<button class="bitmap-minimap-marker" type="button" data-row="${rowNumber}" aria-label="Jump to revoked entries ${escapeHtml(rowRevoked.join(", "))}" title="Revoked: ${escapeHtml(rowRevoked.join(", "))}"></button>`
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
      document.querySelector("#lst-caption").textContent =
        `Entries 0 to ${last} of ${lst.entries}. Red bars mark revoked rows; click a bar to jump there.`;
    }

    function renderAssignments(data) {
      const rows = document.querySelector("#lst-rows");
      rows.innerHTML = data.assignments.length
        ? data.assignments.map((item) => `<tr>
            <td class="cell-mono">${escapeHtml(item.credential_id)}</td>
            <td class="cell-mono">${item.idx}</td>
            <td><span class="status-chip status-${escapeHtml(item.status.toLowerCase())}">${escapeHtml(item.status)}</span></td>
          </tr>`).join("")
        : `<tr class="empty-row"><td colspan="3">No credential is assigned to an index yet.</td></tr>`;
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
      previous.onclick = async () => renderDecodedToken(await jsonFetch(
        `/debug/status-list?assignment_offset=${Math.max(0, data.assignment_offset - data.assignment_limit)}&assignment_limit=${data.assignment_limit}`
      ));
      const next = document.createElement("button");
      next.className = "btn btn-sm btn-outline";
      next.type = "button";
      next.textContent = "Next";
      next.disabled = end >= data.assignment_total;
      next.onclick = async () => renderDecodedToken(await jsonFetch(
        `/debug/status-list?assignment_offset=${data.assignment_offset + data.assignment_limit}&assignment_limit=${data.assignment_limit}`
      ));
      pagination.append(previous, next);

    }
    function renderDecodedToken(data) {
      currentToken = data.token;
      renderJwt(data.token);
      document.querySelector("#jwt-header").textContent = JSON.stringify(data.header, null, 2);
      document.querySelector("#jwt-payload").textContent = JSON.stringify(data.payload, null, 2);
      document.querySelector("#jwks").textContent = JSON.stringify(data.jwks, null, 2);
      document.querySelector("#lst-bits").textContent = data.bits;
      document.querySelector("#lst-size").textContent = data.size;
      document.querySelector("#lst-valid").textContent = data.valid;
      document.querySelector("#lst-revoked").textContent = data.revoked;
      renderBitmap(data.lst, data.revoked_indices);
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
    // Mutations change the list payload; always fetch a fresh decoded view.
    async function refreshToken(force = false) {
      if (tokenCard.hidden && !force) return;
      renderDecodedToken(await jsonFetch("/debug/status-list"));
    }

    document.querySelector("#token").onclick = async () => {
      const data = await jsonFetch("/debug/status-list");
      renderDecodedToken(data);
      write("Status list token fetched. The decoded token, status list and signing key are shown below the output.");
      tokenCard.scrollIntoView({ behavior: "smooth", block: "start" });
    };

    document.querySelector("#reset").onclick = async () => {
      const data = await jsonFetch("/reset", { method: "POST" });
      verification = {};
      write(data);
      await load();
      await refreshToken(true);
    };

    load().catch(write);
  </script>"""


def console_html() -> str:
    """The credential console."""
    return page(
        title="Token status list console · Credimi",
        active="Console",
        body=_CONSOLE_BODY,
        scripts=_CONSOLE_SCRIPT,
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
  <main class="container page-content">
    <div class="docs-frame"><div id="swagger-ui"></div></div>
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
