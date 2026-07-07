"""Deterministic, no-API scoring for the Saudi Opportunity Command Room.

Every company gets six sub-scores derived from keyword signals in its fields.
No paid APIs, no network calls — the same input always yields the same output.

    total = fit + signal + urgency + value + accessibility - trust_risk

Bands (see ``classify``):
    total >= 80  -> hot      (target now)
    total >= 60  -> warm     (enrich and draft)
    total >= 40  -> research (hold)
    else         -> not_fit
"""

from __future__ import annotations

from typing import Any

from dealix.opportunity_graph.schemas import ScoreClass

# Sub-score caps keep total within a predictable 0..105 range.
_FIT_CAP = 25
_SIGNAL_CAP = 25
_URGENCY_CAP = 20
_VALUE_CAP = 20
_ACCESS_CAP = 15
_RISK_CAP = 15

_B2B_HINTS = (
    "b2b",
    "saas",
    "software",
    "platform",
    "enterprise",
    "clinic",
    "clinics",
    "logistics",
    "training",
    "agency",
    "consult",
    "supplier",
    "distributor",
    "industrial",
    "healthtech",
    "fintech",
    "compliance",
)

_ICP_HINTS = (
    "saas",
    "ai",
    "clinic",
    "training",
    "logistics",
    "agency",
    "consult",
    "legal",
    "accounting",
    "contractor",
    "healthtech",
    "supplier",
    "distributor",
)

_SAUDI_SIGNALS = (
    "saudi",
    "ksa",
    "riyadh",
    "jeddah",
    "dammam",
    "neom",
    "vision 2030",
    "misa",
    "invest saudi",
    "rhq",
    "regional headquarters",
    "expansion",
    "mena expansion",
    "localization",
    "arabic",
    "السعودية",
    "الرياض",
    "توسع",
)

_URGENCY_HINTS = (
    "hiring",
    "now hiring",
    "just announced",
    "recently announced",
    "launching",
    "upcoming event",
    "exhibiting",
    "leap",
    "campaign",
    "rfp",
    "tender",
    "deadline",
    "this quarter",
    "توظيف",
    "أعلنت",
    "مناقصة",
)

_VALUE_HINTS = (
    "enterprise",
    "retainer",
    "distributor",
    "partner",
    "government",
    "b2g",
    "ministry",
    "authority",
    "large",
    "group",
    "holding",
)

_ACCESS_HINTS = (
    "founder",
    "ceo",
    "coo",
    "cro",
    "head of",
    "director",
    "vp",
    "chief",
    "contact",
    "email",
    "linkedin",
    "warm intro",
    "referral",
    "مدير",
    "الرئيس التنفيذي",
)

_RISK_HINTS = (
    "healthcare data",
    "patient records",
    "minors",
    "children",
    "gambling",
    "crypto scam",
    "scraped",
    "purchased list",
    "no consent",
    "unverified",
    "military",
    "weapons",
)

_GOV_SECTORS = ("government", "ministry", "authority", "public sector", "municipal")


def _blob(fields: dict[str, Any]) -> str:
    parts = [
        fields.get("name"),
        fields.get("sector"),
        fields.get("country"),
        fields.get("city"),
        fields.get("company_type"),
        fields.get("saudi_signal"),
        fields.get("signal_type"),
        fields.get("buyer_persona"),
        fields.get("pain_hypothesis"),
        fields.get("offer_match"),
        fields.get("estimated_deal_size"),
        fields.get("source"),
        fields.get("notes"),
    ]
    return " ".join(str(p or "") for p in parts).lower()


def _cap(value: int, cap: int) -> int:
    return max(0, min(value, cap))


def score_company(fields: dict[str, Any]) -> dict[str, Any]:
    """Return sub-scores, total, class and a keyword breakdown for a company.

    ``fields`` is a plain dict (row from CSV or model dump). Missing keys are
    treated as empty. The function is pure and deterministic.
    """
    blob = _blob(fields)
    sector = str(fields.get("sector") or "").lower()
    company_type = str(fields.get("company_type") or "").lower()
    country = str(fields.get("country") or "").lower()
    consent = bool(fields.get("consent_to_contact"))
    deal = str(fields.get("estimated_deal_size") or "").lower()
    persona = str(fields.get("buyer_persona") or "").lower()
    breakdown: dict[str, int] = {}

    # ── fit_score ──────────────────────────────────────────────────────
    fit = 0
    if any(h in blob for h in _B2B_HINTS):
        fit += 10
        breakdown["b2b"] = 10
    if any(h in blob for h in _ICP_HINTS):
        fit += 8
        breakdown["icp_match"] = 8
    if str(fields.get("pain_hypothesis") or "").strip():
        fit += 5
        breakdown["clear_pain"] = 5
    if persona:
        fit += 2
        breakdown["known_buyer"] = 2
    fit = _cap(fit, _FIT_CAP)

    # ── signal_score ───────────────────────────────────────────────────
    signal = 0
    hits = [h for h in _SAUDI_SIGNALS if h in blob]
    if hits:
        signal += min(len(hits) * 6, 18)
        breakdown["saudi_signal"] = min(len(hits) * 6, 18)
    if "saudi" in country or "ksa" in country:
        signal += 4
        breakdown["saudi_based"] = 4
    if str(fields.get("saudi_signal") or "").strip():
        signal += 3
        breakdown["explicit_signal"] = 3
    signal = _cap(signal, _SIGNAL_CAP)

    # ── urgency_score ──────────────────────────────────────────────────
    urgency = 0
    uhits = [h for h in _URGENCY_HINTS if h in blob]
    if uhits:
        urgency += min(len(uhits) * 7, 16)
        breakdown["urgency_signal"] = min(len(uhits) * 7, 16)
    if str(fields.get("signal_date") or "").strip():
        urgency += 4
        breakdown["dated_signal"] = 4
    urgency = _cap(urgency, _URGENCY_CAP)

    # ── value_score ────────────────────────────────────────────────────
    value = 0
    if any(h in blob for h in _VALUE_HINTS):
        value += 10
        breakdown["value_signal"] = 10
    if any(tok in deal for tok in ("25", "35", "50", "90", "100", "enterprise", "retainer")):
        value += 8
        breakdown["deal_size"] = 8
    elif deal.strip():
        value += 4
        breakdown["deal_size_known"] = 4
    value = _cap(value, _VALUE_CAP)

    # ── accessibility_score ────────────────────────────────────────────
    access = 0
    if any(h in blob for h in _ACCESS_HINTS):
        access += 8
        breakdown["reachable_dm"] = 8
    if str(fields.get("website") or "").strip():
        access += 3
        breakdown["has_website"] = 3
    if consent:
        access += 4
        breakdown["consent"] = 4
    access = _cap(access, _ACCESS_CAP)

    # ── trust_risk_score (penalty) ─────────────────────────────────────
    risk = 0
    rhits = [h for h in _RISK_HINTS if h in blob]
    if rhits:
        risk += min(len(rhits) * 6, 12)
        breakdown["risk_flag"] = -min(len(rhits) * 6, 12)
    if not consent and any(g in sector or g in company_type for g in _GOV_SECTORS):
        risk += 3
        breakdown["sensitive_gov"] = -3
    if not str(fields.get("source_url") or "").strip() and not str(fields.get("website") or "").strip():
        risk += 2
        breakdown["weak_evidence"] = -2
    risk = _cap(risk, _RISK_CAP)

    total = fit + signal + urgency + value + access - risk
    total = max(0, total)

    return {
        "fit_score": fit,
        "signal_score": signal,
        "urgency_score": urgency,
        "value_score": value,
        "accessibility_score": access,
        "trust_risk_score": risk,
        "total_score": total,
        "score_class": classify(total),
        "score_breakdown": breakdown,
    }


def classify(total: int) -> ScoreClass:
    if total >= 80:
        return "hot"
    if total >= 60:
        return "warm"
    if total >= 40:
        return "research"
    return "not_fit"


def recommended_next_action(score_class: ScoreClass, segment: str) -> str:
    """Deterministic next-action hint. Draft-only language, never 'send now'."""
    if score_class == "hot":
        return "Draft outreach and queue for founder approval (do not send)."
    if score_class == "warm":
        return "Enrich signal, then draft outreach for approval."
    if score_class == "research":
        return "Research and re-score next cycle; hold outreach."
    return "Archive — not a fit this cycle."
