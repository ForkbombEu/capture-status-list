from pydantic import BaseModel, Field


class CredentialCreateRequest(BaseModel):
    credential_id: str = Field(min_length=1)
    idx: int | None = Field(default=None, ge=0)


class RandomBatchCreateRequest(BaseModel):
    count: int = Field(default=10, ge=1, le=500)
    prefix: str = Field(
        default="cred",
        min_length=1,
        max_length=32,
        pattern=r"^[A-Za-z0-9_-]+$",
    )
    country: str = Field(default="EU", min_length=1, max_length=16)
    doctype: str = Field(default="org.iso.18013.5.1.mDL", min_length=1, max_length=128)
    expiry_date: str = Field(default="2099-12-31", pattern=r"^\d{4}-\d{2}-\d{2}$")


class CredentialResponse(BaseModel):
    credential_id: str
    idx: int
    status_list_uri: str
    referenced_token_status: dict[str, dict[str, int | str]]


class CredentialListItem(BaseModel):
    credential_id: str
    idx: int
    status_list_uri: str
    status: str
    verification_result: str | None = None


class AllocatedStatusListEntry(BaseModel):
    country: str
    doctype: str
    status_list_uri: str
    identifier_list_uri: str
    idx: int
    expiry_date: str
    status: str


class CredentialListResponse(BaseModel):
    credentials: list[CredentialListItem]
    allocated_entries: list[AllocatedStatusListEntry]


class StatusListReference(BaseModel):
    uri: str
    idx: int


class IdentifierListReference(BaseModel):
    uri: str
    id: str


class StatusListTakeResponse(BaseModel):
    status_list: StatusListReference
    identifier_list: IdentifierListReference


class RandomBatchCreateResponse(BaseModel):
    created: list[CredentialResponse]


class RevokeResponse(BaseModel):
    credential_id: str
    idx: int
    status: str


class CredentialIdsRequest(BaseModel):
    credential_ids: list[str] = Field(min_length=1, max_length=500)


class BatchError(BaseModel):
    credential_id: str
    error: str


class RevokeBatchResponse(BaseModel):
    revoked: list[RevokeResponse]
    errors: list[BatchError] = Field(default_factory=list)


class VerifyResponse(BaseModel):
    credential_id: str
    idx: int
    result: str
    status: str


class VerifyBatchResponse(BaseModel):
    verified: list[VerifyResponse]
    errors: list[BatchError] = Field(default_factory=list)


class DebugStatusResponse(BaseModel):
    warning: str = "TEST/DEBUG ONLY"
    idx: int
    status: str


class StatusListAssignment(BaseModel):
    idx: int
    credential_id: str
    status: str


class StatusListBits(BaseModel):
    """The inflated `lst` byte array, rendered for human reading.

    `window` holds one hex digit per entry (two when `bits` is 8), so a
    1-bit list reads as a run of `0` and `1` characters.
    """

    compressed_bytes: int
    inflated_bytes: int
    entries: int
    chars_per_entry: int
    window_start: int
    window_size: int
    window: str
    full: str


class StatusListDebugResponse(BaseModel):
    warning: str = "TEST/DEBUG ONLY"
    token: str
    header: dict[str, str]
    payload: dict
    bits: int
    size: int
    valid: int
    revoked: int
    revoked_indices: list[int]
    lst: StatusListBits
    assignments: list[StatusListAssignment]
    assignment_offset: int = 0
    assignment_limit: int = 100
    assignment_total: int = 0
    jwks: dict[str, list[dict[str, str]]]


class ResetResponse(BaseModel):
    status: str = "RESET"
    size: int = 10000
    default_status: str = "VALID"
