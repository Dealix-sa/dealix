from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PartnerComplianceCheck:
    partner_id: str
    passed: bool
    failing: list[str]


_REQUIRED = (
    "signed_partner_agreement",
    "data_processing_addendum_signed",
    "approved_claims_acknowledgement",
    "no_open_compliance_incidents",
)


def run_partner_compliance(
    partner_id: str, evidence: dict[str, bool]
) -> PartnerComplianceCheck:
    failing = [r for r in _REQUIRED if not evidence.get(r, False)]
    return PartnerComplianceCheck(
        partner_id=partner_id, passed=not failing, failing=failing
    )
