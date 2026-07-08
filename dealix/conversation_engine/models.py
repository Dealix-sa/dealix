"""Typed data models for Dealix launch conversation generation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class FounderProfile:
    founder_name: str
    primary_email: str
    approved_sender_identity: str
    email_policy: str
    channels_enabled_for_drafts: list[str]
    channels_enabled_for_live_send: list[str]
    external_send_rule: str
    proof_rule: str
    tone: str


@dataclass(frozen=True)
class Offer:
    name: str
    price: str
    best_for: str
    promise: str
    deliverables: list[str]
    proof_metrics: list[str]
    forbidden_claims: list[str]


@dataclass(frozen=True)
class TargetProfile:
    company: str
    segment: str
    contact_name: str
    role: str
    channel_context: str
    pain_hypothesis: str
    urgency: int
    accessibility: int
    value: int
    risk: int
    source: str
    warmth: str


@dataclass(frozen=True)
class GeneratedMessage:
    target_company: str
    channel: str
    subject: str
    short_draft: str
    detailed_draft: str
    follow_up_1: str
    follow_up_2: str
    cta: str
    risk_flags: list[str]
    approval_required: bool = True
    status: str = "pending_founder_approval"


@dataclass(frozen=True)
class ObjectionResponse:
    objection: str
    understanding: str
    short_response: str
    detailed_response: str
    follow_up_question: str
    negotiation_move: str
    proof_needed: list[str]
    risk_flags: list[str]


@dataclass(frozen=True)
class NegotiationPlan:
    target_company: str
    offer: str
    starting_position: str
    minimum_commitment: str
    value_proof: str
    likely_objections: list[str]
    response_strategy: list[str]
    concession_rules: list[str]
    close_question: str
    next_best_action: str
    approval_required: bool = True


@dataclass(frozen=True)
class ProofPack:
    target_company: str
    pain_hypothesis: str
    evidence_source: str
    opportunity_score: int
    offer_match: str
    what_to_measure: list[str]
    client_inputs_needed: list[str]
    dealix_deliverables: list[str]
    next_approval_needed: str
    risk_flags: list[str]


@dataclass(frozen=True)
class ApprovalItem:
    approval_id: str
    target_company: str
    contact_name: str
    channel: str
    draft: str
    reason: str
    risk: str
    proof_attached: str
    decision_options: list[str] = field(default_factory=lambda: ["approve", "revise", "reject", "hold"])
    status: str = "pending_founder_approval"
    approval_required: bool = True


@dataclass(frozen=True)
class ConversationPacket:
    target: TargetProfile
    offer: Offer
    score: int
    messages: list[GeneratedMessage]
    objections: list[ObjectionResponse]
    negotiation: NegotiationPlan
    proof_pack: ProofPack
    approvals: list[ApprovalItem]
    followups: list[dict[str, str]]
    learning_notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
