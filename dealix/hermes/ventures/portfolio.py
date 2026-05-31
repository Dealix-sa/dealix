"""Active vertical portfolio."""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.ventures.vertical_launcher import VerticalCard


@dataclass
class VenturePortfolio:
    _verticals: dict[str, VerticalCard] = field(default_factory=dict)

    def add(self, card: VerticalCard) -> VerticalCard:
        self._verticals[card.vertical_id] = card
        return card

    def remove(self, vertical_id: str) -> None:
        self._verticals.pop(vertical_id, None)

    def list(self) -> list[VerticalCard]:
        return list(self._verticals.values())
