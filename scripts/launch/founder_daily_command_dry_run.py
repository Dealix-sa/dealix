"""Dry-run: generate today's founder daily brief from sample data.

Usage:
    python scripts/launch/founder_daily_command_dry_run.py
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dealix.launch_os.founder_daily_command import generate_daily_command, render_brief
from dealix.launch_os.pipeline_tracker import PipelineStage, PipelineTracker

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
    },
]


def main() -> None:
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        tmp_path = f.name

    try:
        tracker = PipelineTracker(path=tmp_path)

        # Seed sample pipeline.
        tracker.add(
            "Riyadh Motors Group",
            offer_id="REVENUE_LEAK_AUDIT",
            value_sar=15_000, icp_score=82,
            next_action="Send intro email today",
        )
        golden = tracker.add(
            "Golden Realty Co",
            offer_id="SALES_COMMAND_CENTER",
            value_sar=25_000, icp_score=70,
            next_action="Book discovery call",
        )
        clinic = tracker.add(
            "Clinic Care Network",
            offer_id="WHATSAPP_FOLLOWUP_OS",
            value_sar=12_000, icp_score=60,
            next_action="Send proposal draft",
        )
        tracker.update_stage(golden.id, PipelineStage.OUTREACH)
        tracker.update_stage(clinic.id, PipelineStage.PROPOSAL)

        approval_queue = [
            {"item": "Email draft for Acme Motors (REVENUE_LEAK_AUDIT) — awaiting founder sign-off"},
        ]

        cmd = generate_daily_command(tracker, SAMPLE_ACCOUNTS, approval_queue=approval_queue)
        brief = render_brief(cmd)

        print(brief)

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


if __name__ == "__main__":
    main()
