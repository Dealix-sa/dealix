#!/usr/bin/env python3
"""Founder Daily Command — generate the daily revenue-to-proof brief (Wave 6).

Reads the Wave 6 ledgers (tolerating empty files) and renders a single-screen
founder brief. No external sends — output is written to a markdown file the
founder reads and acts on manually.

Inputs (all optional / may be empty):
  - data/revenue/pipeline.jsonl
  - data/revenue/outreach_queue.jsonl
  - data/revenue/diagnostics.jsonl
  - data/revenue/offers.jsonl
  - data/revenue/payments.jsonl
  - data/revenue/upsells.jsonl
  - data/customers/customer_health.jsonl
  - reports/launch/launch_blockers.md (if it exists)

Output:
  reports/founder/daily_command.md  (or --out / --format json)

Usage:
  python scripts/founder_daily_command.py
  python scripts/founder_daily_command.py --format json
  python scripts/founder_daily_command.py --out -   # stdout

Reference: docs/05_founder/REVENUE_COMMAND_CENTER.md
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

LEDGERS = {
    "pipeline": "data/revenue/pipeline.jsonl",
    "outreach": "data/revenue/outreach_queue.jsonl",
    "diagnostics": "data/revenue/diagnostics.jsonl",
    "offers": "data/revenue/offers.jsonl",
    "payments": "data/revenue/payments.jsonl",
    "upsells": "data/revenue/upsells.jsonl",
    "customer_health": "data/customers/customer_health.jsonl",
}
LAUNCH_BLOCKERS = "reports/launch/launch_blockers.md"


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _load_jsonl(rel: str) -> list[dict]:
    path = REPO_ROOT / rel
    if not path.is_file():
        return []
    records: list[dict] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"WARN: skipping invalid JSON in {rel}:{i}: {exc}", file=sys.stderr)
            continue
        if isinstance(obj, dict):
            records.append(obj)
    return records


def _is_due(rec: dict, today: str) -> bool:
    due = str(rec.get("due_date", "") or "")
    return bool(due) and due <= today


def build_brief() -> dict:
    today = _today()
    data = {key: _load_jsonl(rel) for key, rel in LEDGERS.items()}

    pipeline = data["pipeline"]
    outreach = data["outreach"]
    diagnostics = data["diagnostics"]
    offers = data["offers"]
    upsells = data["upsells"]

    outreach_due = [
        r for r in outreach
        if r.get("approval_status") == "approved" and r.get("stage") != "sent"
    ] or [r for r in outreach if _is_due(r, today)]

    diagnostics_due = [
        r for r in diagnostics if r.get("outcome") in (None, "", "command_sprint_offer") and _is_due(r, today)
    ]

    offers_pending = [
        r for r in offers if str(r.get("payment_status", "unpaid")) not in ("paid",)
    ]

    active_deliveries = [
        r for r in pipeline if r.get("stage") in ("delivery_started", "proof_pack_delivered")
    ]

    proof_events = [r for r in pipeline if r.get("stage") == "proof_pack_delivered"]

    upsell_opps = [
        r for r in upsells if r.get("recommended_upsell") not in (None, "", "none")
    ]

    blockers: list[str] = []
    lb_path = REPO_ROOT / LAUNCH_BLOCKERS
    if lb_path.is_file():
        blockers.append(f"See {LAUNCH_BLOCKERS}")
    blockers += [
        f"{r.get('company', '?')}: {r.get('risk')}" for r in pipeline if r.get("risk")
    ]

    # Top 5 founder actions: prioritise approved outreach, due diagnostics, pending offers.
    actions: list[str] = []
    for r in outreach_due[:2]:
        actions.append(f"Send approved message to {r.get('company', '?')} (manual).")
    for r in diagnostics_due[:1]:
        actions.append(f"Run/close diagnostic for {r.get('company', '?')}.")
    for r in offers_pending[:1]:
        actions.append(f"Follow up offer for {r.get('company', '?')}.")
    for r in upsell_opps[:1]:
        actions.append(f"Offer {r.get('recommended_upsell')} to {r.get('company', '?')}.")
    if not actions:
        actions.append("Research First 30 Targets — add evidence_url and score (see playbook).")
    actions = actions[:5]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": today,
        "counts": {k: len(v) for k, v in data.items()},
        "outreach_due": outreach_due,
        "diagnostics_due": diagnostics_due,
        "offers_pending": offers_pending,
        "active_deliveries": active_deliveries,
        "proof_events": proof_events,
        "upsell_opportunities": upsell_opps,
        "blockers": blockers,
        "top_actions": actions,
    }


def _li(items: list[str]) -> list[str]:
    return [f"- {x}" for x in items] if items else ["- (none / لا شيء)"]


def render_md(brief: dict) -> str:
    c = brief["counts"]
    lines = [
        "# Founder Daily Command — أمر المؤسس اليومي",
        "",
        f"Generated: {brief['generated_at']}  ·  Date: {brief['date']}",
        "",
        "> No auto-send · every external message is manual and founder-approved.",
        "> Schema: docs/05_founder/REVENUE_COMMAND_CENTER.md",
        "",
        "## 1. Today's revenue focus / تركيز اليوم",
        f"- Pipeline: {c['pipeline']} · Offers: {c['offers']} · Payments: {c['payments']} · Upsells: {c['upsells']}",
        "",
        "## 2. Outreach due / تواصل مستحق (approved only)",
        *_li([f"{r.get('company', '?')} — {r.get('cta', r.get('next_action', ''))}" for r in brief["outreach_due"]]),
        "",
        "## 3. Diagnostics due / تشخيصات مستحقة",
        *_li([f"{r.get('company', '?')} — due {r.get('due_date', '?')}" for r in brief["diagnostics_due"]]),
        "",
        "## 4. Offers pending / عروض معلّقة",
        *_li([f"{r.get('company', '?')} — {r.get('price_sar', '?')} SAR ({r.get('payment_status', 'unpaid')})" for r in brief["offers_pending"]]),
        "",
        "## 5. Active deliveries / تسليمات نشطة",
        *_li([f"{r.get('company', '?')} — {r.get('stage', '?')}" for r in brief["active_deliveries"]]),
        "",
        "## 6. Proof events / أحداث الإثبات",
        *_li([f"{r.get('company', '?')}" for r in brief["proof_events"]]),
        "",
        "## 7. Upsell opportunities / فرص التوسعة",
        *_li([f"{r.get('company', '?')} — {r.get('recommended_upsell')}" for r in brief["upsell_opportunities"]]),
        "",
        "## 8. Blockers / معوّقات",
        *_li(brief["blockers"]),
        "",
        "## 9. Top 5 founder actions / أهم 5 إجراءات",
        *[f"{i}. {a}" for i, a in enumerate(brief["top_actions"], 1)],
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--format", choices=("md", "json"), default="md")
    p.add_argument("--out", default="reports/founder/daily_command.md",
                   help="output path; '-' for stdout (default: reports/founder/daily_command.md)")
    args = p.parse_args()

    brief = build_brief()
    content = json.dumps(brief, ensure_ascii=False, indent=2) if args.format == "json" else render_md(brief)

    if args.out == "-":
        print(content)
        return 0

    out_path = REPO_ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content + ("\n" if not content.endswith("\n") else ""), encoding="utf-8")
    print(f"OK: wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
