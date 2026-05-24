"""Per-vertical kill/scale decisions."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.ventures.vertical_launcher import VerticalTest


@dataclass
class VentureVerdict:
    vertical: str
    verdict: str
    reason: str


class VentureKillScale:
    def evaluate(
        self,
        test: VerticalTest,
        *,
        replies: int,
        paid_customers: int,
        outreach_count: int,
    ) -> VentureVerdict:
        if paid_customers >= 2:
            return VentureVerdict(test.vertical, "scale", "Paying threshold met.")
        if outreach_count >= 50 and replies == 0:
            return VentureVerdict(test.vertical, "kill", "Kill rule triggered.")
        if replies >= 3:
            return VentureVerdict(test.vertical, "hold", "Live conversations — keep working it.")
        return VentureVerdict(test.vertical, "pause", "Not enough signal — pause and revise.")
