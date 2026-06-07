"""Daily Now pack orchestrator for the Dealix Now engine.

``build_now_pack`` runs the full deterministic pipeline:

    load targets -> score -> route offer -> brief -> draft (high/medium only)
    -> safety -> assemble metrics / pipeline / priorities / intelligence

The returned dict matches the frozen contract in
``apps/web/public/now-pack.json`` exactly (same top-level keys and lead/draft
shapes). ``is_sample`` is False for engine output. ``build_now_pack`` does not
write files.

Pure and deterministic given ``today`` and the seed dataset: no network, no API
keys, no LLM, no implicit clock reads beyond the optional ``today`` default.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from dealix.now.brief import write_company_brief
from dealix.now.draft import write_outreach_draft
from dealix.now.offer_router import route_offer
from dealix.now.safety import check_draft_safety
from dealix.now.scoring import score_company
from dealix.now.seed import load_targets

log = logging.getLogger(__name__)

SCHEMA_VERSION = "now-pack/1.0"
_TZ_NAME = "Asia/Riyadh"
_RIYADH = timezone(timedelta(hours=3), name=_TZ_NAME)

# Founder daily targets (os/10 / Founder Operating Manual).
_FOUNDER_DAILY_TARGETS = {
    "company_briefs": 20,
    "drafts": 20,
    "follow_ups": 5,
    "proposals": 1,
}

# Sector -> Arabic label.
SECTOR_AR: dict[str, str] = {
    "logistics": "الخدمات اللوجستية",
    "engineering": "الهندسة والاستشارات",
    "contracting": "المقاولات وإدارة المشاريع",
    "healthcare": "الرعاية الصحية",
    "food_and_beverage": "الأغذية والمشروبات",
    "marketing_agency": "وكالة تسويق",
    "b2b_services": "الخدمات المهنية B2B",
    "training": "التدريب والتطوير",
    "real_estate": "الخدمات العقارية",
    "technology": "التقنية",
    "ecommerce": "التجارة الإلكترونية",
    "aviation": "خدمات الطيران",
    "facilities_management": "إدارة المرافق والصيانة",
    "maintenance": "الصيانة والعمليات الميدانية",
    "industrial": "الصناعة والتصنيع",
}

# Sector -> best buyer title (from os/04_MARKETS.yml best_buyer_titles).
BEST_BUYER_TITLE: dict[str, str] = {
    "logistics": "Operations Director",
    "engineering": "PMO Director",
    "contracting": "Project Director",
    "healthcare": "General Manager",
    "food_and_beverage": "Operations Manager",
    "marketing_agency": "Managing Partner",
    "b2b_services": "Managing Partner",
    "training": "Managing Director",
    "real_estate": "Operations Director",
    "technology": "COO",
    "ecommerce": "Operations Manager",
    "aviation": "Operations Director",
    "facilities_management": "FM Director",
    "maintenance": "Maintenance Manager",
    "industrial": "Plant Manager",
}
_DEFAULT_BUYER_TITLE = "Operations Director"

# Offer id -> default Arabic pain points (operational, not row-specific). Row
# signals from the brief are layered on top when present.
_OFFER_PAINS: dict[str, list[str]] = {
    "RET": [
        "متابعة تقارير العمليات يدويًا أسبوعيًا",
        "تتبّع SLA للشحنات",
        "قرار التشغيل المستمر متوقف",
    ],
    "PCOS": [
        "تسرّب الإيراد في فوترة أوامر التغيير",
        "تقارير التقدم الأسبوعية يدوية",
        "متابعة الموافقات المعلقة",
    ],
    "AGP": [
        "جاهزية ZATCA قبل الموعد",
        "التزامات PDPL على البيانات الحساسة",
        "أتمتة بلا إطار حوكمة = خطر",
    ],
    "RAOS": ["فقدان فرص بعد الديمو", "متابعة يدوية ضعيفة", "لا تسلسل متابعة منظّم"],
    "MIOS": ["متابعة البلاغات يدويًا", "تأخّر إشعارات تجاوز SLA", "تقارير الفنيين متأخرة"],
    "ECC": ["تجميع تقارير الأقسام يدويًا", "تأخّر وصول المخاطر للإدارة", "لا رؤية موحّدة"],
    "WFA": ["عمليات يدوية متكررة", "تقارير دورية تستهلك وقتًا", "لا خريطة واضحة لفرص الأتمتة"],
}


def _now_riyadh() -> datetime:
    return datetime.now(_RIYADH)


def _resolve_today(today: Any) -> datetime:
    """Resolve the ``today`` argument to a Riyadh-tz-aware datetime."""
    if today is None:
        return _now_riyadh()
    if isinstance(today, datetime):
        if today.tzinfo is None:
            return today.replace(tzinfo=_RIYADH)
        return today
    # Accept a date string (YYYY-MM-DD) or date object.
    text = str(today)
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        dt = datetime.strptime(text, "%Y-%m-%d")
    if dt.tzinfo is None:
        # Default the brief's generation moment to 08:00 Riyadh for stability.
        dt = dt.replace(hour=8, minute=0, second=0, microsecond=0, tzinfo=_RIYADH)
    return dt


def _pain_points(offer_id: str, brief: dict) -> list[str]:
    """Offer baseline pains, with the first public signal surfaced if useful."""
    pains = list(_OFFER_PAINS.get(offer_id, _OFFER_PAINS["WFA"]))
    return pains


def _next_action(tier: str) -> str:
    if tier in ("high", "medium"):
        return "draft"
    if tier == "nurture":
        return "nurture"
    return "archive"


def _build_lead(target: dict, score: dict, offer: dict, brief: dict) -> dict:
    sector = (target.get("sector") or "").strip().lower()
    tier = score["tier"]
    return {
        "id": target.get("id", ""),
        "company_name": target.get("company_name", ""),
        "sector": sector,
        "sector_ar": SECTOR_AR.get(sector, sector),
        "city": target.get("city", ""),
        "website": "",
        "source": target.get("source", ""),
        "relationship_status": target.get("relationship_status", ""),
        "fit_score": score["total_score"],
        "tier": tier,
        "tier_color": score["tier_color"],
        "tier_action_ar": score["tier_action_ar"],
        "dimension_scores": score["dimension_scores"],
        "top_strengths": score["top_strengths"],
        "top_weaknesses": score["top_weaknesses"],
        "best_buyer_title": BEST_BUYER_TITLE.get(sector, _DEFAULT_BUYER_TITLE),
        "pain_points": _pain_points(offer["id"], brief),
        "recommended_offer": offer,
        "next_action": _next_action(tier),
        "brief": brief,
    }


def _build_draft(target: dict, score: dict, offer: dict) -> dict | None:
    draft = write_outreach_draft(target, score, offer)
    if draft is None:
        return None
    draft["safety"] = check_draft_safety(draft)
    return draft


def _round1(value: float) -> float:
    return round(value, 1)


def _assemble_metrics(leads: list[dict], drafts: list[dict]) -> dict:
    tiers = {"high": 0, "medium": 0, "nurture": 0, "disqualified": 0}
    for lead in leads:
        tiers[lead["tier"]] = tiers.get(lead["tier"], 0) + 1

    avg = _round1(sum(lead["fit_score"] for lead in leads) / len(leads)) if leads else 0.0

    low = sum(lead["recommended_offer"]["entry_price_sar"]["min"] for lead in leads)
    typical = sum(lead["recommended_offer"]["entry_price_sar"]["typical"] for lead in leads)
    high = sum(lead["recommended_offer"]["entry_price_sar"]["max"] for lead in leads)

    return {
        "leads_total": len(leads),
        "priority_high": tiers["high"],
        "priority_medium": tiers["medium"],
        "nurture": tiers["nurture"],
        "disqualified": tiers["disqualified"],
        "drafts_ready": len(drafts),
        "avg_fit_score": avg,
        "founder_daily_targets": dict(_FOUNDER_DAILY_TARGETS),
        "pipeline_value_sar": {"low": low, "typical": typical, "high": high},
    }


def _deals_at_risk(leads: list[dict]) -> int:
    """A warm, high-fit lead with a stalled prior decision is a deal at risk."""
    risk = 0
    for lead in leads:
        notes_signals = lead["brief"].get("public_signals", [])
        if lead["relationship_status"] == "warm" and any(
            "retainer" in s or "معلّق" in s or "بانتظار قرار" in s for s in notes_signals
        ):
            risk += 1
    return risk


def _assemble_pipeline(leads: list[dict], drafts: list[dict]) -> dict:
    return {
        "new_leads_24h": len(leads),
        "drafts_awaiting": len(drafts),
        "replies_to_handle": 0,
        "calls_today": 0,
        "proposals_pending": 0,
        "deals_at_risk": _deals_at_risk(leads),
    }


def _urgency_rank(lead: dict) -> tuple:
    """Sort key for priorities: regulatory urgency, then warm+stalled, then fit.

    Returns a tuple compared descending. Higher = more urgent.
    """
    signals = lead["brief"].get("public_signals", [])
    zatca = any("ZATCA" in s for s in signals)
    stalled = lead["relationship_status"] == "warm" and any(
        "retainer" in s or "بانتظار قرار" in s for s in signals
    )
    return (
        1 if stalled and lead["tier"] == "high" else 0,
        1 if zatca else 0,
        lead["fit_score"],
    )


def _build_priorities(leads: list[dict]) -> list[dict]:
    """Top-3 priorities ranked by urgency signals + fit score."""
    draftable = [lead for lead in leads if lead["next_action"] == "draft"]
    ranked = sorted(draftable, key=_urgency_rank, reverse=True)[:3]

    priorities: list[dict] = []
    for idx, lead in enumerate(ranked, start=1):
        signals = lead["brief"].get("public_signals", [])
        zatca = any("ZATCA" in s for s in signals)
        stalled = lead["relationship_status"] == "warm" and any(
            "retainer" in s or "بانتظار قرار" in s for s in signals
        )
        if stalled:
            what = f"أغلق قرار العرض المعلّق مع {lead['company_name']}"
            why = "أعلى lead دافئ بقرار متوقف — أقرب إيراد متكرر."
            minutes = 30
        elif zatca:
            what = f"خصّص وأرسل draft {lead['company_name']} قبل فوات موعد ZATCA"
            why = "موعد ZATCA المقبل — الإلحاح التنظيمي يفتح الباب الآن تحديدًا."
            minutes = 20
        else:
            what = f"راجع draft {lead['company_name']} وحدّد جهة الاتصال"
            why = f"ملاءمة قوية ({lead['fit_score']}/100) وعرض {lead['recommended_offer']['id']} مناسب."
            minutes = 20
        priorities.append(
            {
                "rank": idx,
                "what_ar": what,
                "why_now_ar": why,
                "est_minutes": minutes,
                "linked_lead_id": lead["id"],
            }
        )
    return priorities


def _build_intelligence_alerts(leads: list[dict]) -> list[str]:
    alerts: list[str] = []
    has_regulated = any(
        lead["sector"] in ("healthcare",)
        or any("ZATCA" in s or "PDPL" in s for s in lead["brief"].get("public_signals", []))
        for lead in leads
    )
    if has_regulated:
        alerts.append(
            "موعد ZATCA Wave 24 (يونيو 2026) قريب — استخدمه كزاوية تواصل للقطاعات المنظَّمة (الصحة، الخدمات المالية)."
        )
        alerts.append("PDPL مفعّل بغرامات مرتفعة — حزمة الحوكمة (AGP) مدخل قوي للشركات المترددة.")
    for lead in leads:
        if lead["relationship_status"] == "warm" and any(
            "retainer" in s or "بانتظار قرار" in s for s in lead["brief"].get("public_signals", [])
        ):
            alerts.append(
                f"صفقة في خطر: قرار العرض لـ {lead['company_name']} معلّق منذ فترة — تابع اليوم."
            )
    if not alerts:
        alerts.append("لا توجد تنبيهات حرجة اليوم — ركّز على أعلى leads حسب الأولويات.")
    return alerts


def build_now_pack(targets: list[dict] | None = None, today: Any = None) -> dict:
    """Assemble the full DailyNowPack dict (does not write files)."""
    rows = targets if targets is not None else load_targets()
    when = _resolve_today(today)

    leads: list[dict] = []
    drafts: list[dict] = []
    for target in rows:
        score = score_company(target)
        offer = route_offer(target, score)
        brief = write_company_brief(target, score, offer)
        leads.append(_build_lead(target, score, offer, brief))
        draft = _build_draft(target, score, offer)
        if draft is not None:
            drafts.append(draft)

    metrics = _assemble_metrics(leads, drafts)
    pipeline = _assemble_pipeline(leads, drafts)
    priorities = _build_priorities(leads)
    intelligence_alerts = _build_intelligence_alerts(leads)

    return {
        "$schema_version": SCHEMA_VERSION,
        "generated_at": when.isoformat(),
        "date": when.date().isoformat(),
        "tz": _TZ_NAME,
        "is_sample": False,
        "note_ar": (
            "مولّد من نظام Dealix Now على بيانات المستودع الحقيقية. تقرير داخلي "
            "للقراءة فقط — لا إرسال تلقائي لأي طرف خارجي."
        ),
        "doctrine": {
            "no_auto_send": True,
            "no_scraping": True,
            "public_data_only": True,
            "approval_first": True,
            "tagline_ar": "AI يكتب، أنت ترسل",
        },
        "metrics": metrics,
        "pipeline": pipeline,
        "leads": leads,
        "drafts": drafts,
        "priorities": priorities,
        "intelligence_alerts": intelligence_alerts,
    }


__all__ = ["SCHEMA_VERSION", "build_now_pack"]
