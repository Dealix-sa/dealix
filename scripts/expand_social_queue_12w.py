#!/usr/bin/env python3
"""Append weeks 9–12 posts to social_content_queue.yaml from AEO calendar slugs."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "dealix/config/social_content_queue.yaml"

WEEKS_9_12 = [
    (9, 0, "founder_media", "معيار SOAEN", "soaen-standard", "Signal · Offer · Action · Evidence · Narrative — خمس فجوات قبل أي upsell."),
    (9, 1, "proof", "لماذا 10 leads؟", "10-lead-audit", "نبدأ بـ pilot صغير — أدلة حقيقية قبل التوسع."),
    (9, 2, "objection", "حوكمة AI قبل التوسع", "govern-ai-before-scale", "لا أتمتة إرسال — موافقة بشرية على كل لمسة خارجية."),
    (9, 3, "trust", "أين يضيع الإيراد؟", "revenue-leakage-after-ads", "بعد الإعلان: لا owner · لا evidence · لا next action."),
    (9, 4, "proof", "كرّر الإيقاع", "repeat-the-rhythm", "War Room · أدلة · مسودات · منشور SOAEN — يومياً."),
    (10, 0, "founder_media", "وكالة تبيع النتيجة", "agency-proof-for-clients", "Proof Pack أسبوعي لعميل الوكالة — ليس تقريراً عاماً."),
    (10, 1, "proof", "قائمة متابعة سعودية", "saudi-agency-follow-up-checklist", "15 دقيقة owner · موافقة · evidence · تاريخ."),
    (10, 2, "objection", "موافقة AI للمبيعات", "ai-approval-sales", "مسودة → موافقة → إرسال يدوي — PDPL وثقة."),
    (10, 3, "trust", "لا CRM جديد", "not-another-crm", "طبقة فوق CRM الحالي — قرار إيراد موثّق."),
    (10, 4, "proof", "من إعلان إلى قرار", "ad-to-decision", "الحملة تجيب lead — Revenue Ops يثبت المتابعة."),
    (11, 0, "founder_media", "تشغيل 95% / موافقة 5%", "sovereign-gtm-95-5", "النظام يجهّز اليوم — أنت توافق وتُرسل."),
    (11, 1, "proof", "أول Diagnostic مدفوع", "first-paid-diagnostic", "هدف تجاري: Diagnostic + Proof قبل ميزات."),
    (11, 2, "objection", "LinkedIn يدوي", "linkedin-manual-by-design", "لا DM آلي — مسودة + أنت ترسل."),
    (11, 3, "trust", "لا واتساب بارد", "no-cold-whatsapp-policy", "قوائم warm فقط — امتثال وثقة."),
    (11, 4, "proof", "Risk Score مجاني", "post-lead-revenue-ops", "ابدأ بقياس الجاهزية — ثم Proof Pack."),
    (12, 0, "founder_media", "Unified Revenue Atlas", "crm-vs-revenue-ops", "خريطة واحدة: استراتيجية + تكتيك + أدلة."),
    (12, 1, "proof", "Sample Proof Pack", "what-is-proof-pack", "عينة عامة قبل الشراء — أقسام وحالة."),
    (12, 2, "objection", "سعر مرتفع؟", "10-lead-audit", "ابدأ بـ 499 ر.س — pilot وليس عقد سنوي."),
    (12, 3, "trust", "شريك co-sell", "partner-intro", "Motion شركاء — عميل واحد مشترك."),
    (12, 4, "proof", "جاهز للتدشين", "governed-max-launch", "صفحة /ar · funnel · آلة يومية — Soft Launch."),
]


def main() -> int:
    data = yaml.safe_load(QUEUE.read_text(encoding="utf-8")) or {}
    posts = list(data.get("posts") or [])
    existing = {(int(p["week"]), int(p["day"])) for p in posts if "week" in p and "day" in p}
    added = 0
    for week, day, pillar, title_ar, slug, body_hint in WEEKS_9_12:
        if (week, day) in existing:
            continue
        posts.append(
            {
                "week": week,
                "day": day,
                "pillar": pillar,
                "title_ar": title_ar,
                "body_ar": f"{body_hint}\n\n#Dealix #RevenueOps #السعودية",
                "cta_ar": "Risk Score · Sample Proof · ديمو 10 دقائق",
                "aeo_slug": slug,
                "status": "draft",
            }
        )
        added += 1
    data["posts"] = posts
    data["cycle_weeks"] = 12
    QUEUE.write_text(
        yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )
    print(f"EXPAND_SOCIAL_QUEUE: added={added} total={len(posts)} cycle_weeks=12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
