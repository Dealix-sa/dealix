#!/usr/bin/env python3
"""Verify the Hermes Agents Operating Layer manifest structure.

Local only. No network calls. No provider calls.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "hermes" / "agents" / "manifest.json"
REQUIRED_AGENT_IDS = {
    "revenue_scout",
    "proposal_architect",
    "ops_guardian",
    "security_compliance_sentinel",
    "market_intel_analyst",
    "content_growth_operator",
    "finance_unit_economics_agent",
    "product_qa_agent",
}


def main() -> int:
    if not MANIFEST.exists():
        raise SystemExit(f"Missing Hermes manifest: {MANIFEST}")

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if data.get("default_mode") != "dry_run":
        raise SystemExit("Hermes default_mode must remain dry_run")

    supervisor = data.get("supervisor") or {}
    if supervisor.get("id") != "hermes_supervisor":
        raise SystemExit("Missing hermes_supervisor")

    agents = data.get("agents") or []
    agent_ids = {agent.get("id") for agent in agents if isinstance(agent, dict)}
    missing = REQUIRED_AGENT_IDS - agent_ids
    if missing:
        raise SystemExit(f"Missing Hermes agents: {sorted(missing)}")

    if not data.get("approval_matrix"):
        raise SystemExit("Missing approval_matrix")

    print("HERMES_LAYER_OK")
    print(f"agents={len(agent_ids)} default_mode={data.get('default_mode')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
