"""Tenant-isolated commercial universe contracts for the Dealix Company OS.

This module is deliberately pure: it classifies relationships, matches a
department objective, and creates an approval envelope. It never sends,
scrapes, mutates a CRM, charges, or contacts a person.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class DepartmentObjective(StrEnum):
    SALES = "sales"
    PARTNERSHIPS = "partnerships"
    MARKETING = "marketing"
    MARKET_ACCESS = "market_access"
    CHANNEL_DISTRIBUTION = "channel_distribution"
    SERVICE_EXCHANGE = "service_exchange"
    B2G_READINESS = "b2g_readiness"
    CUSTOMER_SUCCESS = "customer_success"
    RENEWAL_EXPANSION = "renewal_expansion"


class RelationshipType(StrEnum):
    CUSTOMER = "customer"
    PROSPECT = "prospect"
    STRATEGIC_PARTNER = "strategic_partner"
    REFERRAL_PARTNER = "referral_partner"
    CHANNEL_DISTRIBUTOR = "channel_distributor"
    IMPLEMENTATION_PARTNER = "implementation_partner"
    TECHNOLOGY_PARTNER = "technology_partner"
    CO_MARKETING_PARTNER = "co_marketing_partner"
    SERVICE_EXCHANGE = "service_exchange"
    SUPPLIER = "supplier"
    INVESTOR = "investor"
    GOVERNMENT_STAKEHOLDER = "government_stakeholder"


class PermissionState(StrEnum):
    UNKNOWN = "unknown"
    RESEARCH_ONLY = "research_only"
    WARM = "warm"
    INBOUND = "inbound"
    REFERRAL = "referral"
    OPTED_IN = "opted_in"
    APPROVED = "approved"


class ApprovalStatus(StrEnum):
    NOT_REQUIRED = "not_required"
    REQUIRED = "required"
    BLOCKED = "blocked"


CONTACTABLE = {
    PermissionState.WARM,
    PermissionState.INBOUND,
    PermissionState.REFERRAL,
    PermissionState.OPTED_IN,
    PermissionState.APPROVED,
}


@dataclass(frozen=True)
class CommercialAccount:
    tenant_id: str
    account_id: str
    company_name: str
    department: DepartmentObjective
    relationship: RelationshipType
    permission: PermissionState
    strategic_fit: int
    urgency: int
    value_exchange: str
    source_ref: str

    def __post_init__(self) -> None:
        for field in ("tenant_id", "account_id", "company_name", "value_exchange", "source_ref"):
            if not getattr(self, field).strip():
                raise ValueError(f"{field} must not be empty")
        for field in ("strategic_fit", "urgency"):
            value = getattr(self, field)
            if not 0 <= value <= 100:
                raise ValueError(f"{field} must be between 0 and 100")


@dataclass(frozen=True)
class ApprovalEnvelope:
    tenant_id: str
    account_id: str
    department: DepartmentObjective
    relationship: RelationshipType
    action: str
    channel: str
    rationale: str
    proof_target: str
    status: ApprovalStatus
    external_action_allowed: bool = False

    def __post_init__(self) -> None:
        if self.external_action_allowed:
            raise ValueError("external_action_allowed must remain false in the draft-only core")
        if not self.action.strip() or not self.rationale.strip() or not self.proof_target.strip():
            raise ValueError("action, rationale, and proof_target are required")


def score_account(account: CommercialAccount) -> int:
    """Return a deterministic fit score; permission never increases the score."""
    return round(account.strategic_fit * 0.6 + account.urgency * 0.4)


def create_approval_envelope(
    account: CommercialAccount,
    *,
    action: str,
    channel: str,
    proof_target: str,
) -> ApprovalEnvelope:
    """Prepare a review card, never a send instruction."""
    normalized_channel = channel.strip().casefold()
    if not normalized_channel:
        raise ValueError("channel must not be empty")
    if account.permission in CONTACTABLE:
        status = ApprovalStatus.REQUIRED
        rationale = (
            f"{account.company_name} is a permitted {account.permission.value} relationship; "
            "founder approval is still required before external action."
        )
    else:
        status = ApprovalStatus.BLOCKED
        rationale = (
            f"{account.company_name} is research-only until explicit permission is recorded; "
            "prepare internal research only."
        )
    return ApprovalEnvelope(
        tenant_id=account.tenant_id,
        account_id=account.account_id,
        department=account.department,
        relationship=account.relationship,
        action=action.strip(),
        channel=normalized_channel,
        rationale=rationale,
        proof_target=proof_target.strip(),
        status=status,
    )


def classify_account(payload: dict[str, Any]) -> CommercialAccount:
    """Parse a trusted internal record with strict taxonomy validation."""
    try:
        return CommercialAccount(
            tenant_id=str(payload["tenant_id"]),
            account_id=str(payload["account_id"]),
            company_name=str(payload["company_name"]),
            department=DepartmentObjective(str(payload["department"])),
            relationship=RelationshipType(str(payload["relationship"])),
            permission=PermissionState(str(payload["permission"])),
            strategic_fit=int(payload["strategic_fit"]),
            urgency=int(payload["urgency"]),
            value_exchange=str(payload["value_exchange"]),
            source_ref=str(payload["source_ref"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"invalid commercial account: {exc}") from exc
