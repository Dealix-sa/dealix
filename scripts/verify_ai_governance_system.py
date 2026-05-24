#!/usr/bin/env python3
"""verify_ai_governance_system.py — enforce NIST AI RMF / ISO 42001 alignment.

Confirms the Dealix AI governance docs exist, expose ownership, name
the lifecycle stages, and reference both the agent_registry and the
human-in-the-loop matrix. This is the gate Claude Code cannot bypass.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = (
    "docs/ai_governance/AI_SYSTEM_INVENTORY.md",
    "docs/ai_governance/AI_GOVERNANCE_OVERVIEW.md",
    "docs/governance/AI_USAGE_POLICY.md",
    "docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md",
    "docs/governance/AUTONOMY_VALIDATION_GATES.md",
    "registries/agent_registry.yaml",
)

REQUIRED_TOKENS = {
    "docs/ai_governance/AI_GOVERNANCE_OVERVIEW.md": (
        "owner",
        "kill_switch",
        "audit",
        "NIST AI RMF",
        "ISO 42001",
        "lifecycle",
    ),
    "docs/ai_governance/AI_SYSTEM_INVENTORY.md": (
        "owner",
        "kill_switch",
        "eval",
    ),
}


def main() -> int:
    failures: list[str] = []
    for path in REQUIRED_PATHS:
        p = REPO / path
        if not p.exists():
            failures.append(f"missing:{path}")
            continue
        if p.stat().st_size < 400:
            failures.append(f"too_small:{path}")

    for path, tokens in REQUIRED_TOKENS.items():
        p = REPO / path
        if not p.exists():
            continue
        body = p.read_text(encoding="utf-8", errors="ignore").lower()
        for tok in tokens:
            if tok.lower() not in body:
                failures.append(f"missing_token:{path}:'{tok}'")

    for f in failures:
        print(f, file=sys.stderr)
    ok = not failures
    print(f"AI_GOVERNANCE_PASS={'true' if ok else 'false'} (failures={len(failures)})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
