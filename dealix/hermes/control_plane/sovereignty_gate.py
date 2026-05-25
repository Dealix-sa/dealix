"""
SovereigntyGate — classifies the request on the S0–S5 sovereignty scale
and decides whether Sami must personally authorize it.

Mapping
-------
S0  PUBLIC               — content, GEO pages, marketing assets
S1  INTERNAL             — internal analysis, drafts, scoring
S2  SAMI_APPROVAL        — anything that touches money, contracts, brand
S3  CUSTOMER_SENSITIVE   — customer data, deliverables, retainers
S4  ENTERPRISE_CRITICAL  — public APIs, marketplace listings, partner SLAs
S5  SOVEREIGN_LOCKED     — never executes; sovereign-only memory / strategy
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from dealix.hermes.control_plane.actor_identity import ActorIdentity, ActorKind
from dealix.hermes.control_plane.request_context import RequestContext


class SovereigntyLevel(StrEnum):
    S0_PUBLIC = "S0_PUBLIC"
    S1_INTERNAL = "S1_INTERNAL"
    S2_SAMI_APPROVAL = "S2_SAMI_APPROVAL"
    S3_CUSTOMER_SENSITIVE = "S3_CUSTOMER_SENSITIVE"
    S4_ENTERPRISE_CRITICAL = "S4_ENTERPRISE_CRITICAL"
    S5_SOVEREIGN_LOCKED = "S5_SOVEREIGN_LOCKED"


_LEVEL_ORDER = list(SovereigntyLevel)


def at_least(a: SovereigntyLevel, b: SovereigntyLevel) -> bool:
    return _LEVEL_ORDER.index(a) >= _LEVEL_ORDER.index(b)


@dataclass(frozen=True)
class SovereigntyDecision:
    level: SovereigntyLevel
    requires_sami: bool
    blocked: bool
    reason: str


# Capabilities that always require sovereign approval, no matter the actor.
_S2_CAPABILITIES = {
    "approve_pricing",
    "sign_contract",
    "publish_brand_claim",
    "launch_campaign",
    "release_product",
    "modify_revenue_share",
}

_S3_CAPABILITIES = {
    "export_customer_data",
    "deliver_customer_report",
    "send_external_email",
    "activate_retainer",
}

_S4_CAPABILITIES = {
    "publish_public_api",
    "publish_marketplace_item",
    "modify_partner_sla",
}

_S5_CAPABILITIES = {
    "read_sovereign_memory",
    "execute_sovereign_strategy",
}


def classify(context: RequestContext) -> SovereigntyLevel:
    cap = context.capability
    if cap in _S5_CAPABILITIES:
        return SovereigntyLevel.S5_SOVEREIGN_LOCKED
    if cap in _S4_CAPABILITIES:
        return SovereigntyLevel.S4_ENTERPRISE_CRITICAL
    if cap in _S3_CAPABILITIES:
        return SovereigntyLevel.S3_CUSTOMER_SENSITIVE
    if cap in _S2_CAPABILITIES:
        return SovereigntyLevel.S2_SAMI_APPROVAL
    if context.external_action:
        return SovereigntyLevel.S2_SAMI_APPROVAL
    if context.workspace_id == "dealix_internal":
        return SovereigntyLevel.S1_INTERNAL
    return SovereigntyLevel.S0_PUBLIC


def evaluate(context: RequestContext, actor: ActorIdentity) -> SovereigntyDecision:
    level = classify(context)

    if level == SovereigntyLevel.S5_SOVEREIGN_LOCKED:
        return SovereigntyDecision(
            level=level,
            requires_sami=True,
            blocked=True,
            reason="S5 actions never execute through the control plane.",
        )

    if level == SovereigntyLevel.S4_ENTERPRISE_CRITICAL and actor.kind != ActorKind.SAMI:
        return SovereigntyDecision(
            level=level,
            requires_sami=True,
            blocked=False,
            reason="S4 requires explicit Sami approval.",
        )

    if level == SovereigntyLevel.S2_SAMI_APPROVAL and actor.kind != ActorKind.SAMI:
        return SovereigntyDecision(
            level=level,
            requires_sami=True,
            blocked=False,
            reason="S2 requires Sami approval before execution.",
        )

    if level == SovereigntyLevel.S3_CUSTOMER_SENSITIVE and actor.kind == ActorKind.PARTNER:
        return SovereigntyDecision(
            level=level,
            requires_sami=True,
            blocked=False,
            reason="Partners cannot act on S3 customer data without Sami approval.",
        )

    return SovereigntyDecision(
        level=level,
        requires_sami=False,
        blocked=False,
        reason="Within actor sovereignty scope.",
    )
