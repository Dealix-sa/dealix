"""Track partner onboarding checklist."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PartnerOnboarding:
    partner_id: str
    items: dict[str, bool] = field(default_factory=lambda: {
        "nda_signed": False,
        "trust_review_completed": False,
        "pricing_reviewed": False,
        "kickoff_held": False,
        "first_lead_pack_sent": False,
    })

    def complete(self, item: str) -> None:
        if item not in self.items:
            raise KeyError(f"Unknown onboarding item: {item}")
        self.items[item] = True

    @property
    def progress(self) -> float:
        return sum(1 for v in self.items.values() if v) / len(self.items)


__all__ = ["PartnerOnboarding"]
