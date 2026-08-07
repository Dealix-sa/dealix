"""Dry-run: score 5 sample accounts and print tier table.

Usage:
    python scripts/launch/icp_score_dry_run.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dealix.launch_os.icp_scorer import batch_score

SAMPLE_ACCOUNTS = [
    {
        "account_id": "riyadh_motors_01",
        "account_name": "Riyadh Motors Group",
        "urgency": "critical",
        "revenue_leak_sar": 500_000,
        "process_chaos_score": 14,
        "decision_maker_access": "direct",
        "start_small_score": 9,
        "proof_speed_score": 9,
        "budget_signal": "confirmed",
        "referral_potential_score": 4,
        "compliance_risk_penalty": 0,
        "notes": "Owner spoke at industry event about CRM problems",
    },
    {
        "account_id": "golden_realty_02",
        "account_name": "Golden Realty Co",
        "urgency": "high",
        "revenue_leak_sar": 300_000,
        "process_chaos_score": 12,
        "decision_maker_access": "champion",
        "start_small_score": 8,
        "proof_speed_score": 8,
        "budget_signal": "likely",
        "referral_potential_score": 3,
        "compliance_risk_penalty": 0,
        "notes": "Champion is head of sales; owner approval needed",
    },
    {
        "account_id": "clinic_care_03",
        "account_name": "Clinic Care Network",
        "urgency": "medium",
        "revenue_leak_sar": 150_000,
        "process_chaos_score": 9,
        "decision_maker_access": "gatekeeper",
        "start_small_score": 7,
        "proof_speed_score": 6,
        "budget_signal": "possible",
        "referral_potential_score": 4,
        "compliance_risk_penalty": -5,
        "notes": "Healthcare compliance adds delivery risk",
    },
    {
        "account_id": "food_chain_04",
        "account_name": "Desert Bites F&B",
        "urgency": "low",
        "revenue_leak_sar": 80_000,
        "process_chaos_score": 6,
        "decision_maker_access": "unknown",
        "start_small_score": 5,
        "proof_speed_score": 5,
        "budget_signal": "unlikely",
        "referral_potential_score": 2,
        "compliance_risk_penalty": 0,
        "notes": "Early stage inquiry; not yet qualified",
    },
    {
        "account_id": "gov_entity_05",
        "account_name": "Northern Province Authority",
        "urgency": "low",
        "revenue_leak_sar": 0,
        "process_chaos_score": 4,
        "decision_maker_access": "gatekeeper",
        "start_small_score": 3,
        "proof_speed_score": 2,
        "budget_signal": "unlikely",
        "referral_potential_score": 1,
        "compliance_risk_penalty": -15,
        "notes": "Government entity; long cycle; do not pursue now",
    },
]


def main() -> None:
    results = batch_score(SAMPLE_ACCOUNTS)

    print("=" * 75)
    print("DEALIX — ICP Score Dry Run (5 Sample Accounts)")
    print("تقييم العملاء المحتملين — 5 حسابات تجريبية")
    print("=" * 75)
    print(f"{'#':<3} {'Account':<30} {'Score':<6} {'Tier':<5} {'Action':<20} {'Notes'}")
    print("-" * 75)

    for i, s in enumerate(results, 1):
        notes = s.notes[:30] + ("..." if len(s.notes) > 30 else "")
        print(
            f"{i:<3} {s.account_id:<30} {s.total:<6} {s.tier:<5} {s.action:<20} {notes}"
        )

    print()
    print("BREAKDOWN — Top Account Dimension Scores:")
    top = results[0]
    print(f"  Account: {top.account_id}")
    for dim, val in top.scores.items():
        print(f"    {dim:<35} {val}")

    print("=" * 75)


if __name__ == "__main__":
    main()
