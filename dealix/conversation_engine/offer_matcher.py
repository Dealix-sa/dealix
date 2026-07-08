"""Offer matching and target scoring for Dealix."""

from __future__ import annotations

from dealix.conversation_engine.models import Offer, TargetProfile


def score_target(target: TargetProfile) -> int:
    warmth_bonus = {
        "inbound": 14,
        "warm": 12,
        "referral": 10,
        "opt-in": 10,
        "research": 0,
        "cold": -25,
    }.get(target.warmth.lower(), 0)
    raw = (
        (target.urgency * 0.30)
        + (target.accessibility * 0.22)
        + (target.value * 0.33)
        - (target.risk * 0.15)
        + warmth_bonus
    )
    return max(0, min(100, round(raw)))


def match_offer(target: TargetProfile, offers: list[Offer]) -> Offer:
    segment = target.segment.lower()
    pain = target.pain_hypothesis.lower()
    if "foreign" in segment or "market" in segment or "ksa" in pain:
        return _find_offer(offers, "Saudi Opportunity Snapshot")
    if "b2g" in segment or "tender" in pain or "proposal" in pain:
        return _find_offer(offers, "B2G Readiness Sprint")
    if target.urgency >= 85 or "follow" in pain or "whatsapp" in pain:
        return _find_offer(offers, "Revenue Proof Sprint")
    if target.value >= 85:
        return _find_offer(offers, "Saudi Market Access Sprint")
    return _find_offer(offers, "Revenue Leak Diagnostic")


def _find_offer(offers: list[Offer], name: str) -> Offer:
    for offer in offers:
        if offer.name == name:
            return offer
    return offers[0]
