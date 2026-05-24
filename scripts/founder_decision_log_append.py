#!/usr/bin/env python3
"""Append a decision to the PRIVATE_OPS decision log JSONL.

Schema validated locally; record is enriched with a UUID and ISO timestamp
by `dealix.private_ops.write_jsonl_append`. PRIVATE_OPS off → exit 0 with the
standard bilingual note (no record written).
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.private_ops import is_enabled, missing_private_ops_note, write_jsonl_append  # noqa: E402

VALID_TYPES = {
    "bet", "cut", "delegate", "hire", "automate",
    "pricing", "partnership", "policy", "other",
}
VALID_STATUS = {"pending", "executing", "done", "reversed"}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--decision", required=True, help="One sentence, present tense")
    p.add_argument("--type", required=True, choices=sorted(VALID_TYPES))
    p.add_argument("--owner", required=True)
    p.add_argument("--reversible", action="store_true")
    p.add_argument("--expected-outcome", default=None)
    p.add_argument("--kill-trigger", default=None)
    p.add_argument("--assumption-ids", nargs="*", default=[])
    p.add_argument("--links", nargs="*", default=[])
    p.add_argument("--supersedes", default=None)
    p.add_argument("--status", default="pending", choices=sorted(VALID_STATUS))
    p.add_argument("--id", default=None, help="Override the generated UUID")
    args = p.parse_args()

    if not is_enabled():
        print(missing_private_ops_note("en"))
        print("DECISION_LOG_VERDICT=SKIPPED_PRIVATE_OPS_OFF")
        return 0

    record = {
        "id": args.id or str(uuid.uuid4()),
        "decision": args.decision,
        "type": args.type,
        "owner": args.owner,
        "reversible": bool(args.reversible),
        "status": args.status,
    }
    if args.expected_outcome:
        record["expected_outcome"] = args.expected_outcome
    if args.kill_trigger:
        record["kill_trigger"] = args.kill_trigger
    if args.assumption_ids:
        record["assumption_ids"] = args.assumption_ids
    if args.links:
        record["links"] = args.links
    if args.supersedes:
        record["supersedes"] = args.supersedes

    target = write_jsonl_append("ceo/decisions.jsonl", record)
    print(json.dumps({
        "appended_id": record["id"],
        "recorded_at": datetime.now(UTC).isoformat(),
        "path": str(target),
    }, ensure_ascii=False, indent=2))
    print("DECISION_LOG_VERDICT=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
