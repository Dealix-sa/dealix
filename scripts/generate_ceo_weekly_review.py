#!/usr/bin/env python3
"""
generate_ceo_weekly_review.py — assemble a CEO weekly review Markdown
from $PRIVATE_OPS CSVs. Pairs with the daily brief.

Writes: $PRIVATE_OPS/founder/ceo_weekly_review.md
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


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
        return f"## {title}\n\n_no_data_\n"
    lines = [f"## {title}", "", "| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for r in rows[:15]:
        lines.append("| " + " | ".join(r.get(c, "") for c in cols) + " |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--private-ops", default=os.environ.get("PRIVATE_OPS", "/opt/dealix"))
    args = p.parse_args()
    root = Path(args.private_ops).expanduser().resolve()
    if not root.exists():
        print(f"CEO_WEEKLY_REVIEW=fail reason=private_ops_missing path={root}")
        return 2

    sections = [
        f"# CEO Weekly Review — {_now()}",
        "",
        "Per `dealix/execution_assurance/registry.yaml` — the 6 weekly CEO questions:",
        "",
        "1. Did qualified leads arrive and from where?",
        "2. Are stages + scores accurate vs human review sample?",
        "3. Meetings / scopes / invoices / paid volumes?",
        "4. Where is the funnel stuck?",
        "5. Top support intents + objections?",
        "6. Any high-risk outbound attempt auto-blocked?",
        "",
        _section("Accounts", _read_rows(root / "graph" / "accounts.csv"),
                 ["account_id", "handle", "sector", "size_band", "source", "last_signal"]),
        _section("Signals", _read_rows(root / "graph" / "signals.csv"),
                 ["signal_id", "account_id", "type", "source", "captured_at"]),
        _section("Strategic Accounts", _read_rows(root / "market_attack" / "strategic_accounts.csv"),
                 ["account_handle", "sector", "score", "stage", "owner", "next_action_en"]),
        _section("Client Health", _read_rows(root / "customer_success" / "client_health.csv"),
                 ["customer_handle", "delivery_score", "engagement_score", "expansion_score", "risk_flags", "as_of"]),
        _section("Hypergrowth Metrics", _read_rows(root / "metrics" / "hypergrowth_metrics.csv"),
                 ["metric_id", "name", "value", "unit", "source", "captured_at", "is_estimate"]),
    ]
    out = root / "founder" / "ceo_weekly_review.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(sections), encoding="utf-8")
    print(f"CEO_WEEKLY_REVIEW=pass output={out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
