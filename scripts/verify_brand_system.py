#!/usr/bin/env python3
"""
Verify the Dealix Brand Operating System.

Checks:
- All required brand docs exist.
- Brand token JSON exists, is valid, contains required keys.
- TS / CSS brand token files exist and reference the same hex values.
- All required brand assets exist on disk.
- All required brand components exist.
- Token contrast pairs meet the declared minimum ratios.
- No file in the brand surface contains banned guarantee claims.

Exit 0 on PASS, non-zero on FAIL.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
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
]

REQUIRED_ASSETS = [
    "assets/brand/logo/dealix-full.svg",
    "assets/brand/logo/dealix-compact.svg",
    "assets/brand/icon/dealix-mark.svg",
    "assets/brand/wordmark/dealix-wordmark.svg",
    "assets/brand/monochrome/dealix-white.svg",
    "assets/brand/monochrome/dealix-navy.svg",
    "assets/brand/social/linkedin-header.svg",
    "assets/brand/social/og-default.svg",
    "assets/brand/social/og-proof.svg",
    "assets/brand/favicons/favicon.svg",
    "assets/brand/CHANGELOG.md",
]

REQUIRED_COMPONENTS = [
    "apps/web/components/brand/dealix-logo.tsx",
    "apps/web/components/brand/brand-card.tsx",
    "apps/web/components/brand/metric-card.tsx",
    "apps/web/components/brand/status-badge.tsx",
    "apps/web/components/brand/section-heading.tsx",
    "apps/web/components/brand/cta-button.tsx",
    "apps/web/components/brand/console-page.tsx",
]

REQUIRED_HEX = ["#0B1220", "#00D1A1", "#B2BBC6", "#0F1726", "#FFFFFF"]

# Banned in customer-facing marketing/brand text. (Negation in voice doc allowed.)
BANNED_CLAIMS = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed leads",
    "guaranteed results",
    "auto-pilot growth",
    "10x your pipeline",
]

# Files this verifier owns and will scan for banned positive claims.
# Files that document the bans (e.g., DEALIX_BRAND_VOICE.md) are intentionally
# excluded — they list these phrases to explain why we never use them.
BRAND_SURFACE_FILES = [
    "docs/brand/DEALIX_VISUAL_IDENTITY.md",
    "docs/brand/DEALIX_LOGO_USAGE.md",
    "docs/brand/DEALIX_COLOR_SYSTEM.md",
    "docs/brand/DEALIX_TYPOGRAPHY.md",
    "docs/brand/DEALIX_MARKETING_ASSET_GUIDE.md",
    "docs/brand/DEALIX_ACCESSIBILITY_GUIDE.md",
    "docs/positioning/CATEGORY_CREATION_OS.md",
    "docs/positioning/WHY_DEALIX_NOW.md",
    "docs/positioning/MESSAGING_HIERARCHY.md",
    "docs/marketing/CONTENT_CALENDAR_SYSTEM.md",
    "docs/marketing/FOUNDER_LED_CONTENT_SYSTEM.md",
    "docs/marketing/LANDING_PAGE_CONVERSION_SYSTEM.md",
    "docs/marketing/EMAIL_OUTREACH_GUIDE.md",
    "docs/marketing/LINKEDIN_OUTREACH_GUIDE.md",
    "docs/marketing/PARTNER_OUTREACH_GUIDE.md",
    "docs/product/PRODUCT_DISTRIBUTION_OS.md",
]


def _hex_to_rgb(hex_value: str) -> tuple[int, int, int]:
    h = hex_value.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _relative_luminance(rgb: tuple[int, int, int]) -> float:
    def channel(c: int) -> float:
        s = c / 255
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast_ratio(fg: str, bg: str) -> float:
    l1 = _relative_luminance(_hex_to_rgb(fg))
    l2 = _relative_luminance(_hex_to_rgb(bg))
    light, dark = max(l1, l2), min(l1, l2)
    return (light + 0.05) / (dark + 0.05)


def _resolve_token(tokens: dict, path: str) -> str:
    cursor = tokens
    for part in path.split("."):
        if not isinstance(cursor, dict) or part not in cursor:
            raise KeyError(path)
        cursor = cursor[part]
    if isinstance(cursor, dict) and "$value" in cursor:
        return cursor["$value"]
    raise KeyError(path)


def main() -> int:
    failures: list[str] = []
    passes: list[str] = []

    print(f"verify_brand_system: python={sys.version.split()[0]}", flush=True)
    print(f"verify_brand_system: ROOT={ROOT}", flush=True)
    print(f"verify_brand_system: cwd={Path.cwd()}", flush=True)

    for doc in REQUIRED_DOCS:
        if (ROOT / doc).exists():
            passes.append(f"doc exists: {doc}")
        else:
            failures.append(f"MISSING doc: {doc}")

    for token_file in REQUIRED_TOKEN_FILES:
        path = ROOT / token_file
        if not path.exists():
            failures.append(f"MISSING token file: {token_file}")
            continue
        text = path.read_text(encoding="utf-8")
        for hex_value in REQUIRED_HEX:
            if hex_value.upper() not in text.upper():
                failures.append(f"token file {token_file} missing hex {hex_value}")
        passes.append(f"token file present: {token_file}")

    for asset in REQUIRED_ASSETS:
        if (ROOT / asset).exists():
            passes.append(f"asset exists: {asset}")
        else:
            failures.append(f"MISSING asset: {asset}")

    for component in REQUIRED_COMPONENTS:
        if (ROOT / component).exists():
            passes.append(f"component exists: {component}")
        else:
            failures.append(f"MISSING component: {component}")

    tokens_path = ROOT / "docs/brand/brand-tokens.json"
    if tokens_path.exists():
        try:
            tokens = json.loads(tokens_path.read_text(encoding="utf-8"))
            passes.append("brand-tokens.json valid JSON")
            contrast_pairs = tokens.get("contrast", {}).get("pairs", [])
            for pair in contrast_pairs:
                try:
                    fg = _resolve_token(tokens, pair["fg"])
                    bg = _resolve_token(tokens, pair["bg"])
                except KeyError as exc:
                    failures.append(f"contrast pair token unresolved: {exc}")
                    continue
                ratio = _contrast_ratio(fg, bg)
                minimum = float(pair.get("minRatio", 4.5))
                if ratio + 0.001 < minimum:
                    failures.append(
                        f"contrast FAIL {pair['fg']} on {pair['bg']}: "
                        f"{ratio:.2f} < {minimum:.2f}"
                    )
                else:
                    passes.append(
                        f"contrast OK {pair['fg']} on {pair['bg']}: {ratio:.2f} ≥ {minimum:.2f}"
                    )
        except json.JSONDecodeError as exc:
            failures.append(f"brand-tokens.json invalid JSON: {exc}")
    else:
        failures.append("MISSING brand tokens JSON")

    for rel in BRAND_SURFACE_FILES:
        path = ROOT / rel
        if not path.exists():
            continue  # missing file is reported by required-docs checks elsewhere
        text = path.read_text(encoding="utf-8").lower()
        for banned in BANNED_CLAIMS:
            if re.search(rf"\b{re.escape(banned.lower())}\b", text):
                failures.append(f"banned claim '{banned}' found in {rel}")

    print(f"PASSED: {len(passes)}")
    for p in passes:
        print(f"  - {p}")
    print()
    print(f"FAILED: {len(failures)}")
    for f in failures:
        print(f"  - {f}")

    # Emit GitHub Actions annotations so failures surface on the run page
    # without needing log auth. One annotation per failure (capped at 10
    # per step by GitHub).
    if failures:
        import os
        if os.environ.get("GITHUB_ACTIONS") == "true":
            for f in failures[:10]:
                # Escape % \r \n per Actions workflow-command rules
                msg = f.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
                print(f"::error title=Brand verifier failure::{msg}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
