#!/usr/bin/env python3
"""Verify Agent Registry: every agent has owner, kpi, kill_switch,
eval_required, audit_required, failure_mode."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO_ROOT, report  # noqa: E402

LAYER = "Agent Registry"
REQUIRED_FIELDS = ("id", "name", "owner", "purpose", "kpi", "kill_switch",
                   "eval_required", "audit_required", "failure_mode")
MIN_AGENTS = 5


def main() -> None:
    reasons: list[str] = []
    path = REPO_ROOT / "registries" / "agent_registry.yaml"
    if not path.exists():
        report(LAYER, False, ["missing: registries/agent_registry.yaml"])

    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
    except ImportError:
        # fallback to token check
        for f in REQUIRED_FIELDS:
            if f"{f}:" not in text:
                reasons.append(f"missing field token: {f}")
        report(LAYER, not reasons, reasons)

    if not isinstance(data, dict):
        report(LAYER, False, ["yaml root must be mapping"])

    agents = data.get("agents") or []
    if len(agents) < MIN_AGENTS:
        reasons.append(f"agents count {len(agents)} < {MIN_AGENTS}")

    seen_ids = set()
    for agent in agents:
        if not isinstance(agent, dict):
            reasons.append("agent entry not a mapping")
            continue
        for f in REQUIRED_FIELDS:
            if f not in agent:
                reasons.append(f"agent {agent.get('id', '?')!r} missing: {f}")
        aid = agent.get("id")
        if aid in seen_ids:
            reasons.append(f"duplicate agent id: {aid}")
        seen_ids.add(aid)

    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
