#!/usr/bin/env python3
"""Run the living, multi-channel engagement loop (safe, draft-only).

Loads accounts + inbound events, drives the brain across channels, and writes
the engagement room report. Exits non-zero only if safety validation fails.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.commercial.engagement_engine import run_engagement, write_engagement_report

DATA_DIR = REPO_ROOT / "data" / "commercial"
REPORT_DIR = REPO_ROOT / "reports" / "commercial" / "engagement"


def _load(path: Path, key: str, default):
    if not path.exists():
        return default
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get(key, default) if isinstance(data, dict) else data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the commercial engagement loop")
    parser.add_argument("--accounts", default=str(DATA_DIR / "accounts.sample.json"))
    parser.add_argument("--inbound", default=str(DATA_DIR / "inbound_events.sample.json"))
    parser.add_argument("--icp-rules", default=str(DATA_DIR / "icp_rules.sample.json"))
    parser.add_argument("--client-rules", default=str(DATA_DIR / "client_rules.sample.json"))
    parser.add_argument("--out", default=str(REPORT_DIR))
    args = parser.parse_args(argv)

    accounts = _load(Path(args.accounts), "accounts", [])
    inbound = _load(Path(args.inbound), "inbound_by_account", {})
    icp = _load(Path(args.icp_rules), "", None)
    client_rules = _load(Path(args.client_rules), "", None)

    result = run_engagement(
        accounts, inbound_by_account=inbound, icp_rules=icp, client_rules=client_rules
    )

    if not result.safety_ok:
        print("COMMERCIAL_ENGAGEMENT_READY=0")
        print("SAFETY_VIOLATIONS=" + ";".join(result.safety_violations))
        return 1

    paths = write_engagement_report(result, args.out)
    print("COMMERCIAL_ENGAGEMENT_READY=1")
    print(f"ACCOUNTS={len(result.accounts)}")
    print(f"CONVERSATIONS={len(result.conversations)}")
    print(f"PAYLOADS={len(result.payloads)}")
    print(f"ACTIONS={len(result.action_plan)}")
    print(f"REPORT_JSON={paths['json']}")
    print(f"REPORT_MD={paths['md']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
