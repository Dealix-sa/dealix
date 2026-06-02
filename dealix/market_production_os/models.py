"""Records + canonical constants for the Market Production OS.

Prices mirror the repo source of truth for pricing,
``docs/commercial/DEALIX_REVOPS_PACKAGES_AR.md``. They are guardrail ranges,
founder-approved, never auto-charged.
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any

# --- Canonical catalog (source of truth: docs/commercial/DEALIX_REVOPS_PACKAGES_AR.md)
OFFERS: dict[str, dict[str, Any]] = {
    "free_diagnostic": {
        "name_en": "Free AI Ops Diagnostic",
        "name_ar": "تشخيص العمليات المجاني",
        "price_sar_min": 0,
        "price_sar_max": 0,
        "recurring": False,
        "duration": "1-2 days",
    },
    "revenue_diagnostic": {
        "name_en": "Revenue Diagnostic",
        "name_ar": "تشخيص الإيراد",
        "price_sar_min": 3500,
        "price_sar_max": 4500,
        "recurring": False,
        "duration": "3-5 business days",
    },
    "lead_intelligence_sprint": {
        "name_en": "Lead Intelligence Sprint",
        "name_ar": "Sprint ذكاء العملاء المحتملين",
        "price_sar_min": 9500,
        "price_sar_max": 18000,
        "recurring": False,
        "duration": "up to 10 business days",
    },
    "pilot_conversion_sprint": {
        "name_en": "Pilot Conversion Sprint",
        "name_ar": "Sprint تحويل التجربة",
        "price_sar_min": 22000,
        "price_sar_max": 45000,
        "recurring": False,
        "duration": "30 days",
    },
    "monthly_revops_starter": {
        "name_en": "Monthly RevOps OS — Starter",
        "name_ar": "RevOps شهري — Starter",
        "price_sar_min": 15000,
        "price_sar_max": 15000,
        "recurring": True,
        "duration": "monthly",
    },
    "monthly_revops_growth": {
        "name_en": "Monthly RevOps OS — Growth",
        "name_ar": "RevOps شهري — Growth",
        "price_sar_min": 25000,
        "price_sar_max": 25000,
        "recurring": True,
        "duration": "monthly",
    },
    "enterprise_revenue_os": {
        "name_en": "Enterprise AI Revenue OS",
        "name_ar": "Enterprise AI Revenue OS",
        "price_sar_min": 85000,
        "price_sar_max": 120000,
        "recurring": True,
        "duration": "per SOW",
    },
}

SECTORS: tuple[str, ...] = (
    "marketing_agencies",
    "training_companies",
    "clinics",
    "real_estate_teams",
    "recruitment_agencies",
    "professional_services",
    "restaurant_groups",
    "education_providers",
    "logistics_companies",
    "local_saas",
    "other",
)

TOUCH_TYPES: tuple[str, ...] = (
    "first_touch",
    "follow_up_1",
    "follow_up_2",
    "proposal_intro",
    "breakup",
)

PERSONALIZATION_LEVELS: tuple[str, ...] = ("P0", "P1", "P2", "P3", "P4")


def email_sha256(email: str) -> str:
    """Stable suppression key: sha256 of the lowercased, trimmed address.

    Lets suppression be enforced + exported without storing raw PII (NO_PII).
    """
    norm = (email or "").strip().lower()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


@dataclass(frozen=True, slots=True)
class SenderIdentity:
    """Accurate sender identity is mandatory (CAN-SPAM)."""

    from_name: str
    from_email: str
    reply_to: str = ""
    physical_address: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def is_complete(self) -> bool:
        return bool(self.from_name and self.from_email and self.physical_address)


@dataclass(frozen=True, slots=True)
class ProspectScore:
    sector_fit: int = 0
    expected_leads: int = 0
    decision_maker_clear: int = 0
    pain_clear: int = 0
    payment_capacity: int = 0
    personalization: int = 0
    low_risk: int = 0

    @property
    def total(self) -> int:
        return (
            self.sector_fit
            + self.expected_leads
            + self.decision_maker_clear
            + self.pain_clear
            + self.payment_capacity
            + self.personalization
            + self.low_risk
        )

    def to_dict(self) -> dict[str, int]:
        d = asdict(self)
        d["total"] = self.total
        return d


@dataclass(slots=True)
class OutreachDraft:
    draft_id: str
    prospect_id: str
    touch_type: str
    subject: str
    body: str
    language: str = "ar"
    unsubscribe_included: bool = False
    company: str = ""
    sector: str = ""
    recipient_role: str = ""
    source: str = ""
    pain_hypothesis: str = ""
    personalization_note: str = ""
    personalization_level: str = "P0"
    offer: str = ""
    cta: str = ""
    evidence_level: str = "L1"
    risk_level: str = "low"
    sender_identity: dict[str, Any] = field(default_factory=dict)
    unsubscribe_method: str = "none"
    compliance_status: str = "pending"
    compliance_failures: list[str] = field(default_factory=list)
    approval_status: str = "pending"
    send_status: str = "not_sent"
    created_at: str = ""
    schema_version: str = "1.0"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OutreachDraft:
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})
