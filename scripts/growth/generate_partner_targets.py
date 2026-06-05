#!/usr/bin/env python3
"""Generate the Dealix partner-target categories (generic types only, no contacts)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.growth._common import (  # noqa: E402
    DATA_DIR,
    assert_single_cta,
    ensure_dirs,
    write_csv,
)

_OUT = DATA_DIR / "partner_targets.csv"

_HEADER = (
    "partner_type",
    "why_fit",
    "tier",
    "commission_range",
    "first_offer",
    "single_cta",
)

# Generic partner categories only. No real company names or contacts (no scraping).
_PARTNERS: list[dict[str, Any]] = [
    {
        "partner_type": "marketing_agencies",
        "why_fit": "Serve the same SMB owners and need proof of delivered value.",
        "tier": "referral",
        "commission_range": "10-15%",
        "first_offer": "Co-branded Free Diagnostic for their client base.",
        "single_cta": "Free Diagnostic",
    },
    {
        "partner_type": "training_providers",
        "why_fit": "Need to evidence post-training adoption and impact.",
        "tier": "referral",
        "commission_range": "10-15%",
        "first_offer": "Adoption visibility add-on after a program.",
        "single_cta": "Business OS Score",
    },
    {
        "partner_type": "independent_consultants",
        "why_fit": "Want to prove value per engagement without heavy tooling.",
        "tier": "reseller",
        "commission_range": "15-20%",
        "first_offer": "Command Sprint delivered under their brand.",
        "single_cta": "Command Sprint",
    },
    {
        "partner_type": "crm_implementers",
        "why_fit": "Complement CRM rollouts with governed proof and value records.",
        "tier": "integration",
        "commission_range": "10-15%",
        "first_offer": "Proof and value layer on top of a CRM go-live.",
        "single_cta": "Free Diagnostic",
    },
    {
        "partner_type": "it_services",
        "why_fit": "Already trusted for delivery; can add governed AI operations.",
        "tier": "reseller",
        "commission_range": "15-20%",
        "first_offer": "Delivery visibility pilot for an existing account.",
        "single_cta": "Business OS Score",
    },
    {
        "partner_type": "accounting_finance",
        "why_fit": "Link work performed to documented client value.",
        "tier": "referral",
        "commission_range": "10-15%",
        "first_offer": "Proof Gap Audit for their advisory clients.",
        "single_cta": "Command Sprint",
    },
    {
        "partner_type": "hr_providers",
        "why_fit": "Preserve candidate and client context across interactions.",
        "tier": "referral",
        "commission_range": "10-15%",
        "first_offer": "Client Memory Score for their service lines.",
        "single_cta": "Free Diagnostic",
    },
]


def build_rows() -> list[tuple[Any, ...]]:
    """Return validated partner rows sorted by partner type."""
    for partner in _PARTNERS:
        assert_single_cta(partner["single_cta"])
    ordered = sorted(_PARTNERS, key=lambda p: p["partner_type"])
    return [tuple(p[col] for col in _HEADER) for p in ordered]


def main() -> int:
    """Write the partner-target CSV and print a summary line."""
    ensure_dirs()
    rows = build_rows()
    size = write_csv(_OUT, _HEADER, rows)
    print(f"partner_targets: wrote {len(rows)} partner types to {_OUT} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
