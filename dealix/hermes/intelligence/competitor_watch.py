"""Competitor Watch — flags competitor moves that change priorities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CompetitorMove:
    competitor: str
    move: str
    threat_level: str
    counter_action: str


class CompetitorWatch:
    def assess(self, *, competitor: str, move: str, our_strength: int, our_speed: int) -> CompetitorMove:
        differential = our_strength + our_speed
        if differential >= 8:
            threat = "low"
            counter = "Publish a counter-positioning post (draft only)."
        elif differential >= 5:
            threat = "medium"
            counter = "Refresh the offer card and revisit pricing."
        else:
            threat = "high"
            counter = "Schedule a S2 review to decide product priorities."
        return CompetitorMove(competitor, move, threat, counter)
