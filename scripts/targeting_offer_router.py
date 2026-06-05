#!/usr/bin/env python3
"""Offer router — Company → Weakness → Dealix OS angle → Offer → Draft type.

Once we know a company's primary weakness, the router picks the right first
commercial offer from the Dealix ladder. The default first offer is the
**Command Sprint** (Revenue + Proof + Command + Governance Lite, 7 days) — every
company can start there. Partner-potential leads route to a Partner Diagnostic
instead of a sell.

Usage:
    python scripts/targeting_offer_router.py --in data/targeting/company_master.jsonl
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.targeting_common import COMPANY_MASTER, load_companies, load_sectors, load_signals
from scripts.targeting_weakness_mapper import map_weaknesses

# Offer catalog — the 5-rung ladder, entry points only. Each offer names the
# draft template the Draft Lab should produce for first contact.
OFFERS = {
    "command_sprint": {
        "name_en": "Dealix Command Sprint (7 days)",
        "name_ar": "Dealix Command Sprint — 7 أيام",
        "price_sar": 499,
        "includes": ["Revenue Map", "Proof Register", "Executive Command Brief", "Next Action Board"],
        "draft": "command_sprint_offer",
    },
    "business_os_setup": {
        "name_en": "Business OS Setup",
        "name_ar": "تأسيس Business OS",
        "price_sar": 1500,
        "includes": ["Delivery visibility", "Client memory", "Data consolidation"],
        "draft": "command_sprint_offer",
    },
    "delivery_os_lite": {
        "name_en": "Delivery OS Lite",
        "name_ar": "Delivery OS Lite",
        "price_sar": 1500,
        "includes": ["Delivery board", "Acceptance criteria", "Status visibility"],
        "draft": "command_sprint_offer",
    },
    "partner_diagnostic": {
        "name_en": "Partner Diagnostic",
        "name_ar": "تشخيص شريك",
        "price_sar": 0,
        "includes": ["Partner fit map", "Co-sell angle", "Referral mechanics"],
        "draft": "partner_outreach",
    },
}

# Primary weakness → offer id. Ordered, specific routing.
WEAKNESS_TO_OFFER = {
    "partner_potential": "partner_diagnostic",
    "delivery_blindness": "delivery_os_lite",
    "data_fragmentation": "business_os_setup",
    "client_memory_gap": "business_os_setup",
    # Everything else (revenue_leakage, proof_gap, command_fog, support_recurrence,
    # governance_risk) starts with the Command Sprint.
}
DEFAULT_OFFER = "command_sprint"


def route_offer(
    company: dict[str, Any],
    *,
    signals: dict[str, Any] | None = None,
    sectors: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the routed offer for a company, with the weakness it is based on."""
    mapping = map_weaknesses(company, signals=signals, sectors=sectors)
    primary = mapping["primary_weakness"]
    offer_id = WEAKNESS_TO_OFFER.get(primary, DEFAULT_OFFER)
    offer = OFFERS[offer_id]
    return {
        "company_name": company.get("company_name"),
        "primary_weakness": primary,
        "primary_os_angle": mapping["primary_os_angle"],
        "offer_id": offer_id,
        "offer": offer,
        "draft_type": offer["draft"],
        "weaknesses": mapping["weaknesses"],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix offer router")
    ap.add_argument("--in", dest="infile", default=str(COMPANY_MASTER))
    args = ap.parse_args(argv)

    companies = load_companies(Path(args.infile))
    routed = [route_offer(c) for c in companies]
    print(json.dumps(routed, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
