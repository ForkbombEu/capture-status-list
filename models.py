from pydantic import BaseModel, Field


class CredentialCreateRequest(BaseModel):
    credential_id: str = Field(min_length=1)
    idx: int | None = Field(default=None, ge=0)


class CredentialResponse(BaseModel):
    credential_id: str
    idx: int
    status_list_uri: str
    referenced_token_status: dict[str, dict[str, int | str]]


class RevokeResponse(BaseModel):
    credential_id: str
    idx: int
    status: str


class VerifyResponse(BaseModel):
    credential_id: str
    idx: int
    result: str
    status: str


class DebugStatusResponse(BaseModel):
    warning: str = "TEST/DEBUG ONLY"
    idx: int
    status: str


class ResetResponse(BaseModel):
    status: str = "RESET"
    size: int = 10000
    default_status: str = "VALID"
