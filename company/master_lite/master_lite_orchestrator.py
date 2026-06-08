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

for p in [REPORTS, OUTBOX, CRM, RUNTIME]:
    p.mkdir(parents=True, exist_ok=True)

def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

def collect_sources() -> list[dict[str, str]]:
    sources: list[Path] = []
    sources += list((ROOT / "company" / "lead_research").glob("*/web_lead_research.csv"))
    sources += list((ROOT / "founder_os" / "output").glob("*/daily_targets.csv"))

    rows: list[dict[str, str]] = []
    for src in sources[-5:]:
        for r in read_csv(src):
            r["_source_file"] = str(src)
            rows.append(r)
    return rows

def score(row: dict[str, str]) -> int:
    s = 40
    if row.get("phone") or row.get("contact"):
        s += 20
    if row.get("website") or row.get("link"):
        s += 15
    if row.get("pain_angle"):
        s += 15
    if row.get("recommended_offer") or row.get("core_offer"):
        s += 10
    try:
        s = max(s, int(float(row.get("priority_score", "0") or 0)))
    except Exception:
        pass
    return min(s, 100)

def normalize(row: dict[str, str]) -> dict[str, str]:
    company = row.get("company_name") or row.get("title") or "Research Target"
    sector = row.get("segment") or row.get("sector") or ""
    offer = row.get("recommended_offer") or row.get("core_offer") or "Transformation Diagnostic Sprint"
    pain = row.get("pain_angle") or "تحتاج نظام تشغيل للمتابعة والتقارير"
    contact = row.get("phone") or row.get("website") or row.get("link") or row.get("contact") or ""

    return {
        "date": TODAY,
        "company": company,
        "sector": sector,
        "contact": contact,
        "offer": offer,
        "priority": str(score(row)),
        "pain_angle": pain,
        "status": "needs_review",
        "next_action": "review_contact_and_send_manually",
        "notes": row.get("snippet") or row.get("notes") or "",
    }

def ensure_crm(queue: list[dict[str, str]]) -> None:
    path = CRM / "pipeline.csv"
    fields = [
        "date","company","sector","contact","phone","email","source","offer",
        "status","next_action","next_followup_date","deal_value_sar","probability","notes"
    ]

    existing = read_csv(path)
    seen = {r.get("company","").strip().lower() for r in existing}

    for q in queue[:25]:
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
            "source": "master_lite_os",
            "offer": q["offer"],
            "status": "needs_review",
            "next_action": q["next_action"],
            "next_followup_date": "",
            "deal_value_sar": "",
            "probability": "10",
            "notes": q["pain_angle"],
        })

    write_csv(path, existing, fields)

def build_report(queue: list[dict[str, str]]) -> None:
    lines = [
        "# Dealix Master Lite CEO Report",
        "",
        f"Date: {TODAY}",
        "",
        "## Executive Summary",
        f"- Approval queue generated: {len(queue)}",
        "- External sending: manual approval required",
        "- Primary offer to push: Transformation Diagnostic Sprint",
        "",
        "## Top Targets",
        "| # | Company | Sector | Priority | Offer | Next Action |",
        "|---:|---|---|---:|---|---|",
    ]

    for i, r in enumerate(queue[:20], 1):
        lines.append(
            f"| {i} | {r['company']} | {r['sector']} | {r['priority']} | {r['offer']} | {r['next_action']} |"
        )

    lines += [
        "",
        "## Founder Actions Today",
        "1. Review top 20 rows in approval queue.",
        "2. Send messages manually.",
        "3. Push Diagnostic Sprint to warm replies.",
        "4. Update CRM statuses.",
        "5. Do not send bulk messages automatically.",
        "",
        "## Diagnostic Sprint Close",
        "التشخيص يكون خلال 3-7 أيام، ومخرجاته: خريطة سير العمل، نقاط التسرب، KPI model، أول نظام مقترح، وعرض تنفيذ واضح. القيمة تبدأ من 7,500 ريال.",
    ]

    report_path = REPORTS / f"{TODAY}_MASTER_LITE_CEO_REPORT.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def main() -> None:
    rows = collect_sources()
    queue = [normalize(r) for r in rows]
    queue.sort(key=lambda r: int(r["priority"]), reverse=True)

    if not queue:
        queue = [
            {
                "date": TODAY,
                "company": "Manual Research Target",
                "sector": "clinics",
                "contact": "",
                "offer": "Transformation Diagnostic Sprint",
                "priority": "50",
                "pain_angle": "تحتاج بحث يدوي اليوم",
                "status": "needs_review",
                "next_action": "find_public_contact",
                "notes": "No generated leads found.",
            }
        ]

    queue_fields = ["date","company","sector","contact","offer","priority","pain_angle","status","next_action","notes"]
    queue_path = OUTBOX / f"{TODAY}_master_lite_approval_queue.csv"
    write_csv(queue_path, queue, queue_fields)
    ensure_crm(queue)
    build_report(queue)

    print(f"CEO report: {REPORTS / (TODAY + '_MASTER_LITE_CEO_REPORT.md')}")
    print(f"Approval queue: {queue_path}")
    print(f"CRM: {CRM / 'pipeline.csv'}")

if __name__ == "__main__":
    main()
