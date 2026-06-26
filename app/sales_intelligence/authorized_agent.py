"""Authorized Sales Agent policy engine.

The goal is to prepare strong, company-specific sales guidance while preventing
misrepresentation, uncontrolled external action, or unsupported claims.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class AuthorizationLevel(StrEnum):
    DRAFT_ONLY = "draft_only"
    REVIEW_APPROVED = "review_approved"
    AUTHORIZED_REPRESENTATIVE = "authorized_representative"


class AgentDecisionStatus(StrEnum):
    BLOCKED = "blocked"
    DRAFT_READY = "draft_ready"
    REVIEW_REQUIRED = "review_required"
    AUTHORIZED_READY = "authorized_ready"


@dataclass(frozen=True)
class CompanyVoiceProfile:
    company_name: str
    tone: str = "professional_saudi_b2b"
    allowed_signatory_names: tuple[str, ...] = ()
    allowed_titles: tuple[str, ...] = ()
    prohibited_phrases: tuple[str, ...] = (
        "guaranteed revenue",
        "guaranteed roi",
        "عميلنا الحالي",
        "نضمن لك",
    )


@dataclass(frozen=True)
class SalesAgentRequest:
    target_company: str
    source_url: str
    pain_hypothesis: str
    recommended_offer: str
    authorization_level: AuthorizationLevel = AuthorizationLevel.DRAFT_ONLY
    requested_sender_name: str | None = None
    requested_sender_title: str | None = None
    requires_external_action: bool = False
    has_human_approval: bool = False
    has_verified_target: bool = False
    has_opt_out_language: bool = True
    claims: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class SalesAgentDecision:
    status: AgentDecisionStatus
    allowed: bool
    reason: str


def contains_prohibited_claim(text: str, voice: CompanyVoiceProfile) -> bool:
    normalized = text.lower()
    return any(phrase.lower() in normalized for phrase in voice.prohibited_phrases)


def evaluate_authorized_sales_action(
    request: SalesAgentRequest,
    voice: CompanyVoiceProfile,
) -> SalesAgentDecision:
    if not request.source_url:
        return SalesAgentDecision(AgentDecisionStatus.BLOCKED, False, "source_url required")
    if not request.pain_hypothesis:
        return SalesAgentDecision(AgentDecisionStatus.BLOCKED, False, "pain hypothesis required")
    if not request.recommended_offer:
        return SalesAgentDecision(AgentDecisionStatus.BLOCKED, False, "recommended offer required")
    if any(contains_prohibited_claim(claim, voice) for claim in request.claims):
        return SalesAgentDecision(AgentDecisionStatus.BLOCKED, False, "unsupported or prohibited claim")

    if request.requires_external_action:
        if not request.has_verified_target:
            return SalesAgentDecision(AgentDecisionStatus.REVIEW_REQUIRED, False, "verified target required")
        if not request.has_human_approval:
            return SalesAgentDecision(AgentDecisionStatus.REVIEW_REQUIRED, False, "human approval required")
        if not request.has_opt_out_language:
            return SalesAgentDecision(AgentDecisionStatus.REVIEW_REQUIRED, False, "opt-out language required")

    if request.authorization_level == AuthorizationLevel.AUTHORIZED_REPRESENTATIVE:
        if not request.requested_sender_name or not request.requested_sender_title:
            return SalesAgentDecision(AgentDecisionStatus.BLOCKED, False, "authorized identity required")
        if request.requested_sender_name not in voice.allowed_signatory_names:
            return SalesAgentDecision(AgentDecisionStatus.BLOCKED, False, "sender name is not authorized")
        if request.requested_sender_title not in voice.allowed_titles:
            return SalesAgentDecision(AgentDecisionStatus.BLOCKED, False, "sender title is not authorized")
        return SalesAgentDecision(AgentDecisionStatus.AUTHORIZED_READY, True, "authorized representative ready")

    if request.authorization_level == AuthorizationLevel.REVIEW_APPROVED:
        return SalesAgentDecision(AgentDecisionStatus.REVIEW_REQUIRED, False, "review queue only")

    return SalesAgentDecision(AgentDecisionStatus.DRAFT_READY, True, "draft ready for review")


def build_sales_angle(target_company: str, sector: str, pain_signal: str, offer: str) -> str:
    return (
        f"For {target_company} in {sector}, position Dealix around the observed pain: "
        f"{pain_signal}. Recommended entry offer: {offer}. Keep the message short, "
        "specific, review-first, and free from guaranteed outcomes."
    )
