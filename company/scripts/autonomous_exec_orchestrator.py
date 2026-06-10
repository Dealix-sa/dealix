#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TODAY = dt.date.today().isoformat()

COMPANY = ROOT / "company"
FOUNDER = ROOT / "founder_os"

REPORTS = COMPANY / "reports"
OUTBOX = COMPANY / "outbox"
CRM = COMPANY / "crm"
DAILY = COMPANY / "daily"
LEAD_RESEARCH = COMPANY / "lead_research" / TODAY
FOUNDER_OUTPUT = FOUNDER / "output" / TODAY

REPORTS.mkdir(parents=True, exist_ok=True)
OUTBOX.mkdir(parents=True, exist_ok=True)
CRM.mkdir(parents=True, exist_ok=True)

def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

def load_text(path: Path, fallback: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else fallback

def capability_status() -> str:
    p = REPORTS / "CAPABILITY_CHECK.md"
    return load_text(p, "Capability check not generated.")

def collect_leads() -> list[dict[str, str]]:
    rows = []
    rows.extend(read_csv(LEAD_RESEARCH / "web_lead_research.csv"))
    rows.extend(read_csv(FOUNDER_OUTPUT / "daily_targets.csv"))
    return rows

def score_row(row: dict[str, str]) -> int:
    score = 50
    if row.get("phone"):
        score += 20
    if row.get("website") or row.get("link"):
        score += 10
    if row.get("recommended_offer") or row.get("core_offer"):
        score += 10
    if row.get("pain_angle"):
        score += 10
    try:
        score = max(score, int(float(row.get("priority_score", 0))))
    except Exception:
        pass
    return min(score, 100)

def build_approval_queue(leads: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row in leads[:50]:
        company = row.get("company_name") or row.get("title") or "Research Target"
        sector = row.get("segment") or row.get("sector") or ""
        offer = row.get("recommended_offer") or row.get("core_offer") or "Transformation Diagnostic Sprint"
        pain = row.get("pain_angle") or "تحتاج نظام تشغيل ومتابعة وتقارير"
        priority = score_row(row)

        rows.append({
            "date": TODAY,
            "company": company,
            "sector": sector,
            "contact": row.get("phone") or row.get("link") or row.get("website") or "",
            "channel": "manual_review",
            "offer": offer,
            "priority": priority,
            "pain_angle": pain,
            "draft_file": "",
            "status": "needs_review",
            "approved_by": "",
            "approved_at": "",
            "sent_at": "",
            "reply_status": "",
            "next_action": "approve_or_research_contact",
            "notes": row.get("snippet") or row.get("notes") or "",
        })

    rows.sort(key=lambda x: int(x["priority"]), reverse=True)
    return rows

def update_crm_from_queue(queue: list[dict[str, Any]]) -> None:
    crm_path = CRM / "pipeline.csv"
    fields = [
        "date","company","sector","contact","phone","email","source","offer",
        "status","next_action","next_followup_date","deal_value_sar","probability","notes"
    ]

    existing = read_csv(crm_path)
    seen = {r.get("company", "").strip().lower() for r in existing}

    for q in queue[:30]:
        key = q["company"].strip().lower()
        if key in seen:
            continue
        existing.append({
            "date": TODAY,
            "company": q["company"],
            "sector": q["sector"],
            "contact": q["contact"],
            "phone": q["contact"] if q["contact"].startswith("+") else "",
            "email": "",
            "source": "autonomous_exec_os",
            "offer": q["offer"],
            "status": "needs_review",
            "next_action": q["next_action"],
            "next_followup_date": "",
            "deal_value_sar": "",
            "probability": "10",
            "notes": q["pain_angle"],
        })

    write_csv(crm_path, existing, fields)

def build_ceo_report(queue: list[dict[str, Any]]) -> None:
    daily_offer_files = sorted(DAILY.glob("*_daily_offer.md"))
    daily_offer = load_text(daily_offer_files[-1], "No daily offer generated.") if daily_offer_files else "No daily offer generated."

    top = queue[:10]
    lines = [
        "# Dealix Autonomous CEO Daily Report",
        "",
        f"Date: {TODAY}",
        "",
        "## Status",
        "- Production check: see morning/company day output",
        f"- Leads collected: {len(queue)}",
        f"- Approval queue: {sum(1 for r in queue if r['status'] == 'needs_review')}",
        "",
        "## Top Targets Today",
        "| # | Company | Sector | Priority | Offer | Next Action |",
        "|---:|---|---|---:|---|---|",
    ]

    for i, r in enumerate(top, 1):
        lines.append(f"| {i} | {r['company']} | {r['sector']} | {r['priority']} | {r['offer']} | {r['next_action']} |")

    lines.extend([
        "",
        "## Daily Offer",
        "",
        daily_offer,
        "",
        "## Capability Snapshot",
        "",
        capability_status(),
        "",
        "## CEO Decisions Required",
        "1. Approve top 20 outreach drafts.",
        "2. Pick today’s primary segment.",
        "3. Move warm replies to discovery call.",
        "4. Push paid Diagnostic Sprint for qualified leads.",
        "",
        "## Hard Rule",
        "No external sending, invoicing, or contract commitment without founder approval.",
    ])

    (REPORTS / f"{TODAY}_AUTONOMOUS_CEO_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def build_weekly_report_if_monday(queue: list[dict[str, Any]]) -> None:
    if dt.date.today().weekday() != 0:
        return

    crm_rows = read_csv(CRM / "pipeline.csv")
    lines = [
        "# Dealix Autonomous Weekly Board Report",
        "",
        f"Generated: {TODAY}",
        "",
        "## Pipeline Snapshot",
        f"- CRM rows: {len(crm_rows)}",
        f"- New approval queue rows today: {len(queue)}",
        "",
        "## Segment Counts",
    ]

    counts: dict[str, int] = {}
    for r in crm_rows:
        counts[r.get("sector") or r.get("segment") or "unknown"] = counts.get(r.get("sector") or r.get("segment") or "unknown", 0) + 1

    for k, v in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"- {k}: {v}")

    lines.extend([
        "",
        "## Weekly CEO Focus",
        "- Close one paid Diagnostic Sprint.",
        "- Build one case study draft.",
        "- Keep production health green.",
        "- Classify security/deploy blockers.",
    ])

    (COMPANY / "weekly" / f"{TODAY}_WEEKLY_BOARD_REPORT.md").parent.mkdir(parents=True, exist_ok=True)
    (COMPANY / "weekly" / f"{TODAY}_WEEKLY_BOARD_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def main() -> None:
    leads = collect_leads()
    queue = build_approval_queue(leads)

    queue_fields = [
        "date","company","sector","contact","channel","offer","priority","pain_angle",
        "draft_file","status","approved_by","approved_at","sent_at","reply_status","next_action","notes"
    ]
    write_csv(OUTBOX / f"{TODAY}_approval_queue.csv", queue, queue_fields)
    update_crm_from_queue(queue)
    build_ceo_report(queue)
    build_weekly_report_if_monday(queue)

    print(REPORTS / f"{TODAY}_AUTONOMOUS_CEO_REPORT.md")
    print(OUTBOX / f"{TODAY}_approval_queue.csv")
    print(CRM / "pipeline.csv")

if __name__ == "__main__":
    main()
