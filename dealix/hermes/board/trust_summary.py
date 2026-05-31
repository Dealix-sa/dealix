"""Summarize trust posture for the board: incidents, escalations, attestations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TrustSummary:
    period: str
    incidents: int
    escalations_resolved: int
    escalations_open: int
    workflows_attested: int
    posture: str


def _posture(incidents: int, escalations_open: int) -> str:
    if incidents == 0 and escalations_open == 0:
        return "clean"
    if incidents == 0 and escalations_open <= 3:
        return "stable"
    if incidents <= 2:
        return "elevated"
    return "needs_action"


def summarize(
    period: str,
    *,
    incidents: int,
    escalations_resolved: int,
    escalations_open: int,
    workflows_attested: int,
) -> TrustSummary:
    """Compose a TrustSummary describing posture for a board period."""
    return TrustSummary(
        period=period,
        incidents=int(incidents),
        escalations_resolved=int(escalations_resolved),
        escalations_open=int(escalations_open),
        workflows_attested=int(workflows_attested),
        posture=_posture(incidents, escalations_open),
    )
