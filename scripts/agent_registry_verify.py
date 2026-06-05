#!/usr/bin/env python3
"""Verify the agent registry + prompt library structure (V9).

Checks that every agent declares a role and a model tier, that global
boundaries enforce founder approval and no external sending, and that every
prompt references a registered agent.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REGISTRY = "config/agent_registry.json"
LIBRARY = "config/agent_prompt_library.json"

EXPECTED_AGENTS = {
    "founder_brief_agent", "commercial_draft_agent", "safety_audit_agent",
    "message_quality_agent", "market_intelligence_agent", "proposal_agent",
    "delivery_agent", "media_social_agent", "investor_readiness_agent",
}

REQUIRED_GLOBAL_BOUNDARIES = {
    "no_external_sending", "no_secrets", "no_unverified_claims",
    "no_autonomous_decisions", "founder_approval_required",
}


def verify() -> dict:
    problems: list[str] = []
    reg_path = v9_lib.REPO / REGISTRY
    lib_path = v9_lib.REPO / LIBRARY

    if not reg_path.is_file():
        problems.append(f"{REGISTRY} missing")
    if not lib_path.is_file():
        problems.append(f"{LIBRARY} missing")

    agent_ids: set[str] = set()
    if reg_path.is_file():
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
        gb = reg.get("global_boundaries", {})
        for b in REQUIRED_GLOBAL_BOUNDARIES:
            if not gb.get(b):
                problems.append(f"global boundary not enforced: {b}")
        for agent in reg.get("agents", []):
            aid = agent.get("id")
            agent_ids.add(aid)
            if not agent.get("role"):
                problems.append(f"agent {aid} missing role")
            if not agent.get("model_tier"):
                problems.append(f"agent {aid} missing model_tier")
        missing_agents = EXPECTED_AGENTS - agent_ids
        if missing_agents:
            problems.append(f"missing expected agents: {sorted(missing_agents)}")

    if lib_path.is_file():
        lib = json.loads(lib_path.read_text(encoding="utf-8"))
        if not lib.get("shared_preamble"):
            problems.append("prompt library missing shared_preamble")
        for p in lib.get("prompts", []):
            if p.get("agent_id") not in agent_ids and agent_ids:
                problems.append(f"prompt {p.get('name')} references unknown agent {p.get('agent_id')}")

    report = {
        "system": "agent_registry",
        "verdict": "PASS" if not problems else "FAIL",
        "agent_count": len(agent_ids),
        "problems": problems,
    }
    v9_lib.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (v9_lib.OUTPUT_DIR / "agent_registry.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    report = verify()
    print(f"[agent_registry] verdict={report['verdict']} agents={report['agent_count']}")
    for p in report["problems"]:
        print(f"  - {p}")
    print(f"AGENT_REGISTRY_VERDICT={report['verdict']}")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
