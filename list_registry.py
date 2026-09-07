from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import PurePosixPath
from uuid import UUID, uuid4

from status_list import DEFAULT_STATUS_LIST_SIZE, IndexScatter, STATUS_VALID


TOKEN_LIST_KIND = "token_status_list"
IDENTIFIER_LIST_KIND = "identifier_list"


@dataclass
class ListState:
    country: str
    doctype: str
    list_id: UUID
    statuses: list[int] = field(default_factory=lambda: [STATUS_VALID] * DEFAULT_STATUS_LIST_SIZE)
    identifiers: dict[str, int] = field(default_factory=dict)
    issued_expiry: date | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    seed: bytes = field(default_factory=lambda: uuid4().bytes + uuid4().bytes)
    cursor: int = 0
    version: int = 0

    @property
    def size(self) -> int:
        return len(self.statuses)

    @property
    def scatter(self) -> IndexScatter:
        return IndexScatter(self.size, self.seed)

    def token_uri(self, base_url: str) -> str:
        return f"{base_url.rstrip('/')}/{TOKEN_LIST_KIND}/{self.country}/{self.doctype}/{self.list_id}"

    def identifier_uri(self, base_url: str) -> str:
        return f"{base_url.rstrip('/')}/{IDENTIFIER_LIST_KIND}/{self.country}/{self.doctype}/{self.list_id}"


@dataclass(frozen=True)
class ListReference:
    status_list_uri: str
    identifier_list_uri: str
    idx: int
    list_id: UUID


@dataclass(frozen=True)
class ListSummary:
    country: str
    doctype: str
    list_id: str
    status_list_uri: str
    identifier_list_uri: str
    allocated: int
    revoked: int
    version: int
    expires: str | None
    expired: bool
    current: bool


class StatusListRegistry:
    def __init__(self, base_url: str, size: int = DEFAULT_STATUS_LIST_SIZE) -> None:
        if size < 1:
            raise ValueError("list size must be positive")
        self.base_url = base_url.rstrip("/")
        self.size = size
        self._current: dict[tuple[str, str], ListState] = {}
        self._lists: dict[tuple[str, str, UUID], ListState] = {}
        self._allocation_replays: dict[tuple[str, str, str], tuple[str, ListReference]] = {}

    def reset(self) -> None:
        self._current.clear()
        self._lists.clear()
        self._allocation_replays.clear()

    def take(
        self,
        country: str,
        doctype: str,
        expiry_date: str,
        allocation_id: str | None = None,
    ) -> ListReference:
        self._validate_components(country, doctype)
        expiry = self._parse_expiry(expiry_date)
        if allocation_id is not None:
            if not allocation_id:
                raise ValueError("allocation_id must not be empty")
            replay_key = (country, doctype, allocation_id)
            replay = self._allocation_replays.get(replay_key)
            if replay is not None:
                replay_expiry, reference = replay
                if replay_expiry != expiry_date:
                    raise ValueError("allocation_id was already used with different parameters")
                return reference

        key = (country, doctype)
        state = self._current.get(key)
        if state is None or state.cursor >= state.size:
            state = self._new_list(country, doctype)
            self._current[key] = state
        state.issued_expiry = max(state.issued_expiry or expiry, expiry)
        cursor = state.cursor
        state.cursor += 1
        idx = state.scatter.permute(cursor)
        reference = ListReference(
            status_list_uri=state.token_uri(self.base_url),
            identifier_list_uri=state.identifier_uri(self.base_url),
            idx=idx,
            list_id=state.list_id,
        )
        if allocation_id is not None:
            self._allocation_replays[(country, doctype, allocation_id)] = (
                expiry_date,
                reference,
            )
        return reference


    def get_by_uri(self, uri: str) -> tuple[str, ListState]:
        kind, country, doctype, list_id = self.parse_uri(uri)
        state = self._lists.get((country, doctype, list_id))
        if state is None:
            raise KeyError(f"unknown {kind} list: {uri}")
        return kind, state

    def expire(self, uri: str, expiry_date: str) -> ListState:
        _, state = self.get_by_uri(uri)
        try:
            state.issued_expiry = date.fromisoformat(expiry_date)
        except (TypeError, ValueError) as exc:
            raise ValueError("expiry_date must use YYYY-MM-DD") from exc
        state.version += 1
        return state

    def set_status(self, uri: str, idx: int, value: int = 1) -> ListState:
        kind, state = self.get_by_uri(uri)
        if value != 1:
            raise ValueError("only status 1 is supported for revocation")
        if idx < 0 or idx >= state.size:
            raise ValueError(f"idx must be between 0 and {state.size - 1}: {idx}")
        state.statuses[idx] = value
        state.identifiers[str(idx)] = value
        state.version += 1
        return state

    def status_at(self, uri: str, idx: int) -> int:
        kind, state = self.get_by_uri(uri)
        if idx < 0 or idx >= state.size:
            raise ValueError(f"idx must be between 0 and {state.size - 1}: {idx}")
        if kind == IDENTIFIER_LIST_KIND:
            return state.identifiers.get(str(idx), 0)
        return state.statuses[idx]

    def list_summaries(self) -> list[ListSummary]:
        result: list[ListSummary] = []
        for key, state in sorted(self._lists.items(), key=lambda item: str(item[0])):
            current = self._current.get(key[:2]) is state
            expired = state.issued_expiry is not None and state.issued_expiry < date.today()
            result.append(
                ListSummary(
                    country=state.country,
                    doctype=state.doctype,
                    list_id=str(state.list_id),
                    status_list_uri=state.token_uri(self.base_url),
                    identifier_list_uri=state.identifier_uri(self.base_url),
                    allocated=state.cursor,
                    revoked=sum(value == 1 for value in state.statuses),
                    version=state.version,
                    expires=state.issued_expiry.isoformat() if state.issued_expiry else None,
                    expired=expired,
                    current=current,
                )
            )
        return result

    def parse_uri(self, uri: str) -> tuple[str, str, str, UUID]:
        prefix = self.base_url + "/"
        if not uri.startswith(prefix):
            raise ValueError("URI is outside this status-list service")
        parts = PurePosixPath(uri[len(prefix) :]).parts
        if len(parts) != 4 or parts[0] not in {TOKEN_LIST_KIND, IDENTIFIER_LIST_KIND}:
            raise ValueError("invalid status-list URI")
        kind, country, doctype, raw_id = parts
        self._validate_components(country, doctype)
        try:
            list_id = UUID(raw_id)
        except ValueError as exc:
            raise ValueError("invalid status-list UUID") from exc
        return kind, country, doctype, list_id

    def _new_list(self, country: str, doctype: str) -> ListState:
        state = ListState(
            country=country,
            doctype=doctype,
            list_id=uuid4(),
            statuses=[STATUS_VALID] * self.size,
        )
        self._lists[(country, doctype, state.list_id)] = state
        return state

    @staticmethod
    def _validate_components(country: str, doctype: str) -> None:
        forbidden = "/?#\\"
        if not country or any(char in forbidden for char in country) or country in {".", ".."}:
            raise ValueError("invalid country")
        if not doctype or any(char in forbidden for char in doctype) or doctype in {".", ".."}:
            raise ValueError("invalid doctype")

    @staticmethod
    def _parse_expiry(value: str) -> date:
        try:
            expiry = date.fromisoformat(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("expiry_date must use YYYY-MM-DD") from exc
        if expiry < date.today():
            raise ValueError("expiry_date must be in the future")
        return expiry
