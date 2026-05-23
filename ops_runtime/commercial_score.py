"""Commercial score for Dealix revenue operations.

Scores the commercial machine on a 0–100 scale using the same funnel
inputs the Revenue Ops Playbook tracks:

    lead_count → contacted → replied → sample_sent → proposal_sent → paid

The result is intentionally simple so it can be wired into mission-control
or surfaced in a daily digest without depending on heavy analytics.
"""
from __future__ import annotations


def calculate_commercial_score(metrics: dict) -> dict:
    score = 0
    if metrics.get("lead_count", 0) >= 25:
        score += 15
    if metrics.get("contacted", 0) >= 25:
        score += 15
    if metrics.get("replied", 0) >= 5:
        score += 10
    if metrics.get("sample_sent", 0) >= 3:
        score += 15
    if metrics.get("proposal_sent", 0) >= 1:
        score += 20
    if metrics.get("cash_collected", 0) > 0 or metrics.get("paid", 0) >= 1:
        score += 25
    if score >= 90:
        status = "Revenue Operating"
    elif score >= 70:
        status = "Revenue Executing"
    elif score >= 40:
        status = "Revenue Partial"
    else:
        status = "Revenue Setup"
    return {
        "commercial_score": score,
        "commercial_status": status,
    }
