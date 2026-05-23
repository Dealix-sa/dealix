#!/usr/bin/env python3
"""Verify the Ultimate Operating Layer (Founder Console + Internal API)."""

from __future__ import annotations

import sys
from pathlib import Path

PAGES = [
    "ceo", "sales-cockpit", "approvals", "workers", "trust", "finance",
    "distribution", "delivery", "retention", "proof", "control-plane",
    "audit", "evals", "product", "security", "sovereign",
]

REQUIRED = [
    "CLAUDE.md",
    "docs/ops/CLAUDE_CODE_EXECUTION_REPORT.md",
    "apps/web/components/founder-shell.tsx",
    "apps/web/lib/dealix-runtime.ts",
    "apps/web/lib/dealix-actions.ts",
    "api/internal/auth.py",
    "api/internal/runtime_reader.py",
    "api/internal/policy_adapter.py",
    "api/routers/internal/founder_console.py",
    "scripts/bootstrap_private_ops_runtime.py",
    "scripts/update_worker_state.py",
    "scripts/generate_operating_scorecard.py",
    "scripts/generate_sovereign_readiness.py",
]


def main() -> int:
    missing = []
    for path in REQUIRED:
        if not Path(path).exists():
            missing.append(path)
    for page in PAGES:
        if not Path(f"apps/web/app/{page}/page.tsx").exists():
            missing.append(f"apps/web/app/{page}/page.tsx")

    if missing:
        for m in missing:
            print(f"[FAIL] ultimate operating layer missing: {m}", file=sys.stderr)
        return 1

    print(f"[PASS] ultimate operating layer: {len(PAGES)} pages + {len(REQUIRED)} core files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
