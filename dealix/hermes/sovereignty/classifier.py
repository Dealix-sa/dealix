"""Classify any proposed action into a SovereigntyLevel."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.sovereignty.levels import SovereigntyLevel


@dataclass(frozen=True)
class ActionContext:
    """Minimum context the classifier needs."""

    action_type: str  # e.g. "send_external_message", "publish_api"
    external: bool = False
    moves_money: bool = False
    binds_contract: bool = False
    affects_pricing: bool = False
    affects_marketplace: bool = False
    affects_partner: bool = False
    affects_public_brand: bool = False
    customer_visible: bool = False
    pdpl_sensitive: bool = False
    workspace_id: str = "dealix_internal"


# Static rules first — explicit beats clever.
_NEVER_AUTONOMOUS_ACTIONS = {
    "transfer_money",
    "sign_contract",
    "issue_share",
    "delete_customer_workspace",
    "publish_marketplace_listing_signed",
}

_SOVEREIGN_ONLY_ACTIONS = {
    "publish_public_api",
    "launch_marketplace",
    "set_enterprise_pricing",
    "publish_brand_position",
}

_SOVEREIGN_MEMO_ACTIONS = {
    "approve_enterprise_pricing",
    "approve_strategic_partnership",
    "publish_geo_landing_at_scale",
}


def classify_action(ctx: ActionContext) -> SovereigntyLevel:
    """Map an ActionContext to the appropriate SovereigntyLevel."""

    if ctx.action_type in _NEVER_AUTONOMOUS_ACTIONS or ctx.moves_money or ctx.binds_contract:
        return SovereigntyLevel.S5_NEVER_AUTONOMOUS

    if ctx.action_type in _SOVEREIGN_ONLY_ACTIONS or ctx.affects_marketplace:
        return SovereigntyLevel.S4_SOVEREIGN_ONLY

    if ctx.action_type in _SOVEREIGN_MEMO_ACTIONS or ctx.affects_pricing or ctx.affects_partner:
        return SovereigntyLevel.S3_SOVEREIGN_MEMO

    if ctx.external or ctx.customer_visible or ctx.pdpl_sensitive:
        return SovereigntyLevel.S2_SAMI_APPROVAL

    if ctx.affects_public_brand:
        return SovereigntyLevel.S2_SAMI_APPROVAL

    if ctx.workspace_id == "dealix_internal":
        return SovereigntyLevel.S1_INTERNAL

    return SovereigntyLevel.S0_AUTO_SAFE
