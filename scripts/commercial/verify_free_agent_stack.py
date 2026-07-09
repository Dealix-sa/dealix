#!/usr/bin/env python3
"""Verify the Dealix free-agent-stack adapter.

This verification intentionally performs no network calls, no model calls, and
no external actions. It checks that the adapter stays approval-first and does
not expose dangerous actions as allowed tools.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.free_agent_stack import (  # noqa: E402
    build_approval_first_tool_manifest,
    build_dealix_free_agent_profile,
    run_plan_act_observe_preview,
)

FORBIDDEN_ALLOWED_TOOL_NAMES = {
    "send_email",
    "send_whatsapp",
    "send_sms",
    "auto_post",
    "merge_pr",
    "deploy_production",
    "capture_payment",
}

REQUIRED_HARD_BLOCKS = {
    "live_outbound",
    "cold_whatsapp_blast",
    "mass_linkedin_automation",
    "auto_posting",
    "payment_capture",
    "production_mutation",
    "public_llm_endpoint",
    "hardcoded_secret",
    "fake_proof",
    "guaranteed_revenue_claim",
    "government_access_claim",
}


def main() -> int:
    profile = build_dealix_free_agent_profile()
    tools = build_approval_first_tool_manifest()
    preview = run_plan_act_observe_preview("Prepare today's Dealix money-now command.")

    assert profile.default_mode == "draft-only"
    assert REQUIRED_HARD_BLOCKS.issubset(set(profile.hard_blocks))
    assert len(tools) >= 5
    assert len(preview) >= 5
    assert any(step.approval_required for step in preview)

    tool_names = {tool.name for tool in tools}
    assert not (FORBIDDEN_ALLOWED_TOOL_NAMES & tool_names), (
        "Forbidden live action exposed as tool: "
        f"{sorted(FORBIDDEN_ALLOWED_TOOL_NAMES & tool_names)}"
    )

    for tool in tools:
        assert tool.allowed_autonomy_level in {"L1", "L2", "L3"}, tool
        if tool.name == "outreach_draft_builder":
            assert tool.approval_required is True
            assert "send_email" in tool.blocked_actions
            assert "send_whatsapp" in tool.blocked_actions

    print("free_agent_stack verification passed")
    print(f"profile={profile.name}")
    print(f"tools={len(tools)}")
    print(f"preview_steps={len(preview)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
