#!/usr/bin/env python3
"""Verify Founder Console: all 17 founder pages exist and the shared shell +
runtime client modules are present."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report  # noqa: E402

LAYER = "Founder Console"

PAGES = [
    "page.tsx",
    "agents/page.tsx",
    "approvals/page.tsx",
    "control-plane/page.tsx",
    "safety/page.tsx",
    "sandbox/page.tsx",
    "self-evolving/page.tsx",
    "value-engine/page.tsx",
    "ceo/page.tsx",
    "ceo-os/page.tsx",
    "founder-leverage/page.tsx",
    "capital-allocation/page.tsx",
    "strategy/page.tsx",
    "market-attack/page.tsx",
    "moat/page.tsx",
    "ai-governance/page.tsx",
    "company-memory/page.tsx",
]


def main() -> None:
    rels = [f"apps/web/app/{p}" for p in PAGES]
    rels.append("apps/web/components/founder-console/founder-shell.tsx")
    rels.append("apps/web/lib/dealix-runtime.ts")
    reasons = must_exist(*rels)
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
