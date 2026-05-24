"""Launch a new vertical only when all readiness fields are present."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class Vertical:
    id: str
    name: str
    buyer: str
    pain: str
    offer_id: str
    first_targets: list[str]
    pilot_metric: str
    scale_rule: str
    kill_rule: str
    trust_requirements: list[str]
    active: bool = True


@dataclass
class VerticalLauncher:
    _by_id: dict[str, Vertical] = field(default_factory=dict)

    def launch(
        self,
        *,
        name: str,
        buyer: str,
        pain: str,
        offer_id: str,
        first_targets: list[str],
        pilot_metric: str,
        scale_rule: str,
        kill_rule: str,
        trust_requirements: list[str],
    ) -> Vertical:
        # Section 122: every required field must be present.
        if len(first_targets) < 50:
            raise ValueError(f"Need ≥50 first targets to launch a vertical; got {len(first_targets)}.")
        for fname, fval in {
            "buyer": buyer,
            "pain": pain,
            "offer_id": offer_id,
            "pilot_metric": pilot_metric,
            "scale_rule": scale_rule,
            "kill_rule": kill_rule,
            "trust_requirements": trust_requirements,
        }.items():
            if not fval:
                raise ValueError(f"Vertical readiness missing field: {fname}")
        v = Vertical(
            id=f"vrt_{uuid.uuid4().hex[:10]}",
            name=name,
            buyer=buyer,
            pain=pain,
            offer_id=offer_id,
            first_targets=list(first_targets),
            pilot_metric=pilot_metric,
            scale_rule=scale_rule,
            kill_rule=kill_rule,
            trust_requirements=list(trust_requirements),
        )
        self._by_id[v.id] = v
        return v

    def kill(self, vertical_id: str) -> Vertical:
        v = self._by_id[vertical_id]
        v.active = False
        return v

    def all(self) -> list[Vertical]:
        return list(self._by_id.values())


__all__ = ["Vertical", "VerticalLauncher"]
