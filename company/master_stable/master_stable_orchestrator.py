#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TODAY = dt.date.today().isoformat()

REPORTS = ROOT / "company" / "reports"
OUTBOX = ROOT / "company" / "outbox"
CRM = ROOT / "company" / "crm"
RUNTIME = ROOT / "company" / "runtime" / TODAY

for directory in [REPORTS, OUTBOX, CRM, RUNTIME]:
    directory.mkdir(parents=True, exist_ok=True)

def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []

def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def collect_rows() -> list[dict[str, str]]:
    paths: list[Path] = []
    paths.extend(sorted((ROOT / "company" / "lead_research").glob("*/web_lead_research.csv"))[-3:])
    paths.extend(sorted((ROOT / "founder_os" / "output").glob("*/daily_targets.csv"))[-3:])

    rows: list[dict[str, str]] = []
    for path in paths:
        for row in read_csv(path):
            row["_source_file"] = str(path)
            rows.append(row)
    return rows

def get(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value:
            return str(value).strip()
    return ""

def score(row: dict[str, str]) -> int:
    value = 40

    if get(row, "phone", "contact"):
        value += 20
    if get(row, "website", "link"):
        value += 15
    if get(row, "pain_angle", "notes", "snippet"):
        value += 15
    if get(row, "recommended_offer", "core_offer", "offer"):
        value += 10

    try:
        value = max(value, int(float(get(row, "priority_score") or 0)))
    except Exception:
        pass

    return min(value, 100)

def normalize(row: dict[str, str]) -> dict[str, str]:
    company = get(row, "company_name", "company", "title") or "Research Target"
    sector = get(row, "segment", "sector") or "general"
    contact = get(row, "phone", "website", "link", "contact")
    offer = get(row, "recommended_offer", "core_offer", "offer") or "Transformation Diagnostic Sprint"
    pain = get(row, "pain_angle", "notes", "snippet") or "تحتاج نظام متابعة وتقارير أوضح"

    return {
        "date": TODAY,
        "company": company,
        "sector": sector,
        "contact": contact,
        "offer": offer,
        "priority": str(score(row)),
        "pain_angle": pain,
        "status": "needs_review",
        "next_action": "review_and_send_manually",
        "notes": get(row, "_source_file"),
    }

def build_queue() -> list[dict[str, str]]:
    rows = [normalize(row) for row in collect_rows()]

    if not rows:
        rows = [
            {
                "date": TODAY,
                "company": "Manual Research Target",
                "sector": "clinics",
                "contact": "",
                "offer": "Transformation Diagnostic Sprint",
                "priority": "50",
                "pain_angle": "لا توجد leads مولدة اليوم؛ ابدأ ببحث يدوي أو شغل company day",
                "status": "needs_review",
                "next_action": "run_company_day_or_add_manual_targets",
                "notes": "fallback",
            }
        ]

    rows.sort(key=lambda row: int(row["priority"]), reverse=True)
    return rows

def update_crm(queue: list[dict[str, str]]) -> None:
    path = CRM / "pipeline.csv"
    fields = [
        "date", "company", "sector", "contact", "phone", "email", "source",
        "offer", "status", "next_action", "next_followup_date",
        "deal_value_sar", "probability", "notes",
    ]

    existing = read_csv(path)
    seen = {get(row, "company").lower() for row in existing}

    for item in queue[:30]:
        key = item["company"].lower()
        if key in seen:
            continue

        existing.append({
            "date": TODAY,
            "company": item["company"],
            "sector": item["sector"],
            "contact": item["contact"],
            "phone": item["contact"] if item["contact"].startswith("+") else "",
            "email": "",
            "source": "master_stable_os",
            "offer": item["offer"],
            "status": "needs_review",
            "next_action": item["next_action"],
            "next_followup_date": "",
            "deal_value_sar": "",
            "probability": "10",
            "notes": item["pain_angle"],
        })

    write_csv(path, existing, fields)

def write_report(queue: list[dict[str, str]]) -> None:
    lines = [
        "# Dealix Master Stable CEO Report",
        "",
        f"Date: {TODAY}",
        "",
        "## Executive Summary",
        f"- Approval queue rows: {len(queue)}",
        "- External sending: manual approval required",
        "- Primary commercial objective: sell one paid Diagnostic Sprint",
        "",
        "## Top 20 Targets",
        "| # | Company | Sector | Priority | Offer | Next Action |",
        "|---:|---|---|---:|---|---|",
    ]

    for index, item in enumerate(queue[:20], start=1):
        lines.append(
            f"| {index} | {item['company']} | {item['sector']} | {item['priority']} | {item['offer']} | {item['next_action']} |"
        )

    lines.extend([
        "",
        "## Founder Actions",
        "1. Review the approval queue.",
        "2. Send top 20 messages manually.",
        "3. Book discovery calls.",
        "4. Push Diagnostic Sprint to warm replies.",
        "5. Update CRM status.",
        "",
        "## Diagnostic Sprint Close",
        "التشخيص يكون خلال 3-7 أيام، ومخرجاته: خريطة سير العمل، نقاط التسرب، KPI model، أول نظام مقترح، وعرض تنفيذ واضح. القيمة تبدأ من 7,500 ريال.",
    ])

    report_path = REPORTS / f"{TODAY}_MASTER_STABLE_CEO_REPORT.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def main() -> None:
    queue = build_queue()

    queue_fields = [
        "date", "company", "sector", "contact", "offer", "priority",
        "pain_angle", "status", "next_action", "notes",
    ]

    queue_path = OUTBOX / f"{TODAY}_master_stable_approval_queue.csv"
    write_csv(queue_path, queue, queue_fields)
    update_crm(queue)
    write_report(queue)

    print(f"CEO report: {REPORTS / (TODAY + '_MASTER_STABLE_CEO_REPORT.md')}")
    print(f"Approval queue: {queue_path}")
    print(f"CRM: {CRM / 'pipeline.csv'}")

if __name__ == "__main__":
    main()
