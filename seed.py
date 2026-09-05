from __future__ import annotations

import argparse
import os
import sys
from typing import Any

import httpx


DEFAULT_BASE_URL = "http://localhost:8000"
DEFAULT_COUNT = 24
DEFAULT_PREFIX = "demo"
DEFAULT_REVOKE_COUNT = 6


def seed_server(
    client: Any,
    *,
    base_url: str = DEFAULT_BASE_URL,
    count: int = DEFAULT_COUNT,
    prefix: str = DEFAULT_PREFIX,
    revoke_count: int = DEFAULT_REVOKE_COUNT,
    reset: bool = True,
) -> dict[str, int]:
    if count < 1:
        raise ValueError("count must be at least 1")
    if revoke_count < 0:
        raise ValueError("revoke count cannot be negative")

    root = base_url.rstrip("/")
    if reset:
        _post_json(client, root, "/reset", None)

    batch = _post_json(
        client,
        root,
        "/credentials/random-batch",
        {"count": count, "prefix": prefix},
    )
    created = batch["created"]
    revoked_ids = [
        credential["credential_id"] for credential in created[: min(revoke_count, count)]
    ]
    if revoked_ids:
        _post_json(client, root, "/credentials/revoke-batch", {"credential_ids": revoked_ids})

    verified = _post_json(
        client,
        root,
        "/verify-batch",
        {"credential_ids": [credential["credential_id"] for credential in created]},
    )["verified"]

    rejected = sum(1 for credential in verified if credential["result"] == "REJECT")
    accepted = sum(1 for credential in verified if credential["result"] == "ACCEPT")
    return {
        "created": len(created),
        "revoked": len(revoked_ids),
        "accepted": accepted,
        "rejected": rejected,
    }


def _post_json(client: Any, base_url: str, path: str, body: dict | None) -> Any:
    url = f"{base_url}{path}"
    response = client.post(url, json=body) if body else client.post(url)
    response.raise_for_status()
    return response.json()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed the local mock TSL server.")
    parser.add_argument(
        "--base-url",
        default=os.environ.get("STATUS_LIST_BASE_URL", DEFAULT_BASE_URL),
    )
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--revoke", type=int, default=DEFAULT_REVOKE_COUNT)
    parser.add_argument("--no-reset", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        with httpx.Client(timeout=10) as client:
            result = seed_server(
                client,
                base_url=args.base_url,
                count=args.count,
                prefix=args.prefix,
                revoke_count=args.revoke,
                reset=not args.no_reset,
            )
    except (httpx.HTTPError, ValueError) as exc:
        print(f"seed failed: {exc}", file=sys.stderr)
        print("start the server first: uvicorn app:app --reload", file=sys.stderr)
        return 1

    print(
        "seeded "
        f"{result['created']} credentials, "
        f"{result['revoked']} revoked, "
        f"{result['accepted']} accepted, "
        f"{result['rejected']} rejected"
    )
    print(f"open {args.base_url.rstrip('/')}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
