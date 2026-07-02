"""Dry-run: build sample proposals for every catalogue offer and render one to markdown.

Usage:
    python scripts/launch/proposal_pack_dry_run.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dealix.launch_os.proposal_engine import VALID_OFFER_IDS, build_proposal, render_markdown

FEATURED_OFFER = "REVENUE_LEAK_AUDIT"


def main() -> None:
    account = {
        "account_id": "riyadh_motors_01",
        "account_name": "Riyadh Motors Group",
        "sector": "automotive",
    }
    discovery = {
        "pain_ar": (
            "فريق المبيعات يتلقى 200+ عميل محتمل شهرياً لكن 70% منهم لا يُتابعون "
            "بعد أول تواصل. لا يوجد نظام CRM فعّال."
        ),
        "leakage_sar": 180_000,
    }

    print("=" * 65)
    print(f"DEALIX — Proposal Pack Dry Run ({len(VALID_OFFER_IDS)} offers)")
    print("عرض الخدمة التجريبي — سلم العروض الكامل")
    print("=" * 65)

    for offer_id in sorted(VALID_OFFER_IDS):
        pack = build_proposal(account, offer_id, discovery)
        markdown = render_markdown(pack)
        if pack.offer_id != offer_id or not markdown.strip():
            raise SystemExit(f"empty render for {offer_id}")

        print(f"\n--- Offer: {offer_id} ---")
        print(f"Proposal ID:   {pack.id}")
        print(f"Offer (AR):    {pack.offer_name_ar}")
        print(f"Client:        {pack.account_name}")
        print(f"Timeline:      {pack.timeline_weeks} weeks")
        print(f"Investment:    {pack.investment_sar:,} SAR")
        print(f"Evidence:      {pack.evidence_level}")
        print(f"Pricing:       {pack.pricing_status}")
        print(f"Markdown len:  {len(markdown)} chars")

    print(f"\n--- Full Markdown for '{FEATURED_OFFER}' ---")
    print(render_markdown(build_proposal(account, FEATURED_OFFER, discovery)))
    print("=" * 65)


if __name__ == "__main__":
    main()
