"""Offer routing for the Dealix Now engine.

Selects the best-fit offer from ``os/03_OFFERS.yml`` using the routing logic in
``os/01_CLAUDE.md`` plus doctrine-aligned special cases, then returns the
offer's id/name/name_ar/entry price (loaded and cached from the YAML) along
with a deterministic Arabic ``why_fit_ar`` rationale.

Pure and deterministic: no network, no API keys, no LLM.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

log = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_OFFERS_YML = _REPO_ROOT / "os" / "03_OFFERS.yml"

# Offer id -> Arabic rationale template. Kept here (not in the YAML) so the
# YAML stays a pure catalog. Each line restates the documented fit.
_WHY_FIT_AR: dict[str, str] = {
    "RET": (
        "التشخيص أُنجز ونتائجه واضحة؛ الخطوة الطبيعية تحويلها لتشغيل شهري "
        "يحدّث التقارير ويتابع الـ SLA تلقائيًا."
    ),
    "AGP": (
        "قطاع منظَّم مع إلحاح ZATCA/PDPL؛ الحزمة تسلّم سياسة استخدام، مصفوفة "
        "صلاحيات، وبوابات موافقة بشرية خلال أسبوعين."
    ),
    "RAOS": (
        "تسرّب في الإيراد بسبب ضعف المتابعة؛ النظام يجهّز تسلسل متابعة ومسودات "
        "تواصل — أنتم تراجعون وترسلون."
    ),
    "PCOS": (
        "عمليات مشاريع كثيفة وأوامر تغيير؛ النظام يتتبع كل change order من الطلب "
        "حتى الفوترة وينبّه قبل ضياع الإيراد."
    ),
    "MIOS": (
        "صيانة وعمليات ميدانية وفنيون وSLA؛ النظام يدير البلاغات ويتابع الـ SLA "
        "ويولّد تقارير الإغلاق تلقائيًا."
    ),
    "ECC": (
        "مؤسسة كبيرة متعددة الأقسام؛ مركز القيادة يجمع تقارير الأقسام والمخاطر في "
        "لوحة تنفيذية واحدة تحدّث نفسها."
    ),
    "WFA": (
        "نقطة دخول آمنة منخفضة المخاطر: نحلل workflow واحدًا ونطلع خريطة فرص AI "
        "خلال 7 أيام قبل أي التزام أكبر."
    ),
}

# Sectors grouped by the doctrine routing buckets (os/01_CLAUDE.md).
_FM_SECTORS = {"facilities_management", "maintenance", "field_service", "industrial"}
_PROJECT_SECTORS = {"contracting", "pmo", "engineering"}
_ENTERPRISE_SECTORS = {"large_enterprise", "holding", "government_adjacent"}
_REVENUE_SECTORS = {"marketing_agency", "b2b_services"}


@lru_cache(maxsize=1)
def _load_offers() -> dict[str, dict[str, Any]]:
    """Load and cache the offers catalog keyed by offer id (e.g. ``WFA``)."""
    with _OFFERS_YML.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    offers: dict[str, dict[str, Any]] = {}
    for _slug, body in (raw.get("offers") or {}).items():
        oid = str(body.get("id") or "").strip()
        if oid:
            offers[oid] = body
    return offers


def _entry_price(offer: dict[str, Any]) -> dict[str, int]:
    """Normalize an offer's entry price to {min, max, typical} integers.

    Handles both ``price_sar`` and the retainer's ``price_sar_monthly``. When a
    catalog entry omits ``typical`` (open-ended offers), it is derived as the
    midpoint so downstream pipeline maths always has a value.
    """
    price = offer.get("price_sar") or offer.get("price_sar_monthly") or {}
    pmin = int(price.get("min", 0) or 0)
    pmax = int(price.get("max", 0) or 0)
    typical = price.get("typical")
    if typical is None:
        typical = (pmin + pmax) // 2 if (pmin or pmax) else 0
    return {"min": pmin, "max": pmax, "typical": int(typical)}


def _select_offer_id(target: dict, score: dict, notes: str, sector: str, status: str) -> str:
    """Return the offer id per doctrine priority order."""
    # 1. Warm + prior diagnostic / retainer intent -> AI Ops Retainer.
    if status == "warm" and ("diagnostic" in notes or "retainer" in notes):
        return "RET"

    # 2. Regulated / healthcare with an active compliance driver -> Governance
    # Pack. The driver must be a regulatory event or obligation (ZATCA wave,
    # PDPL obligation, a flagged compliance risk) — not merely the presence of
    # sensitive data. A clinic that only notes "PII-heavy, manual review" has
    # no active regulatory deadline, so it routes to the safe entry audit
    # instead (matching the golden sample: Alshifa=AGP with a ZATCA deadline,
    # NorthStar=WFA with only a data caution).
    regulated_sector = sector in {"healthcare", "financial_services", "insurance", "legal"}
    compliance_driver = any(
        k in notes
        for k in ("zatca", "pdpl", "compliance", "regulat", "governance", "امتثال", "حوكمة")
    )
    if (regulated_sector or compliance_driver) and compliance_driver:
        return "AGP"

    # 3. Marketing / B2B services with a revenue / follow-up leak -> Revenue AI OS.
    if sector in _REVENUE_SECTORS and any(
        k in notes
        for k in (
            "revenue",
            "leak",
            "follow-up",
            "follow up",
            "losing",
            "proposals",
            "تسرّب",
            "متابعة",
        )
    ):
        return "RAOS"

    # 4. Engineering / contracting / PMO -> Project Controls AI OS.
    if sector in _PROJECT_SECTORS:
        return "PCOS"

    # 5. FM / maintenance / field / industrial -> Maintenance Intelligence OS.
    if sector in _FM_SECTORS:
        return "MIOS"

    # 6. Large enterprise / holding -> Executive Command Center.
    if sector in _ENTERPRISE_SECTORS or "holding" in notes:
        return "ECC"

    # 7. Safe default entry point -> AI Workflow Audit.
    return "WFA"


def route_offer(target: dict, score: dict) -> dict:
    """Route a scored target to its recommended offer.

    Returns ``{id, name, name_ar, why_fit_ar, entry_price_sar:{min,max,typical}}``
    with names and prices sourced from ``os/03_OFFERS.yml``.
    """
    notes = (target.get("notes") or "").lower()
    sector = (target.get("sector") or "").strip().lower()
    status = (target.get("relationship_status") or "").strip().lower()

    offers = _load_offers()
    offer_id = _select_offer_id(target, score, notes, sector, status)
    offer = offers.get(offer_id)
    if offer is None:
        # Defensive fallback: the safe entry offer must always exist.
        offer_id = "WFA"
        offer = offers.get(offer_id, {})

    return {
        "id": offer_id,
        "name": str(offer.get("name", "")),
        "name_ar": str(offer.get("name_ar", "")),
        "why_fit_ar": _WHY_FIT_AR.get(offer_id, _WHY_FIT_AR["WFA"]),
        "entry_price_sar": _entry_price(offer),
    }


__all__ = ["route_offer"]
