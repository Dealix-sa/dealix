"""Partner compliance checks: only approved claims, evidence-backed assets."""

from __future__ import annotations

from dataclasses import dataclass, field

from .approved_claims import is_approved


@dataclass(frozen=True)
class ComplianceReport:
    partner_id: str
    compliant: bool
    violations: tuple[str, ...] = field(default_factory=tuple)


def review(partner_id: str, claims_used: list[tuple[str, str]]) -> ComplianceReport:
    """Return ComplianceReport flagging any claim not in the signed registry."""
    violations: list[str] = []
    for claim_id, text in claims_used:
        if not is_approved(claim_id, text):
            violations.append(f"unapproved claim: {claim_id}")
    return ComplianceReport(partner_id=partner_id, compliant=not violations, violations=tuple(violations))
