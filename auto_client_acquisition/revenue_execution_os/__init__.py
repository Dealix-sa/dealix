"""Revenue Execution OS — approval-first product distribution layer.

Unifies the existing Dealix primitives (data_os, governance_os, proof_os,
value_os, sales_os, offer ladder, evidence levels) into one daily founder
workflow: target -> draft -> quality -> approval -> follow-up -> proposal ->
proof -> payment handoff -> onboarding -> renewal.

Doctrine (always): no external sends, no cold automation, no scraping, no
guaranteed claims, every draft pending approval, every output carries a
``governance_decision``.
"""

from __future__ import annotations

from auto_client_acquisition.revenue_execution_os.daily_report import render_daily_report
from auto_client_acquisition.revenue_execution_os.draft_factory import (
    generate_draft,
    generate_drafts,
    render_draft,
)
from auto_client_acquisition.revenue_execution_os.draft_quality import review_drafts, score_draft
from auto_client_acquisition.revenue_execution_os.followup_engine import build_followup_queue
from auto_client_acquisition.revenue_execution_os.metrics import daily_metrics, weekly_metrics
from auto_client_acquisition.revenue_execution_os.offers import OFFER_LADDER, offer_by_key
from auto_client_acquisition.revenue_execution_os.payment_handoff import generate_payment_handoff
from auto_client_acquisition.revenue_execution_os.proof_pack_factory import generate_proof_pack
from auto_client_acquisition.revenue_execution_os.proposal_factory import generate_proposal
from auto_client_acquisition.revenue_execution_os.renewal_engine import generate_renewal
from auto_client_acquisition.revenue_execution_os.sectors import rank_sectors, top_sector
from auto_client_acquisition.revenue_execution_os.win_loss import record_outcome, weekly_learning

__all__ = [
    "OFFER_LADDER",
    "build_followup_queue",
    "daily_metrics",
    "generate_draft",
    "generate_drafts",
    "generate_payment_handoff",
    "generate_proof_pack",
    "generate_proposal",
    "generate_renewal",
    "offer_by_key",
    "rank_sectors",
    "record_outcome",
    "render_daily_report",
    "render_draft",
    "review_drafts",
    "score_draft",
    "top_sector",
    "weekly_learning",
    "weekly_metrics",
]
