#!/usr/bin/env python3
"""List or delete LangSmith feedback records with tight filters."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List or delete LangSmith feedback records for an experiment/project."
    )
    parser.add_argument("--session-id", required=True, help="LangSmith experiment/project UUID.")
    parser.add_argument("--key", required=True, help="Feedback key, for example correctness.")
    parser.add_argument(
        "--source",
        default="auto_eval",
        help="Feedback source filter. Defaults to auto_eval.",
    )
    parser.add_argument("--rule-id", help="Only include feedback from this evaluator/run rule ID.")
    parser.add_argument("--created-after", help="Only include feedback created at/after this time.")
    parser.add_argument("--created-before", help="Only include feedback created at/before this time.")
    parser.add_argument(
        "--comment-contains",
        help="Only include feedback whose comment contains this substring, case-insensitive.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Page size for LangSmith feedback API. Defaults to 100.",
    )
    parser.add_argument(
        "--confirm-delete",
        action="store_true",
        help="Actually delete matching records. Without this, the script only lists matches.",
    )
    parser.add_argument(
        "--show-comments",
        action="store_true",
        help="Print full comments instead of a short preview.",
    )
    return parser.parse_args()


def request_json(url: str, api_key: str, timeout: int = 20) -> Any:
    request = urllib.request.Request(url, headers={"x-api-key": api_key})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def delete_feedback(base_url: str, api_key: str, feedback_id: str) -> str:
    request = urllib.request.Request(
        f"{base_url}/api/v1/feedback/{feedback_id}",
        headers={"x-api-key": api_key},
        method="DELETE",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            response.read()
        return "deleted"
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return "already_deleted"
        raise


def source_metadata(row: dict[str, Any]) -> dict[str, Any]:
    source = row.get("feedback_source")
    if not isinstance(source, dict):
        return {}
    metadata = source.get("metadata")
    return metadata if isinstance(metadata, dict) else {}


def matches_local_filters(row: dict[str, Any], args: argparse.Namespace) -> bool:
    if args.rule_id:
        metadata = source_metadata(row)
        if metadata.get("rule_id") != args.rule_id:
            return False

    if args.comment_contains:
        comment = row.get("comment")
        if not isinstance(comment, str):
            return False
        if args.comment_contains.lower() not in comment.lower():
            return False

    return True


def fetch_feedback(base_url: str, api_key: str, args: argparse.Namespace) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    offset = 0

    while True:
        params: dict[str, Any] = {
            "session": args.session_id,
            "key": args.key,
            "source": args.source,
            "limit": args.limit,
            "offset": offset,
        }
        if args.created_after:
            params["min_created_at"] = args.created_after
        if args.created_before:
            params["max_created_at"] = args.created_before

        query = urllib.parse.urlencode(params)
        page = request_json(f"{base_url}/api/v1/feedback?{query}", api_key)
        if not isinstance(page, list):
            raise TypeError(f"Expected feedback list, got {type(page).__name__}")

        rows.extend(row for row in page if isinstance(row, dict))
        if len(page) < args.limit:
            break
        offset += args.limit

    deduped = {row["id"]: row for row in rows if isinstance(row.get("id"), str)}
    return [row for row in deduped.values() if matches_local_filters(row, args)]


def print_rows(rows: list[dict[str, Any]], args: argparse.Namespace) -> None:
    for index, row in enumerate(rows, start=1):
        metadata = source_metadata(row)
        comment = row.get("comment") or ""
        if not args.show_comments and isinstance(comment, str) and len(comment) > 160:
            comment = f"{comment[:160]}..."
        print(
            json.dumps(
                {
                    "index": index,
                    "id": row.get("id"),
                    "run_id": row.get("run_id"),
                    "score": row.get("score"),
                    "value": row.get("value"),
                    "created_at": row.get("created_at"),
                    "source": (row.get("feedback_source") or {}).get("type")
                    if isinstance(row.get("feedback_source"), dict)
                    else None,
                    "source_metadata": metadata,
                    "comment": comment,
                },
                ensure_ascii=True,
            )
        )


def main() -> int:
    args = parse_args()
    api_key = os.environ.get("LANGSMITH_API_KEY")
    if not api_key:
        print("LANGSMITH_API_KEY is required.", file=sys.stderr)
        return 2

    base_url = os.environ.get("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com").rstrip("/")
    rows = fetch_feedback(base_url, api_key, args)

    print(
        f"Matched {len(rows)} feedback records "
        f"session={args.session_id} key={args.key} source={args.source}"
    )
    print_rows(rows, args)

    if not args.confirm_delete:
        print("Dry run only. Re-run with --confirm-delete to delete these records.")
        return 0

    deleted = 0
    already_deleted = 0
    errors: list[tuple[str, str]] = []
    for row in rows:
        feedback_id = row["id"]
        try:
            result = delete_feedback(base_url, api_key, feedback_id)
            if result == "deleted":
                deleted += 1
            else:
                already_deleted += 1
            print(f"{result} {feedback_id}", flush=True)
            time.sleep(0.05)
        except Exception as error:  # noqa: BLE001 - preserve exact failure text for audit.
            errors.append((feedback_id, repr(error)))
            print(f"ERROR {feedback_id}: {error!r}", flush=True)

    remaining = fetch_feedback(base_url, api_key, args)
    print(
        f"Deleted {deleted}; already_deleted={already_deleted}; "
        f"errors={len(errors)}; remaining={len(remaining)}"
    )
    if errors:
        print(json.dumps(errors, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
