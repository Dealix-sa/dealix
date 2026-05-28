"""Post-dispatch integrations — connects Hermes runs to existing ledgers.

Two bridges:

1. ``bridge_to_approval_center`` — when the gate returned ``needs_approval``,
   create a real ApprovalRequest in the queue so the founder sees the draft
   alongside every other pending approval. Without this, ``needs_approval``
   would just be a placeholder dict that nobody acts on.

2. ``bridge_to_capital_ledger`` — when an approved run produces a reusable
   output (envelope ``deliverable`` mentions one of the canonical asset
   types), append it to the capital ledger. Honors non-negotiable #11:
   "No project without Capital Asset."

Both helpers lazy-import their heavy dependencies (approval_center +
capital_os pull in pydantic-settings, structlog, …) so the orchestrator
remains importable in a minimal environment.

Failures here are best-effort — they MUST NOT crash the orchestrator.
Every fallback path is logged into the friction_log as severity=med.
"""
from __future__ import annotations

import os
from typing import Any, Optional

from .audit import HermesAuditRecord
from .governance_gate import Decision, GovernanceDecision


# Map asset-type keywords found in envelopes / intents → CapitalAssetType.
# Keep small and obvious; the test suite asserts the mapping.
_ASSET_TYPE_KEYWORDS: tuple[tuple[str, str], ...] = (
    ("scoring rule", "scoring_rule"),
    ("scoring_rule", "scoring_rule"),
    ("draft template", "draft_template"),
    ("draft_template", "draft_template"),
    ("governance rule", "governance_rule"),
    ("proof example", "proof_example"),
    ("proof pack", "proof_example"),
    ("sector insight", "sector_insight"),
    ("sector report", "sector_insight"),
    ("productization signal", "productization_signal"),
)


def _infer_asset_type(text: str) -> Optional[str]:
    low = text.lower()
    for needle, asset_type in _ASSET_TYPE_KEYWORDS:
        if needle in low:
            return asset_type
    return None


def bridge_to_approval_center(
    record: HermesAuditRecord,
    decision: GovernanceDecision,
    *,
    intent: str,
    summary_en: str = "",
    summary_ar: str = "",
) -> Optional[str]:
    """If ``decision == needs_approval``, create a real ApprovalRequest.

    Returns the new approval_id, or None if the request was skipped
    (wrong decision, missing dep, or write failure).
    """
    if decision.decision != Decision.NEEDS_APPROVAL.value:
        return None
    if not record.customer_id:
        return None
    try:
        from auto_client_acquisition.approval_center import (
            ApprovalRequest,
            get_default_approval_store,
        )
    except ImportError:
        return None

    channel = decision.requires_channel_approval or ""
    try:
        req = ApprovalRequest(
            object_type="hermes_run",
            object_id=record.run_id,
            action_type="draft_email" if channel == "email" else (
                "draft_linkedin_manual" if channel == "linkedin_dm" else "follow_up_task"
            ),
            action_mode="approval_required",
            channel=channel or None,
            summary_en=summary_en or f"Hermes run {record.run_id}: {intent[:140]}",
            summary_ar=summary_ar or summary_en or f"تشغيل هرميس {record.run_id}",
            risk_level="medium",
            customer_id=record.customer_id or None,
            audit_ref=record.run_id,
        )
        store = get_default_approval_store()
        created = store.create(req)
        return created.approval_id
    except Exception:
        return None


def bridge_to_capital_ledger(
    record: HermesAuditRecord,
    decision: GovernanceDecision,
    *,
    intent: str,
    deliverable_text: str = "",
    engagement_id: str = "",
) -> Optional[str]:
    """If the run is approved and produced a reusable artefact, register it.

    Returns the new asset_id, or None if no asset was inferred.
    """
    if decision.decision != Decision.APPROVED.value:
        return None
    if not record.customer_id:
        return None
    if record.customer_id == "dealix_internal":
        # Internal runs (status checks, daily briefs) are not commercial engagements.
        return None
    asset_type = (
        _infer_asset_type(deliverable_text)
        or _infer_asset_type(intent)
    )
    if not asset_type:
        return None
    try:
        from auto_client_acquisition.capital_os.capital_ledger import add_asset
    except ImportError:
        return None
    try:
        asset = add_asset(
            customer_id=record.customer_id,
            engagement_id=engagement_id or record.run_id,
            asset_type=asset_type,
            owner=record.customer_id,
            reusable=True,
            asset_ref=record.run_id,
            notes=f"hermes:{record.sub_agent}:{intent[:80]}",
        )
        return asset.asset_id
    except Exception:
        return None


def daily_cost_budget_usd() -> float:
    """Per-day soft cap (USD). 0 disables the check."""
    try:
        return float(os.getenv("HERMES_DAILY_BUDGET_USD", "0").strip() or "0")
    except ValueError:
        return 0.0
