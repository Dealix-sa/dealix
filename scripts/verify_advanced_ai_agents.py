#!/usr/bin/env python3
"""Verify the advanced AI agents — Brand Guardian, Growth Strategist,
Distribution Operator, Content Strategist, Offer Architect, Performance
Analyst — are documented and obey the doctrine.

Each agent doc must declare:
- approval_class_max no higher than A2
- eval_required true
- kill_switch true
- audit_required true
- external_send false
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_AGENTS = {
    "brand_guardian": "docs/ai/BRAND_GUARDIAN_AGENT.md",
    "growth_strategist": "docs/ai/GROWTH_STRATEGIST_AGENT.md",
    "distribution_operator": "docs/ai/DISTRIBUTION_OPERATOR_AGENT.md",
    "content_strategist": "docs/ai/CONTENT_STRATEGIST_AGENT.md",
    "offer_architect": "docs/ai/OFFER_ARCHITECT_AGENT.md",
    "performance_analyst": "docs/ai/PERFORMANCE_ANALYST_AGENT.md",
}

ALLOWED_APPROVAL_CLASSES = {"A0", "A1", "A2"}

# These are the doctrine declarations every agent doc must include.
REQUIRED_DECLARATIONS = [
    "eval_required",
    "kill_switch",
    "audit_required",
    "external_send",
]


def check_agent(agent_id: str, rel: str, failures: list[str]) -> None:
    path = ROOT / rel
    if not path.exists():
        failures.append(f"missing agent doc: {rel}")
        return
    text = path.read_text(encoding="utf-8", errors="ignore")

    if f"`{agent_id}`" not in text and f"agent_id = {agent_id}" not in text:
        failures.append(f"{rel}: agent_id '{agent_id}' not declared in doc")

    # approval_class_max
    m = re.search(
        r"approval_class_max\s*[:=]\s*(`?)(A\d)\1", text, re.IGNORECASE
    )
    if not m:
        failures.append(f"{rel}: missing approval_class_max declaration")
    else:
        cls = m.group(2).upper()
        if cls not in ALLOWED_APPROVAL_CLASSES:
            failures.append(
                f"{rel}: approval_class_max={cls} above doctrine cap A2"
            )

    # required declarations
    for key in REQUIRED_DECLARATIONS:
        if key not in text:
            failures.append(f"{rel}: missing declaration '{key}'")

    # external_send must be false
    m_es = re.search(
        r"external_send\s*[:=]\s*(`?)(true|false)\1", text, re.IGNORECASE
    )
    if m_es and m_es.group(2).lower() != "false":
        failures.append(f"{rel}: external_send must be false (doctrine)")


def main() -> int:
    failures: list[str] = []
    for agent_id, rel in REQUIRED_AGENTS.items():
        check_agent(agent_id, rel, failures)

    print("=" * 60)
    print("Dealix Advanced AI Agents Verifier")
    print("=" * 60)
    if not failures:
        print("[PASS] advanced AI agents verified")
        return 0
    print(f"[FAIL] {len(failures)} issue(s):")
    for f in failures:
        print(f"  - {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
