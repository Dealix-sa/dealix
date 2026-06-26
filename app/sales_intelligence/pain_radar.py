"""Company Pain Radar.

Converts public or client-provided signals into a safe pain hypothesis and offer fit.
No claim is treated as fact until verified by the founder or client.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PainSignal:
    source: str
    signal_type: str
    description: str
    confidence: int


@dataclass(frozen=True)
class PainRadarResult:
    score: int
    primary_pain: str
    recommended_offer: str
    why_it_matters: str
    first_question: str


OFFER_MAP = {
    "follow_up_leakage": "7-Day Revenue Command Room Sprint",
    "unclear_management_reporting": "Company Brain Sprint",
    "weak_offer_clarity": "Offer Intelligence Sprint",
    "delivery_bottleneck": "Client Delivery OS Sprint",
    "ai_governance_gap": "AI Trust & Compliance OS",
}


def classify_signal(signal: PainSignal) -> str:
    text = f"{signal.signal_type} {signal.description}".lower()
    if any(word in text for word in ["follow", "lead", "whatsapp", "reply", "متابعة", "واتساب"]):
        return "follow_up_leakage"
    if any(word in text for word in ["report", "dashboard", "decision", "تقرير", "قرار"]):
        return "unclear_management_reporting"
    if any(word in text for word in ["price", "proposal", "offer", "عرض", "سعر"]):
        return "weak_offer_clarity"
    if any(word in text for word in ["delivery", "sla", "delay", "تسليم", "تأخير"]):
        return "delivery_bottleneck"
    if any(word in text for word in ["privacy", "policy", "governance", "خصوصية", "حوكمة"]):
        return "ai_governance_gap"
    return "follow_up_leakage"


def analyze_company_pain(signals: list[PainSignal]) -> PainRadarResult:
    if not signals:
        return PainRadarResult(
            score=0,
            primary_pain="not enough verified signals",
            recommended_offer="AI Revenue Diagnostic",
            why_it_matters="Dealix should start with a diagnostic before proposing a build.",
            first_question="What is the most expensive workflow delay you see every week?",
        )

    weighted: dict[str, int] = {}
    for signal in signals:
        category = classify_signal(signal)
        weighted[category] = weighted.get(category, 0) + max(0, min(signal.confidence, 10))

    primary = max(weighted, key=weighted.get)
    score = weighted[primary]
    offer = OFFER_MAP[primary]
    return PainRadarResult(
        score=score,
        primary_pain=primary,
        recommended_offer=offer,
        why_it_matters=(
            "This pain is commercially relevant because it can affect replies, proposals, "
            "management decisions, delivery speed, or trust. Treat it as a hypothesis until verified."
        ),
        first_question="Where does this workflow break today, and who owns the next action?",
    )
