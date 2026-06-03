"""Founder Approval Queue — rank gate-passing drafts for human review.

Only drafts that passed the quality gate are eligible. Ranking favors
lower risk, higher personalization, and higher evidence so the founder's
limited approval time is spent on the strongest drafts first.
"""

from __future__ import annotations

from collections.abc import Sequence

from auto_client_acquisition.market_production_os.schemas import (
    ComplianceStatus,
    OutreachDraft,
    RiskLevel,
)

_RISK_RANK: dict[str, int] = {
    RiskLevel.LOW.value: 0,
    RiskLevel.MEDIUM.value: 1,
    RiskLevel.HIGH.value: 2,
}


def _sort_key(draft: OutreachDraft) -> tuple[int, int, int]:
    # lower risk first, then higher personalization, then higher evidence
    return (
        _RISK_RANK.get(draft.risk_level, 1),
        -int(draft.personalization_level),
        -int(draft.evidence_level),
    )


def eligible_drafts(drafts: Sequence[OutreachDraft]) -> list[OutreachDraft]:
    """Drafts that passed the gate (compliance passed + not BLOCK)."""
    return [
        d
        for d in drafts
        if d.compliance_status == ComplianceStatus.PASSED.value
        and d.governance_decision != "BLOCK"
    ]


def rank_for_approval(
    drafts: Sequence[OutreachDraft], *, top_n: int = 50
) -> list[OutreachDraft]:
    """Return the top ``top_n`` eligible drafts for the founder queue."""
    ranked = sorted(eligible_drafts(drafts), key=_sort_key)
    return ranked[: max(0, top_n)]


__all__ = ["eligible_drafts", "rank_for_approval"]
