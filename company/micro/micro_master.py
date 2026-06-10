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

for d in (REPORTS, OUTBOX, CRM):
    d.mkdir(parents=True, exist_ok=True)

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
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

def pick(value: dict[str, str], *keys: str) -> str:
    for k in keys:
        v = value.get(k)
        if v:
            return str(v).strip()
    return ""

def score(row: dict[str, str]) -> int:
    s = 40
    if pick(row, "phone", "contact"):
        s += 20
    if pick(row, "website", "link"):
        s += 15
    if pick(row, "pain_angle", "snippet", "notes"):
        s += 15
    if pick(row, "recommended_offer", "core_offer", "offer"):
        s += 10
    try:
        s = max(s, int(float(pick(row, "priority_score") or 0)))
    except Exception:
        pass
    return min(s, 100)

def collect() -> list[dict[str, str]]:
    paths = []
    paths += sorted((ROOT / "company" / "lead_research").glob("*/web_lead_research.csv"))[-3:]
    paths += sorted((ROOT / "founder_os" / "output").glob("*/daily_targets.csv"))[-3:]
    rows = []
    for p in paths:
        for r in read_csv(p):
            r["_source"] = str(p)
            rows.append(r)
    return rows

def normalize(row: dict[str, str]) -> dict[str, str]:
    company = pick(row, "company_name", "company", "title") or "Manual Research Target"
    sector = pick(row, "segment", "sector") or "general"
    contact = pick(row, "phone", "website", "link", "contact")
    offer = pick(row, "recommended_offer", "core_offer", "offer") or "Transformation Diagnostic Sprint"
    pain = pick(row, "pain_angle", "snippet", "notes") or "تحتاج نظام متابعة وتقارير أوضح"
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
    }

def fallback_rows() -> list[dict[str, str]]:
    sectors = [
        ("عيادات ومراكز طبية", "WhatsApp Revenue OS", "الاستفسارات والحجوزات تضيع في واتساب"),
        ("مراكز تدريب", "Growth Engine OS", "استفسارات الدورات تحتاج متابعة وتسجيل"),
        ("وكالات تسويق", "Client Command Center OS", "تقارير العملاء والمهام متفرقة"),
        ("مطاعم وكافيهات", "Review Intelligence OS", "التقييمات والشكاوى لا تتحول لقرارات"),
        ("عقار وخدمات B2B", "Sales Pipeline OS", "العروض والعملاء يحتاجون متابعة طويلة"),
    ]
    rows = []
    for i, (sector, offer, pain) in enumerate(sectors, 1):
        rows.append({
            "date": TODAY,
            "company": f"Research Target #{i}",
            "sector": sector,
            "contact": "",
            "offer": offer,
            "priority": "50",
            "pain_angle": pain,
            "status": "needs_review",
            "next_action": "find_public_contact",
        })
    return rows

def update_crm(queue: list[dict[str, str]]) -> None:
    crm_path = CRM / "pipeline.csv"
    fields = [
        "date", "company", "sector", "contact", "phone", "email", "source",
        "offer", "status", "next_action", "next_followup_date",
        "deal_value_sar", "probability", "notes",
    ]

    existing = read_csv(crm_path)
    seen = {pick(r, "company").lower() for r in existing}

    for q in queue[:20]:
        key = q["company"].lower()
        if key in seen:
            continue
        existing.append({
            "date": TODAY,
            "company": q["company"],
            "sector": q["sector"],
            "contact": q["contact"],
            "phone": q["contact"] if q["contact"].startswith("+") else "",
            "email": "",
            "source": "micro_master_os",
            "offer": q["offer"],
            "status": "needs_review",
            "next_action": q["next_action"],
            "next_followup_date": "",
            "deal_value_sar": "",
            "probability": "10",
            "notes": q["pain_angle"],
        })

    write_csv(crm_path, existing, fields)

def report(queue: list[dict[str, str]]) -> None:
    lines = [
        "# Dealix Micro Master CEO Report",
        "",
        f"Date: {TODAY}",
        "",
        "## هدف اليوم",
        "بيع أو دفع عميل واحد نحو Transformation Diagnostic Sprint.",
        "",
        "## Approval Queue Summary",
        f"- Rows: {len(queue)}",
        "- Sending: manual only",
        "- Contracts/invoices: manual approval only",
        "",
        "## Top Targets",
        "| # | Company | Sector | Priority | Offer | Next Action |",
        "|---:|---|---|---:|---|---|",
    ]

    for i, q in enumerate(queue[:20], 1):
        lines.append(f"| {i} | {q['company']} | {q['sector']} | {q['priority']} | {q['offer']} | {q['next_action']} |")

    lines += [
        "",
        "## الرسالة الجاهزة",
        "السلام عليكم، أنا سامي من Dealix.",
        "",
        "لاحظت أن كثير من الشركات تخسر فرص بسبب تشتت واتساب، ضعف المتابعة، التقييمات غير المستغلة، وغياب تقرير يومي للإدارة.",
        "",
        "Dealix يبني نظام تشغيل للشركة يربط العملاء + المتابعة + التقييمات + العروض + التقارير.",
        "",
        "نبدأ عادة بتشخيص مدفوع خلال 3-7 أيام يطلع لكم أين تضيع الفرص وما أول نظام يحتاج يتركب.",
        "",
        "إذا مناسب، أرسل لك ملخص التشخيص وطريقة البداية؟",
        "",
        "## Next Founder Actions",
        "1. افتح approval queue.",
        "2. اختر أعلى 20.",
        "3. أرسل يدوياً.",
        "4. أي رد مهتم ادفعه إلى Diagnostic Sprint.",
        "5. حدّث CRM.",
    ]

    (REPORTS / f"{TODAY}_MICRO_MASTER_CEO_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def main() -> None:
    raw = collect()
    queue = [normalize(r) for r in raw]
    if not queue:
        queue = fallback_rows()

    queue.sort(key=lambda x: int(x["priority"]), reverse=True)

    fields = ["date", "company", "sector", "contact", "offer", "priority", "pain_angle", "status", "next_action"]
    queue_path = OUTBOX / f"{TODAY}_micro_master_approval_queue.csv"
    write_csv(queue_path, queue, fields)
    update_crm(queue)
    report(queue)

    print(f"OK CEO report: {REPORTS / (TODAY + '_MICRO_MASTER_CEO_REPORT.md')}")
    print(f"OK Approval queue: {queue_path}")
    print(f"OK CRM: {CRM / 'pipeline.csv'}")

if __name__ == "__main__":
    main()
