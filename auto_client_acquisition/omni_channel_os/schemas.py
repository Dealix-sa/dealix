"""Pydantic v2 data models for the Omni-Channel Growth OS."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class GCCCountry(str, Enum):
    KSA = "KSA"
    UAE = "UAE"
    Kuwait = "Kuwait"
    Bahrain = "Bahrain"
    Qatar = "Qatar"
    Oman = "Oman"
    Other = "Other"


class Sector(str, Enum):
    legal = "legal"
    facilities_management = "facilities_management"
    consulting = "consulting"
    real_estate = "real_estate"
    healthcare = "healthcare"
    education_training = "education_training"
    international_company = "international_company"
    local_sme = "local_sme"
    government_adjacent = "government_adjacent"
    technology = "technology"
    manufacturing = "manufacturing"
    retail = "retail"
    financial_services = "financial_services"
    other = "other"


class CompanySize(str, Enum):
    micro = "micro"
    sme = "sme"
    mid_market = "mid_market"
    enterprise = "enterprise"


class Language(str, Enum):
    arabic = "arabic"
    english = "english"
    bilingual = "bilingual"


class ChannelType(str, Enum):
    email = "email"
    linkedin = "linkedin"
    whatsapp_optin = "whatsapp_optin"
    website_form = "website_form"
    google_lead_form = "google_lead_form"
    linkedin_lead_gen = "linkedin_lead_gen"
    meta_lead_ads = "meta_lead_ads"
    seo_content = "seo_content"
    webinar = "webinar"
    phone_call = "phone_call"
    partnership = "partnership"
    procurement_portal = "procurement_portal"
    community = "community"
    retargeting = "retargeting"
    founder_brand = "founder_brand"


class AutomationLevel(str, Enum):
    full = "full"
    partial = "partial"
    manual = "manual"


class AssetType(str, Enum):
    email_draft = "email_draft"
    linkedin_connection_note = "linkedin_connection_note"
    linkedin_dm = "linkedin_dm"
    linkedin_followup_1 = "linkedin_followup_1"
    linkedin_followup_2 = "linkedin_followup_2"
    linkedin_comment_idea = "linkedin_comment_idea"
    linkedin_post_ar = "linkedin_post_ar"
    linkedin_post_en = "linkedin_post_en"
    website_form_message = "website_form_message"
    whatsapp_optin_reply = "whatsapp_optin_reply"
    whatsapp_qualification = "whatsapp_qualification"
    call_script = "call_script"
    partner_intro = "partner_intro"
    webinar_invite = "webinar_invite"
    lead_ad_followup = "lead_ad_followup"
    content_post_ar = "content_post_ar"
    content_post_en = "content_post_en"
    proposal_seed = "proposal_seed"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ReviewAction(str, Enum):
    review_and_send = "review_and_send"
    review_and_submit_form = "review_and_submit_form"
    approve_and_queue = "approve_and_queue"
    manual_only = "manual_only"


class Company(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str
    country: GCCCountry = GCCCountry.KSA
    city: str | None = None
    sector: Sector = Sector.other
    sub_sector: str | None = None
    language: Language = Language.arabic
    company_size: CompanySize = CompanySize.sme
    decision_maker_title: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    linkedin_url: str | None = None
    website_url: str | None = None
    enrichment_notes: str | None = None
    source: str = "manual"
    enrichment_score: int = Field(default=50, ge=0, le=100)


class BuyerPersona(BaseModel):
    sector: str
    typical_titles: list[str]
    pain_points: list[str]
    preferred_channels: list[ChannelType]
    offer_fit: str
    language_preference: Language = Language.arabic
    decision_style: str = "relationship_first"


class ChannelDecision(BaseModel):
    company_id: str
    segment: str
    primary_channels: list[ChannelType]
    secondary_channels: list[ChannelType]
    avoid_channels: list[ChannelType]
    automation_levels: dict[str, AutomationLevel]
    rationale: str


class ChannelAsset(BaseModel):
    asset_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    company_id: str
    asset_type: AssetType
    channel: ChannelType
    language: Language
    subject_or_hook: str | None = None
    body: str
    cta: str
    is_auto_sendable: bool = False
    requires_founder_approval: bool = True
    risk_level: RiskLevel = RiskLevel.medium
    quality_score: float = Field(default=70.0, ge=0.0, le=100.0)
    word_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    sector: str = ""
    country: str = ""
    approval_status: str = "pending"

    def model_post_init(self, __context: Any) -> None:
        if self.word_count == 0 and self.body:
            object.__setattr__(self, "word_count", len(self.body.split()))


class FounderReviewItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    company: str
    country: str
    sector: str
    language: Language
    buyer_title: str
    best_channel: ChannelType
    backup_channel: ChannelType | None = None
    offer_name: str
    angle: str
    asset_ready: list[AssetType]
    quality_score: float
    risk_level: RiskLevel
    recommended_action: ReviewAction
    assets: dict[str, ChannelAsset] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    priority_rank: int = 50


class DailyQuota(BaseModel):
    date: str
    company_briefs_target: int = 300
    email_drafts_target: int = 150
    linkedin_drafts_target: int = 150
    website_form_drafts_target: int = 100
    whatsapp_drafts_target: int = 50
    call_scripts_target: int = 50
    partner_intros_target: int = 30
    content_assets_target: int = 10
    proposal_seeds_target: int = 10
    founder_actions_target: int = 200
    company_briefs_done: int = 0
    email_drafts_done: int = 0
    linkedin_drafts_done: int = 0
    website_form_drafts_done: int = 0
    whatsapp_drafts_done: int = 0
    call_scripts_done: int = 0
    partner_intros_done: int = 0
    content_assets_done: int = 0
    proposal_seeds_done: int = 0
    founder_actions_done: int = 0

    @property
    def total_assets_done(self) -> int:
        return (
            self.email_drafts_done
            + self.linkedin_drafts_done
            + self.website_form_drafts_done
            + self.whatsapp_drafts_done
            + self.call_scripts_done
            + self.partner_intros_done
            + self.content_assets_done
            + self.proposal_seeds_done
        )

    @property
    def completion_pct(self) -> float:
        target = (
            self.email_drafts_target
            + self.linkedin_drafts_target
            + self.website_form_drafts_target
            + self.whatsapp_drafts_target
        )
        if target == 0:
            return 0.0
        return round(self.total_assets_done / target * 100, 1)


class LeadCapture(BaseModel):
    lead_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    source: str
    name: str
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    sector: str | None = None
    country: str = "KSA"
    language_preference: Language = Language.arabic
    captured_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    campaign_name: str | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    raw_form_data: dict = Field(default_factory=dict)


class InboundLead(BaseModel):
    lead: LeadCapture
    qualification_score: float = 50.0
    offer_route: str = "free_diagnostic"
    auto_reply_draft: str | None = None
    one_pager_url: str | None = None
    booking_link_sent: bool = False
    call_brief_created: bool = False
    crm_added: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ChannelReport(BaseModel):
    date: str
    total_companies: int = 0
    total_assets: int = 0
    by_channel: dict[str, int] = Field(default_factory=dict)
    by_sector: dict[str, int] = Field(default_factory=dict)
    by_country: dict[str, int] = Field(default_factory=dict)
    founder_queue_size: int = 0
    auto_sent_count: int = 0
    pending_approval_count: int = 0
    reply_rate_7d: float | None = None
    conversion_rate_7d: float | None = None
    top_actions: list[str] = Field(default_factory=list)


class LearningSignal(BaseModel):
    signal_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    company_id: str
    channel: str
    asset_type: str
    sent_at: datetime
    response_type: str
    response_text: str | None = None
    sector: str
    country: str
    language: str
    offer: str
    quality_score_at_send: float = 70.0


class PlaybookUpdate(BaseModel):
    sector: str
    channel: str
    what_works: list[str] = Field(default_factory=list)
    what_doesnt: list[str] = Field(default_factory=list)
    best_subject_lines: list[str] = Field(default_factory=list)
    best_hooks: list[str] = Field(default_factory=list)
    sample_winning_messages: list[str] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class OmniChannelBrief(BaseModel):
    brief_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    company: Company
    buyer_persona: BuyerPersona
    channel_decision: ChannelDecision
    offer_name: str
    angle: str
    assets: dict[str, ChannelAsset] = Field(default_factory=dict)
    brief_score: float = 70.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


__all__ = [
    "AssetType",
    "AutomationLevel",
    "BuyerPersona",
    "ChannelAsset",
    "ChannelDecision",
    "ChannelReport",
    "ChannelType",
    "Company",
    "CompanySize",
    "DailyQuota",
    "FounderReviewItem",
    "GCCCountry",
    "InboundLead",
    "Language",
    "LeadCapture",
    "LearningSignal",
    "OmniChannelBrief",
    "PlaybookUpdate",
    "ReviewAction",
    "RiskLevel",
    "Sector",
]
