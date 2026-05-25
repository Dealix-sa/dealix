"""
Quality checklist runner.

Takes a DeliveryPlaybook and a dict of evidence and returns whether all
required quality gates were satisfied.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.delivery.delivery_playbook import DeliveryPlaybook


@dataclass
class QualityCheckResult:
    offer_id: str
    passed: bool
    failing_gates: list[str]


def run_quality_checklist(
    playbook: DeliveryPlaybook, evidence: dict[str, bool]
) -> QualityCheckResult:
    failing = [g for g in playbook.quality_gates if not evidence.get(g, False)]
    return QualityCheckResult(
        offer_id=playbook.offer_id, passed=not failing, failing_gates=failing
    )
