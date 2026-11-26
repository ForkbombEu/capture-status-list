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

    /* Tables are the brand's Scoreboard pattern (`.test-table`, DESIGN.md §11
       Tables); the console only adds the registry's two-line first cell. */
    .list-name {
      display: block;
      color: var(--brand-primary);
      font-size: var(--fs-base);
      font-weight: 600;
    }
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
    .entries-scroll { max-height: 420px; overflow: auto; border-radius: var(--radius); }
    .entries-scroll .test-table-wrap { overflow: visible; }
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
    /* Action feedback: one alert (DESIGN.md §11) floating like a toast in the
       bottom-right corner until dismissed; successful actions show their result
       in the panels. Solid white rather than 60%, since it floats over content. */
    .notice {
      position: fixed;
      right: var(--space-6);
      bottom: var(--space-6);
      z-index: 200;
      display: grid;
      grid-template-columns: 18px minmax(0, 1fr) auto;
      gap: var(--space-3);
      align-items: start;
      width: min(440px, calc(100vw - 2 * var(--space-4)));
      padding: 17px;
      border: 1px solid currentColor;
      border-radius: var(--radius-md);
      background: var(--bg);
      box-shadow: var(--shadow-lg);
      animation: notice-in 220ms ease-out;
    }
    .notice[hidden] { display: none; }
    .notice-destructive { color: var(--destructive); }
    .notice-info { color: var(--brand-primary); }
    .notice-icon {
      width: 18px;
      height: 18px;
      margin-top: 1px;
      fill: none;
      stroke: currentColor;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
    .notice-destructive .notice-icon-info,
    .notice-info .notice-icon-destructive { display: none; }
    .notice-title { font: 500 var(--fs-md)/1.25 var(--font-sans); }
    .notice-body {
      margin-top: var(--space-1);
      font-size: var(--fs-base);
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      max-height: 40vh;
      overflow: auto;
    }
    .notice .btn-ghost { color: var(--fg); }
    @keyframes notice-in { from { opacity: 0; transform: translateY(8px); } }
    @media (prefers-reduced-motion: reduce) { .notice { animation: none; } }
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
    /* The working list's URI, under the card title: an outline button whose
       arrow-up-right says it opens the served token in a new tab. Long URIs
       wrap instead of stretching the card. */
    .list-uri {
      height: auto;
      min-height: 28px;
      max-width: 100%;
      margin-top: var(--space-3);
      padding-block: var(--space-1);
      overflow-wrap: anywhere;
      text-align: left;
    }
    /* Icons in buttons (the URI arrow, refresh, new) follow the label colour. */
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

    /* A group heading inside a panel or section (the brand .subsection-heading),
       set off by a hairline. No trailing colon (DESIGN.md §15). */
    .subhead {
      margin: var(--space-6) 0 var(--space-3);
      padding-bottom: var(--space-2);
      border-bottom: 1px solid var(--border);
    }
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
    /* The registry is the chooser: clicking a row makes it the working list.
       Rows top-align like the scoreboard; the chosen row takes the soft
       lavender and an indigo edge, apart from both the hover and the header. */
    .registry-row { cursor: pointer; }
    .registry-row td { vertical-align: top; }
    .registry-row td.cell-mono { line-height: 20px; }
    .registry-row:hover td { background: var(--bg-muted); }
    .registry-row[aria-current="true"] td { background: var(--brand-secondary); }
    .registry-row[aria-current="true"] td:first-child {
      box-shadow: inset 3px 0 0 var(--brand-primary);
    }
    .registry-row:focus-visible { outline: 2px solid var(--ring); outline-offset: -2px; }
    /* The JWKS wraps so the key's long x5c certificate stays readable. */
    #jwks { white-space: pre-wrap; overflow-wrap: anywhere; }
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
          <table class="test-table">
            <thead><tr><th>List</th><th>List UUID</th><th>Expiry</th></tr></thead>
            <tbody id="registry-rows"></tbody>
          </table>
        </div>
        <div class="btn-row mt-4">
          <button id="registry-refresh" class="btn btn-lg btn-outline"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>Refresh lists</button>
          <button id="new-list-toggle" class="btn btn-lg btn-primary" aria-expanded="false" aria-controls="new-list-form"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="M12 5v14"/></svg>New status list</button>
        </div>
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
            <button id="new-list" class="btn btn-lg btn-primary">Create status list</button>
            <button id="new-list-cancel" class="btn btn-lg btn-outline">Cancel</button>
          </div>
        </div>
      </div>

      <section class="card" id="working-card" aria-labelledby="working-title" hidden>
        <div class="panel-head">
          <div>
            <h3 class="subsection-heading" id="working-title"></h3>
            <p class="text-sm text-muted font-mono" id="working-meta"></p>
            <a class="btn btn-sm btn-outline list-uri" id="lst-uri" target="_blank" rel="noreferrer"><span class="mono" id="lst-uri-text"></span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7h10v10"/><path d="M7 17 17 7"/></svg></a>
          </div>
        </div>
        <div class="tabs" role="tablist" id="working-tabs" aria-label="Working list views">
          <button class="tab-btn active" type="button" role="tab" id="tab-entries" data-tab="entries" aria-selected="true" aria-controls="entries-panel">Entries <span id="allocation-count" class="count-chip">0</span></button>
          <button class="tab-btn" type="button" role="tab" id="tab-token" data-tab="token" aria-selected="false" aria-controls="token-panel" tabindex="-1">Token</button>
          <button class="tab-btn" type="button" role="tab" id="tab-key" data-tab="key" aria-selected="false" aria-controls="key-panel" tabindex="-1">Signing key</button>
        </div>

        <div role="tabpanel" id="entries-panel" aria-labelledby="tab-entries">
          <div class="batch-fields">
            <div>
              <label class="field-label" for="entries-count">Count</label>
              <input id="entries-count" type="number" min="1" max="500" value="10">
            </div>
            <div>
              <label class="field-label" for="entries-expiry">Entry expiry</label>
              <input id="entries-expiry" type="date" value="2099-12-31">
            </div>
          </div>
          <div class="btn-row mt-4 mb-4">
            <button id="add-entries" class="btn btn-md btn-secondary">Add entries to this list</button>
          </div>
          <div class="entries-scroll">
            <div class="test-table-wrap">
              <table class="test-table">
                <thead><tr><th>Index</th><th>Expiry</th><th>Status</th><th>Actions</th></tr></thead>
                <tbody id="allocation-rows"></tbody>
              </table>
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

          <h4 class="subsection-heading subhead">Status list</h4>
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

        <div role="tabpanel" id="key-panel" aria-labelledby="tab-key" hidden>
          <p class="eyebrow">JWKS · list signer key</p>
          <pre id="jwks"></pre>
        </div>
      </section>

      <div id="notice" class="notice" role="alert" hidden>
        <svg class="notice-icon notice-icon-destructive" viewBox="0 0 24 24" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
        <svg class="notice-icon notice-icon-info" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
        <div>
          <p class="notice-title" id="notice-title"></p>
          <p class="notice-body" id="notice-body"></p>
        </div>
        <button id="notice-dismiss" class="btn btn-sm btn-ghost" type="button">Dismiss</button>
      </div>

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
    const notice = document.querySelector("#notice");
    const jwtBox = document.querySelector("#jwt");
    const copyButton = document.querySelector("#copy-token");
    let allocations = [];
    let registry = [];
    let currentToken = "";
    // The working list the whole console is scoped to: null until the
    // operator clicks a list in the registry.
    let activeListUri = null;

    function describe(value) {
      if (typeof value === "string") return value;
      if (value instanceof Error) return value.message;
      if (value && typeof value.detail === "string") return value.detail;
      return JSON.stringify(value, null, 2);
    }

    // Failures and hints float in one alert until dismissed or until the next
    // action starts; successful actions show their result in the panels.
    function notify(value, kind = "destructive") {
      notice.className = `notice notice-${kind}`;
      document.querySelector("#notice-title").textContent =
        kind === "info" ? "Nothing selected" : "The action failed";
      document.querySelector("#notice-body").textContent = describe(value);
      notice.hidden = false;
    }
    document.querySelector("#notice-dismiss").onclick = () => { notice.hidden = true; };

    // Every dashboard fetch reports failures in the notice: an unhandled
    // rejection would leave the operator with a stale table and no explanation.
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

    // The registry is both the inventory and the chooser: clicking a row makes
    // that list the working list.
    function renderRegistry() {
      registryRows.innerHTML = registry.length
        ? registry.map((item) => `<tr class="registry-row" tabindex="0" data-list="${escapeHtml(item.status_list_uri)}"${item.status_list_uri === activeListUri ? ' aria-current="true"' : ""}>
            <td>
              <span class="list-name">${escapeHtml(item.country)} · ${escapeHtml(item.doctype)}</span>
              <span class="list-meta"><span class="status-chip status-${item.expired ? "revoked" : "valid"}">${item.expired ? "Expired" : "Active"}</span><span class="font-mono">${item.allocated} allocated · ${item.revoked} revoked</span></span>
            </td>
            <td class="cell-mono">${escapeHtml(item.list_id)}</td>
            <td class="cell-mono">${escapeHtml(formatDate(item.expires))}</td>
          </tr>`).join("")
        : `<tr class="empty-row"><td colspan="3">No country × doctype list allocated yet.</td></tr>`;
    }

    // The working-list card follows the chosen list.
    function renderContext() {
      const pool = workingPool();
      workingCard.hidden = !pool;
      if (pool) {
        document.querySelector("#working-title").textContent = `${pool.country} · ${pool.doctype}`;
        document.querySelector("#working-meta").textContent =
          `${pool.allocated} allocated · ${pool.revoked} revoked · ` +
          (pool.expired ? "expired" : `expires ${formatDate(pool.expires)}`);
        const link = document.querySelector("#lst-uri");
        link.href = pool.status_list_uri;
        document.querySelector("#lst-uri-text").textContent = pool.status_list_uri;
      }
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
      if (uri !== activeListUri) showTab("entries");
      activeListUri = uri;
      renderContext();
      await showCard(uri);
    }

    // The working-list views: one tab visible at a time keeps the page short.
    const tabs = [...document.querySelectorAll("#working-tabs [role=tab]")];
    function showTab(name) {
      for (const tab of tabs) {
        const active = tab.dataset.tab === name;
        tab.classList.toggle("active", active);
        tab.setAttribute("aria-selected", String(active));
        tab.tabIndex = active ? 0 : -1;
        document.getElementById(tab.getAttribute("aria-controls")).hidden = !active;
      }
    }
    tabs.forEach((tab) => { tab.onclick = () => showTab(tab.dataset.tab); });
    // Arrow keys move between tabs, as in the WAI-ARIA tabs pattern.
    document.querySelector("#working-tabs").onkeydown = (event) => {
      const step = { ArrowRight: 1, ArrowLeft: -1 }[event.key];
      if (!step) return;
      const index = tabs.findIndex((tab) => tab.getAttribute("aria-selected") === "true");
      const next = tabs[(index + step + tabs.length) % tabs.length];
      showTab(next.dataset.tab);
      next.focus();
    };

    function chooseRow(event) {
      const row = event.target.closest("tr[data-list]");
      if (!row) return;
      guard(async () => {
        await selectList(row.dataset.list);
        // Re-rendering the registry drops focus; keyboard users keep their row.
        if (event.type === "keydown") registryRows.querySelector('tr[aria-current="true"]')?.focus();
      });
    }
    registryRows.onclick = chooseRow;
    registryRows.onkeydown = (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      event.preventDefault();
      chooseRow(event);
    };

    // Top-up of the working list: entries only, no credentials.
    document.querySelector("#add-entries").onclick = () => guard(async () => {
      const pool = workingPool();
      if (!pool) return notify("Click a country × doctype list first.", "info");
      await jsonFetch("/dashboard/status-lists", {
        method: "POST",
        body: JSON.stringify({
          country: pool.country,
          doctype: pool.doctype,
          expiry_date: document.querySelector("#entries-expiry").value || pool.expires,
          count: Number(document.querySelector("#entries-count").value || 10),
        }),
      });
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
      showNewListForm(false);
      await load();
      await selectList(data.status_list_uri);
    });

    document.querySelector("#registry-refresh").onclick = () => guard(load);

    function renderJwt(token) {
      const [header, payload, signature] = token.split(".");
      jwtBox.innerHTML =
        `<span class="jwt-header">${escapeHtml(header)}</span>` +
        `<span class="jwt-dot">.</span>` +
        `<span class="jwt-payload">${escapeHtml(payload)}</span>` +
        `<span class="jwt-dot">.</span>` +
        `<span class="jwt-signature">${escapeHtml(signature)}</span>`;
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
        "Payload",
        'Accepts a JWT, a CWT as hex or base64, the JSON payload, or the bare <span class="mono">lst</span>'
        " value. Signatures are not verified.",
    )
    + """
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
          <button id="explore" class="btn btn-lg btn-primary">Inspect payload</button>
          <button id="explore-current" class="btn btn-lg btn-outline">Load this server's status list</button>
        </div>
        <pre class="output mt-4" id="explore-out">Paste a payload, then inspect it.</pre>
    </div>
    </section>

    <section class="page-section page-section-white" id="explore-card" aria-labelledby="decoded-title" hidden>
    <div class="container">
"""
    + _section_intro(2, "decoded-title", "Decoded status list")
    + """
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

        <h3 class="subsection-heading subhead">Check an index</h3>
        <div class="index-lookup">
          <input id="explore-index" type="number" min="0" value="0" aria-label="Index">
          <button id="explore-lookup" class="btn btn-sm btn-secondary">Check index</button>
          <span id="explore-index-status"></span>
        </div>

        <h3 class="subsection-heading subhead">Non-valid indices</h3>
        <div id="explore-indices" class="index-groups"></div>
        <div class="btn-row mt-4">
          <button id="explore-copy-indices" class="btn btn-sm btn-outline">Copy the indices</button>
        </div>

        <h3 class="subsection-heading subhead">Inflated lst spectrum</h3>
        <div class="bitmap-shell">
          <div class="bitmap-scroll" id="explore-bitmap-scroll" tabindex="0" aria-label="Full inflated status list">
            <div class="bitmap" id="explore-bitmap"></div>
          </div>
          <div class="bitmap-minimap-scroll" id="explore-minimap-scroll" tabindex="0" aria-label="Non-valid entry minimap">
            <div class="bitmap-minimap" id="explore-minimap"></div>
          </div>
        </div>
        <p class="bitmap-caption" id="explore-caption"></p>

        <h3 class="subsection-heading subhead">Decoded token</h3>
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
    </div>
    </section>
  </main>"""
)


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
      target.innerHTML = `<span class="status-chip status-${escapeHtml(name.toLowerCase())}">${escapeHtml(statusLabel(name))}</span>`;
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
