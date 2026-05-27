"""Per-partner risk review."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PartnerRiskReview:
    partner_id: str
    flags: list[str] = field(default_factory=list)
    severity: str = "low"   # low|medium|high

    def add(self, flag: str, *, severity: str = "medium") -> None:
        order = {"low": 0, "medium": 1, "high": 2}
        self.flags.append(flag)
        if order.get(severity, 0) > order.get(self.severity, 0):
            self.severity = severity

    def clear(self) -> None:
        self.flags.clear()
        self.severity = "low"


__all__ = ["PartnerRiskReview"]
