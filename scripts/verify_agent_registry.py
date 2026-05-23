#!/usr/bin/env python3
"""Verify the agent registry declares the required agents and required fields."""

from __future__ import annotations

from pathlib import Path

from _verify_common import ROOT, Verifier

REQUIRED_AGENTS = [
    "ceo_copilot",
    "brand_guardian",
    "growth_strategist",
    "distribution_operator",
    "content_strategist",
    "offer_architect",
    "performance_analyst",
    "trust_guardian",
    "eval_guardian",
    "finance_copilot",
    "delivery_copilot",
    "security_guardian",
    "productization_agent",
    "partner_revenue_agent",
    "proof_safety_agent",
    "incident_response_agent",
]

REQUIRED_FIELDS = [
    "approval_class_max",
    "eval_required",
    "kill_switch",
    "audit_required",
    "external_action_allowed",
    "owner",
    "allowed_write_targets",
]


def populate(v: Verifier) -> None:
    if not v.check_file("registries/agent_registry.yaml"):
        return
    text = Path(ROOT / "registries" / "agent_registry.yaml").read_text(encoding="utf-8")
    for agent in REQUIRED_AGENTS:
        v.custom(f"id: {agent}" in text, f"agent registered: {agent}")
    for field in REQUIRED_FIELDS:
        v.custom(f"{field}:" in text, f"registry declares field: {field}")


if __name__ == "__main__":
    from _verify_common import main_for

    main_for("agent-registry", populate)
