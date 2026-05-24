"""Capability + exposure gates.

The same code path that powers an internal capability becomes an external
API only after its readiness gates close. Public exposure is S4 — the
gateway refuses to publish without sovereign approval.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Exposure(str, Enum):
    INTERNAL = "internal"
    CUSTOMER = "customer"
    PARTNER = "partner"
    PUBLIC = "public"


@dataclass
class ReadinessGate:
    name: str
    closed: bool = False
    note: str = ""


_PUBLIC_REQUIRED_GATES = (
    "authentication",
    "rate_limits",
    "billing",
    "audit",
    "abuse_prevention",
    "terms",
    "monitoring",
    "kill_switch",
    "developer_docs",
    "sovereign_approval",
)


@dataclass
class Capability:
    id: str
    name: str
    exposure: Exposure
    gates: dict[str, ReadinessGate] = field(default_factory=dict)

    def declare_gate(self, name: str) -> ReadinessGate:
        g = ReadinessGate(name=name)
        self.gates[name] = g
        return g

    def close_gate(self, name: str, *, note: str = "") -> ReadinessGate:
        if name not in self.gates:
            raise KeyError(f"Unknown gate: {name}")
        self.gates[name].closed = True
        self.gates[name].note = note
        return self.gates[name]


@dataclass
class CapabilityGateway:
    _by_id: dict[str, Capability] = field(default_factory=dict)
    sovereign_approver: str = "sami"

    def register(self, *, id: str, name: str, exposure: Exposure = Exposure.INTERNAL) -> Capability:
        cap = Capability(id=id, name=name, exposure=exposure)
        self._by_id[id] = cap
        return cap

    def graduate(self, cap_id: str, *, to: Exposure, by: str = "sami") -> Capability:
        cap = self._by_id[cap_id]
        if to == Exposure.PUBLIC:
            if by != self.sovereign_approver:
                raise PermissionError("Only sovereign may publish a capability (S4).")
            for gate_name in _PUBLIC_REQUIRED_GATES:
                if gate_name not in cap.gates:
                    raise ValueError(f"Public exposure requires gate '{gate_name}'.")
                if not cap.gates[gate_name].closed:
                    raise ValueError(f"Gate '{gate_name}' is still open.")
        cap.exposure = to
        return cap

    def get(self, cap_id: str) -> Capability:
        return self._by_id[cap_id]

    def all(self) -> list[Capability]:
        return list(self._by_id.values())


__all__ = ["Capability", "CapabilityGateway", "Exposure", "ReadinessGate"]
