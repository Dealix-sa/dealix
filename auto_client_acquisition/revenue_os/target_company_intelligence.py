"""Target Company Intelligence — deterministic dossier + governed draft layer.

Pure, import-safe, no I/O, no LLM. Every number is a deterministic estimate
computed from declared, founder-provided inputs only. The system NEVER fetches
external data and NEVER invents facts about a named real company.

Doctrine:
  - All facts come from declared inputs (no scraping / web collection).
  - Every number carries ``is_estimate: true`` and ``assumptions``.
  - Structural weaknesses are derived from declared fields only; declared
    weaknesses are operator hypotheses (``is_hypothesis: true``).
  - All outreach is draft-only and queued for human approval.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.data_os.data_quality_score import account_row_completeness
from auto_client_acquisition.revenue_os.draft_pack import build_revenue_draft_pack
from auto_client_acquisition.revenue_os.scoring import score_account_row
from auto_client_acquisition.safe_send_gateway import enforce_doctrine_non_negotiables

# Required keys used for completeness + scoring (mirrors scoring defaults).
_REQUIRED_KEYS: tuple[str, ...] = ("company_name", "sector", "city", "source")

_TRUST_RELATIONSHIPS = ("warm_intro", "explicit_consent", "contracted")

# Catalog of structural weakness codes. Each maps to a deterministic offer.
WEAKNESS_CATALOG: dict[str, dict[str, str]] = {
    "untracked_source": {
        "label_ar": "مصدر غير موثّق",
        "label_en": "Untracked source",
        "severity": "high",
        "implied_offer": "data_pack",
        "angle_ar": "نوثّق مصدر كل عميل محتمل لتصبح القرارات قابلة للتدقيق.",
        "angle_en": "We document every lead source so decisions become auditable.",
    },
    "incomplete_profile": {
        "label_ar": "ملف ناقص",
        "label_en": "Incomplete profile",
        "severity": "medium",
        "implied_offer": "data_pack",
        "angle_ar": "نكمل الحقول الناقصة من بياناتكم المعلنة لرفع جودة البيانات.",
        "angle_en": "We complete missing fields from your declared data to raise data quality.",
    },
    "stale_relationship": {
        "label_ar": "علاقة متوقفة",
        "label_en": "Stale relationship",
        "severity": "medium",
        "implied_offer": "revenue_ops",
        "angle_ar": "نعيد تنشيط العلاقات المتوقفة بمتابعة محكومة كمسودة فقط.",
        "angle_en": "We re-activate stalled relationships with governed draft-only follow-up.",
    },
    "sector_outside_icp": {
        "label_ar": "قطاع خارج الملف المثالي",
        "label_en": "Sector outside ICP",
        "severity": "low",
        "implied_offer": "diagnostic",
        "angle_ar": "نقيّم الملاءمة قبل الاستثمار في القطاعات خارج ملفكم المثالي.",
        "angle_en": "We assess fit before investing in sectors outside your ICP.",
    },
    "no_followup_owner": {
        "label_ar": "لا مالك للمتابعة",
        "label_en": "No follow-up owner",
        "severity": "high",
        "implied_offer": "managed_ops",
        "angle_ar": "نسند مالكًا واضحًا لكل متابعة حتى لا تضيع الفرص.",
        "angle_en": "We assign a clear owner to every follow-up so deals do not slip.",
    },
    "slow_first_response": {
        "label_ar": "بطء أول استجابة",
        "label_en": "Slow first response",
        "severity": "high",
        "implied_offer": "revenue_ops",
        "angle_ar": "نختصر زمن أول استجابة عبر مسارات متابعة محكومة.",
        "angle_en": "We cut first-response time with governed follow-up workflows.",
    },
    "no_proof": {
        "label_ar": "لا إثبات",
        "label_en": "No proof",
        "severity": "medium",
        "implied_offer": "proof_pack",
        "angle_ar": "نبني حزمة إثبات من نتائجكم الحقيقية فقط — بلا أرقام مخترعة.",
        "angle_en": "We build a proof pack from your real results only — no invented numbers.",
    },
    "low_data_quality": {
        "label_ar": "جودة بيانات منخفضة",
        "label_en": "Low data quality",
        "severity": "medium",
        "implied_offer": "data_pack",
        "angle_ar": "نرفع جودة البيانات بمقاييس شفافة قابلة للتدقيق.",
        "angle_en": "We raise data quality with transparent, auditable metrics.",
    },
    "no_clear_offer": {
        "label_ar": "لا عرض واضح",
        "label_en": "No clear offer",
        "severity": "medium",
        "implied_offer": "diagnostic",
        "angle_ar": "نبلور عرضًا واضحًا مبنيًا على نقاط القوة المعلنة لديكم.",
        "angle_en": "We crystallize a clear offer built on your declared strengths.",
    },
    "manual_excel_ops": {
        "label_ar": "عمليات يدوية على إكسل",
        "label_en": "Manual Excel ops",
        "severity": "medium",
        "implied_offer": "managed_ops",
        "angle_ar": "نحوّل العمليات اليدوية إلى مسارات محكومة قابلة للتكرار.",
        "angle_en": "We turn manual spreadsheet ops into governed, repeatable workflows.",
    },
}

_SEVERITY_RANK = {"high": 3, "medium": 2, "low": 1}
_SEVERITY_BONUS = {"high": 15, "medium": 8, "low": 3}


def _catalog_weakness(code: str, *, evidence: str, is_hypothesis: bool) -> dict[str, Any]:
    """Build a normalized weakness dict from a known catalog code."""
    entry = WEAKNESS_CATALOG[code]
    return {
        "code": code,
        "label_ar": entry["label_ar"],
        "label_en": entry["label_en"],
        "severity": entry["severity"],
        "implied_offer": entry["implied_offer"],
        "evidence": evidence,
        "is_hypothesis": is_hypothesis,
    }


def detect_structural_weaknesses(
    company: dict[str, Any],
    *,
    icp_sectors: frozenset[str] | None = None,
    icp_cities: frozenset[str] | None = None,
) -> list[dict[str, Any]]:
    """Derive deterministic structural weaknesses from declared fields + scoring.

    Rules (declared-only):
      - missing/empty ``source`` -> ``untracked_source``
      - ``account_row_completeness`` < 1.0 -> ``incomplete_profile``
      - ``last_contact_days`` > 60 -> ``stale_relationship``
      - scoring risk ``sector_outside_icp`` present -> ``sector_outside_icp``

    ``sector_outside_icp`` only fires when ``icp_sectors`` is supplied, since the
    risk is relative to a declared ICP.
    """
    weaknesses: list[dict[str, Any]] = []

    src = company.get("source")
    if src is None or not str(src).strip():
        weaknesses.append(
            _catalog_weakness(
                "untracked_source",
                evidence="declared field 'source' missing or empty",
                is_hypothesis=False,
            )
        )

    completeness = account_row_completeness(company, _REQUIRED_KEYS)
    if completeness < 1.0:
        weaknesses.append(
            _catalog_weakness(
                "incomplete_profile",
                evidence=(
                    f"account_row_completeness={round(completeness, 4)} "
                    f"over required keys {list(_REQUIRED_KEYS)}"
                ),
                is_hypothesis=False,
            )
        )

    lcd = company.get("last_contact_days")
    try:
        days = int(lcd)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        days = None
    if days is not None and days > 60:
        weaknesses.append(
            _catalog_weakness(
                "stale_relationship",
                evidence=f"declared last_contact_days={days} (> 60)",
                is_hypothesis=False,
            )
        )

    scoring = score_account_row(
        company, icp_sectors=icp_sectors, icp_cities=icp_cities
    )
    if "sector_outside_icp" in scoring.get("risks", []):
        weaknesses.append(
            _catalog_weakness(
                "sector_outside_icp",
                evidence="icp scoring risk 'sector_outside_icp'",
                is_hypothesis=False,
            )
        )

    return weaknesses


def declared_weaknesses_to_signals(
    company: dict[str, Any],
) -> list[dict[str, Any]]:
    """Map ``company['declared_weaknesses']`` (catalog codes) into signals.

    These are operator hypotheses, not verified facts (``is_hypothesis: true``).
    Unknown codes are skipped (see :func:`split_declared_weaknesses` to inspect
    which codes were ignored).
    """
    known, _ignored = split_declared_weaknesses(company)
    return known


def split_declared_weaknesses(
    company: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Return (known_signals, ignored_codes) for declared weaknesses."""
    declared = company.get("declared_weaknesses") or []
    known: list[dict[str, Any]] = []
    ignored: list[str] = []
    for raw in declared:
        code = str(raw).strip()
        if code in WEAKNESS_CATALOG:
            known.append(
                _catalog_weakness(
                    code,
                    evidence="declared_by_operator",
                    is_hypothesis=True,
                )
            )
        else:
            ignored.append(code)
    return known, ignored


def _merge_weaknesses(
    company: dict[str, Any],
    *,
    icp_sectors: frozenset[str] | None = None,
    icp_cities: frozenset[str] | None = None,
) -> list[dict[str, Any]]:
    """Structural + declared weaknesses, de-duplicated by code (structural wins)."""
    merged: dict[str, dict[str, Any]] = {}
    for w in detect_structural_weaknesses(
        company, icp_sectors=icp_sectors, icp_cities=icp_cities
    ):
        merged[w["code"]] = w
    for w in declared_weaknesses_to_signals(company):
        merged.setdefault(w["code"], w)
    return list(merged.values())


def _filter_public_observations(
    company: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Keep only public_observations that carry a non-empty source.

    Returns (kept, notes). Unsourced observations are dropped and noted —
    never passed through as facts.
    """
    kept: list[dict[str, Any]] = []
    notes: list[str] = []
    for obs in company.get("public_observations") or []:
        if not isinstance(obs, dict):
            notes.append("dropped non-dict public observation (no verifiable source)")
            continue
        text = str(obs.get("observation") or "").strip()
        source = str(obs.get("source") or "").strip()
        if text and source:
            kept.append({"observation": text, "source": source})
        else:
            notes.append("dropped public observation without a non-empty source")
    return kept, notes


def _highest_severity_weakness(
    weaknesses: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not weaknesses:
        return None
    return max(weaknesses, key=lambda w: _SEVERITY_RANK.get(w["severity"], 0))


def _priority_band(score: int) -> str:
    if score >= 80:
        return "P0"
    if score >= 60:
        return "P1"
    if score >= 40:
        return "P2"
    return "P3"


def build_company_dossier(
    company: dict[str, Any],
    *,
    icp_sectors: frozenset[str] | None = None,
    icp_cities: frozenset[str] | None = None,
) -> dict[str, Any]:
    """Build the deterministic dossier ("numbers and information") for a company.

    Every numeric output is labeled as an estimate. Facts come from declared
    inputs only; unsourced public observations are dropped, never asserted.
    """
    scoring = score_account_row(
        company, icp_sectors=icp_sectors, icp_cities=icp_cities
    )
    completeness = account_row_completeness(company, _REQUIRED_KEYS)
    weaknesses = _merge_weaknesses(
        company, icp_sectors=icp_sectors, icp_cities=icp_cities
    )
    kept_observations, observation_notes = _filter_public_observations(company)

    icp_score = int(scoring["score"])

    severity_bonus = 0
    for w in weaknesses:
        severity_bonus += _SEVERITY_BONUS.get(w["severity"], 0)
    severity_bonus = min(severity_bonus, 25)

    bonus = 0
    if bool(company.get("manual_priority")):
        bonus += 10
    rs = str(company.get("relationship_status") or "").strip().lower()
    if rs in _TRUST_RELATIONSHIPS:
        bonus += 5

    priority_score = int(
        max(0, min(100, round(0.6 * icp_score + severity_bonus + bonus)))
    )
    priority_band = _priority_band(priority_score)

    top = _highest_severity_weakness(weaknesses)
    recommended_offer = top["implied_offer"] if top is not None else "diagnostic"

    if weaknesses or kept_observations:
        if top is not None:
            why_now_ar = f"إشارة بنيوية: {top['label_ar']} — {top['evidence']}"
            why_now_en = f"Structural signal: {top['label_en']} — {top['evidence']}"
        else:
            first = kept_observations[0]
            why_now_ar = f"ملاحظة مصدّرة: {first['observation']} (المصدر: {first['source']})"
            why_now_en = f"Sourced observation: {first['observation']} (source: {first['source']})"
    else:
        why_now_ar = "لا توجد إشارة معلنة بعد"
        why_now_en = "No declared signal yet"

    assumptions = [
        "كل الأرقام تقديرية من بيانات معلنة فقط — لا جمع خارجي",
        "All numbers are estimates from declared inputs only — no external collection",
    ]
    if observation_notes:
        assumptions.extend(observation_notes)

    return {
        "company_name": company.get("company_name"),
        "sector": company.get("sector"),
        "city": company.get("city"),
        "source": company.get("source"),
        "icp_fit": {
            "score": icp_score,
            "reasons": scoring["reasons"],
            "risks": scoring["risks"],
            "is_estimate": True,
        },
        "data_quality": {
            "completeness_pct": round(completeness * 100, 1),
            "is_estimate": True,
        },
        "weaknesses": weaknesses,
        "public_observations": kept_observations,
        "priority_score": priority_score,
        "priority_band": priority_band,
        "recommended_offer": recommended_offer,
        "why_now_ar": why_now_ar,
        "why_now_en": why_now_en,
        "assumptions": assumptions,
        "governance": {
            "draft_only": True,
            "approval_required": True,
            "no_external_send_without_approval": True,
        },
    }


def build_target_company_draft(
    company: dict[str, Any],
    dossier: dict[str, Any],
    *,
    request_cold_whatsapp: bool = False,
    request_linkedin_automation: bool = False,
    request_scraping: bool = False,
    request_bulk_outreach: bool = False,
    include_whatsapp_draft: bool = False,
) -> dict[str, Any]:
    """Build a governed, draft-only outreach pack augmented with the offer angle.

    Enforces doctrine non-negotiables first; ``request_fake_proof`` is never set.
    """
    enforce_doctrine_non_negotiables(
        request_cold_whatsapp=request_cold_whatsapp,
        request_linkedin_automation=request_linkedin_automation,
        request_scraping=request_scraping,
        request_bulk_outreach=request_bulk_outreach,
        request_fake_proof=False,
    )

    pack = build_revenue_draft_pack(
        company,
        request_cold_whatsapp=request_cold_whatsapp,
        request_linkedin_automation=request_linkedin_automation,
        request_scraping=request_scraping,
        request_bulk_outreach=request_bulk_outreach,
        include_whatsapp_draft=include_whatsapp_draft,
        relationship_status=str(company.get("relationship_status") or ""),
    )

    recommended_offer = dossier.get("recommended_offer", "diagnostic")
    angle_code: str | None = None
    for code, entry in WEAKNESS_CATALOG.items():
        if entry["implied_offer"] == recommended_offer:
            angle_code = code
            break
    if angle_code is not None:
        entry = WEAKNESS_CATALOG[angle_code]
        pack["angle_ar"] = entry["angle_ar"]
        pack["angle_en"] = entry["angle_en"]
    else:
        pack["angle_ar"] = "نبدأ بتشخيص محكوم مبني على بياناتكم المعلنة."
        pack["angle_en"] = "We start with a governed diagnostic built on your declared data."

    pack["recommended_offer"] = recommended_offer
    pack["priority_band"] = dossier.get("priority_band", "P3")
    pack["draft_only"] = True
    pack["approval_required"] = True
    return pack


__all__ = [
    "WEAKNESS_CATALOG",
    "build_company_dossier",
    "build_target_company_draft",
    "declared_weaknesses_to_signals",
    "detect_structural_weaknesses",
    "split_declared_weaknesses",
]
