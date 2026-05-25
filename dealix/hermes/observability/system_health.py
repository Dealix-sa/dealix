"""System-wide health snapshot."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SystemHealth:
    open_incidents: int
    open_risks: int
    pending_approvals: int
    killed_assets: int
    revenue_at_risk_sar: float

    @property
    def is_healthy(self) -> bool:
        return (
            self.open_incidents == 0
            and self.pending_approvals < 10
            and self.revenue_at_risk_sar == 0
        )
