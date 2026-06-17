#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TODAY = dt.date.today().isoformat()

OUT = ROOT / "company" / "runtime" / "revenue" / TODAY
CRM = ROOT / "company" / "crm" / "pipeline.csv"
OUTBOX_DIR = ROOT / "company" / "outbox"
LEADS_DIR = ROOT / "company" / "lead_research"
FOUNDER_DIR = ROOT / "founder_os" / "output"

OUT.mkdir(parents=True, exist_ok=True)

OFFERS = {
    0: ("WhatsApp Revenue OS", "الفرص تضيع في واتساب والمتابعة", "عيادات، عقار، تدريب"),
    1: ("Review Intelligence OS", "التقييمات والشكاوى لا تتحول لقرارات", "مطاعم، عيادات، كافيهات"),
    2: ("AI Business Command Center", "الإدارة لا ترى الحقيقة اليومية", "وكالات، B2B، فروع متعددة"),
    3: ("Brand Intelligence OS", "الهوية والرسائل والعروض غير موحدة", "خدمات، عيادات، مطاعم"),
    4: ("Transformation Diagnostic Sprint", "ابدأ بتشخيص مدفوع قبل بناء نظام كامل", "كل القطاعات"),
    5: ("Growth Engine OS", "لا يوجد outbound/follow-up cadence واضح", "تدريب، B2B، وكالات"),
    6: ("Customer Experience OS", "رحلة العميل متفرقة من أول تواصل إلى retention", "عيادات، مطاعم، خدمات"),
}

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

def pick(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value:
            return str(value).strip()
    return ""

def score(row: dict[str, str]) -> int:
    value = 40
    if pick(row, "phone", "contact"):
        value += 20
    if pick(row, "website", "link"):
        value += 15
    if pick(row, "pain_angle", "snippet", "notes"):
        value += 15
    if pick(row, "recommended_offer", "core_offer", "offer"):
        value += 10
    try:
        value = max(value, int(float(pick(row, "priority_score") or 0)))
    except Exception:
        pass
    return min(value, 100)

def collect_targets() -> list[dict[str, str]]:
    paths = []
    paths.extend(sorted((ROOT / "company" / "runtime" / "places").glob("*/real_leads.csv"))[-5:])
    paths.extend(sorted(LEADS_DIR.glob("*/web_lead_research.csv"))[-5:])
    paths.extend(sorted(FOUNDER_DIR.glob("*/daily_targets.csv"))[-5:])
    paths.extend(sorted(OUTBOX_DIR.glob("*approval_queue.csv"))[-5:])

    rows: list[dict[str, str]] = []
    for path in paths:
        for row in read_csv(path):
            row["_source"] = str(path)
            rows.append(row)

    if not rows:
        for i, sector in enumerate(["clinics", "training", "agencies", "restaurants", "real_estate"], 1):
            rows.append({
                "company": f"Research Target {i}",
                "sector": sector,
                "pain_angle": "تحتاج بحث يدوي واستهداف",
                "recommended_offer": "Transformation Diagnostic Sprint",
            })

    normalized = []
    for row in rows:
        company = pick(row, "company", "company_name", "title") or "Research Target"
        sector = pick(row, "sector", "segment") or "general"
        contact = pick(row, "contact", "phone", "website", "link")
        pain = pick(row, "pain_angle", "snippet", "notes") or "تحتاج نظام متابعة وتقارير أوضح"
        offer = pick(row, "offer", "recommended_offer", "core_offer") or "Transformation Diagnostic Sprint"
        normalized.append({
            "date": TODAY,
            "company": company,
            "sector": sector,
            "contact": contact,
            "pain_angle": pain,
            "offer": offer,
            "priority": str(score(row)),
            "source": pick(row, "_source"),
            "next_action": "review_and_send_manually",
        })

    normalized.sort(key=lambda x: int(x["priority"]), reverse=True)
    return normalized

def write_offer_of_day() -> tuple[str, str, str]:
    offer, pain, targets = OFFERS[dt.date.today().weekday()]
    text = f"""# Offer of the Day

Date: {TODAY}

## Offer
{offer}

## Pain angle
{pain}

## Best targets
{targets}

## CTA
ابدأ بتشخيص تحولي مدفوع

## Founder instruction
Use this offer in the first 20 reviewed messages today.
"""
    (OUT / "OFFER_OF_THE_DAY.md").write_text(text, encoding="utf-8")
    return offer, pain, targets

def write_whatsapp(targets: list[dict[str, str]], offer_of_day: str) -> None:
    lines = ["# WhatsApp Drafts", ""]
    for i, row in enumerate(targets[:20], 1):
        lines += [
            f"## {i}. {row['company']}",
            "",
            "السلام عليكم، أنا سامي من Dealix.",
            "",
            f"لاحظت أن كثير من الشركات في مجال {row['sector']} تخسر فرص بسبب {row['pain_angle']}.",
            "",
            "Dealix يبني نظام تشغيل للشركة يربط العملاء + المتابعة + التقييمات + العروض + التقارير.",
            "",
            f"أقترح كبداية: {offer_of_day}.",
            "",
            "نبدأ بتشخيص مدفوع خلال 3-7 أيام يوضح أين تضيع الفرص وما أول نظام يحتاج يتركب.",
            "",
            "إذا مناسب، أرسل لك ملخص التشخيص وطريقة البداية؟",
            "",
        ]
    (OUT / "WHATSAPP_DRAFTS.md").write_text("\n".join(lines), encoding="utf-8")

def write_email(targets: list[dict[str, str]], offer_of_day: str) -> None:
    lines = ["# Email Drafts", ""]
    for i, row in enumerate(targets[:10], 1):
        lines += [
            f"## {i}. {row['company']}",
            "",
            f"Subject: فكرة نظام تشغيل ذكي لـ {row['company']}",
            "",
            "السلام عليكم،",
            "",
            "أنا سامي من Dealix.",
            "",
            f"أرسل لك فكرة مختصرة لأن {row['company']} قد تستفيد من تقليل التسرب التشغيلي المرتبط بـ: {row['pain_angle']}.",
            "",
            "Dealix يبني أنظمة تشغيل للشركات تربط العملاء، المتابعة، التقييمات، العروض، والتقارير التنفيذية.",
            "",
            f"اقتراحي كبداية: {offer_of_day}.",
            "",
            "إذا مناسب، نحدد مكالمة 20 دقيقة لتقييم fit.",
            "",
            "تحياتي،",
            "سامي",
            "",
        ]
    (OUT / "EMAIL_DRAFTS.md").write_text("\n".join(lines), encoding="utf-8")

def write_linkedin(offer: str, pain: str) -> None:
    text = f"""# LinkedIn Posts

## Post 1
كثير من الشركات لا تخسر العملاء بسبب ضعف المنتج.

تخسرهم بسبب:
- واتساب مشتت
- متابعة غير واضحة
- تقييمات لا تتحول لقرارات
- عروض بدون follow-up
- إدارة لا ترى تقرير يومي

الحل ليس بوت فقط.
الحل نظام تشغيل أعمال.

في Dealix نبدأ غالباً بـ {offer} لمعالجة: {pain}.

## Post 2
إذا الشركة لا تعرف يومياً:
كم فرصة دخلت؟
كم متابعة تأخرت؟
كم عرض لم يتم متابعته؟
ما أكثر سبب خسارة؟

فهي لا تحتاج أداة جديدة فقط.
تحتاج operating system.
"""
    (OUT / "LINKEDIN_POSTS.md").write_text(text, encoding="utf-8")

def write_proposals(targets: list[dict[str, str]]) -> None:
    lines = ["# Proposal Stubs", ""]
    for i, row in enumerate(targets[:5], 1):
        lines += [
            f"## {i}. {row['company']}",
            "",
            f"Sector: {row['sector']}",
            f"Pain: {row['pain_angle']}",
            f"Recommended offer: {row['offer']}",
            "",
            "### Proposed first step",
            "Transformation Diagnostic Sprint",
            "",
            "### Outputs",
            "- Workflow map",
            "- Leakage map",
            "- KPI model",
            "- Recommended first system",
            "- Implementation quote",
            "",
            "### Commercial direction",
            "7,500 - 25,000 SAR, paid upfront.",
            "",
        ]
    (OUT / "PROPOSAL_STUBS.md").write_text("\n".join(lines), encoding="utf-8")

def write_site_brief(offer: str, pain: str) -> None:
    text = f"""# Website Update Brief

## Today’s homepage emphasis
{offer}

## Hero angle
{pain}

## CTA
ابدأ بتشخيص تحولي مدفوع

## Section to highlight
- Problem: operational leakage
- Solution: Dealix operating systems
- Proof: daily operating engine
- Offer: Diagnostic Sprint
- Next step: 20-minute fit call

## Suggested Arabic headline
نحوّل فوضى واتساب والمتابعة والتقارير إلى نظام تشغيل واضح للشركة.
"""
    (OUT / "WEBSITE_UPDATE_BRIEF.md").write_text(text, encoding="utf-8")

def write_report(targets: list[dict[str, str]], offer: str) -> None:
    lines = [
        "# CEO Revenue Report",
        "",
        f"Date: {TODAY}",
        "",
        f"Offer of the day: {offer}",
        f"Targets found: {len(targets)}",
        "",
        "## Top 20",
        "| # | Company | Sector | Priority | Offer | Contact |",
        "|---:|---|---|---:|---|---|",
    ]

    for i, row in enumerate(targets[:20], 1):
        lines.append(f"| {i} | {row['company']} | {row['sector']} | {row['priority']} | {row['offer']} | {row['contact']} |")

    lines += [
        "",
        "## Actions",
        "1. Open WHATSAPP_DRAFTS.md.",
        "2. Send top 20 manually.",
        "3. Push Diagnostic Sprint to interested replies.",
        "4. Update company/crm/pipeline.csv.",
        "5. Turn one reply into a 20-minute call.",
    ]
    (OUT / "CEO_REVENUE_REPORT.md").write_text("\n".join(lines), encoding="utf-8")

def main() -> None:
    targets = collect_targets()
    offer, pain, _ = write_offer_of_day()

    fields = ["date", "company", "sector", "contact", "pain_angle", "offer", "priority", "source", "next_action"]
    write_csv(OUT / "TOP_20_OUTBOUND.csv", targets[:20], fields)

    write_whatsapp(targets, offer)
    write_email(targets, offer)
    write_linkedin(offer, pain)
    write_proposals(targets)
    write_site_brief(offer, pain)
    write_report(targets, offer)

    print(f"Revenue day generated: {OUT}")
    print(f"Open: {OUT / 'CEO_REVENUE_REPORT.md'}")

if __name__ == "__main__":
    main()
