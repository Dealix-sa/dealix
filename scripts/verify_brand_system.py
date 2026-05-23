#!/usr/bin/env python3
"""
Verify the Dealix brand system.

Checks:
- Required brand docs exist.
- Brand tokens JSON parses and contains required keys.
- TypeScript / CSS bindings exist.
- Brand SVG sources exist.
- Public brand assets exist.
- Brand components exist.
- Color contrasts meet WCAG AA for the documented combinations.

Exits non-zero on any failure. Prints a bilingual summary at the end.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "docs/brand/DEALIX_BRAND_SYSTEM.md",
    "docs/brand/DEALIX_VISUAL_IDENTITY.md",
    "docs/brand/DEALIX_LOGO_USAGE.md",
    "docs/brand/DEALIX_COLOR_SYSTEM.md",
    "docs/brand/DEALIX_TYPOGRAPHY.md",
    "docs/brand/DEALIX_BRAND_VOICE.md",
    "docs/brand/DEALIX_MARKETING_ASSET_GUIDE.md",
    "docs/brand/DEALIX_ACCESSIBILITY_GUIDE.md",
]

REQUIRED_TOKEN_FILES = [
    "docs/brand/brand-tokens.json",
    "apps/web/lib/brand-tokens.ts",
    "apps/web/styles/brand.css",
]

REQUIRED_ASSETS = [
    "assets/brand/source/dealix-logo-full.svg",
    "assets/brand/source/dealix-mark.svg",
    "assets/brand/source/dealix-wordmark.svg",
    "assets/brand/source/dealix-mark-mono.svg",
    "assets/brand/source/dealix-favicon.svg",
    "assets/brand/source/dealix-social-card.svg",
    "assets/brand/logo/dealix-logo-full.svg",
    "assets/brand/icon/dealix-mark.svg",
    "assets/brand/wordmark/dealix-wordmark.svg",
    "assets/brand/monochrome/dealix-mark-mono.svg",
    "assets/brand/social/dealix-social-card.svg",
    "assets/brand/favicons/favicon.svg",
    "apps/web/public/brand/dealix-logo-full.svg",
    "apps/web/public/brand/dealix-mark.svg",
    "apps/web/public/brand/favicon.svg",
    "apps/web/public/brand/og.svg",
]

REQUIRED_COMPONENTS = [
    "apps/web/components/brand/dealix-logo.tsx",
    "apps/web/components/brand/brand-card.tsx",
    "apps/web/components/brand/metric-card.tsx",
    "apps/web/components/brand/status-badge.tsx",
    "apps/web/components/brand/section-heading.tsx",
    "apps/web/components/brand/cta-button.tsx",
    "apps/web/components/brand/founder-nav.tsx",
    "apps/web/components/brand/page-shell.tsx",
]

REQUIRED_TOKEN_KEYS = ["brand", "color", "typography", "spacing", "radius", "shadow", "accessibility"]

BANNED_VOICE = [
    r"guarantee[d]?\s+(revenue|sales|leads|results|pipeline|roi)",
    r"\d+x\s+(your|in)\s+(sales|revenue|pipeline|leads|growth)",
    r"fully\s+autonomous\s+(outbound|sales|sending|posting)",
    r"unlimited\s+(sends|outreach|automation|leads|messages)",
    r"set\s+(it|and)\s+forget\s*(it)?",
    r"revolutioniz(e|es|ed|ing)\s+(your|the)\s+(sales|revenue|business)",
]

# Files designed to document anti-examples — voice patterns may appear
# verbatim inside ❌ blocks or regex listings.
VOICE_EXAMPLE_FILES = {
    "docs/marketing/COPYWRITING_RULES.md",
    "docs/marketing/BRAND_VOICE_EXAMPLES.md",
    "docs/brand/DEALIX_BRAND_VOICE.md",
}


def _is_documented_anti_example(text: str, match_start: int) -> bool:
    """Return True when the match sits inside an anti-example block."""
    line_start = text.rfind("\n", 0, match_start) + 1
    line_end = text.find("\n", match_start)
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end]
    if any(marker in line for marker in ("❌", "Banned", "Forbidden")):
        return True
    if re.search(r"\bno\s+(guaranteed|guarantee|multipliers|claims)\b", line, re.IGNORECASE):
        return True
    if re.search(
        r"\b(no|never|do\s+not|don['’]t)\b.{0,60}\b(claim|claims|guarantee|guarantees|guaranteed|revenue|leads)\b",
        line,
        re.IGNORECASE,
    ):
        return True
    block_start = max(0, line_start - 600)
    block_end = min(len(text), line_end + 200)
    block = text[block_start:block_end]
    if (
        "❌" in block
        or "Off-voice" in block
        or "### Forbidden" in block
        or "## Banned" in block
        or "Banned phrases" in block
        or "anti-pattern" in block.lower()
    ):
        return True
    if "```" in block and ("regex" in block.lower() or "(?i)" in block):
        return True
    return False


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _channel_l(c: int) -> float:
    s = c / 255.0
    return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4


def _luminance(hex_color: str) -> float:
    r, g, b = _hex_to_rgb(hex_color)
    return 0.2126 * _channel_l(r) + 0.7152 * _channel_l(g) + 0.0722 * _channel_l(b)


def contrast_ratio(fg: str, bg: str) -> float:
    l1, l2 = _luminance(fg), _luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def main() -> int:
    failures: list[str] = []
    passes: list[str] = []

    # 1. Required docs
    for rel in REQUIRED_DOCS + REQUIRED_TOKEN_FILES + REQUIRED_ASSETS + REQUIRED_COMPONENTS:
        p = REPO_ROOT / rel
        if not p.exists() or p.stat().st_size == 0:
            failures.append(f"missing: {rel}")
        else:
            passes.append(rel)

    # 2. Tokens JSON shape
    tokens_path = REPO_ROOT / "docs/brand/brand-tokens.json"
    if tokens_path.exists():
        try:
            tokens = json.loads(tokens_path.read_text(encoding="utf-8"))
            for k in REQUIRED_TOKEN_KEYS:
                if k not in tokens:
                    failures.append(f"brand-tokens.json missing key: {k}")
            colors = tokens.get("color", {}).get("primary", {})
            expected_colors = {
                "deep_navy": "#0B1220",
                "emerald_teal": "#00D1A1",
                "soft_silver": "#B2BBC6",
                "slate": "#0F1726",
                "white": "#FFFFFF",
            }
            for k, expected in expected_colors.items():
                actual = colors.get(k)
                if actual is None or actual.upper() != expected.upper():
                    failures.append(f"brand-tokens.json color.{k} = {actual} (expected {expected})")
        except Exception as exc:
            failures.append(f"brand-tokens.json parse error: {exc}")

    # 3. Contrast checks (WCAG AA body: 4.5; large: 3.0)
    contrast_cases = [
        ("#FFFFFF", "#0B1220", 4.5, "white on deep_navy (body)"),
        ("#B2BBC6", "#0B1220", 4.5, "soft_silver on deep_navy (body)"),
        ("#00D1A1", "#0B1220", 3.0, "emerald_teal on deep_navy (large/CTA)"),
        ("#FFFFFF", "#0F1726", 4.5, "white on slate (body)"),
        ("#B2BBC6", "#0F1726", 4.5, "soft_silver on slate (body)"),
    ]
    for fg, bg, floor, label in contrast_cases:
        ratio = contrast_ratio(fg, bg)
        if ratio + 1e-6 < floor:
            failures.append(f"contrast {label}: {ratio:.2f} < {floor}")
        else:
            passes.append(f"contrast {label}: {ratio:.2f} ≥ {floor}")

    # 4. Banned voice patterns inside brand + positioning docs
    for rel in REQUIRED_DOCS + [
        "docs/marketing/COPYWRITING_RULES.md",
        "docs/marketing/BRAND_VOICE_EXAMPLES.md",
    ]:
        p = REPO_ROOT / rel
        if not p.exists():
            continue
        if rel in VOICE_EXAMPLE_FILES:
            # Files designed to document banned patterns — skip body scan.
            continue
        text = p.read_text(encoding="utf-8")
        for pattern in BANNED_VOICE:
            for m in re.finditer(pattern, text, flags=re.IGNORECASE):
                if _is_documented_anti_example(text, m.start()):
                    continue
                snippet = text[max(0, m.start() - 60): m.end() + 60].replace("\n", " ")
                failures.append(f"banned voice in {rel}: …{snippet}…")

    print("=== Dealix Brand System Verifier ===")
    print(f"checks passed: {len(passes)}")
    if failures:
        print(f"failures: {len(failures)}")
        for f in failures:
            print(f"  - {f}")
        print("\nVERDICT: FAIL")
        print("الحُكم: فشل (راجع القائمة أعلاه)")
        return 1
    print("\nVERDICT: PASS")
    print("الحُكم: اجتاز نظام الهوية")
    return 0


if __name__ == "__main__":
    sys.exit(main())
