from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

from issuer import (
    STATUS_LIST_URI,
    create_credential_record,
    debug_status_at,
    generate_current_status_list_token,
    get_credential_record,
    public_jwks,
    reset_state,
    revoke_credential_record,
)
from models import (
    CredentialCreateRequest,
    CredentialResponse,
    DebugStatusResponse,
    ResetResponse,
    RevokeResponse,
    VerifyResponse,
)
from status_list import InvalidStatusListIndex
from verifier import VerificationError, check_status


app = FastAPI(
    title="Mock EUDI Token Status List Server",
    version="0.1.0",
    description="Minimal FCA test harness using an IETF Token Status List JWT.",
)


@app.post("/credentials", response_model=CredentialResponse)
def create_credential(request: CredentialCreateRequest) -> CredentialResponse:
    try:
        return create_credential_record(request.credential_id, idx=request.idx)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.post("/credentials/{credential_id}/revoke", response_model=RevokeResponse)
def revoke_credential(credential_id: str) -> RevokeResponse:
    try:
        return revoke_credential_record(credential_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/status/1", response_class=PlainTextResponse)
def status_list_token() -> PlainTextResponse:
    token = generate_current_status_list_token()
    return PlainTextResponse(token, media_type="application/statuslist+jwt")


@app.get("/.well-known/jwks.json")
def jwks() -> dict[str, list[dict[str, str]]]:
    return public_jwks()


@app.post("/verify/{credential_id}", response_model=VerifyResponse)
def verify_credential(credential_id: str) -> VerifyResponse:
    try:
        credential = get_credential_record(credential_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    token = generate_current_status_list_token()
    try:
        status = check_status(credential.idx, token, expected_subject=STATUS_LIST_URI)
    except (InvalidStatusListIndex, VerificationError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return VerifyResponse(
        credential_id=credential.credential_id,
        idx=credential.idx,
        result="ACCEPT" if status == "VALID" else "REJECT",
        status=status,
    )


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
