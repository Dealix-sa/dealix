#!/usr/bin/env python3
"""Verify the product ladder + distribution docs are in place."""

from __future__ import annotations

from _verify_common import Verifier


def populate(v: Verifier) -> None:
    v.check_files(
        [
            "docs/product/DEALIX_PRODUCT_LADDER.md",
            "docs/product/PRODUCT_DISTRIBUTION_OS.md",
            "docs/product/PRODUCT_POSITIONING.md",
            "docs/product/OFFER_PACKAGING.md",
            "docs/product/PRICING_GUARDRAILS.md",
        ]
    )


if __name__ == "__main__":
    from _verify_common import main_for

    main_for("product-distribution", populate)
