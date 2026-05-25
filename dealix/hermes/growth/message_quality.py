"""
MessageQuality — score outbound message variants on the variables that
actually predict verified revenue: reply, qualified-reply, and
proposal-conversion rates.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MessageMetrics:
    message_id: str
    sent: int
    replies: int
    qualified_replies: int
    booked_calls: int
    proposals: int
    deals_won: int


@dataclass
class MessageQualityScore:
    message_id: str
    score: float
    grade: str
    recommendation: str


def score_message(metrics: MessageMetrics) -> MessageQualityScore:
    if metrics.sent == 0:
        return MessageQualityScore(metrics.message_id, 0.0, "F", "No data; ship a test cohort.")
    reply = metrics.replies / metrics.sent
    qualified = metrics.qualified_replies / max(metrics.replies, 1)
    booking = metrics.booked_calls / max(metrics.qualified_replies, 1)
    propose = metrics.proposals / max(metrics.booked_calls, 1)
    win = metrics.deals_won / max(metrics.proposals, 1)
    score = round(0.15 * reply + 0.2 * qualified + 0.2 * booking + 0.2 * propose + 0.25 * win, 4)
    if score >= 0.35:
        grade, rec = "A", "Promote variant to default; archive losing variants."
    elif score >= 0.2:
        grade, rec = "B", "Continue testing variants alongside this one."
    elif score >= 0.08:
        grade, rec = "C", "Rework the opening and CTA before continuing."
    else:
        grade, rec = "D", "Retire variant; root-cause low reply rate."
    return MessageQualityScore(metrics.message_id, score, grade, rec)
