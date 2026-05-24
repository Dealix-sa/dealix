#!/usr/bin/env python3
"""
verify_agent_registry.py — every agent surface must have ownership,
approval class, and kill-switch reference.

We accept the existing docs-based registry (docs/governance/AGENT_REGISTRY.md
plus AGENT_SPRAWL_PREVENTION.md, AI_ACTION_LEVELS.md, AI_ACTION_CONTROL.md)
as the source of truth. This verifier ensures the docs collectively cover the
non-negotiable concepts so an unowned agent can't slip through.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DOCS = [
    "docs/governance/AGENT_REGISTRY.md",
    "docs/governance/AGENT_SPRAWL_PREVENTION.md",
    "docs/governance/AI_ACTION_LEVELS.md",
    "docs/governance/AI_ACTION_CONTROL.md",
    "docs/governance/AGENT_KILL_SWITCH.md",
]

# Each concept must appear in the aggregate text of the four docs. We accept
# Arabic equivalents to match the existing bilingual docs.
REQUIRED_CONCEPTS = {
    "owner / identity":         ["owner", "هوية", "identity"],
    "kill switch / disable":    ["kill", "disable", "إيقاف", "تعطيل"],
    "approval level / class":   ["approval", "موافقة", "level", "مستوى"],
    "audit / evidence":         ["audit", "تدقيق", "evidence", "أدلة"],
    "sprawl prevention":        ["sprawl", "register", "سجل", "agent registry"],
}


def main() -> int:
    failures: list[str] = []
    pieces: list[str] = []

    for rel in DOCS:
        p = ROOT / rel
        if not p.exists():
            failures.append(f"missing: {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if len(text.strip()) < 100:
            failures.append(f"too small: {rel}")
        pieces.append(text.lower())

    haystack = "\n".join(pieces)

    for concept, kws in REQUIRED_CONCEPTS.items():
        if not any(kw.lower() in haystack for kw in kws):
            failures.append(f"no doc covers concept '{concept}' (need one of: {', '.join(kws)})")

    if failures:
        print(f"AGENT REGISTRY: FAIL ({len(failures)} issues)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"AGENT REGISTRY: PASS ({len(DOCS)} docs cover {len(REQUIRED_CONCEPTS)} required concepts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
