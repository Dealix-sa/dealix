"""Launch OS — entry-point module for the Dealix 90-day commercial plan.

Exports the main classes and functions from each submodule so callers can do:

    from dealix.launch_os import ICPScore, score_account, VerticalScore, ...
"""
from __future__ import annotations

from dealix.launch_os.founder_daily_command import (
    DailyCommand,
    generate_daily_command,
    render_brief,
)
from dealix.launch_os.icp_scorer import (
    ICPScore,
    batch_score,
    score_account,
    tier_label,
)
from dealix.launch_os.outreach_factory import (
    CHANNEL_TEMPLATES,
    OutreachDraft,
    build_draft,
)
from dealix.launch_os.pipeline_tracker import (
    PipelineItem,
    PipelineStage,
    PipelineTracker,
)
from dealix.launch_os.proposal_engine import (
    ProposalPack,
    build_proposal,
    render_markdown,
)
from dealix.launch_os.trust_preflight import (
    TrustViolation,
    run_preflight,
)
from dealix.launch_os.vertical_scorer import (
    SAUDI_VERTICALS,
    VerticalScore,
    rank_verticals,
    top_wedge,
)

__all__ = [
    # icp_scorer
    "ICPScore",
    "batch_score",
    "score_account",
    "tier_label",
    # vertical_scorer
    "SAUDI_VERTICALS",
    "VerticalScore",
    "rank_verticals",
    "top_wedge",
    # trust_preflight
    "TrustViolation",
    "run_preflight",
    # outreach_factory
    "CHANNEL_TEMPLATES",
    "OutreachDraft",
    "build_draft",
    # proposal_engine
    "ProposalPack",
    "build_proposal",
    "render_markdown",
    # pipeline_tracker
    "PipelineItem",
    "PipelineStage",
    "PipelineTracker",
    # founder_daily_command
    "DailyCommand",
    "generate_daily_command",
    "render_brief",
]
