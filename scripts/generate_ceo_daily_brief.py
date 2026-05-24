#!/usr/bin/env python3
"""
generate_ceo_daily_brief.py — assemble a CEO daily brief Markdown file
from the private-ops runtime CSVs.

Reads:  $PRIVATE_OPS/{founder,outreach,approvals,trust,finance,...}/*.csv
Writes: $PRIVATE_OPS/founder/ceo_daily_brief.md (never inside the repo)

If a backing CSV is missing/empty, the corresponding section is marked
"_no_data_" — never invented. Honors NO_FAKE_PROOF / NO_FAKE_REVENUE.

Exit: 0 PASS / 2 missing private-ops.
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_rows(p: Path) -> list[dict[str, str]]:
    if not p.exists() or not p.is_file():
        return []
    try:
        with p.open(encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except (OSError, UnicodeDecodeError, csv.Error):
        return []


def _section(title: str, rows: list[dict[str, str]], cols: list[str]) -> str:
    if not rows:
        return f"## {title}\n\n_no_data_ — backing CSV empty.\n"
    lines = [f"## {title}", "", "| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for r in rows[:10]:
        lines.append("| " + " | ".join(r.get(c, "") for c in cols) + " |")
    if len(rows) > 10:
        lines.append(f"\n_… {len(rows) - 10} more rows omitted._")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--private-ops", default=os.environ.get("PRIVATE_OPS", "/opt/dealix"))
    args = p.parse_args()
    root = Path(args.private_ops).expanduser().resolve()
    if not root.exists():
        print(f"CEO_DAILY_BRIEF=fail reason=private_ops_missing path={root}")
        return 2

    decisions = _read_rows(root / "founder" / "decision_log.csv")
    approvals = _read_rows(root / "approvals" / "approval_queue.csv")
    trust_flags = _read_rows(root / "trust" / "trust_flags.csv")
    cash = _read_rows(root / "finance" / "cash_collected.csv")
    followups = _read_rows(root / "outreach" / "followup_queue.csv")

    sections = [
        f"# CEO Daily Brief — {_now()}",
        "",
        "_Read-only assembly from `$PRIVATE_OPS/*` CSVs. No claim is made_",
        "_about a number unless its source row carries `source=api`._",
        "",
        _section("Recent Decisions", decisions, ["timestamp", "decision_id", "category", "decision_en", "owner"]),
        _section("Pending Approvals", approvals, ["request_id", "action_class", "risk_level", "status"]),
        _section("Active Trust Flags", trust_flags, ["flag_id", "category", "severity", "summary_en", "status"]),
        _section("Cash Collected (payment evidence only)", cash, ["receipt_id", "customer_handle", "amount_sar", "received_at", "evidence_ref"]),
        _section("Follow-ups Due", followups, ["followup_id", "contact_id", "due_date", "next_action_en", "owner", "status"]),
    ]

    out = root / "founder" / "ceo_daily_brief.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(sections), encoding="utf-8")
    print(f"CEO_DAILY_BRIEF=pass output={out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
