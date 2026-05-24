#!/usr/bin/env python3
"""Verify the Dealix brand system is in place."""

from __future__ import annotations

import json
from pathlib import Path

from _verify_common import ROOT, Verifier


def populate(v: Verifier) -> None:
    v.check_files(
        [
            "docs/brand/brand-tokens.json",
            "docs/brand/DEALIX_BRAND_SYSTEM.md",
            "docs/brand/DEALIX_VISUAL_IDENTITY.md",
            "docs/brand/DEALIX_LOGO_USAGE.md",
            "docs/brand/DEALIX_COLOR_SYSTEM.md",
            "docs/brand/DEALIX_TYPOGRAPHY.md",
            "docs/brand/DEALIX_BRAND_VOICE.md",
            "docs/brand/DEALIX_MARKETING_ASSET_GUIDE.md",
            "docs/brand/DEALIX_ACCESSIBILITY_GUIDE.md",
            "apps/web/lib/brand-tokens.ts",
            "apps/web/styles/brand.css",
            "apps/web/components/brand/DealixLogo.tsx",
            "apps/web/components/brand/BrandCard.tsx",
            "apps/web/components/brand/MetricCard.tsx",
            "apps/web/components/brand/StatusBadge.tsx",
            "apps/web/components/brand/SectionHeading.tsx",
            "apps/web/components/brand/CTAButton.tsx",
            "apps/web/components/brand/DataSourceTag.tsx",
            "apps/web/components/brand/index.ts",
            "assets/brand/logo/dealix-logo.svg",
            "assets/brand/wordmark/dealix-wordmark.svg",
            "assets/brand/icon/dealix-icon.svg",
            "assets/brand/monochrome/dealix-wordmark-mono.svg",
            "assets/brand/social/dealix-og.svg",
            "assets/brand/favicons/favicon.svg",
            "public/brand/dealix-logo.svg",
            "apps/web/public/brand/dealix-logo.svg",
        ]
    )

    tokens_path = ROOT / "docs" / "brand" / "brand-tokens.json"
    if tokens_path.exists():
        try:
            with tokens_path.open("r", encoding="utf-8") as fh:
                tokens = json.load(fh)
            primary = tokens.get("color", {}).get("primary", {})
            for key, expected in {
                "deep_navy": "#0B1220",
                "emerald_teal": "#00D1A1",
                "soft_silver": "#B2BBC6",
                "slate": "#0F1726",
                "white": "#FFFFFF",
            }.items():
                v.custom(primary.get(key) == expected, f"brand-tokens.color.primary.{key} == {expected}")
        except json.JSONDecodeError as exc:
            v.custom(False, f"brand-tokens.json parses cleanly ({exc})")


if __name__ == "__main__":
    from _verify_common import main_for

    main_for("brand-system", populate)
