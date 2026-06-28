#!/usr/bin/env python3
"""Build the command-room snapshot and write latest.json / latest.md."""
from __future__ import annotations

from _common import DATA_DIR, REPORT_DIR, dump, load_json

from app.commercial.orchestrator import run_growth_os, write_reports


def main() -> int:
    accounts = load_json(DATA_DIR / "accounts.sample.json", key="accounts")
    replies = load_json(DATA_DIR / "replies.sample.json", key="replies")
    icp = load_json(DATA_DIR / "icp_rules.sample.json")
    pricing = load_json(DATA_DIR / "pricing_guardrails.sample.json")
    result = run_growth_os(accounts, replies, icp_rules=icp, pricing_guardrails=pricing)
    if not result.safety_ok:
        dump({"safety_ok": False, "violations": result.safety_violations})
        return 1
    paths = write_reports(result, REPORT_DIR)
    dump({"safety_ok": True, "paths": paths, "counts": result.counts()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
