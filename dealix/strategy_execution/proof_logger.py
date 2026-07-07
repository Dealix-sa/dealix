"""Proof log builder for daily Dealix strategy runs."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def build_proof_log(plan: dict[str, Any], action_queue: list[dict[str, Any]], approval_queue: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": plan.get("mode", "draft-only"),
        "autonomy_level": plan.get("autonomy_level"),
        "external_execution_enabled": False,
        "strategies_count": len(plan.get("planned", [])),
        "internal_actions_count": len(action_queue),
        "approval_items_count": len(approval_queue),
        "blocked_count": len(plan.get("blocked", [])),
        "evidence_policy": "Only cite source-backed signals, generated artifacts, workflow runs, or founder-approved notes.",
        "safety_summary": {
            "draft_only": True,
            "founder_approval_required_for_external_work": True,
            "no_cold_whatsapp": True,
            "no_mass_automation": True,
            "no_guaranteed_claims": True,
            "no_fake_proof": True,
        },
    }
