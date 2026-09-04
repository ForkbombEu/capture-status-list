from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse

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


def _red_ui_html() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mock TSL Red Route</title>
  <style>
    :root {
      --black: #000000;
      --paper: #FFFDF5;
      --yellow: #FFD23F;
      --red: #FF6B6B;
      --blue: #74B9FF;
      --green: #88D498;
      --orange: #FFA552;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--paper);
      color: var(--black);
      font: 16px/1.45 Inter, Arial, sans-serif;
    }
    main {
      display: grid;
      gap: 16px;
      max-width: 1180px;
      margin: 0 auto;
      padding: 20px;
    }
    header {
      border: 3px solid var(--black);
      background: var(--red);
      box-shadow: 6px 6px 0 0 var(--black);
      padding: 16px;
    }
    h1, h2 {
      margin: 0;
      font-family: "Space Grotesk", Arial, sans-serif;
      letter-spacing: 0;
    }
    h1 { font-size: clamp(30px, 7vw, 52px); line-height: 1; }
    h2 { font-size: 22px; }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }
    section {
      border: 3px solid var(--black);
      background: var(--paper);
      box-shadow: 5px 5px 0 0 var(--black);
      padding: 14px;
    }
    label {
      display: block;
      margin: 10px 0 4px;
      font: 700 12px/1.2 "Space Mono", monospace;
      text-transform: uppercase;
      letter-spacing: .06em;
    }
    input {
      width: 100%;
      border: 2px solid var(--black);
      background: var(--paper);
      padding: 9px;
      font: inherit;
      border-radius: 0;
    }
    button {
      width: 100%;
      min-height: 42px;
      margin-top: 10px;
      border: 3px solid var(--black);
      background: var(--yellow);
      color: var(--black);
      box-shadow: 4px 4px 0 0 var(--black);
      cursor: pointer;
      font: 700 12px/1.2 "Space Mono", monospace;
      letter-spacing: .06em;
      text-transform: uppercase;
    }
    button:hover { transform: translate(2px, 2px); box-shadow: 2px 2px 0 0 var(--black); }
    button.danger { background: var(--red); }
    button.info { background: var(--blue); }
    button.reset { background: var(--orange); }
    .bar {
      display: flex;
      gap: 10px;
      align-items: stretch;
    }
    .bar button { width: auto; min-width: 140px; margin-top: 0; }
    .table-wrap {
      overflow-x: auto;
      border: 3px solid var(--black);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 720px;
      background: var(--paper);
    }
    th, td {
      border: 2px solid var(--black);
      padding: 8px;
      text-align: left;
      vertical-align: middle;
    }
    th {
      background: var(--yellow);
      font: 700 12px/1.2 "Space Mono", monospace;
      letter-spacing: .06em;
      text-transform: uppercase;
    }
    tr.revoked td { background: #FFD6D6; }
    .badge {
      display: inline-block;
      border: 2px solid var(--black);
      background: var(--blue);
      padding: 3px 6px;
      font: 700 12px/1.2 "Space Mono", monospace;
    }
    .badge.valid { background: var(--green); }
    .badge.revoked { background: var(--red); }
    pre {
      min-height: 66px;
      margin: 0;
      overflow: auto;
      border: 3px solid var(--black);
      background: var(--black);
      color: var(--paper);
      padding: 10px;
      font: 12px/1.35 "Space Mono", monospace;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .full { display: grid; gap: 12px; }
    @media (max-width: 820px) {
      .grid { grid-template-columns: 1fr; }
      .bar { flex-direction: column; }
      .bar button { width: 100%; }
      main { padding: 12px; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <h1>TSL RED ROUTE</h1>
    </header>

    <div class="grid">
      <section>
        <h2>Add Batch</h2>
        <label for="count">count</label>
        <input id="count" type="number" min="1" max="500" value="10">
        <label for="prefix">prefix</label>
        <input id="prefix" value="cred">
        <button id="create">Create Random</button>
      </section>
      <section>
        <h2>Selected</h2>
        <button id="verify" class="info">Verify Selected</button>
        <button id="revoke" class="danger">Revoke Selected</button>
      </section>
      <section>
        <h2>State</h2>
        <button id="refresh">Refresh</button>
        <button id="reset" class="reset">Reset</button>
      </section>
    </div>

    <section class="full">
      <div class="bar">
        <button id="all">Select All</button>
        <button id="none">Select None</button>
        <button id="token" class="info">Fetch Token</button>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th></th>
              <th>credential</th>
              <th>idx</th>
              <th>status</th>
              <th>verify</th>
            </tr>
          </thead>
          <tbody id="rows"></tbody>
        </table>
      </div>
    </section>

    <section class="full">
      <h2>Output</h2>
      <pre id="out">ready</pre>
    </section>
  </main>

  <script>
    const rows = document.querySelector("#rows");
    const out = document.querySelector("#out");
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
      return [...document.querySelectorAll("tbody input:checked")].map((box) => box.value);
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
      const selected = new Set(selectedIds());
      rows.innerHTML = credentials.map((item) => {
        const safeCredentialId = escapeHtml(item.credential_id);
        const checked = selected.has(item.credential_id) ? "checked" : "";
        const key = item.credential_id;
        const result = verification[key]
          ? `${escapeHtml(verification[key].result)} / ${escapeHtml(verification[key].status)}`
          : "";
        const state = item.status.toLowerCase();
        return `<tr class="${state}">
          <td><input type="checkbox" value="${safeCredentialId}" ${checked}></td>
          <td>${safeCredentialId}</td>
          <td>${item.idx}</td>
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
