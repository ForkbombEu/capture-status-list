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
    rich: bool = False,
) -> dict[str, int]:
    if count < 1:
        raise ValueError("count must be at least 1")
    if revoke_count < 0:
        raise ValueError("revoke count cannot be negative")

    root = base_url.rstrip("/")
    if reset:
        _post_json(client, root, "/reset", None)

    if rich:
        return _seed_rich(client, root, prefix)

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
    return _seed_counts(created, revoked_ids, verified)


def _seed_rich(client: Any, root: str, prefix: str) -> dict[str, int]:
    profiles = [
        ("EU", "eu.europa.ec.eudi.pid.1", "2099-12-31", 8, (0, 1), (0, 1, 2, 3)),
        ("DE", "org.iso.18013.5.1.mDL", "2099-12-31", 6, (0,), (1, 2)),
        ("PT", "eu.europa.ec.eudi.ehic.1", "2099-12-31", 5, (), (0, 1)),
        ("NL", "org.iso.23220.2.photoid.1", "2099-12-31", 5, (4,), (),),
    ]
    created: list[dict] = []
    revoked_ids: list[str] = []
    verified_ids: list[str] = []
    for country, doctype, expiry, count, revoke_positions, verify_positions in profiles:
        batch = _post_json(
            client,
            root,
            "/credentials/random-batch",
            {
                "count": count,
                "prefix": f"{prefix}-{country.lower()}",
                "country": country,
                "doctype": doctype,
                "expiry_date": expiry,
            },
        )
        profile_created = batch["created"]
        created.extend(profile_created)
        revoked_ids.extend(
            profile_created[position]["credential_id"] for position in revoke_positions
        )
        verified_ids.extend(
            profile_created[position]["credential_id"] for position in verify_positions
        )

    if revoked_ids:
        _post_json(client, root, "/credentials/revoke-batch", {"credential_ids": revoked_ids})
    verified = []
    if verified_ids:
        verified = _post_json(
            client, root, "/verify-batch", {"credential_ids": verified_ids}
        )["verified"]

    summaries = _get_json(client, root, "/debug/status-lists")
    expired = next(summary for summary in summaries if summary["country"] == "DE")
    _post_json(
        client,
        root,
        "/debug/status-lists/expire",
        {"uri": expired["status_list_uri"], "expiry_date": "2020-01-01"},
    )
    return _seed_counts(created, revoked_ids, verified)


def _seed_counts(
    created: list[dict], revoked_ids: list[str], verified: list[dict]
) -> dict[str, int]:
    return {
        "created": len(created),
        "revoked": len(revoked_ids),
        "accepted": sum(credential["result"] == "ACCEPT" for credential in verified),
        "rejected": sum(credential["result"] == "REJECT" for credential in verified),
    }


def _get_json(client: Any, base_url: str, path: str) -> Any:
    response = client.get(f"{base_url}{path}")
    response.raise_for_status()
    return response.json()


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
    parser.add_argument(
        "--simple",
        action="store_true",
        help="seed one legacy batch instead of the rich multi-pool fixture",
    )
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
                rich=not args.simple,
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
