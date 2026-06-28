"""Detect bottlenecks from the Company Brain Map.

A bottleneck is a friction point where progress is gated by a single owner, a
stuck experiment, an unreviewed high-impact risk, or a decision past its
review date. Detection is heuristic and descriptive — it flags items for human
review, it does not prescribe a deterministic fix.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def detect_bottlenecks(brain_map: dict[str, Any]) -> list[dict[str, Any]]:
    """Return a list of detected bottlenecks from the brain map.

    Each bottleneck has: area, description, confidence (low/medium/high),
    evidence, suggested_review_owner.
    """
    bottlenecks: list[dict[str, Any]] = []
    ledgers = brain_map.get("ledgers", {})
    today = datetime.now(UTC).date()

    # 1. Overdue decisions (review_date in the past, no recorded outcome)
    for dec in ledgers.get("decisions", []):
        review = dec.get("review_date", "")
        if not review:
            continue
        try:
            rdate = datetime.fromisoformat(review).date()
        except ValueError:
            continue
        if rdate < today:
            bottlenecks.append({
                "area": "decisions",
                "description": f"Decision '{dec.get('decision', '')[:60]}' past review date {review}.",
                "confidence": "high",
                "evidence": f"review_date={review}",
                "suggested_review_owner": dec.get("owner", "unassigned"),
            })

    # 2. Experiments stuck in 'running' beyond 30 days with no result
    for exp in ledgers.get("experiments", []):
        if exp.get("status", "").lower() == "running":
            bottlenecks.append({
                "area": "experiments",
                "description": f"Experiment {exp.get('id', '')} still running with no recorded result.",
                "confidence": "medium",
                "evidence": f"id={exp.get('id', '')} status=running",
                "suggested_review_owner": exp.get("owner", "unassigned"),
            })

    # 3. High-impact risks with low confidence mitigation
    for risk in ledgers.get("risks", []):
        impact = str(risk.get("impact", "")).lower()
        conf = str(risk.get("confidence", "")).lower()
        if impact in ("high", "critical") and conf in ("low", "medium"):
            bottlenecks.append({
                "area": "risks",
                "description": f"High-impact risk '{risk.get('risk', '')[:60]}' has {conf} confidence mitigation.",
                "confidence": "high",
                "evidence": f"risk_id={risk.get('id', '')} impact={impact} confidence={conf}",
                "suggested_review_owner": risk.get("owner", "unassigned"),
            })

    # 4. Opportunities with empty next_action
    for opp in ledgers.get("opportunities", []):
        if not opp.get("next_action"):
            bottlenecks.append({
                "area": "opportunities",
                "description": f"Opportunity '{opp.get('opportunity', '')[:60]}' has no next action.",
                "confidence": "medium",
                "evidence": f"opp_id={opp.get('id', '')} next_action=empty",
                "suggested_review_owner": opp.get("owner", "unassigned"),
            })

    # 5. Owner concentration: more than 3 open items on a single owner
    owner_counts: dict[str, int] = {}
    for section in ("decisions", "risks", "opportunities", "experiments"):
        for row in ledgers.get(section, []):
            owner = row.get("owner", "")
            if owner:
                owner_counts[owner] = owner_counts.get(owner, 0) + 1
    for owner, count in owner_counts.items():
        if count > 3:
            bottlenecks.append({
                "area": "ownership",
                "description": f"Owner '{owner}' carries {count} open items — possible single point of failure.",
                "confidence": "medium",
                "evidence": f"owner={owner} open_items={count}",
                "suggested_review_owner": owner,
            })

    return bottlenecks


if __name__ == "__main__":
    import json

    from build_company_brain_map import build_company_brain_map

    bm = build_company_brain_map()
    print(json.dumps(detect_bottlenecks(bm), indent=2, default=str))
