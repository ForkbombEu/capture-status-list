import zlib
from pathlib import Path
from uuid import uuid4

import jwt

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from issuer import (
    STATUS_LIST_URI,
    create_credential_record,
    debug_status_at,
    generate_current_status_list_token,
    get_credential_record,
    list_credential_records,
    list_version,
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
    StatusListAssignment,
    StatusListBits,
    StatusListDebugResponse,
    RevokeBatchResponse,
    RevokeResponse,
    VerifyBatchResponse,
    VerifyResponse,
)
from status_list import (
    STATUS_INVALID,
    TOKEN_TTL_SECONDS,
    InvalidStatusListIndex,
    base64url_decode,
    status_label,
    unpack_status_values,
)
from ui import console_html, docs_html
from verifier import VerificationError, check_status


app = FastAPI(
    title="Mock EUDI Token Status List Server",
    version="0.1.0",
    description="Minimal FCA test harness using an IETF Token Status List JWT.",
    docs_url=None,
    redoc_url=None,
)

# Runtime copies of the canonical Credimi brand assets. `fonts/` stays a
# sibling of `style.css` so the relative url() in each @font-face resolves.
BRAND_DIR = Path(__file__).resolve().parent / "brand"
FAVICON = BRAND_DIR / "logos" / "credimi_logo.svg"
app.mount("/brand", StaticFiles(directory=BRAND_DIR), name="brand")


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
    return HTMLResponse(console_html())


@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
def docs() -> HTMLResponse:
    return HTMLResponse(docs_html(app.openapi_url or "/openapi.json"))


@app.get("/favicon.svg", include_in_schema=False)
def favicon() -> FileResponse:
    return FileResponse(FAVICON, media_type="image/svg+xml")


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


def _status_list_etag() -> str:
    return f'W/"{list_version()}"'


def _etag_matches(if_none_match: str, etag: str) -> bool:
    candidates = [tag.strip() for tag in if_none_match.split(",")]
    bare = etag.removeprefix("W/")
    return "*" in candidates or etag in candidates or bare in candidates


@app.get("/status/1", response_class=PlainTextResponse)
def status_list_token(request: Request) -> PlainTextResponse:
    """Serve the signed Status List Token with weak-ETag revalidation.

    ``max-age = ttl`` mirrors the German national wallet backend: verifiers
    cache the token for its validity window and revalidate via
    ``If-None-Match``, so a revocation propagates within one ttl.
    """
    etag = _status_list_etag()
    headers = {
        "Cache-Control": f"max-age={TOKEN_TTL_SECONDS}",
        "ETag": etag,
    }
    if_none_match = request.headers.get("if-none-match")
    if if_none_match and _etag_matches(if_none_match, etag):
        return PlainTextResponse(b"", status_code=304, headers=headers)
    token = generate_current_status_list_token()
    return PlainTextResponse(
        token, media_type="application/statuslist+jwt", headers=headers
    )


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


@app.get("/debug/status-list", response_model=StatusListDebugResponse)
def debug_status_list() -> StatusListDebugResponse:
    """Decode the current Status List Token into its human-readable parts.

    Test infrastructure: it exposes the token header, payload, the inflated
    `lst` bit string and the signing JWKS in one response so the console can
    show what `GET /status/1` actually carries.
    """
    token = generate_current_status_list_token()
    header = jwt.get_unverified_header(token)
    payload = jwt.decode(token, options={"verify_signature": False})

    status_list = payload["status_list"]
    bits = status_list["bits"]
    compressed = base64url_decode(status_list["lst"])
    inflated = zlib.decompress(compressed)
    statuses = unpack_status_values(inflated, bits=bits)
    revoked_indices = [
        idx for idx, value in enumerate(statuses) if value == STATUS_INVALID
    ]
    assignments = [
        StatusListAssignment(
            idx=record.idx,
            credential_id=record.credential_id,
            status=status_label(statuses[record.idx]),
        )
        for record in list_credential_records()
    ]

    return StatusListDebugResponse(
        token=token,
        header=header,
        payload=payload,
        bits=bits,
        size=len(statuses),
        valid=len(statuses) - len(revoked_indices),
        revoked=len(revoked_indices),
        revoked_indices=revoked_indices,
        lst=_status_list_bits(
            statuses,
            bits=bits,
            compressed_bytes=len(compressed),
            inflated_bytes=len(inflated),
            around=[record.idx for record in list_credential_records()],
        ),
        assignments=assignments,
        jwks=public_jwks(),
    )


STATUS_BITS_WINDOW = 256


def _status_list_bits(
    statuses: list[int],
    *,
    bits: int,
    compressed_bytes: int,
    inflated_bytes: int,
    around: list[int],
) -> StatusListBits:
    """Render a readable slice of the inflated status array.

    The list holds 10,000 entries, so the console shows a window of
    `STATUS_BITS_WINDOW` entries, aligned to a 64-entry row and positioned to
    contain the assigned indices when there are any.
    """
    chars_per_entry = 2 if bits == 8 else 1
    first = min(around) if around else 0
    start = max(0, (first // 64) * 64)
    start = min(start, max(0, len(statuses) - STATUS_BITS_WINDOW))
    window_values = statuses[start : start + STATUS_BITS_WINDOW]

    return StatusListBits(
        compressed_bytes=compressed_bytes,
        inflated_bytes=inflated_bytes,
        entries=len(statuses),
        chars_per_entry=chars_per_entry,
        window_start=start,
        window_size=len(window_values),
        window="".join(
            format(value, "x").rjust(chars_per_entry, "0") for value in window_values
        ),
    )


@app.post("/reset", response_model=ResetResponse)
def reset() -> ResetResponse:
    reset_state()
    return ResetResponse()
