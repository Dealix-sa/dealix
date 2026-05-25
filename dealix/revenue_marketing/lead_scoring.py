"""Revenue Marketing lead score (§12 of the doctrine).

Lead Score =
  0.25 * ICP fit
+ 0.20 * pain likelihood
+ 0.20 * ability to pay
+ 0.15 * urgency
+ 0.10 * partner potential
+ 0.10 * trust fit

Each sub-score is normalised to [0, 1]. The output is also rendered as an
integer 0–100 plus a transparent breakdown.
"""

from __future__ import annotations

from typing import Any

_WEIGHTS = {
    "icp_fit": 0.25,
    "pain_likelihood": 0.20,
    "ability_to_pay": 0.20,
    "urgency": 0.15,
    "partner_potential": 0.10,
    "trust_fit": 0.10,
}

_DECISION_MAKER_HINTS = (
    "founder", "ceo", "coo", "cro", "cto", "chief", "vp", "head", "director",
    "owner", "managing", "general manager",
    "مدير عام", "الرئيس التنفيذي", "رئيس عمليات", "مدير تجاري",
)

_ENTERPRISE_HINTS = ("enterprise", "ministry", "bank", "aramco", "stc", "sabic", "neom", "pif")
_AGENCY_HINTS = ("agency", "consulting", "وكالة", "استشارات")
_TRUST_HINTS = ("compliance", "governance", "audit", "خصوصية", "حوكمة", "تدقيق", "pdpl")
_AI_USE_HINTS = ("chatgpt", "claude", "gpt", "ai agent", "automation", "ذكاء اصطناعي", "وكلاء")
_URGENCY_HINTS_HIGH = ("this week", "this month", "أسبوع", "شهر", "عاجل", "now", "today")


def _icp_fit(f: dict[str, Any]) -> float:
    score = 0.0
    role = str(f.get("role") or f.get("title") or "").lower()
    company = str(f.get("company") or "").strip()
    industry = str(f.get("industry") or "").lower()
    country = str(f.get("country") or f.get("region") or "").lower()

    if any(h in role for h in _DECISION_MAKER_HINTS):
        score += 0.45
    if company and company.lower() not in {"-", "n/a", "personal"}:
        score += 0.25
    if "saudi" in country or "ksa" in country or "سعودي" in country:
        score += 0.15
    if industry in {"saas", "fintech", "b2b", "healthtech", "edtech"} or industry:
        score += 0.15
    return min(score, 1.0)


def _pain_likelihood(f: dict[str, Any]) -> float:
    text = " ".join(str(f.get(k) or "") for k in ("pain", "message", "notes")).lower()
    if not text.strip():
        return 0.2
    score = 0.0
    for keyword, weight in (
        ("revenue", 0.25),
        ("pipeline", 0.2),
        ("متابعة", 0.25),
        ("leads", 0.2),
        ("compliance", 0.2),
        ("manual", 0.15),
        ("crm", 0.15),
        ("ai", 0.1),
    ):
        if keyword in text:
            score += weight
    return min(score, 1.0)


def _ability_to_pay(f: dict[str, Any]) -> float:
    budget_raw = str(f.get("budget_range") or f.get("budget") or "").lower()
    company = str(f.get("company") or "").lower()
    if any(h in company for h in _ENTERPRISE_HINTS):
        return 1.0
    if not budget_raw:
        return 0.3
    if any(tok in budget_raw for tok in ("100k", "100,000", "≥100", "+100", "enterprise")):
        return 1.0
    if any(tok in budget_raw for tok in ("50k", "50,000", "25k", "25,000")):
        return 0.75
    if any(tok in budget_raw for tok in ("10k", "10,000", "5k", "5,000")):
        return 0.55
    if any(tok in budget_raw for tok in ("1k", "1,000", "999")):
        return 0.35
    return 0.3


def _urgency(f: dict[str, Any]) -> float:
    text = " ".join(str(f.get(k) or "") for k in ("urgency", "timeline", "message", "notes")).lower()
    if not text.strip():
        return 0.3
    if any(h in text for h in _URGENCY_HINTS_HIGH):
        return 0.95
    if any(h in text for h in ("next quarter", "ربع", "q1", "q2", "q3", "q4")):
        return 0.65
    if any(h in text for h in ("exploring", "researching", "نبحث", "نستكشف")):
        return 0.35
    return 0.4


def _partner_potential(f: dict[str, Any]) -> float:
    text = " ".join(str(f.get(k) or "") for k in ("company", "industry", "notes", "role")).lower()
    if any(h in text for h in _AGENCY_HINTS):
        return 0.9
    if "partner" in text or "reseller" in text or "شريك" in text:
        return 0.7
    return 0.2


def _trust_fit(f: dict[str, Any]) -> float:
    text = " ".join(str(f.get(k) or "") for k in ("pain", "message", "notes", "industry")).lower()
    score = 0.0
    if any(h in text for h in _TRUST_HINTS):
        score += 0.5
    if any(h in text for h in _AI_USE_HINTS):
        score += 0.4
    if f.get("consent_marketing") is True:
        score += 0.1
    return min(score, 1.0)


def revenue_marketing_lead_score(fields: dict[str, Any]) -> dict[str, Any]:
    """Returns {score_0_100, weighted_0_1, breakdown, recommendations}."""
    sub = {
        "icp_fit": round(_icp_fit(fields), 3),
        "pain_likelihood": round(_pain_likelihood(fields), 3),
        "ability_to_pay": round(_ability_to_pay(fields), 3),
        "urgency": round(_urgency(fields), 3),
        "partner_potential": round(_partner_potential(fields), 3),
        "trust_fit": round(_trust_fit(fields), 3),
    }
    weighted = sum(sub[k] * _WEIGHTS[k] for k in _WEIGHTS)

    recommendations: list[str] = []
    if sub["partner_potential"] >= 0.7:
        recommendations.append("agency_white_label_kit")
    if sub["trust_fit"] >= 0.6:
        recommendations.append("ai_trust_kit")
    if sub["ability_to_pay"] >= 0.75:
        recommendations.append("monthly_revenue_command")
    if not recommendations:
        recommendations.append("revenue_hunter_pilot")

    return {
        "score_0_100": int(round(weighted * 100)),
        "weighted_0_1": round(weighted, 4),
        "weights": _WEIGHTS,
        "breakdown": sub,
        "recommended_offers": recommendations,
    }
