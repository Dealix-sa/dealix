#!/usr/bin/env python3
"""Verify the Agent Governance OS + Delegation OS (V9). Static, read-only."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REQUIRED_FILES = [
    "docs/agent-governance-os/00_AGENT_GOVERNANCE_OS.md",
    "docs/agent-governance-os/01_AGENT_ROLES.md",
    "docs/agent-governance-os/02_AGENT_BOUNDARIES.md",
    "docs/agent-governance-os/03_AGENT_PROMPT_LIBRARY.md",
    "docs/agent-governance-os/04_AGENT_OUTPUT_QA.md",
    "docs/agent-governance-os/05_AGENT_COST_CONTROL.md",
    "docs/agent-governance-os/06_AGENT_FAILURE_MODES.md",
    "docs/agent-governance-os/07_AGENT_AUDIT_LOG_POLICY.md",
    "docs/agent-governance-os/99_AGENT_GOVERNANCE_REPORT.md",
    "docs/delegation-os/00_DELEGATION_OS.md",
    "docs/delegation-os/01_WHAT_ONLY_FOUNDER_DOES.md",
    "docs/delegation-os/02_WHAT_CAN_BE_DELEGATED.md",
    "docs/delegation-os/03_FIRST_OPERATOR_PLAYBOOK.md",
    "docs/delegation-os/04_GROWTH_OPERATOR_PLAYBOOK.md",
    "docs/delegation-os/05_DELIVERY_OPERATOR_PLAYBOOK.md",
    "docs/delegation-os/06_WEEKLY_DELEGATION_REVIEW.md",
    "docs/delegation-os/99_DELEGATION_OS_REPORT.md",
]

REQUIRED_CONFIGS = [
    ("config/agent_registry.json", ("version", "global_boundaries", "agents")),
    ("config/agent_prompt_library.json", ("version", "shared_preamble", "prompts")),
]


def verify() -> dict:
    return v9_lib.run_system_check("agent_governance", REQUIRED_FILES, REQUIRED_CONFIGS)


def main() -> int:
    return v9_lib.print_and_exit(verify())


if __name__ == "__main__":
    raise SystemExit(main())
