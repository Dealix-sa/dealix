"""Product catalog files are complete."""

from __future__ import annotations

from pathlib import Path

import pytest

REQUIRED_PRODUCTS = [
    "REVENUE_COMMAND_ROOM_OS.md",
    "WHATSAPP_INBOX_FOLLOWUP_OS.md",
    "AI_OUTREACH_TARGETING_OS.md",
    "AI_TRUST_COMPLIANCE_OS.md",
    "PRICING_AND_PACKAGING.md",
    "DELIVERY_SOP.md",
]


def test_all_product_files_exist():
    base = Path("business/products")
    missing = [f for f in REQUIRED_PRODUCTS if not (base / f).exists()]
    assert not missing, f"Missing product files: {missing}"


def test_pricing_has_monthly_range():
    content = Path("business/products/PRICING_AND_PACKAGING.md").read_text(encoding="utf-8")
    assert "ريال" in content
    assert "Sprint" in content


def test_delivery_sop_has_weeks():
    content = Path("business/products/DELIVERY_SOP.md").read_text(encoding="utf-8")
    assert "أسبوع" in content or "Sprint" in content
