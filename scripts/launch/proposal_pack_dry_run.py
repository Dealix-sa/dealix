"""Dry-run: build a sample proposal and render it to markdown.

Usage:
    python scripts/launch/proposal_pack_dry_run.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dealix.launch_os.proposal_engine import VALID_TIERS, build_proposal, render_markdown


def main() -> None:
    account = {
        "account_id": "riyadh_motors_01",
        "company_name": "Riyadh Motors Group",
        "sector": "automotive",
        "pain_ar": (
            "فريق المبيعات يتلقى 200+ عميل محتمل شهرياً لكن 70% منهم لا يُتابعون "
            "بعد أول تواصل. لا يوجد نظام CRM فعّال."
        ),
    }

    print("=" * 65)
    print("DEALIX — Proposal Pack Dry Run (3 Tiers)")
    print("عرض الخدمة التجريبي — ثلاث باقات")
    print("=" * 65)

    for tier in sorted(VALID_TIERS):
        pack = build_proposal(account, tier)
        markdown = render_markdown(pack)

        print(f"\n--- Tier: {tier.upper()} ---")
        print(f"Proposal ID:   {pack.id}")
        print(f"Tier:          {pack.offer_tier}")
        print(f"Client:        {pack.company_name}")
        print(f"Timeline:      {pack.timeline_weeks} weeks")
        print(f"Investment:    {pack.investment_sar:,} SAR")
        print(f"Evidence:      {pack.evidence_level}")
        print(f"Governance:    {pack.governance_status}")
        print(f"Markdown len:  {len(markdown)} chars")

    print("\n--- Full Markdown for 'growth' tier ---")
    growth_pack = build_proposal(account, "growth")
    print(render_markdown(growth_pack))
    print("=" * 65)


if __name__ == "__main__":
    main()
