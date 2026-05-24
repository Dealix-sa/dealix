"""Autonomous Distribution — the unified end-to-end engine that wires the
9 canonical OS modules into a single, governable customer journey.

Layers wired (left → right):
    data_os ─► governance_os ─► sales_os ─► proof_os ─► value_os
                                                ▲           ▼
                                          adoption_os ─► capital_os
                                                ▲           ▼
                                          client_os ─► friction_log

This package owns the *contract* between layers. It must not bypass any
governance gate, must not perform external I/O, and must always carry a
`governance_decision` on any output object.

Public API:
    - engine.process_lead(...)             -> LeadDecision
    - engine.process_payment(...)          -> PaymentDecision
    - engine.assemble_proof_pack(...)      -> ProofPackDecision
    - engine.assess_retainer(...)          -> RetainerDecision
    - loops.morning_loop(...)              -> MorningLoopResult
    - loops.evening_loop(...)              -> EveningLoopResult
    - loops.weekly_loop(...)               -> WeeklyLoopResult
    - loops.monthly_loop(...)              -> MonthlyLoopResult

All decisions and loop results are dataclasses with:
    - governance_decision: GovernanceDecision
    - evidence_refs: tuple[str, ...]
    - bilingual rationale (ar / en)
"""

from auto_client_acquisition.autonomous_distribution.engine import (
    LeadDecision,
    PaymentDecision,
    ProofPackDecision,
    RetainerDecision,
    assemble_proof_pack,
    assess_retainer,
    process_lead,
    process_payment,
)
from auto_client_acquisition.autonomous_distribution.loops import (
    EveningLoopResult,
    MonthlyLoopResult,
    MorningLoopResult,
    WeeklyLoopResult,
    evening_loop,
    monthly_loop,
    morning_loop,
    weekly_loop,
)

__all__ = [
    "LeadDecision",
    "PaymentDecision",
    "ProofPackDecision",
    "RetainerDecision",
    "assemble_proof_pack",
    "assess_retainer",
    "process_lead",
    "process_payment",
    "EveningLoopResult",
    "MonthlyLoopResult",
    "MorningLoopResult",
    "WeeklyLoopResult",
    "evening_loop",
    "monthly_loop",
    "morning_loop",
    "weekly_loop",
]
