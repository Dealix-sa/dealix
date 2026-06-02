"""Market Production OS — governed market-production layer.

Composes existing governance cores (``governance_os``, ``revenue_os``,
``approval_center``, ``safe_send_gateway``) into a single
research -> draft -> gate -> approve -> ramped-send -> reply pipeline.

Hard invariants (see ``docs/market_production_os/``):
  - 250 drafts/day production capacity (``DAILY_DRAFT_TARGET``).
  - 0 auto-sends in every environment (``MAX_AUTO_SENDS == 0``).
  - Every draft carries a ``governance_decision`` and an ``evidence_level``.
"""

from __future__ import annotations

from auto_client_acquisition.market_production_os.approval_queue import (
    eligible_drafts,
    rank_for_approval,
)
from auto_client_acquisition.market_production_os.draft_factory import (
    DAILY_DRAFT_TARGET,
    MAX_AUTO_SENDS,
    build_draft,
    daily_mix,
    produce_drafts,
    summarize_batch,
)
from auto_client_acquisition.market_production_os.prospect_score import (
    QUALIFY_THRESHOLD,
    ProspectScore,
    score_prospect,
)
from auto_client_acquisition.market_production_os.quality_gate import (
    GateResult,
    check_draft,
)
from auto_client_acquisition.market_production_os.reply_router import (
    ReplyRouting,
    classify_and_route,
    classify_reply,
    route_reply,
)
from auto_client_acquisition.market_production_os.report import (
    daily_gtm_report,
    weekly_gtm_review,
)
from auto_client_acquisition.market_production_os.schemas import (
    ApprovalAction,
    BuyingSignal,
    OutreachDraft,
    PersonalizationLevel,
    Prospect,
    ProspectState,
    Reply,
    ReplyClass,
    RiskLevel,
    SendingBatch,
    SendStatus,
    SuppressionEntry,
)
from auto_client_acquisition.market_production_os.sending_ramp import (
    RampDecision,
    allowed_sends_today,
    max_sends_for_week,
)

__all__ = [
    "DAILY_DRAFT_TARGET",
    "MAX_AUTO_SENDS",
    "QUALIFY_THRESHOLD",
    "ApprovalAction",
    "BuyingSignal",
    "GateResult",
    "OutreachDraft",
    "PersonalizationLevel",
    "Prospect",
    "ProspectScore",
    "ProspectState",
    "RampDecision",
    "Reply",
    "ReplyClass",
    "ReplyRouting",
    "RiskLevel",
    "SendStatus",
    "SendingBatch",
    "SuppressionEntry",
    "allowed_sends_today",
    "build_draft",
    "check_draft",
    "classify_and_route",
    "classify_reply",
    "daily_gtm_report",
    "daily_mix",
    "eligible_drafts",
    "max_sends_for_week",
    "produce_drafts",
    "rank_for_approval",
    "route_reply",
    "score_prospect",
    "summarize_batch",
    "weekly_gtm_review",
]
