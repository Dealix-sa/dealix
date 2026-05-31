"""
DeliveryPlaybook — the canonical shape for every offer.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DeliveryPlaybook:
    offer_id: str
    name: str
    inputs_required: tuple[str, ...]
    steps: tuple[str, ...]
    outputs: tuple[str, ...]
    quality_gates: tuple[str, ...]
    target_delivery_days: int = 14
    notes: tuple[str, ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, object]:
        return {
            "offer_id": self.offer_id,
            "name": self.name,
            "inputs_required": list(self.inputs_required),
            "steps": list(self.steps),
            "outputs": list(self.outputs),
            "quality_gates": list(self.quality_gates),
            "target_delivery_days": self.target_delivery_days,
            "notes": list(self.notes),
        }
