"""Portfolio view over verticals."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.ventures.vertical_launcher import Vertical, VerticalLauncher


@dataclass
class VenturePortfolio:
    launcher: VerticalLauncher

    def active(self) -> list[Vertical]:
        return [v for v in self.launcher.all() if v.active]

    def killed(self) -> list[Vertical]:
        return [v for v in self.launcher.all() if not v.active]


__all__ = ["VenturePortfolio"]
