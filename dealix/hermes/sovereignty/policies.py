"""Static sovereign policies the kernel enforces."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.sovereignty.levels import SovereigntyLevel


@dataclass(frozen=True)
class SovereignPolicy:
    name: str
    description: str
    minimum_level: SovereigntyLevel
    requires_memo: bool = False
    requires_dual_approval: bool = False


SOVEREIGN_POLICIES: dict[str, SovereignPolicy] = {
    "external_action": SovereignPolicy(
        name="external_action",
        description="Any externally visible message, post, or send requires approval.",
        minimum_level=SovereigntyLevel.S2_SAMI_APPROVAL,
    ),
    "pricing_change": SovereignPolicy(
        name="pricing_change",
        description="Changing published pricing requires a sovereign memo.",
        minimum_level=SovereigntyLevel.S3_SOVEREIGN_MEMO,
        requires_memo=True,
    ),
    "marketplace_listing": SovereignPolicy(
        name="marketplace_listing",
        description="Marketplace publishing is sovereign-only.",
        minimum_level=SovereigntyLevel.S4_SOVEREIGN_ONLY,
        requires_memo=True,
    ),
    "money_transfer": SovereignPolicy(
        name="money_transfer",
        description="Money movement is never autonomous.",
        minimum_level=SovereigntyLevel.S5_NEVER_AUTONOMOUS,
        requires_memo=True,
        requires_dual_approval=True,
    ),
    "contract_sign": SovereignPolicy(
        name="contract_sign",
        description="Contract signing is never autonomous.",
        minimum_level=SovereigntyLevel.S5_NEVER_AUTONOMOUS,
        requires_memo=True,
        requires_dual_approval=True,
    ),
}


def get_policy(name: str) -> SovereignPolicy | None:
    return SOVEREIGN_POLICIES.get(name)
