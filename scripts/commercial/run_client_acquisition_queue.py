#!/usr/bin/env python3
"""Generate a safe Dealix client acquisition queue.

This runner is intentionally offline and file-based. It can be wired to Gmail,
Sheets, HubSpot, or other sources later, but this first version produces a
review queue from a seed JSON/CSV-free fallback.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from dealix.client_acquisition import ClientCard, build_queue, write_queue_bundle


def sample_cards(limit: int) -> list[ClientCard]:
    cards = [
        ClientCard(
            company="Saudi service company",
            segment="local_b2b",
            signal="Needs clearer follow-up and opportunity tracking",
            likely_pain="Leads and replies are scattered across channels",
            offer_fit="Revenue Proof Sprint",
            intent_score=75,
            urgency_score=70,
            value_score=65,
            trust_score=60,
            risk_score=20,
        ),
        ClientCard(
            company="Foreign B2B SaaS",
            segment="foreign_market_access",
            signal="Potential Saudi expansion fit",
            likely_pain="Needs local positioning and partner map before hiring",
            offer_fit="Saudi Opportunity Snapshot",
            intent_score=68,
            urgency_score=58,
            value_score=80,
            trust_score=55,
            risk_score=30,
        ),
        ClientCard(
            company="B2G-ready supplier",
            segment="b2g_readiness",
            signal="Needs readiness material and partner map",
            likely_pain="Proposal material and local readiness are incomplete",
            offer_fit="B2G Readiness Diagnostic",
            intent_score=60,
            urgency_score=62,
            value_score=85,
            trust_score=52,
            risk_score=45,
        ),
    ]
    return cards[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Dealix client acquisition queue")
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument(
        "--output",
        default="reports/client_acquisition/latest_queue.json",
        help="Output JSON path",
    )
    args = parser.parse_args()

    bundle = build_queue(sample_cards(args.limit), mode=args.mode)
    output_path = write_queue_bundle(bundle, Path(args.output))
    print(f"CLIENT_ACQUISITION_QUEUE={output_path}")
    print(f"ITEMS={len(bundle.items)}")
    print("MODE=draft-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
