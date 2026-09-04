from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from issuer import (
    STATUS_LIST_URI,
    create_credential_record,
    debug_status_at,
    generate_current_status_list_token,
    get_credential_record,
    list_credential_records,
    public_jwks,
    reset_state,
    revoke_credential_record,
)
from models import (
    BatchError,
    CredentialIdsRequest,
    CredentialListItem,
    CredentialListResponse,
    CredentialCreateRequest,
    CredentialResponse,
    DebugStatusResponse,
    RandomBatchCreateRequest,
    RandomBatchCreateResponse,
    ResetResponse,
    RevokeBatchResponse,
    RevokeResponse,
    VerifyBatchResponse,
    VerifyResponse,
)
from status_list import InvalidStatusListIndex
from verifier import VerificationError, check_status


app = FastAPI(
    title="Mock EUDI Token Status List Server",
    version="0.1.0",
    description="Minimal FCA test harness using an IETF Token Status List JWT.",
)

DESIGN_DIR = Path(__file__).resolve().parent / ".puria" / "design"
app.mount("/design-assets", StaticFiles(directory=DESIGN_DIR), name="design-assets")


def _red_ui_html() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Credimi TSL console</title>
  <link rel="stylesheet" href="/design-assets/colors_and_type.css">
  <style>
    * { box-sizing: border-box; }
    html { background: var(--bg-tint); }
    body {
      margin: 0;
      background: var(--bg-tint);
      color: var(--fg);
      font: 400 var(--fs-base)/var(--lh-base) var(--font-sans);
    }
    .topbar {
      position: sticky;
      top: 0;
      z-index: 10;
      background: var(--bg);
      border-bottom: 1px solid var(--border);
    }
    .topbar-inner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: var(--space-4);
      max-width: 1280px;
      margin: 0 auto;
      padding: var(--space-3) var(--space-6);
    }
    .logo {
      height: 26px;
      display: block;
    }
    .topbar-meta {
      display: flex;
      gap: var(--space-2);
      align-items: center;
      color: var(--fg-muted);
      font: 500 var(--fs-sm)/1 var(--font-mono);
    }
    .page-header {
      position: relative;
      overflow: hidden;
      background: var(--brand-secondary);
      border-bottom: 1px solid var(--border);
    }
    .page-header-inner {
      max-width: 1280px;
      margin: 0;
      padding: var(--space-10) var(--space-6);
      margin-inline: auto;
    }
    .crosshatch {
      position: absolute;
      right: -70px;
      top: -80px;
      width: 300px;
      height: 300px;
      pointer-events: none;
      opacity: .08;
      background:
        repeating-linear-gradient(45deg, var(--fg) 0 1px, transparent 1px 18px),
        repeating-linear-gradient(-45deg, var(--fg) 0 1px, transparent 1px 18px);
    }
    .eyebrow {
      margin: 0 0 var(--space-2);
      font: 500 var(--fs-xs)/1.2 var(--font-sans);
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--fg-muted);
    }
    h1 {
      max-width: 820px;
      margin: 0;
      font: 700 var(--fs-4xl)/var(--lh-4xl) var(--font-display);
      letter-spacing: -.012em;
      color: var(--brand-primary);
    }
    .sub {
      max-width: 760px;
      margin: var(--space-3) 0 0;
      color: var(--fg-subtle);
      font: 400 var(--fs-md)/1.5 var(--font-sans);
    }
    main {
      display: flex;
      flex-direction: column;
      gap: var(--space-6);
      max-width: 1280px;
      margin: 0 auto;
      padding: var(--space-8) var(--space-6) var(--space-20);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: var(--space-4);
    }
    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: var(--space-5);
    }
    .card:hover { border-color: var(--border-strong); }
    .section-header {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: var(--space-3);
      border-bottom: 1px solid var(--border);
      padding-bottom: var(--space-2);
      margin-bottom: var(--space-4);
    }
    h2 {
      margin: 0;
      font: 700 var(--fs-2xl)/var(--lh-2xl) var(--font-display);
      letter-spacing: -.006em;
      color: var(--fg);
    }
    .count {
      display: inline-block;
      margin-left: var(--space-2);
      padding: 2px var(--space-2);
      border-radius: var(--radius-pill);
      background: var(--bg-muted);
      color: var(--fg-muted);
      font: 600 var(--fs-xs)/1 var(--font-sans);
    }
    .metrics {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: var(--space-3);
    }
    .metric {
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: var(--space-4);
    }
    .metric strong {
      display: block;
      color: var(--brand-primary);
      font: 700 var(--fs-2xl)/1 var(--font-display);
      letter-spacing: -.006em;
    }
    .metric span {
      color: var(--fg-muted);
      font: 500 var(--fs-xs)/1.3 var(--font-sans);
      letter-spacing: .14em;
      text-transform: uppercase;
    }
    label {
      display: block;
      margin: var(--space-3) 0 var(--space-2);
      color: var(--fg);
      font: 500 var(--fs-base)/1 var(--font-sans);
    }
    input {
      width: 100%;
      height: 36px;
      border: 1px solid var(--input);
      background: var(--bg);
      color: var(--fg);
      border-radius: var(--radius);
      padding: 0 var(--space-3);
      font: 400 var(--fs-base)/1 var(--font-sans);
      outline: none;
    }
    input:focus {
      border-color: var(--brand-primary);
      box-shadow: 0 0 0 3px color-mix(in oklch, var(--brand-primary) 18%, transparent);
    }
    button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-2);
      min-height: 40px;
      border: 1px solid transparent;
      border-radius: var(--radius);
      background: var(--brand-primary);
      color: var(--fg-on-primary);
      padding: 0 var(--space-4);
      cursor: pointer;
      font: 500 var(--fs-base)/var(--lh-base) var(--font-sans);
      transition: background 150ms ease-out, border-color 150ms ease-out;
    }
    button:hover { background: var(--brand-primary-700); }
    button.secondary {
      background: var(--brand-secondary-deep);
      color: var(--brand-primary);
    }
    button.secondary:hover { background: var(--brand-secondary-strong); }
    button.outline {
      background: var(--bg);
      border-color: var(--border);
      color: var(--fg);
    }
    button.outline:hover { background: var(--bg-muted); }
    button.danger {
      background: var(--destructive);
      color: var(--fg-on-primary);
    }
    button.danger:hover { filter: brightness(.94); }
    .button-stack {
      display: grid;
      gap: var(--space-2);
      margin-top: var(--space-3);
    }
    .bar, .actions {
      display: flex;
      gap: var(--space-2);
      align-items: stretch;
      flex-wrap: wrap;
    }
    .bar button, .actions button { min-width: 130px; }
    .table-wrap {
      overflow-x: auto;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--bg);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 720px;
      background: var(--bg);
    }
    th, td {
      border-bottom: 1px solid var(--border);
      padding: var(--space-3) var(--space-4);
      text-align: left;
      vertical-align: middle;
      font: 400 var(--fs-base)/1.35 var(--font-sans);
    }
    tbody tr:last-child td { border-bottom: 0; }
    tbody tr:hover td { background: var(--brand-secondary); }
    th {
      background: var(--bg-muted);
      color: var(--fg-muted);
      font: 500 var(--fs-xs)/1.2 var(--font-sans);
      letter-spacing: .14em;
      text-transform: uppercase;
    }
    td.mono { font-family: var(--font-mono); font-size: 13px; }
    tr.revoked td { background: var(--destructive-bg); }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: var(--space-2);
      border: .5px solid currentColor;
      border-radius: var(--radius-pill);
      padding: 3px var(--space-2);
      font: 500 var(--fs-sm)/1 var(--font-sans);
    }
    .badge::before {
      content: "";
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: currentColor;
    }
    .badge.valid, .badge.accept { background: var(--success-bg); color: var(--success); }
    .badge.revoked, .badge.reject { background: var(--destructive-bg); color: var(--destructive); }
    .badge.pending { background: var(--brand-secondary); color: var(--brand-primary); }
    pre {
      margin: 0;
      min-height: 74px;
      overflow: auto;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--bg-muted);
      color: var(--fg);
      padding: var(--space-4);
      font: 400 13px/1.45 var(--font-mono);
      white-space: pre-wrap;
      word-break: break-word;
    }
    .full { display: grid; gap: var(--space-4); }
    @media (max-width: 820px) {
      .grid, .metrics { grid-template-columns: 1fr; }
      .topbar-inner, .page-header-inner, main { padding-inline: var(--space-4); }
      .bar button, .actions button { flex: 1 1 100%; }
      h1 { font-size: 34px; line-height: 38px; }
    }
  </style>
</head>
<body>
  <nav class="topbar">
    <div class="topbar-inner">
      <img class="logo" src="/design-assets/assets/credimi_logo.svg" alt="Credimi">
      <div class="topbar-meta"><span>JWT</span><span>ES256</span><span>TSL</span></div>
    </div>
  </nav>
  <header class="page-header">
    <div class="crosshatch"></div>
    <div class="page-header-inner">
      <p class="eyebrow">EUDI conformance utility</p>
      <h1>Token Status List console</h1>
      <p class="sub">Create test credentials, revoke selected entries, and verify against the signed Status List Token.</p>
    </div>
  </header>
  <main>
    <div class="grid">
      <section class="card">
        <div class="section-header"><h2>Add batch:</h2></div>
        <label for="count">Count:</label>
        <input id="count" type="number" min="1" max="500" value="10">
        <label for="prefix">Credential prefix:</label>
        <input id="prefix" value="cred">
        <div class="button-stack">
          <button id="create">Create random batch</button>
        </div>
      </section>
      <section class="card">
        <div class="section-header"><h2>Selected:</h2></div>
        <div class="button-stack">
          <button id="verify" class="secondary">Verify selected</button>
          <button id="revoke" class="danger">Revoke selected</button>
        </div>
      </section>
      <section class="card">
        <div class="section-header"><h2>State:</h2></div>
        <div class="button-stack">
          <button id="refresh" class="outline">Refresh</button>
          <button id="reset" class="outline">Reset</button>
        </div>
      </section>
    </div>

    <section class="metrics" aria-label="Credential metrics">
      <div class="metric"><strong id="total">0</strong><span>Total credentials</span></div>
      <div class="metric"><strong id="valid">0</strong><span>Valid</span></div>
      <div class="metric"><strong id="revoked">0</strong><span>Revoked</span></div>
      <div class="metric"><strong id="verified">0</strong><span>Verified rows</span></div>
    </section>

    <section class="card full">
      <div class="section-header">
        <h2>Credentials <span id="row-count" class="count">0</span>:</h2>
        <button id="token" class="outline">Fetch token</button>
      </div>
      <div class="bar">
        <button id="all" class="outline">Select all</button>
        <button id="none" class="outline">Select none</button>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th></th>
              <th>Credential</th>
              <th>Index</th>
              <th>Status</th>
              <th>Verification</th>
            </tr>
          </thead>
          <tbody id="rows"></tbody>
        </table>
      </div>
    </section>

    <section class="card full">
      <div class="section-header"><h2>Output:</h2></div>
      <pre id="out">ready</pre>
    </section>
  </main>

  <script>
    const rows = document.querySelector("#rows");
    const out = document.querySelector("#out");
    const total = document.querySelector("#total");
    const valid = document.querySelector("#valid");
    const revoked = document.querySelector("#revoked");
    const verified = document.querySelector("#verified");
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
        headers: { "content-type": "application/json", ...(options.headers || {}) },
        ...options,
      });
      const type = response.headers.get("content-type") || "";
      const body = type.includes("application/json") ? await response.json() : await response.text();
      if (!response.ok) throw body;
      return body;
    }

    function render() {
      const selectedIndexes = new Set([...document.querySelectorAll("tbody input:checked")].map((box) => box.value));
      const counts = credentials.reduce((acc, item) => {
        acc.total += 1;
        if (item.status === "REVOKED") acc.revoked += 1;
        if (item.status === "VALID") acc.valid += 1;
        return acc;
      }, { total: 0, valid: 0, revoked: 0 });
      total.textContent = counts.total;
      valid.textContent = counts.valid;
      revoked.textContent = counts.revoked;
      verified.textContent = Object.keys(verification).length;
      rowCount.textContent = counts.total;

      if (!credentials.length) {
        rows.innerHTML = `<tr><td colspan="5">No credentials yet.</td></tr>`;
        return;
      }

      rows.innerHTML = credentials.map((item, index) => {
        const safeCredentialId = escapeHtml(item.credential_id);
        const checked = selectedIndexes.has(String(index)) ? "checked" : "";
        const key = item.credential_id;
        const result = verification[key]
          ? `<span class="badge ${escapeHtml(verification[key].result.toLowerCase())}">${escapeHtml(verification[key].result)} / ${escapeHtml(verification[key].status)}</span>`
          : `<span class="badge pending">Not verified</span>`;
        const state = item.status.toLowerCase();
        return `<tr class="${state}">
          <td><input type="checkbox" value="${index}" ${checked}></td>
          <td class="mono">${safeCredentialId}</td>
          <td class="mono">${item.idx}</td>
          <td><span class="badge ${state}">${escapeHtml(item.status)}</span></td>
          <td>${result}</td>
        </tr>`;
      }).join("");
    }

    async function load() {
      const data = await jsonFetch("/credentials");
      credentials = data.credentials;
      render();
    }

    document.querySelector("#create").onclick = async () => {
      const body = {
        count: Number(document.querySelector("#count").value || 10),
        prefix: document.querySelector("#prefix").value || "cred",
      };
      const data = await jsonFetch("/credentials/random-batch", {
        method: "POST",
        body: JSON.stringify(body),
      });
      write(data);
      await load();
    };

    document.querySelector("#revoke").onclick = async () => {
      const ids = selectedIds();
      if (!ids.length) return write("select credentials first");
      const data = await jsonFetch("/credentials/revoke-batch", {
        method: "POST",
        body: JSON.stringify({ credential_ids: ids }),
      });
      write(data);
      await load();
    };

    document.querySelector("#verify").onclick = async () => {
      const ids = selectedIds();
      if (!ids.length) return write("select credentials first");
      const data = await jsonFetch("/verify-batch", {
        method: "POST",
        body: JSON.stringify({ credential_ids: ids }),
      });
      verification = Object.fromEntries(data.verified.map((item) => [item.credential_id, item]));
      write(data);
      render();
    };

    document.querySelector("#refresh").onclick = load;
    document.querySelector("#all").onclick = () => {
      document.querySelectorAll("tbody input").forEach((box) => { box.checked = true; });
    };
    document.querySelector("#none").onclick = () => {
      document.querySelectorAll("tbody input").forEach((box) => { box.checked = false; });
    };
    document.querySelector("#token").onclick = async () => {
      const token = await jsonFetch("/status/1", { headers: { accept: "application/statuslist+jwt" } });
      write(token);
    };
    document.querySelector("#reset").onclick = async () => {
      const data = await jsonFetch("/reset", { method: "POST" });
      verification = {};
      write(data);
      await load();
    };

    load().catch(write);
  </script>
</body>
</html>"""


def _verify_record(credential_id: str, token: str | None = None) -> VerifyResponse:
    try:
        credential = get_credential_record(credential_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    status_list_token = token if token is not None else generate_current_status_list_token()
    try:
        status = check_status(
            credential.idx,
            status_list_token,
            expected_subject=STATUS_LIST_URI,
        )
    except (InvalidStatusListIndex, VerificationError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return VerifyResponse(
        credential_id=credential.credential_id,
        idx=credential.idx,
        result="ACCEPT" if status == "VALID" else "REJECT",
        status=status,
    )


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    return HTMLResponse(_red_ui_html())


@app.get("/red", response_class=HTMLResponse)
def red_route() -> HTMLResponse:
    return HTMLResponse(_red_ui_html())


@app.get("/credentials", response_model=CredentialListResponse)
def list_credentials() -> CredentialListResponse:
    return CredentialListResponse(
        credentials=[
            CredentialListItem(
                credential_id=record.credential_id,
                idx=record.idx,
                status_list_uri=record.status_list_uri,
                status=debug_status_at(record.idx),
            )
            for record in list_credential_records()
        ]
    )


@app.post("/credentials", response_model=CredentialResponse)
def create_credential(request: CredentialCreateRequest) -> CredentialResponse:
    try:
        return create_credential_record(request.credential_id, idx=request.idx)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.post("/credentials/random-batch", response_model=RandomBatchCreateResponse)
def create_random_batch(request: RandomBatchCreateRequest) -> RandomBatchCreateResponse:
    created: list[CredentialResponse] = []
    for _ in range(request.count):
        for _attempt in range(10):
            credential_id = f"{request.prefix}-{uuid4().hex[:12]}"
            try:
                created.append(create_credential_record(credential_id))
                break
            except KeyError:
                continue
        else:
            raise HTTPException(
                status_code=409,
                detail="could not generate an unused credential id",
            )
    return RandomBatchCreateResponse(created=created)


@app.post("/credentials/{credential_id}/revoke", response_model=RevokeResponse)
def revoke_credential(credential_id: str) -> RevokeResponse:
    try:
        return revoke_credential_record(credential_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/credentials/revoke-batch", response_model=RevokeBatchResponse)
def revoke_batch(request: CredentialIdsRequest) -> RevokeBatchResponse:
    revoked: list[RevokeResponse] = []
    errors: list[BatchError] = []
    for credential_id in request.credential_ids:
        try:
            revoked.append(revoke_credential_record(credential_id))
        except KeyError as exc:
            errors.append(BatchError(credential_id=credential_id, error=str(exc)))
    return RevokeBatchResponse(revoked=revoked, errors=errors)


@app.get("/status/1", response_class=PlainTextResponse)
def status_list_token() -> PlainTextResponse:
    token = generate_current_status_list_token()
    return PlainTextResponse(token, media_type="application/statuslist+jwt")


@app.get("/.well-known/jwks.json")
def jwks() -> dict[str, list[dict[str, str]]]:
    return public_jwks()


@app.post("/verify/{credential_id}", response_model=VerifyResponse)
def verify_credential(credential_id: str) -> VerifyResponse:
    return _verify_record(credential_id)


@app.post("/verify-batch", response_model=VerifyBatchResponse)
def verify_batch(request: CredentialIdsRequest) -> VerifyBatchResponse:
    verified: list[VerifyResponse] = []
    errors: list[BatchError] = []
    token = generate_current_status_list_token()
    for credential_id in request.credential_ids:
        try:
            verified.append(_verify_record(credential_id, token=token))
        except HTTPException as exc:
            errors.append(BatchError(credential_id=credential_id, error=str(exc.detail)))
    return VerifyBatchResponse(verified=verified, errors=errors)


@app.get("/debug/status/{idx}", response_model=DebugStatusResponse)
def debug_status(idx: int) -> DebugStatusResponse:
    try:
        status = debug_status_at(idx)
    except InvalidStatusListIndex as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return DebugStatusResponse(idx=idx, status=status)


@app.post("/reset", response_model=ResetResponse)
def reset() -> ResetResponse:
    reset_state()
    return ResetResponse()
