from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.security.claim_verifier import verify_claims

# The single approved master claim. Partners may rephrase only inside the
# guardrails enforced by `verify_claims`.
APPROVED_MASTER_CLAIM = (
    "Dealix helps prepare B2B opportunity packs, messages, and proposal "
    "drafts under governed approval flows."
)

FORBIDDEN_CLAIMS = (
    "guarantees sales",
    "fully replaces your sales team",
    "compliant with all regulations",
    "100% secure",
    "zero risk",
    "guaranteed roi",
)


@dataclass
class ApprovedClaimsCheck:
    safe: bool
    findings: list[str]
    requires_editor: bool


def check_partner_claim(text: str) -> ApprovedClaimsCheck:
    findings: list[str] = []
    lower = (text or "").lower()
    for banned in FORBIDDEN_CLAIMS:
        if banned in lower:
            findings.append(f"contains_forbidden_claim:{banned}")
    verifier = verify_claims(text)
    findings.extend(verifier.findings)
    requires_editor = bool(findings)
    return ApprovedClaimsCheck(
        safe=not findings, findings=findings, requires_editor=requires_editor
    )
