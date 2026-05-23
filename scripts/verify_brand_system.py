#!/usr/bin/env python3
"""Verify the Dealix brand system is present and internally consistent."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/brand/brand-tokens.json",
    "docs/brand/DEALIX_BRAND_SYSTEM.md",
    "docs/brand/DEALIX_VISUAL_IDENTITY.md",
    "docs/brand/DEALIX_LOGO_USAGE.md",
    "docs/brand/DEALIX_COLOR_SYSTEM.md",
    "docs/brand/DEALIX_TYPOGRAPHY.md",
    "docs/brand/DEALIX_BRAND_VOICE.md",
    "apps/web/lib/brand-tokens.ts",
    "apps/web/styles/brand.css",
    "apps/web/components/brand/dealix-logo.tsx",
    "apps/web/components/brand/brand-card.tsx",
    "apps/web/components/brand/metric-card.tsx",
    "apps/web/components/brand/status-badge.tsx",
    "apps/web/components/brand/section-heading.tsx",
    "apps/web/components/brand/cta-button.tsx",
    "apps/web/components/brand/trust-badge.tsx",
    "apps/web/components/brand/growth-arrow.tsx",
    "apps/web/components/brand/proof-card.tsx",
    "apps/web/components/brand/offer-card.tsx",
    "apps/web/components/founder-shell.tsx",
    "assets/brand/source/README.md",
]

REQUIRED_COLORS = ["#0B1220", "#00D1A1", "#B2BBC6", "#0F1726", "#FFFFFF"]


def main() -> int:
    print(f"[brand-system] REPO={REPO}", flush=True)
    print(f"[brand-system] cwd={Path.cwd()}", flush=True)
    print(f"[brand-system] __file__={__file__}", flush=True)
    print(f"[brand-system] REPO exists={REPO.exists()}", flush=True)
    print(f"[brand-system] docs/brand exists={(REPO / 'docs/brand').exists()}", flush=True)
    print(f"[brand-system] assets/brand exists={(REPO / 'assets/brand').exists()}", flush=True)
    missing = [f for f in REQUIRED_FILES if not (REPO / f).exists()]
    tokens_path = REPO / "docs/brand/brand-tokens.json"
    color_issues: list[str] = []
    if tokens_path.exists():
        tokens = json.loads(tokens_path.read_text(encoding="utf-8"))
        present_colors = set(tokens.get("colors", {}).values())
        for c in REQUIRED_COLORS:
            if c not in present_colors:
                color_issues.append(f"missing color {c}")
    else:
        color_issues.append("brand-tokens.json not readable")

    print("[brand-system]", flush=True)
    print(f"  missing files     : {len(missing)}", flush=True)
    for m in missing:
        print(f"    - {m}", flush=True)
    print(f"  color issues      : {len(color_issues)}", flush=True)
    for c in color_issues:
        print(f"    - {c}", flush=True)
    fail = bool(missing) or bool(color_issues)
    if fail:
        # GitHub Actions ::error annotation surfaces in PR check details.
        msg = f"missing={missing} colors={color_issues}"
        # Trim to keep annotation under GH's 4000 char cap
        print(f"::error file=scripts/verify_brand_system.py::brand verifier failed: {msg[:3000]}", flush=True)
    print("RESULT:", "FAIL" if fail else "PASS", flush=True)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
