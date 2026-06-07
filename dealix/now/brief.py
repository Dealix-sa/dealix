"""Company brief writer for the Dealix Now engine (Company Research Agent).

Produces the deterministic ``brief`` sub-object used in the Now pack:
``{what_they_do_ar, operations_complexity, public_signals, confidence}``.

No hallucinated facts: every statement either restates a field already present
in the row (sector, city, notes) or is generic sector knowledge. Inferred
public signals are extracted from the notes verbatim-ish (translated to the
brief's register) and never invented. Confidence is lower for cold / low-data
rows.

Pure and deterministic: no network, no API keys, no LLM.
"""

from __future__ import annotations

# Arabic "what they do" templates keyed by sector. ``{city}`` is filled from
# the row. These describe the sector generically; row-specific facts come from
# public_signals only.
_WHAT_TEMPLATES: dict[str, str] = {
    "logistics": "شركة خدمات لوجستية ونقل في {city} بعمليات يومية كثيفة.",
    "engineering": "مكتب هندسة واستشارات في {city} يدير مشاريع متعددة.",
    "contracting": "شركة مقاولات وإدارة مشاريع في {city}.",
    "healthcare": "مجمع رعاية صحية متعدد التخصصات في {city}.",
    "food_and_beverage": "سلسلة مطاعم في {city} تعتمد على الحجوزات والفروع.",
    "marketing_agency": "وكالة تسويق رقمي في {city}.",
    "b2b_services": "شركة خدمات مهنية B2B في {city}.",
    "training": "جهة تدريب وتطوير مهني في {city}.",
    "real_estate": "شركة خدمات عقارية في {city}.",
    "technology": "شركة تقنية / SaaS في {city}.",
    "ecommerce": "متجر تجارة إلكترونية في {city}.",
    "aviation": "شركة خدمات طيران في {city}.",
    "facilities_management": "شركة إدارة مرافق وصيانة في {city}.",
    "maintenance": "شركة صيانة وعمليات ميدانية في {city}.",
    "industrial": "منشأة صناعية / تصنيع في {city}.",
}

_DEFAULT_WHAT = "شركة في قطاع {sector} في {city}."

# Note-keyword -> Arabic public-signal phrasing. Order is stable so output is
# deterministic. Only signals whose keyword is present are emitted.
_SIGNAL_RULES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("diagnostic delivered", "previous diagnostic", "diagnostic"), "تشخيص سابق مُسلَّم"),
    (("awaiting retainer", "retainer decision"), "بانتظار قرار retainer"),
    (("paid diagnostic", "eligible for sprint"), "تشخيص مدفوع سابق — مؤهّل لـ Sprint"),
    (("proof pack", "proof-pack"), "Proof Pack نشط قيد الإعداد"),
    (("zatca", "wave 24"), "موعد ZATCA Wave 24 (يونيو 2026)"),
    (("pdpl",), "إلحاح PDPL مُعلَّم"),
    (("pii", "patient", "مرضى"), "بيانات PII حساسة"),
    (
        ("multi-branch", "multi branch", "branches", "فروع", "فرع", "12 branches"),
        "عمليات متعددة الفروع",
    ),
    (("no-show", "no show", "appointment loss"), "نسبة عدم حضور مرتفعة في الحجوزات"),
    (("revenue leak", "leakage", "change-order billing"), "تسرّب محتمل في الإيراد"),
    (("follow-up", "follow up", "proposals after demo"), "ضعف نظام المتابعة"),
    (("crm gap", "losing", "pre-qualification"), "فجوة CRM تُفقد عملاء محتملين"),
    (("chatbot", "without governance"), "أتمتة منشورة دون إطار حوكمة"),
    (("senior sponsor", "sponsor identified"), "راعٍ تنفيذي محدَّد"),
    (("clean data",), "بيانات نظيفة"),
    (
        ("legacy crm", "stale", "data quality untested", "untested", "low data", "mixed sources"),
        "جودة بيانات غير مؤكدة",
    ),
    (("inbound",), "استفسار وارد حديث"),
)


def _operations_complexity(score: dict) -> str:
    """Map the operations_complexity dimension level to low/medium/high."""
    for dim in score.get("dimension_scores", []):
        if dim.get("id") == "operations_complexity":
            level = dim.get("level")
            if level == "high":
                return "high"
            if level == "medium":
                return "medium"
            return "low"
    return "medium"


def _public_signals(notes: str) -> list[str]:
    notes_l = notes.lower()
    seen: set[str] = set()
    signals: list[str] = []
    for keys, phrase in _SIGNAL_RULES:
        if any(k in notes_l for k in keys) and phrase not in seen:
            signals.append(phrase)
            seen.add(phrase)
    return signals


def _confidence(target: dict, signals: list[str]) -> float:
    """Confidence in [0.4, 0.7], lower for cold / low-data rows.

    Warm relationships and richer public signals raise confidence; cold rows
    and explicit data-quality flags lower it.
    """
    status = (target.get("relationship_status") or "").strip().lower()
    notes_l = (target.get("notes") or "").lower()
    score = 0.5
    if status == "warm":
        score += 0.1
    elif status == "cold":
        score -= 0.05
    if len(signals) >= 2:
        score += 0.05
    if any(
        k in notes_l
        for k in (
            "untested",
            "data quality",
            "low data",
            "mixed sources",
            "unclear",
            "legacy crm",
            "empty fields",
        )
    ):
        score -= 0.1
    # Clamp and round to one decimal for a stable, human-readable value.
    return round(max(0.4, min(0.7, score)), 2)


def write_company_brief(target: dict, score: dict, offer: dict) -> dict:
    """Build the deterministic company brief sub-object.

    Returns ``{what_they_do_ar, operations_complexity, public_signals,
    confidence}``. ``offer`` is accepted for interface symmetry with the rest
    of the pipeline but the brief restates only row + sector facts.
    """
    sector = (target.get("sector") or "").strip().lower()
    city = (target.get("city") or "").strip() or "—"
    notes = target.get("notes") or ""

    template = _WHAT_TEMPLATES.get(sector, _DEFAULT_WHAT)
    what_they_do_ar = template.format(city=city, sector=sector or "أعمال")

    signals = _public_signals(notes)
    return {
        "what_they_do_ar": what_they_do_ar,
        "operations_complexity": _operations_complexity(score),
        "public_signals": signals,
        "confidence": _confidence(target, signals),
    }


__all__ = ["write_company_brief"]
