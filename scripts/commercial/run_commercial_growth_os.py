#!/usr/bin/env python3
"""Run the full Dealix Commercial Growth OS v2 (safe, draft-only).

Loads sample/client accounts and replies, runs the orchestrator end to end,
writes the command-room reports, and prints a machine-readable status block.

Exits non-zero ONLY if safety validation fails (i.e. a live-send flag is set
when the OS expects the safe-by-default posture).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Make the repo root importable when run as a script.
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.commercial.orchestrator import run_growth_os, write_reports

DATA_DIR = REPO_ROOT / "data" / "commercial"
REPORT_DIR = REPO_ROOT / "reports" / "commercial" / "growth_os"


def _load_json(path: Path, key: str) -> list:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return data.get(key, [])
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Commercial Growth OS")
    parser.add_argument("--accounts", default=str(DATA_DIR / "accounts.sample.json"))
    parser.add_argument("--replies", default=str(DATA_DIR / "replies.sample.json"))
    parser.add_argument("--icp-rules", default=str(DATA_DIR / "icp_rules.sample.json"))
    parser.add_argument("--client-rules", default=str(DATA_DIR / "client_rules.sample.json"))
    parser.add_argument(
        "--pricing", default=str(DATA_DIR / "pricing_guardrails.sample.json")
    )
    parser.add_argument("--out", default=str(REPORT_DIR))
    args = parser.parse_args(argv)

    accounts = _load_json(Path(args.accounts), "accounts")
    replies = _load_json(Path(args.replies), "replies")
    icp_rules = (
        json.loads(Path(args.icp_rules).read_text(encoding="utf-8"))
        if Path(args.icp_rules).exists()
        else None
    )
    client_rules = (
        json.loads(Path(args.client_rules).read_text(encoding="utf-8"))
        if Path(args.client_rules).exists()
        else None
    )
    pricing = (
        json.loads(Path(args.pricing).read_text(encoding="utf-8"))
        if Path(args.pricing).exists()
        else None
    )

    result = run_growth_os(
        accounts,
        replies,
        icp_rules=icp_rules,
        client_rules=client_rules,
        pricing_guardrails=pricing,
    )

    if not result.safety_ok:
        print("COMMERCIAL_GROWTH_OS_READY=0")
        print("SAFETY_VIOLATIONS=" + ";".join(result.safety_violations))
        print(
            "Refusing to run: live-send flags must be disabled for the default "
            "draft-only OS run.",
            file=sys.stderr,
        )
        return 1

    paths = write_reports(result, args.out)
    counts = result.counts()

    print("COMMERCIAL_GROWTH_OS_READY=1")
    print(f"ACCOUNTS={counts['accounts']}")
    print(f"CARDS={counts['cards']}")
    print(f"REPLIES={counts['replies']}")
    print(f"BOOKING_OPTIONS={counts['booking_options']}")
    print(f"PROPOSALS={counts['proposals']}")
    print(f"FOLLOWUPS={counts['followups']}")
    print(f"DECISIONS_REQUIRED={counts['decisions_required']}")
    print(f"REPORT_JSON={paths['json']}")
    print(f"REPORT_MD={paths['md']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
