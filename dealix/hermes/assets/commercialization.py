"""
Commercialization planner — given an asset, produces a structured plan
for turning it into a paid offer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CommercializationPlan:
    asset_id: str
    proposed_offer_name: str
    tier: str  # "entry" | "core" | "expansion" | "enterprise"
    proposed_price_sar: float
    required_assets: list[str]
    required_delivery_playbook: bool
    required_legal_review: bool
    rationale: list[str]


def plan_commercialization(
    *,
    asset_id: str,
    asset_kind: str,
    typical_buyer_size: str,  # "smb" | "mid_market" | "enterprise"
    typical_outcome_value_sar: float,
    requires_data_handling: bool,
    requires_external_send: bool,
) -> CommercializationPlan:
    if typical_buyer_size == "enterprise":
        tier = "enterprise"
        price = max(typical_outcome_value_sar * 0.15, 25000)
    elif typical_buyer_size == "mid_market":
        tier = "core"
        price = max(typical_outcome_value_sar * 0.12, 9500)
    else:
        tier = "entry"
        price = max(typical_outcome_value_sar * 0.10, 1500)

    required_assets = [asset_id, "delivery_playbook"]
    if requires_data_handling:
        required_assets.append("data_handling_addendum")
    if requires_external_send:
        required_assets.append("approval_flow_doc")

    rationale = [
        f"asset_kind={asset_kind}",
        f"typical_buyer_size={typical_buyer_size}",
        f"price_floor_applied",
    ]
    if requires_external_send:
        rationale.append(
            "external send is in scope — bundle approval-flow doc + claim verifier"
        )
    return CommercializationPlan(
        asset_id=asset_id,
        proposed_offer_name=f"{asset_kind.title()} (from {asset_id})",
        tier=tier,
        proposed_price_sar=round(price, 2),
        required_assets=required_assets,
        required_delivery_playbook=True,
        required_legal_review=tier == "enterprise" or requires_external_send,
        rationale=rationale,
    )
