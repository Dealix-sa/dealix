#!/usr/bin/env python3
"""
Dealix Client Intake Engine v2 — scores, qualifies, and generates full client pack.
Never sends anything. All output is draft for founder review.
"""
from __future__ import annotations

import csv
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TODAY = dt.date.today().isoformat()
OUT = ROOT / "company" / "runtime" / "intake" / TODAY
CRM = ROOT / "company" / "crm" / "pipeline.csv"

OUT.mkdir(parents=True, exist_ok=True)
CRM.parent.mkdir(parents=True, exist_ok=True)

# ─── Field definitions ───────────────────────────────────────────────────────

FIELDS = [
    "company_name", "sector", "city", "employees", "branches",
    "contact_name", "contact_role", "whatsapp", "email", "website",
    "weekly_leads", "main_channel", "response_time_hrs", "has_crm",
    "crm_name", "has_reports", "report_frequency", "has_reviews",
    "avg_review_score", "has_proposals", "proposal_close_rate",
    "main_problem", "secondary_problem", "goal_30_days", "goal_90_days",
    "budget_range", "decision_maker", "timeline",
    "fit_score", "tier", "recommended_offer", "recommended_price",
    "leakage_areas", "next_action", "followup_date", "notes",
]

SECTOR_OFFERS = {
    "clinics": "WhatsApp Revenue OS",
    "عيادات": "WhatsApp Revenue OS",
    "medical": "WhatsApp Revenue OS",
    "طبي": "WhatsApp Revenue OS",
    "training": "Growth Engine OS",
    "تدريب": "Growth Engine OS",
    "education": "Growth Engine OS",
    "تعليم": "Growth Engine OS",
    "restaurant": "Review Intelligence OS",
    "مطعم": "Review Intelligence OS",
    "cafe": "Review Intelligence OS",
    "كافيه": "Review Intelligence OS",
    "food": "Review Intelligence OS",
    "legal": "AI Business Command Center",
    "قانون": "AI Business Command Center",
    "محاسبة": "AI Business Command Center",
    "accounting": "AI Business Command Center",
    "real_estate": "Sales Pipeline OS",
    "عقار": "Sales Pipeline OS",
    "retail": "WhatsApp Revenue OS",
    "تجزئة": "WhatsApp Revenue OS",
    "logistics": "AI Agent Workforce OS",
    "لوجستيات": "AI Agent Workforce OS",
    "agency": "Client Command Center OS",
    "وكالة": "Client Command Center OS",
}

PROBLEM_OFFERS = {
    "واتساب": "WhatsApp Revenue OS",
    "whatsapp": "WhatsApp Revenue OS",
    "تقييم": "Review Intelligence OS",
    "review": "Review Intelligence OS",
    "هوية": "Brand Intelligence OS",
    "brand": "Brand Intelligence OS",
    "محتوى": "Brand Intelligence OS",
    "تقرير": "AI Business Command Center",
    "report": "AI Business Command Center",
    "إدارة": "AI Business Command Center",
    "متابعة": "WhatsApp Revenue OS",
    "عروض": "Sales Pipeline OS",
    "proposal": "Sales Pipeline OS",
    "موظفين": "AI Agent Workforce OS",
    "أتمتة": "AI Agent Workforce OS",
    "automation": "AI Agent Workforce OS",
    "نمو": "Growth Engine OS",
    "growth": "Growth Engine OS",
    "عملاء": "Customer Experience OS",
}

BUDGET_TO_PRICE = {
    "أقل من 10k": "7,500 SAR",
    "10k - 25k": "12,500 SAR",
    "25k - 75k": "25,000 SAR",
    "75k+": "75,000 SAR",
    "less_10k": "7,500 SAR",
    "10k_25k": "12,500 SAR",
    "25k_75k": "25,000 SAR",
    "75k_plus": "75,000 SAR",
}

LEAKAGE_SIGNALS = [
    ("has_crm",        "No",  "no_crm",        "لا يوجد CRM — استفسارات تضيع بدون تتبع"),
    ("has_reports",    "No",  "no_reports",     "لا توجد تقارير إدارية — قرارات بدون بيانات"),
    ("has_reviews",    "Yes", "unmanaged_reviews", "تقييمات غير مدارة — سمعة تؤثر على العملاء الجدد"),
    ("response_time_hrs", "", "slow_response",  "وقت استجابة بطيء — عملاء محتملون يذهبون للمنافس"),
]

# ─── Scoring ─────────────────────────────────────────────────────────────────

def score(row: dict[str, str]) -> tuple[int, str, list[str]]:
    """Returns (score 0-100, tier, leakage_areas)."""
    points = 30
    leakage: list[str] = []

    # Volume: more leads = more pain = higher priority
    try:
        weekly = int(row.get("weekly_leads") or 0)
        if weekly >= 100:
            points += 25
        elif weekly >= 30:
            points += 18
        elif weekly >= 10:
            points += 10
        elif weekly >= 3:
            points += 5
    except ValueError:
        pass

    # Contact quality
    if row.get("whatsapp"):
        points += 8
    if row.get("email"):
        points += 4
    if row.get("contact_name"):
        points += 3

    # Pain clarity
    if row.get("main_problem"):
        points += 10
    if row.get("secondary_problem"):
        points += 5

    # Budget signal
    budget = row.get("budget_range", "")
    if "75k+" in budget or "75k_plus" in budget:
        points += 15
    elif "25k" in budget:
        points += 10
    elif "10k" in budget:
        points += 6
    else:
        points += 3

    # Decision maker
    role = (row.get("contact_role") or "").lower()
    if any(k in role for k in ["ceo", "owner", "مدير", "مؤسس", "founder", "مالك"]):
        points += 8

    # Operational gaps → higher urgency
    if row.get("has_crm", "").lower() in ("no", "لا"):
        points += 5
        leakage.append("no_crm")
    if row.get("has_reports", "").lower() in ("no", "لا"):
        points += 5
        leakage.append("no_reports")

    # Response time gap
    try:
        hrs = float(row.get("response_time_hrs") or 0)
        if hrs > 4:
            points += 5
            leakage.append("slow_response")
    except ValueError:
        pass

    # Review exposure
    if row.get("has_reviews", "").lower() in ("yes", "نعم"):
        try:
            avg = float(row.get("avg_review_score") or 5)
            if avg < 4.0:
                points += 8
                leakage.append("low_review_score")
            elif avg < 4.5:
                points += 4
                leakage.append("medium_review_score")
        except ValueError:
            leakage.append("unmanaged_reviews")

    final = min(points, 100)

    if final >= 80:
        tier = "A"
    elif final >= 60:
        tier = "B"
    elif final >= 40:
        tier = "C"
    else:
        tier = "D"

    return final, tier, leakage


def recommend_offer(row: dict[str, str]) -> str:
    problem = (row.get("main_problem") or "").lower()
    sector = (row.get("sector") or "").lower()

    for kw, offer in PROBLEM_OFFERS.items():
        if kw in problem:
            return offer

    for kw, offer in SECTOR_OFFERS.items():
        if kw in sector:
            return offer

    return "Transformation Diagnostic Sprint"


def recommend_price(row: dict[str, str]) -> str:
    return BUDGET_TO_PRICE.get(row.get("budget_range", ""), "7,500 SAR")


def next_action(fit_score: int, tier: str) -> tuple[str, str]:
    if tier == "A":
        return "book_discovery_call_priority", (dt.date.today() + dt.timedelta(days=1)).isoformat()
    elif tier == "B":
        return "send_diagnostic_summary_and_book_call", (dt.date.today() + dt.timedelta(days=2)).isoformat()
    elif tier == "C":
        return "send_overview_and_nurture", (dt.date.today() + dt.timedelta(days=5)).isoformat()
    else:
        return "add_to_nurture_list", (dt.date.today() + dt.timedelta(days=14)).isoformat()


# ─── Writers ─────────────────────────────────────────────────────────────────

def write_template() -> Path:
    """Write an empty intake template CSV with one sample row."""
    path = OUT / "CLIENT_INTAKE_TEMPLATE.csv"
    sample = {
        "company_name": "شركة المثال للخدمات الطبية",
        "sector": "عيادات",
        "city": "الرياض",
        "employees": "25",
        "branches": "2",
        "contact_name": "أحمد محمد",
        "contact_role": "مدير عام",
        "whatsapp": "+9665xxxxxxxx",
        "email": "ahmed@example.com",
        "website": "https://example.sa",
        "weekly_leads": "80",
        "main_channel": "واتساب",
        "response_time_hrs": "6",
        "has_crm": "لا",
        "crm_name": "",
        "has_reports": "لا",
        "report_frequency": "",
        "has_reviews": "نعم",
        "avg_review_score": "3.8",
        "has_proposals": "نعم",
        "proposal_close_rate": "20%",
        "main_problem": "الاستفسارات تضيع في واتساب ولا متابعة",
        "secondary_problem": "لا تقرير يومي للإدارة",
        "goal_30_days": "تنظيم المتابعة وزيادة الحجوزات",
        "goal_90_days": "نظام متابعة كامل وتقارير إدارية",
        "budget_range": "10k - 25k",
        "decision_maker": "نعم",
        "timeline": "هذا الشهر",
        "fit_score": "", "tier": "", "recommended_offer": "",
        "recommended_price": "", "leakage_areas": "",
        "next_action": "", "followup_date": "", "notes": "",
    }
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerow(sample)
    return path


def process_file(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    rows = []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                fit, tier, leakage = score(row)
                action, followup = next_action(fit, tier)
                row["fit_score"] = str(fit)
                row["tier"] = tier
                row["recommended_offer"] = recommend_offer(row)
                row["recommended_price"] = recommend_price(row)
                row["leakage_areas"] = "|".join(leakage)
                row["next_action"] = action
                row["followup_date"] = followup
                rows.append(row)
    except Exception as e:
        print(f"WARN: could not process {path}: {e}")
    return rows


def write_summary(rows: list[dict[str, str]]) -> Path:
    path = OUT / "INTAKE_SUMMARY.md"
    lines = [
        "# Dealix Client Intake Summary",
        "",
        f"**Date**: {TODAY}",
        f"**Total intakes processed**: {len(rows)}",
        "",
    ]

    if not rows:
        lines += [
            "## لا يوجد intake مُدخل بعد",
            "",
            "لملء البيانات، افتح:",
            f"`company/runtime/intake/{TODAY}/CLIENT_INTAKE_TEMPLATE.csv`",
            "",
            "أضف صف لكل شركة واحفظ الملف، ثم أعد تشغيل:",
            "```bash",
            "python company/intake/intake_engine.py",
            "```",
        ]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    # Tier summary
    tiers = {"A": [], "B": [], "C": [], "D": []}
    for r in rows:
        tiers.get(r.get("tier", "D"), tiers["D"]).append(r)

    lines += [
        "## توزيع الـ Tiers",
        "",
        f"- **Tier A** (أولوية قصوى — {len(tiers['A'])} شركة): اتصل اليوم",
        f"- **Tier B** (أولوية عالية — {len(tiers['B'])} شركة): أرسل ملخص وحدد موعد",
        f"- **Tier C** (مؤهلة — {len(tiers['C'])} شركة): أرسل overview ونمّ العلاقة",
        f"- **Tier D** (تحتاج تأهيل — {len(tiers['D'])} شركة): أضف لقائمة النشر",
        "",
        "---",
        "",
        "## Tier A — اتصل اليوم",
        "",
        "| الشركة | القطاع | المشكلة | العرض | السعر | الإجراء |",
        "|--------|--------|--------|-------|-------|--------|",
    ]
    for r in sorted(tiers["A"], key=lambda x: -int(x.get("fit_score", 0))):
        lines.append(
            f"| {r.get('company_name','')} | {r.get('sector','')} | "
            f"{r.get('main_problem','')[:40]} | {r.get('recommended_offer','')} | "
            f"{r.get('recommended_price','')} | {r.get('next_action','')} |"
        )

    if tiers["B"]:
        lines += [
            "",
            "## Tier B — أرسل ملخص وحدد موعد",
            "",
            "| الشركة | القطاع | الدرجة | العرض | موعد المتابعة |",
            "|--------|--------|-------|-------|--------------|",
        ]
        for r in sorted(tiers["B"], key=lambda x: -int(x.get("fit_score", 0))):
            lines.append(
                f"| {r.get('company_name','')} | {r.get('sector','')} | "
                f"{r.get('fit_score','')} | {r.get('recommended_offer','')} | "
                f"{r.get('followup_date','')} |"
            )

    lines += [
        "",
        "---",
        "",
        "## نقاط التسرب الأكثر شيوعاً",
        "",
    ]
    all_leakages: list[str] = []
    for r in rows:
        all_leakages.extend((r.get("leakage_areas") or "").split("|"))
    leakage_counts: dict[str, int] = {}
    for l in all_leakages:
        if l:
            leakage_counts[l] = leakage_counts.get(l, 0) + 1
    for k, v in sorted(leakage_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- **{k}**: {v} شركة")

    lines += [
        "",
        "---",
        "",
        "## القواعد",
        "- لا إرسال تلقائي — كل تواصل يحتاج مراجعة المؤسس",
        "- Tier A: تواصل خلال 24 ساعة",
        "- Tier B: تواصل خلال 48 ساعة",
        "- بعد كل رد → حدّث CRM",
        "- بعد كل مكالمة → وثّق في `clients/`",
    ]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_whatsapp_drafts(rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    path = OUT / "INTAKE_WHATSAPP_DRAFTS.md"
    lines = [f"# واتساب درافتس للـ Intake — {TODAY}", ""]

    for r in rows:
        if r.get("tier") not in ("A", "B"):
            continue
        name = r.get("contact_name") or r.get("company_name") or "العميل"
        offer = r.get("recommended_offer", "Transformation Diagnostic Sprint")
        price = r.get("recommended_price", "7,500 SAR")
        problem = r.get("main_problem", "")
        lines += [
            f"## {r.get('company_name','')} [{r.get('tier','')}]",
            f"**WhatsApp**: {r.get('whatsapp', 'TBD')}",
            "",
            f"السلام عليكم {name}،",
            "",
            f"ممنونين على اهتمامكم بـ Dealix.",
            f"بناءً على ما شاركتوه معنا عن {r.get('company_name','شركتكم')} في قطاع {r.get('sector','')}،",
            f"نرى أن المشكلة الرئيسية لديكم هي: **{problem}**",
            "",
            f"التوصية الأولى: **{offer}**",
            f"السعر: {price}",
            "",
            "نبدأ بتشخيص مدفوع خلال 3-7 أيام يطلع لكم:",
            "• خارطة العمليات الحالية",
            "• أين يتسرب الإيراد",
            "• أول نظام AI يستحق التركيب",
            "• خطة تنفيذ 14 يوم",
            "",
            "هل يناسبكم نحدد موعد Zoom قصير هذا الأسبوع؟",
            "",
            "⚠️ *مسودة — لا ترسل قبل مراجعة المؤسس*",
            "",
            "---",
            "",
        ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_proposal_stubs(rows: list[dict[str, str]]) -> None:
    tier_a = [r for r in rows if r.get("tier") == "A"]
    if not tier_a:
        return
    path = OUT / "INTAKE_PROPOSAL_STUBS.md"
    lines = [f"# Proposal Stubs — Tier A — {TODAY}", ""]

    for r in tier_a:
        lines += [
            f"## {r.get('company_name', 'TBD')}",
            "",
            f"| الحقل | القيمة |",
            f"|-------|--------|",
            f"| القطاع | {r.get('sector','')} |",
            f"| المدينة | {r.get('city','')} |",
            f"| الموظفون | {r.get('employees','')} |",
            f"| المشكلة الرئيسية | {r.get('main_problem','')} |",
            f"| المشكلة الثانوية | {r.get('secondary_problem','')} |",
            f"| العرض الموصى به | {r.get('recommended_offer','')} |",
            f"| السعر المقترح | {r.get('recommended_price','')} |",
            f"| درجة الملاءمة | {r.get('fit_score','')}/100 |",
            f"| مناطق التسرب | {r.get('leakage_areas','').replace('|', ', ')} |",
            f"| الميزانية | {r.get('budget_range','')} |",
            f"| صانع القرار | {r.get('decision_maker','')} |",
            f"| الجدول الزمني | {r.get('timeline','')} |",
            "",
            "### مخرجات التشخيص المقترحة",
            "1. خارطة العمليات الحالية (Workflow Map)",
            "2. خريطة تسرب الإيراد (Leakage Map)",
            f"3. نموذج KPI لـ {r.get('sector','')}",
            f"4. توصية أول نظام: **{r.get('recommended_offer','')}**",
            "5. عرض تنفيذي بالسعر والجدول الزمني",
            "6. خطة تنفيذ 14 يوم",
            "",
            f"**الحالة**: ⚠️ يحتاج موافقة المؤسس قبل الإرسال",
            "",
            "---",
            "",
        ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_crm(rows: list[dict[str, str]]) -> None:
    crm_fields = [
        "date", "company", "sector", "contact", "phone", "email", "source",
        "offer", "status", "next_action", "next_followup_date",
        "deal_value_sar", "probability", "notes",
    ]

    existing: list[dict[str, str]] = []
    if CRM.exists():
        try:
            with CRM.open("r", encoding="utf-8-sig", newline="") as f:
                existing = list(csv.DictReader(f))
        except Exception:
            pass

    seen = {r.get("company", "").lower() for r in existing}

    tier_prob = {"A": "70", "B": "40", "C": "20", "D": "10"}
    offer_values = {
        "WhatsApp Revenue OS": "12500",
        "Review Intelligence OS": "12500",
        "Brand Intelligence OS": "12500",
        "AI Business Command Center": "25000",
        "Growth Engine OS": "12500",
        "Customer Experience OS": "12500",
        "AI Agent Workforce OS": "25000",
        "Sales Pipeline OS": "12500",
        "Client Command Center OS": "12500",
        "Transformation Diagnostic Sprint": "12500",
    }

    for r in rows:
        key = (r.get("company_name") or "").lower()
        if not key or key in seen:
            continue
        existing.append({
            "date": TODAY,
            "company": r.get("company_name", ""),
            "sector": r.get("sector", ""),
            "contact": r.get("contact_name", ""),
            "phone": r.get("whatsapp", ""),
            "email": r.get("email", ""),
            "source": "intake_engine_v2",
            "offer": r.get("recommended_offer", ""),
            "status": "intake_processed",
            "next_action": r.get("next_action", ""),
            "next_followup_date": r.get("followup_date", ""),
            "deal_value_sar": offer_values.get(r.get("recommended_offer", ""), "12500"),
            "probability": tier_prob.get(r.get("tier", "D"), "10"),
            "notes": f"Tier {r.get('tier','')} | Score {r.get('fit_score','')} | {r.get('main_problem','')}",
        })

    with CRM.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=crm_fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(existing)


def main() -> None:
    template = write_template()
    rows = process_file(template)

    summary = write_summary(rows)
    write_whatsapp_drafts(rows)
    write_proposal_stubs(rows)
    if rows:
        update_crm(rows)

        with (OUT / "INTAKE_PROCESSED.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)

    print(f"OK Template:    {template}")
    print(f"OK Summary:     {summary}")
    print(f"OK Intakes:     {len(rows)} processed")
    if rows:
        tiers = {t: sum(1 for r in rows if r.get("tier") == t) for t in "ABCD"}
        for t, n in tiers.items():
            print(f"   Tier {t}: {n}")
    print(f"OK CRM:         {CRM}")


if __name__ == "__main__":
    main()
