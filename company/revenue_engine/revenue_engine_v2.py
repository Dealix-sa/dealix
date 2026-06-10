#!/usr/bin/env python3
"""Revenue Engine v2 — generates full daily commercial pack. Never sends anything."""
from __future__ import annotations

import csv
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TODAY = dt.date.today().isoformat()
RUNTIME = ROOT / "company" / "runtime" / "revenue" / TODAY

OFFER_LADDER = [
    ("Transformation Diagnostic Sprint", "7,500–25,000 SAR", "3–7 days",
     "نكتشف أين يتسرب إيرادك ونبني خارطة الحل"),
    ("Managed AI Operations", "2,999–4,999 SAR/month", "ongoing",
     "نشغّل نظام AI يومياً ونسلمك تقرير أسبوعي"),
    ("Data Intelligence Pack", "1,500 SAR", "2–3 days",
     "نبني قاعدة بيانات عملاء مؤهلة وجاهزة للتواصل"),
    ("Micro Sprint", "499 SAR", "1–2 days",
     "نثبت قدرتنا بحل واحد سريع وملموس"),
]

SECTOR_PAIN = {
    "عيادات ومراكز طبية": "الاستفسارات والحجوزات تضيع في واتساب، لا يوجد متابعة منظمة",
    "مراكز تدريب": "استفسارات الدورات تحتاج تسجيل وردود سريعة وتذكيرات",
    "وكالات تسويق": "تقارير العملاء والمهام متفرقة بين أدوات مختلفة",
    "مطاعم وكافيهات": "التقييمات السلبية لا تُرد عليها، الشكاوى لا تتحول لقرارات",
    "عقار وخدمات B2B": "العروض والعملاء يحتاجون متابعة طويلة بدون نظام",
    "تجزئة": "لا يوجد قراءة يومية لأداء المبيعات والمخزون",
    "خدمات قانونية": "الملفات والمواعيد والمتابعة تعتمد على الذاكرة الشخصية",
    "لوجستيات": "التتبع والتحديثات للعملاء يدوي وبطيء",
    "general": "غياب نظام متابعة وتقارير يومية للإدارة",
}

WA_TEMPLATE = """\
السلام عليكم،

أنا سامي من Dealix — نبني أنظمة تشغيل AI للشركات السعودية.

لاحظت أن شركات في قطاع {sector} تخسر فرصاً بسبب: {pain}

نبدأ بتشخيص مدفوع خلال {duration} يطلع لكم:
• خارطة العمليات الحالية
• نقاط تسرب الإيراد
• أول نظام AI يستحق التركيب
• خطة تنفيذ 14 يوم

السعر: {price}

إذا مناسب، أرسل لك ملخص التشخيص؟
"""

EMAIL_TEMPLATE = """\
Subject: كيف يمكن لـ AI أن يوقف تسرب الإيراد في {company}

السلام عليكم،

اسمي سامي عسيري، مؤسس Dealix — شركة سعودية متخصصة في بناء أنظمة تشغيل AI للشركات.

رأيت أن شركات في قطاع {sector} تواجه: {pain}

نحن نحل هذا عبر {offer} — نبدأ بتشخيص دقيق خلال {duration} يطلع لكم خارطة واضحة وخطة تنفيذ.

هل لديكم 20 دقيقة هذا الأسبوع لمناقشة ذلك؟

مع التحية،
سامي عسيري
Dealix | AI Business Transformation
"""

LINKEDIN_TEMPLATE = """\
**كيف تعرف أن شركتك تخسر إيراداً بدون ما تلاحظ؟**

في Dealix، رأينا نمطاً متكرراً:

❌ واتساب مليان استفسارات بدون متابعة
❌ تقييمات سلبية بدون رد
❌ قرارات بدون بيانات يومية
❌ فريق يشتغل على أدوات غير مترابطة

الحل مو تطبيق جديد. الحل هو **نظام تشغيل مربوط**.

نحن نبني نظاماً يجمع:
• واتساب + CRM + تقارير يومية
• أو تقييمات + ردود تلقائية + تحليل
• أو قاعدة عملاء + تواصل + متابعة

نبدأ بـ **تشخيص تحولي مدفوع** خلال 3-7 أيام — يطلع لكم خارطة واضحة وخطة تنفيذ.

السعر يبدأ من 7,500 ريال.

إذا كنت تدير شركة سعودية وتحس أن الأمور أبطأ مما يجب — تواصل معي.

#Dealix #AI #السعودية #B2B #تحول_رقمي
"""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def pick(row: dict[str, str], *keys: str) -> str:
    for k in keys:
        v = row.get(k)
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


def collect_leads() -> list[dict[str, str]]:
    paths: list[Path] = []
    paths += sorted((ROOT / "company" / "lead_research").glob("*/web_lead_research.csv"))[-3:]
    paths += sorted((ROOT / "founder_os" / "output").glob("*/daily_targets.csv"))[-3:]
    rows: list[dict[str, str]] = []
    for p in paths:
        for r in read_csv(p):
            r["_source"] = str(p)
            rows.append(r)
    return rows


def normalize(row: dict[str, str]) -> dict[str, str]:
    company = pick(row, "company_name", "company", "title") or "Research Target"
    sector = pick(row, "segment", "sector") or "general"
    contact = pick(row, "phone", "website", "link", "contact")
    offer_name = pick(row, "recommended_offer", "core_offer", "offer") or "Transformation Diagnostic Sprint"
    pain = pick(row, "pain_angle", "snippet", "notes") or SECTOR_PAIN.get(sector, SECTOR_PAIN["general"])
    return {
        "date": TODAY,
        "company": company,
        "sector": sector,
        "contact": contact,
        "offer": offer_name,
        "priority": str(score(row)),
        "pain_angle": pain,
        "status": "needs_review",
        "next_action": "review_and_send_manually",
    }


def fallback_targets() -> list[dict[str, str]]:
    entries = [
        ("عيادات ومراكز طبية", "Transformation Diagnostic Sprint", "7,500 SAR"),
        ("مراكز تدريب وتعليم", "Growth Engine OS", "7,500 SAR"),
        ("وكالات تسويق رقمي", "Client Command Center OS", "7,500 SAR"),
        ("مطاعم وكافيهات", "Review Intelligence OS", "7,500 SAR"),
        ("وكالات عقار", "Sales Pipeline OS", "7,500 SAR"),
        ("خدمات قانونية ومحاسبية", "Client Command Center OS", "7,500 SAR"),
        ("لوجستيات وتوصيل", "AI Agent Workforce OS", "7,500 SAR"),
        ("تجزئة ومتاجر", "WhatsApp Revenue OS", "7,500 SAR"),
        ("شركات B2B صناعية", "Transformation Diagnostic Sprint", "15,000 SAR"),
        ("مراكز خدمات طبية متخصصة", "WhatsApp Revenue OS", "7,500 SAR"),
    ]
    rows = []
    for i, (sector, offer, price) in enumerate(entries, 1):
        rows.append({
            "date": TODAY,
            "company": f"Research Target #{i}",
            "sector": sector,
            "contact": "",
            "offer": offer,
            "priority": str(70 - i * 2),
            "pain_angle": SECTOR_PAIN.get(sector, SECTOR_PAIN["general"]),
            "status": "needs_research",
            "next_action": "find_company_and_contact",
        })
    return rows


def pick_offer_of_day(targets: list[dict[str, str]]) -> tuple[str, str, str, str]:
    sector_counts: dict[str, int] = {}
    for t in targets:
        sector_counts[t["sector"]] = sector_counts.get(t["sector"], 0) + 1
    top_sector = max(sector_counts, key=lambda s: sector_counts[s]) if sector_counts else "general"
    offer = OFFER_LADDER[0]
    return offer[0], offer[1], offer[2], top_sector


def write_daily_offer(out: Path, targets: list[dict[str, str]]) -> None:
    offer_name, price, duration, top_sector = pick_offer_of_day(targets)
    pain = SECTOR_PAIN.get(top_sector, SECTOR_PAIN["general"])
    lines = [
        f"# عرض اليوم — {TODAY}",
        "",
        f"## {offer_name}",
        f"**السعر**: {price}",
        f"**المدة**: {duration}",
        f"**قطاع الفرصة اليوم**: {top_sector}",
        "",
        "## رسالة التركيز",
        pain,
        "",
        "## CTA",
        "ابدأ بتشخيص تحولي مدفوع — نكتشف أين يتسرب إيرادك ونبني خطة واضحة.",
        "",
        "## مؤشر الأداء اليومي",
        "- هدف المحادثات الجديدة: 5",
        "- هدف الردود المهتمة: 2",
        "- هدف تحويل إلى Sprint: 1",
    ]
    (out / "DAILY_OFFER.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_top20(out: Path, targets: list[dict[str, str]]) -> None:
    fields = ["date", "company", "sector", "contact", "offer", "priority", "pain_angle", "status", "next_action"]
    top20 = targets[:20]
    path = out / "TOP20_TARGETS.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(top20)


def write_whatsapp_drafts(out: Path, targets: list[dict[str, str]]) -> None:
    lines = [f"# واتساب درافتس — {TODAY}", ""]
    for t in targets[:10]:
        offer_match = next((o for o in OFFER_LADDER if o[0] == t["offer"]), OFFER_LADDER[0])
        msg = WA_TEMPLATE.format(
            sector=t["sector"],
            pain=t["pain_angle"],
            duration=offer_match[2],
            price=offer_match[1],
        )
        lines += [f"## {t['company']} ({t['sector']})", f"Contact: {t['contact'] or 'TBD'}", "", msg, "---", ""]
    (out / "WHATSAPP_DRAFTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_email_drafts(out: Path, targets: list[dict[str, str]]) -> None:
    lines = [f"# Email Drafts — {TODAY}", ""]
    for t in targets[:10]:
        offer_match = next((o for o in OFFER_LADDER if o[0] == t["offer"]), OFFER_LADDER[0])
        msg = EMAIL_TEMPLATE.format(
            company=t["company"],
            sector=t["sector"],
            pain=t["pain_angle"],
            offer=t["offer"],
            duration=offer_match[2],
        )
        lines += [f"## {t['company']}", f"To: {t['contact'] or 'TBD'}", "", msg, "---", ""]
    (out / "EMAIL_DRAFTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_linkedin(out: Path) -> None:
    (out / "LINKEDIN_POST.md").write_text(
        f"# LinkedIn Post — {TODAY}\n\n" + LINKEDIN_TEMPLATE + "\n", encoding="utf-8"
    )


def write_proposal_stubs(out: Path, targets: list[dict[str, str]]) -> None:
    lines = [f"# Proposal Stubs — {TODAY}", ""]
    for t in targets[:5]:
        offer_match = next((o for o in OFFER_LADDER if o[0] == t["offer"]), OFFER_LADDER[0])
        lines += [
            f"## Proposal: {t['company']}",
            f"**قطاع**: {t['sector']}",
            f"**العرض**: {t['offer']}",
            f"**السعر**: {offer_match[1]}",
            f"**المدة**: {offer_match[2]}",
            f"**المشكلة**: {t['pain_angle']}",
            "",
            "### المخرجات المقترحة",
            "- خارطة العمليات الحالية",
            "- خريطة تسرب الإيراد",
            "- نموذج KPI مقترح",
            "- أول نظام موصى به",
            "- عرض تنفيذي بالسعر",
            "- خطة تنفيذ 14 يوم",
            "",
            f"**الحالة**: يحتاج موافقة المؤسس قبل الإرسال",
            "",
            "---",
            "",
        ]
    (out / "PROPOSAL_STUBS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_website_brief(out: Path, targets: list[dict[str, str]]) -> None:
    _, _, _, top_sector = pick_offer_of_day(targets)
    pain = SECTOR_PAIN.get(top_sector, SECTOR_PAIN["general"])
    lines = [
        f"# Website Update Brief — {TODAY}",
        "",
        f"## القطاع الأولوية اليوم: {top_sector}",
        "",
        "## التحديثات المقترحة للموقع",
        "",
        "### الصفحة الرئيسية",
        f"- Hero subtitle: أوقف تسرب الإيراد في شركتك — نبدأ بتشخيص خلال أسبوع",
        f"- Pain point highlight: {pain}",
        "",
        "### صفحة التشخيص (/ar/diagnostic-sprint)",
        f"- Featured sector: {top_sector}",
        "- Add: شهادة مختصرة أو نتيجة ملموسة من قطاع مشابه",
        "",
        "### CTA الموحد",
        "ابدأ بتشخيص تحولي مدفوع ← يوجه إلى /ar/intake",
        "",
        "**ملاحظة**: هذا مقترح فقط. لا تتم أي تغييرات تلقائية على الموقع.",
    ]
    (out / "WEBSITE_BRIEF.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_ceo_report(out: Path, targets: list[dict[str, str]]) -> None:
    offer_name, price, duration, top_sector = pick_offer_of_day(targets)
    lines = [
        f"# CEO Revenue Report — {TODAY}",
        "",
        "## ملخص اليوم",
        f"- إجمالي الأهداف: {len(targets)}",
        f"- القطاع الأولوية: {top_sector}",
        f"- العرض الموصى به اليوم: {offer_name} ({price})",
        "",
        "## الملفات المولدة",
        "| الملف | الوصف |",
        "|-------|-------|",
        "| DAILY_OFFER.md | عرض اليوم والرسالة المركزة |",
        "| TOP20_TARGETS.csv | أفضل 20 هدف مرتبين بالأولوية |",
        "| WHATSAPP_DRAFTS.md | مسودات واتساب لأول 10 أهداف |",
        "| EMAIL_DRAFTS.md | مسودات إيميل لأول 10 أهداف |",
        "| LINKEDIN_POST.md | بوست لينكد إن جاهز للمراجعة |",
        "| PROPOSAL_STUBS.md | ملخصات عروض لأفضل 5 أهداف |",
        "| WEBSITE_BRIEF.md | مقترح تحديث الموقع لهذا اليوم |",
        "",
        "## أهم 5 أهداف",
        "| الشركة | القطاع | الأولوية | العرض | الإجراء |",
        "|--------|--------|---------|-------|--------|",
    ]
    for t in targets[:5]:
        lines.append(f"| {t['company']} | {t['sector']} | {t['priority']} | {t['offer']} | {t['next_action']} |")

    lines += [
        "",
        "## قواعد التنفيذ",
        "1. راجع كل مسودة قبل الإرسال",
        "2. أرسل يدوياً فقط — لا إرسال تلقائي",
        "3. أي رد مهتم → ادفعه نحو Diagnostic Sprint",
        "4. حدّث CRM بعد كل تواصل",
        "5. لا تصدر فاتورة أو عقد بدون موافقة",
        "",
        "---",
        f"*Generated by Revenue Engine v2 — {TODAY} — draft only*",
    ]
    (out / "CEO_REVENUE_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RUNTIME.mkdir(parents=True, exist_ok=True)

    raw = collect_leads()
    targets = [normalize(r) for r in raw]
    if not targets:
        targets = fallback_targets()

    targets.sort(key=lambda x: int(x["priority"]), reverse=True)

    write_daily_offer(RUNTIME, targets)
    write_top20(RUNTIME, targets)
    write_whatsapp_drafts(RUNTIME, targets)
    write_email_drafts(RUNTIME, targets)
    write_linkedin(RUNTIME)
    write_proposal_stubs(RUNTIME, targets)
    write_website_brief(RUNTIME, targets)
    write_ceo_report(RUNTIME, targets)

    print(f"OK Revenue pack: {RUNTIME}/")
    print(f"OK Targets: {len(targets)}")
    for f in sorted(RUNTIME.iterdir()):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
