"""Customer onboarding checklist."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CustomerOnboarding:
    customer_id: str
    items: dict[str, bool] = field(default_factory=lambda: {
        "kickoff_call": False,
        "data_passport": False,
        "first_signals_loaded": False,
        "trust_policy_signed": False,
        "first_value_report": False,
    })

    def complete(self, name: str) -> None:
        if name not in self.items:
            raise KeyError(f"Unknown onboarding item: {name}")
        self.items[name] = True

    @property
    def progress(self) -> float:
        return sum(1 for v in self.items.values() if v) / len(self.items)


__all__ = ["CustomerOnboarding"]
