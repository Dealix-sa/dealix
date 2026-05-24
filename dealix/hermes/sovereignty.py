"""
Hermes Sovereignty Gate.

Classifies every action by sovereignty level (S0..S5) and decides whether it
may run autonomously, internally, or only with Sami's explicit approval.
This is the top of the Kernel: nothing reaches Execution without passing here.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class SovereigntyLevel(str, Enum):
    S0_AUTO_SAFE = "S0_AUTO_SAFE"
    S1_INTERNAL = "S1_INTERNAL"
    S2_SAMI_APPROVAL = "S2_SAMI_APPROVAL"
    S3_SOVEREIGN_MEMO = "S3_SOVEREIGN_MEMO"
    S4_SOVEREIGN_ONLY = "S4_SOVEREIGN_ONLY"
    S5_NEVER_AUTONOMOUS = "S5_NEVER_AUTONOMOUS"


SOVEREIGN_ONLY_ACTIONS: frozenset[str] = frozenset(
    {
        "sign_contract",
        "approve_enterprise_pricing",
        "create_strategic_partnership",
        "export_sensitive_data",
        "enable_external_tool",
        "launch_public_api",
        "launch_marketplace",
        "grant_agent_permissions",
        "approve_revenue_share_agreement",
        "change_company_strategy",
        "transfer_money",
        "enable_mcp_server",
    }
)

NEVER_AUTONOMOUS_ACTIONS: frozenset[str] = frozenset(
    {
        "claim_unverified_partnership",
        "send_sensitive_customer_data",
        "sign_on_behalf_of_sami",
        "make_legal_commitment",
        "make_financial_transfer",
    }
)


class SovereigntyDecision(BaseModel):
    allowed: bool
    level: SovereigntyLevel
    requires_sami_approval: bool
    requires_memo: bool
    reasons: list[str]


def classify_action(
    action_type: str,
    contains_sensitive_data: bool = False,
) -> SovereigntyDecision:
    """Classify ``action_type`` into a sovereignty bucket.

    Order of precedence (highest restriction wins):
      1. Never-autonomous actions      → S5
      2. Sovereign-only actions        → S4
      3. Sensitive data payloads       → S3
      4. ``external_*`` actions        → S2
      5. ``internal_*`` actions        → S1
      6. Everything else (safe ops)    → S0
    """
    if action_type in NEVER_AUTONOMOUS_ACTIONS:
        return SovereigntyDecision(
            allowed=False,
            level=SovereigntyLevel.S5_NEVER_AUTONOMOUS,
            requires_sami_approval=True,
            requires_memo=True,
            reasons=["This action is never allowed autonomously."],
        )
    if action_type in SOVEREIGN_ONLY_ACTIONS:
        return SovereigntyDecision(
            allowed=False,
            level=SovereigntyLevel.S4_SOVEREIGN_ONLY,
            requires_sami_approval=True,
            requires_memo=True,
            reasons=["This is a sovereign-only action."],
        )
    if contains_sensitive_data:
        return SovereigntyDecision(
            allowed=False,
            level=SovereigntyLevel.S3_SOVEREIGN_MEMO,
            requires_sami_approval=True,
            requires_memo=True,
            reasons=["Sensitive data requires sovereign memo and approval."],
        )
    if action_type.startswith("external_"):
        return SovereigntyDecision(
            allowed=False,
            level=SovereigntyLevel.S2_SAMI_APPROVAL,
            requires_sami_approval=True,
            requires_memo=False,
            reasons=["External action requires Sami approval."],
        )
    if action_type.startswith("internal_"):
        return SovereigntyDecision(
            allowed=True,
            level=SovereigntyLevel.S1_INTERNAL,
            requires_sami_approval=False,
            requires_memo=False,
            reasons=["Internal low-risk action."],
        )
    return SovereigntyDecision(
        allowed=True,
        level=SovereigntyLevel.S0_AUTO_SAFE,
        requires_sami_approval=False,
        requires_memo=False,
        reasons=["Safe automatic action."],
    )
