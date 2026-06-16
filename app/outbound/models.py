"""Pydantic and data models for outbound operations."""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class Channel(StrEnum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"


class MessageStatus(StrEnum):
    DRAFT = "draft"
    QUEUED = "queued"
    APPROVED = "approved"
    SENT = "sent"
    FAILED = "failed"
    REPLIED = "replied"
    BOUNCED = "bounced"
    OPTED_OUT = "opted_out"


class VerificationStatus(StrEnum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    LOW_CONFIDENCE = "low"
    MEDIUM_CONFIDENCE = "medium"
    HIGH_CONFIDENCE = "high"
    REJECTED = "rejected"


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PipelineStage(StrEnum):
    NEW = "new"
    CONTACTED = "contacted"
    REPLIED = "replied"
    MEETING = "meeting"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"
    ON_HOLD = "on_hold"


class OutboundContact(BaseModel):
    """A target contact / account."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company_name: str
    contact_name: str | None = None
    email: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    sector: str | None = None
    city: str | None = None
    website: str | None = None
    source_url: str
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    confidence: Confidence = Confidence.LOW
    pain_hypothesis: str | None = None
    dealix_angle: str | None = None
    email_opt_out: bool = False
    whatsapp_opt_in: bool = False
    whatsapp_opt_out: bool = False
    consent_source: str | None = None
    consent_timestamp: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OutboundMessage(BaseModel):
    """A single outbound message (draft or sent)."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    contact_id: str
    channel: Channel
    status: MessageStatus = MessageStatus.DRAFT
    subject: str | None = None
    body: str
    template_name: str | None = None
    provider_message_id: str | None = None
    error_message: str | None = None
    approved_by: str | None = None
    approved_at: datetime | None = None
    queued_at: datetime | None = None
    sent_at: datetime | None = None
    replied_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OutboundEvent(BaseModel):
    """An event emitted by a provider or internal subsystem."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message_id: str
    event_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SuppressionEntry(BaseModel):
    """A channel + value on the suppression list."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    channel: Channel
    value: str
    reason: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DealPipeline(BaseModel):
    """Pipeline row linked to a contact."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    contact_id: str
    stage: PipelineStage = PipelineStage.NEW
    value_sar: float = 0.0
    next_action: str | None = None
    next_action_at: datetime | None = None
    owner: str = "sami"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PolicyVerdict(BaseModel):
    """Result of policy gate evaluation."""

    ok: bool
    channel: Channel
    reason: str = ""
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class SendResult(BaseModel):
    """Result of attempting to send one message."""

    message_id: str
    channel: Channel
    status: MessageStatus
    provider_message_id: str | None = None
    error_message: str | None = None
    dry_run: bool = False
