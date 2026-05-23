"""
System improvement planner.

Turns scorecard gaps into concrete proposals the founder can approve.
"""
from __future__ import annotations

from dataclasses import dataclass

from control_plane.system_scorecard import SystemScorecard


@dataclass(frozen=True, slots=True)
class ImprovementProposal:
    system: str
    current_score: int
    target_score: int
    proposed_action: str


class SystemImprovementPlanner:
    def __init__(self, target_band: int = 80) -> None:
        self.target_band = target_band

    def plan(self, scorecards: list[SystemScorecard]) -> list[ImprovementProposal]:
        out: list[ImprovementProposal] = []
        for sc in scorecards:
            if sc.score >= self.target_band:
                continue
            weakest = min(sc.signals.items(), key=lambda kv: kv[1]) if sc.signals else None
            action = (
                f"Lift '{weakest[0]}' from {weakest[1]:.2f}" if weakest
                else "Establish baseline signals"
            )
            out.append(ImprovementProposal(
                system=sc.name,
                current_score=sc.score,
                target_score=self.target_band,
                proposed_action=action,
            ))
        out.sort(key=lambda p: p.current_score)
        return out
