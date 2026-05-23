#!/usr/bin/env python3
"""Verify the Dealix brand system.

Checks:
- Required brand docs exist under docs/brand/.
- Brand tokens exist in TS / JSON / CSS, and the core hex values agree.
- Reusable brand components exist under apps/web/components/brand/.
- Founder shell exists.
- Brand asset folders exist (with README placeholders).
- The canonical tagline appears in tokens + docs.
- No banned phrases are present anywhere under docs/brand/.

Designed to run from the repo root, no external dependencies.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_BRAND_DOCS = [
    "docs/brand/DEALIX_BRAND_SYSTEM.md",
    "docs/brand/DEALIX_VISUAL_IDENTITY.md",
    "docs/brand/DEALIX_LOGO_USAGE.md",
    "docs/brand/DEALIX_COLOR_SYSTEM.md",
    "docs/brand/DEALIX_TYPOGRAPHY.md",
    "docs/brand/DEALIX_BRAND_VOICE.md",
    "docs/brand/DEALIX_MARKETING_ASSET_GUIDE.md",
    "docs/brand/DEALIX_ACCESSIBILITY_GUIDE.md",
    "docs/brand/brand-tokens.json",
]

REQUIRED_TOKEN_FILES = [
    "apps/web/lib/brand-tokens.ts",
    "apps/web/styles/brand.css",
    "docs/brand/brand-tokens.json",
]

REQUIRED_COMPONENTS = [
    "apps/web/components/brand/dealix-logo.tsx",
    "apps/web/components/brand/brand-card.tsx",
    "apps/web/components/brand/metric-card.tsx",
    "apps/web/components/brand/status-badge.tsx",
    "apps/web/components/brand/section-heading.tsx",
    "apps/web/components/brand/cta-button.tsx",
    "apps/web/components/founder-shell.tsx",
]

REQUIRED_ASSET_PLACEHOLDERS = [
    "assets/brand/source/README.md",
    "apps/web/public/brand/README.md",
    "public/brand/README.md",
]

CANONICAL_HEX = {
    "deepNavy": "#0B1220",
    "emeraldTeal": "#00D1A1",
    "softSilver": "#B2BBC6",
    "slate": "#0F1726",
    "white": "#FFFFFF",
}

TAGLINE_EN = "Intelligent Deals. Real Growth."

# Phrases the Brand Guardian refuses. The case-insensitive search must NOT find
# any of these in brand documents.
BANNED_PHRASES = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed results",
    "guaranteed outcome",
    "fully autonomous",
    "ai that sells for you",
    "10x revenue",
    "100x",
    "revolutionise",
    "revolutionize",
    "world's first revenue operating",
]

# A small allow-list of files where banned phrases may legitimately appear
# because they list what is banned. Path-relative to repo root.
BANNED_ALLOWLIST = {
    "docs/brand/DEALIX_BRAND_VOICE.md",
    "docs/brand/DEALIX_BRAND_SYSTEM.md",
    "docs/brand/DEALIX_MARKETING_ASSET_GUIDE.md",
    "docs/marketing/COPYWRITING_RULES.md",
    "docs/marketing/BRAND_VOICE_EXAMPLES.md",
    "docs/marketing/DEALIX_MARKETING_OS.md",
    "docs/marketing/CONTENT_CALENDAR_SYSTEM.md",
    "docs/marketing/LANDING_PAGE_CONVERSION_SYSTEM.md",
    "docs/marketing/EMAIL_OUTREACH_GUIDE.md",
    "docs/marketing/LINKEDIN_OUTREACH_GUIDE.md",
    "docs/growth/STRATEGIC_TARGETING_OS.md",
    "docs/growth/OUTBOUND_DRAFT_MACHINE.md",
    "docs/growth/INBOUND_CONTENT_MACHINE.md",
    "docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md",
    "docs/product/DEALIX_PRODUCT_LADDER.md",
    "docs/product/PRODUCT_POSITIONING.md",
    "docs/product/OFFER_PACKAGING.md",
    "docs/product/PRICING_GUARDRAILS.md",
    "docs/performance/PERFORMANCE_IMPROVEMENT_OS.md",
    "docs/performance/REVENUE_KPI_TREE.md",
    "docs/ai/BRAND_GUARDIAN_AGENT.md",
    "docs/ai/GROWTH_STRATEGIST_AGENT.md",
    "docs/ai/DISTRIBUTION_OPERATOR_AGENT.md",
    "docs/ai/CONTENT_STRATEGIST_AGENT.md",
    "docs/ai/PERFORMANCE_ANALYST_AGENT.md",
    "docs/ai/OFFER_ARCHITECT_AGENT.md",
}


def _check_exists(rel: str, failures: list[str]) -> None:
    p = ROOT / rel
    if not p.exists():
        failures.append(f"missing file: {rel}")


def _file_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="ignore")


def check_required_files(failures: list[str]) -> None:
    for rel in (
        REQUIRED_BRAND_DOCS
        + REQUIRED_TOKEN_FILES
        + REQUIRED_COMPONENTS
        + REQUIRED_ASSET_PLACEHOLDERS
    ):
        _check_exists(rel, failures)


def check_token_consistency(failures: list[str]) -> None:
    ts_path = ROOT / "apps/web/lib/brand-tokens.ts"
    css_path = ROOT / "apps/web/styles/brand.css"
    json_path = ROOT / "docs/brand/brand-tokens.json"

    if not (ts_path.exists() and css_path.exists() and json_path.exists()):
        # missing-file check will have already reported these
        return

    ts_text = ts_path.read_text(encoding="utf-8")
    css_text = css_path.read_text(encoding="utf-8")
    try:
        json_data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        failures.append(f"brand-tokens.json is not valid JSON: {e}")
        return

    json_colors = json_data.get("colors", {})

    for token, hex_value in CANONICAL_HEX.items():
        # TS file uses camelCase keys with the hex literal
        if hex_value.upper() not in ts_text.upper():
            failures.append(
                f"brand-tokens.ts missing canonical hex {hex_value} for {token}"
            )
        if hex_value.upper() not in css_text.upper():
            failures.append(
                f"styles/brand.css missing canonical hex {hex_value} for {token}"
            )
        json_val = json_colors.get(token, "")
        if json_val.upper() != hex_value.upper():
            failures.append(
                f"brand-tokens.json {token}={json_val!r} does not match {hex_value}"
            )


def check_tagline(failures: list[str]) -> None:
    targets = [
        "docs/brand/DEALIX_BRAND_SYSTEM.md",
        "docs/brand/brand-tokens.json",
        "apps/web/lib/brand-tokens.ts",
    ]
    for rel in targets:
        if not (ROOT / rel).exists():
            continue
        if TAGLINE_EN not in _file_text(rel):
            failures.append(
                f"canonical tagline missing in {rel}: expected exact '{TAGLINE_EN}'"
            )


def check_banned_phrases(failures: list[str]) -> None:
    brand_dirs = ["docs/brand"]
    for sub in brand_dirs:
        d = ROOT / sub
        if not d.exists():
            continue
        for path in d.rglob("*.md"):
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            if rel in BANNED_ALLOWLIST:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            for phrase in BANNED_PHRASES:
                if phrase in text:
                    failures.append(
                        f"banned phrase '{phrase}' found in {rel}"
                    )


def check_color_docs(failures: list[str]) -> None:
    color_doc = ROOT / "docs/brand/DEALIX_COLOR_SYSTEM.md"
    if not color_doc.exists():
        return
    text = color_doc.read_text(encoding="utf-8")
    for token, hex_value in CANONICAL_HEX.items():
        if hex_value not in text:
            failures.append(
                f"DEALIX_COLOR_SYSTEM.md missing canonical hex {hex_value}"
            )


def main() -> int:
    failures: list[str] = []

    check_required_files(failures)
    check_token_consistency(failures)
    check_tagline(failures)
    check_banned_phrases(failures)
    check_color_docs(failures)

    print("=" * 60)
    print("Dealix Brand System Verifier")
    print("=" * 60)
    if not failures:
        print("[PASS] brand system verified")
        return 0

    print(f"[FAIL] {len(failures)} issue(s):")
    for f in failures:
        print(f"  - {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
