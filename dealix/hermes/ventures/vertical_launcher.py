"""Vertical Launcher — kicks off a structured vertical experiment."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class VerticalTest:
    vertical: str
    buyer: str
    pain: str
    offer: str
    price: str
    first_50_targets: list[str] = field(default_factory=list)
    pilot_metric: str = "3 replies or 1 paid pilot"
    scale_rule: str = "2 paying customers"
    kill_rule: str = "No replies after 50 targeted outreaches"


class VerticalLauncher:
    def plan(
        self,
        *,
        vertical: str,
        buyer: str,
        pain: str,
        offer: str,
        price: str,
        first_50_targets: list[str] | None = None,
    ) -> VerticalTest:
        return VerticalTest(
            vertical=vertical,
            buyer=buyer,
            pain=pain,
            offer=offer,
            price=price,
            first_50_targets=first_50_targets or [],
        )
