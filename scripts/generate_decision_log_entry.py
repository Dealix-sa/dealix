#!/usr/bin/env python3
"""generate_decision_log_entry.py.

Append a single founder decision to data/decision_log.jsonl. Append-only:
never overwrites existing lines. Prepends an ISO timestamp and uuid4 id.

This is the one script that writes by design, but only to the local repo.
No external network calls. No DB writes. No API calls.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG = REPO_ROOT / "data" / "decision_log.jsonl"

MAX_DECISION_LEN = 280


def _str2bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"true", "t", "yes", "y", "1"}:
        return True
    if lowered in {"false", "f", "no", "n", "0"}:
        return False
    raise argparse.ArgumentTypeError(f"invalid boolean value: {value!r}")


def build_entry(
    decision: str,
    context: str,
    alternatives: str,
    owner: str,
    reversible: bool,
    tags: list[str],
    *,
    now: datetime | None = None,
    entry_id: str | None = None,
) -> dict[str, Any]:
    timestamp = (now or datetime.now(timezone.utc)).isoformat()
    return {
        "id": entry_id or str(uuid.uuid4()),
        "timestamp": timestamp,
        "decision": decision,
        "context": context,
        "alternatives": alternatives,
        "owner": owner,
        "reversible": reversible,
        "tags": tags,
    }


def append_entry(path: Path, entry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def validate_decision(decision: str) -> str | None:
    if not decision or not decision.strip():
        return "decision must be non-empty"
    if len(decision) > MAX_DECISION_LEN:
        return f"decision must be <= {MAX_DECISION_LEN} chars (got {len(decision)})"
    return None


def _split_tags(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [t.strip() for t in raw.split(",") if t.strip()]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append a founder decision to the local decision log (JSONL).",
    )
    parser.add_argument("--decision", type=str, required=True, help="Decision text (<=280 chars).")
    parser.add_argument("--context", type=str, default="", help="Context behind the decision.")
    parser.add_argument(
        "--alternatives",
        type=str,
        default="",
        help="Alternatives considered.",
    )
    parser.add_argument("--owner", type=str, default="", help="Decision owner.")
    parser.add_argument(
        "--reversible",
        type=_str2bool,
        default=True,
        help="Whether the decision is reversible (default true).",
    )
    parser.add_argument("--tags", type=str, default="", help="Comma-separated tags.")
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_LOG,
        help="Path to decision log JSONL file.",
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        default=False,
        help="Print the entry without writing to disk.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    err = validate_decision(args.decision)
    if err is not None:
        print(f"error: {err}", file=sys.stderr)
        return 2

    entry = build_entry(
        decision=args.decision.strip(),
        context=args.context.strip(),
        alternatives=args.alternatives.strip(),
        owner=args.owner.strip(),
        reversible=bool(args.reversible),
        tags=_split_tags(args.tags),
    )

    if args.dry_run:
        sys.stdout.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
        return 0

    append_entry(args.out, entry)
    print(f"Appended decision {entry['id']} to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
