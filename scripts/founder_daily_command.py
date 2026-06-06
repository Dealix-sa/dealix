#!/usr/bin/env python3
"""Founder Daily Command — the one screen the founder reads each morning.

Reads the revenue pipeline, proof assets, target list, and customer workspaces,
then writes a prioritized command sheet to ``reports/founder/daily_command.md``.
See ``docs/founder/REVENUE_COMMAND_CENTER.md``.

Pure stdlib. Safe to run any time; it only reads data and writes a report.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PIPELINE = REPO / "data/revenue/pipeline.jsonl"
PROOF = REPO / "data/revenue/proof_assets.jsonl"
TARGETS = REPO / "data/growth/first_30_targets.csv"
CUSTOMERS = REPO / "customers"
OUT_DIR = REPO / "reports/founder"
OUT = OUT_DIR / "daily_command.md"

DISCLAIMER = "> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def main() -> int:
    pipeline = read_jsonl(PIPELINE)
    proof = read_jsonl(PROOF)

    won = [e for e in pipeline if str(e.get("status", "")).startswith("won")]
    cumulative = sum(int(e.get("amount_sar", 0)) for e in won)
    open_pipeline = sum(
        int(e.get("amount_sar", 0))
        for e in pipeline
        if e.get("stage") in {"offer_sent", "outreach_drafted"}
        and not str(e.get("status", "")).startswith("won")
    )
    pending_approval = [e for e in pipeline if e.get("status") == "pending_founder_approval"]
    capital_assets = [a for a in proof if a.get("capital_asset")]

    active_customers: list[str] = []
    if CUSTOMERS.is_dir():
        active_customers = sorted(
            p.name for p in CUSTOMERS.iterdir() if p.is_dir() and not p.name.startswith("_")
        )

    target_count = 0
    if TARGETS.is_file():
        with TARGETS.open(newline="", encoding="utf-8") as fh:
            target_count = sum(1 for _ in csv.DictReader(fh))

    # Recommended next action — priority order from the command center doc.
    if pending_approval:
        nxt = (
            f"Clear {len(pending_approval)} item(s) awaiting your approval "
            "(unblocks revenue). See each customer's 06_approval_register.md."
        )
    elif won:
        nxt = "Advance the furthest-along paid engagement to a Proof Pack (score ≥ 70)."
    elif any(e.get("stage") == "diagnostic_delivered" for e in pipeline):
        nxt = "Convert a delivered diagnostic into a 499 SAR Sprint offer."
    elif target_count:
        nxt = "Approve the next warm-intro draft from data/growth/first_30_targets.csv."
    else:
        nxt = "Seed the pipeline: pick a warm target and draft the first outreach."

    today = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: list[str] = []
    lines.append("# Founder Daily Command — أمر اليوم")
    lines.append("")
    lines.append(f"_Generated: {today} (Asia/Riyadh)_")
    lines.append("")
    lines.append("## The five numbers")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Cumulative revenue (SAR) | {cumulative:,} |")
    lines.append(f"| Open pipeline value (SAR) | {open_pipeline:,} |")
    lines.append(f"| Items awaiting approval | {len(pending_approval)} |")
    lines.append(f"| Active deliveries | {len(active_customers)} |")
    lines.append(f"| Proof Packs / Capital Assets | {len(capital_assets)} |")
    lines.append("")
    lines.append(f"_Targets in warm list: {target_count}_")
    lines.append("")
    lines.append("## Awaiting your approval (non-negotiable #8)")
    lines.append("")
    if pending_approval:
        for e in pending_approval:
            lines.append(
                f"- [ ] `{e.get('event_id', '?')}` {e.get('target_id', '?')} — "
                f"{e.get('stage', '?')} ({e.get('offer', '?')})"
            )
    else:
        lines.append("- Nothing queued. Clean board.")
    lines.append("")
    lines.append("## Active deliveries")
    lines.append("")
    if active_customers:
        for c in active_customers:
            lines.append(f"- `customers/{c}/` → check 07_next_action_board.md")
    else:
        lines.append("- No active customer workspaces yet.")
    lines.append("")
    lines.append("## ► Your one move today")
    lines.append("")
    lines.append(f"**{nxt}**")
    lines.append("")
    lines.append("## North-star (90-day)")
    lines.append("")
    lines.append("8–15K SAR MRR + 30–40K SAR one-time ≈ 40–55K SAR cumulative by day 90.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(DISCLAIMER)
    lines.append("")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(REPO)}")
    print(
        f"  revenue={cumulative} open={open_pipeline} "
        f"pending_approval={len(pending_approval)} "
        f"active={len(active_customers)} proof={len(capital_assets)}"
    )
    print(f"  next: {nxt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
