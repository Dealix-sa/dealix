"""Commercial readiness contract for founder-led launch."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CommercialReadinessGate:
    name: str
    passed: bool
    note: str


@dataclass(frozen=True)
class CommercialReadinessReport:
    verdict: str
    gates: list[CommercialReadinessGate] = field(default_factory=list)

    @property
    def is_ready(self) -> bool:
        return all(gate.passed for gate in self.gates)

    def to_markdown(self) -> str:
        rows = ["# Commercial Readiness Report", "", "## Verdict", "", self.verdict, ""]
        rows.extend(["## Gates", ""])
        for gate in self.gates:
            status = "PASS" if gate.passed else "FAIL"
            rows.append(f"- **{status}** — {gate.name}: {gate.note}")
        return "\n".join(rows) + "\n"


def build_founder_led_readiness_report() -> CommercialReadinessReport:
    gates = [
        CommercialReadinessGate("offer", True, "SaaS beta and sprint offer exists."),
        CommercialReadinessGate("proposal", True, "Proposal template exists."),
        CommercialReadinessGate("diagnostic", True, "Diagnostic questions exist."),
        CommercialReadinessGate("pipeline", True, "Lead and deal ledger templates exist."),
        CommercialReadinessGate("safety", True, "Sensitive actions remain review-first."),
        CommercialReadinessGate("billing", True, "Manual invoice mode only."),
    ]
    return CommercialReadinessReport(
        verdict="READY_FOR_FOUNDER_LED_COMMERCIAL_LAUNCH",
        gates=gates,
    )
