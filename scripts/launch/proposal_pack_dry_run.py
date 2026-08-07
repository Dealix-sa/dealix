"""Dry-run: build a sample proposal and render it to markdown.

Usage:
    python scripts/launch/proposal_pack_dry_run.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dealix.launch_os.proposal_engine import VALID_OFFER_IDS, build_proposal, render_markdown


def main() -> None:
    account = {
        "account_id": "riyadh_motors_01",
        "account_name": "Riyadh Motors Group",
        "sector": "automotive",
    }
    discovery_notes = {
        "pain_ar": (
            "فريق المبيعات يتلقى 200+ عميل محتمل شهرياً لكن 70% منهم لا يُتابعون "
            "بعد أول تواصل. لا يوجد نظام CRM فعّال."
        ),
    }

    print("=" * 65)
    print("DEALIX — Proposal Pack Dry Run (All Offers)")
    print("عرض الخدمة التجريبي — جميع الباقات")
    print("=" * 65)

    for offer_id in sorted(VALID_OFFER_IDS):
        pack = build_proposal(account, offer_id, discovery_notes)
        markdown = render_markdown(pack)

        print(f"\n--- Offer: {offer_id} ---")
        print(f"Proposal ID:   {pack.id}")
        print(f"Offer:         {pack.offer_name_ar}")
        print(f"Client:        {pack.account_name}")
        print(f"Timeline:      {pack.timeline_weeks} weeks")
        print(f"Investment:    {pack.investment_sar:,} SAR")
        print(f"Evidence:      {pack.evidence_level}")
        print(f"Pricing:       {pack.pricing_status}")
        print(f"Markdown len:  {len(markdown)} chars")

    print("\n--- Full Markdown for 'REVENUE_LEAK_AUDIT' offer ---")
    sample_pack = build_proposal(account, "REVENUE_LEAK_AUDIT", discovery_notes)
    print(render_markdown(sample_pack))
    print("=" * 65)


if __name__ == "__main__":
    main()
