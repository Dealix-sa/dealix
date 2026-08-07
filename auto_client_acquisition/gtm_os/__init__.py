"""GTM OS — draft-only go-to-market production primitives.

Every module here is draft-only and governance-gated:
  - ``content_calendar`` / ``message_experiment`` — suggested slots + experiments.
  - ``outreach_draft`` — the canonical PII-free draft object.
  - ``offer_catalog`` — operational offer ids (pricing governed in docs).
  - ``draft_quality_gate`` — the executable Compliance/Quality Gate.
  - ``sending_ramp`` — domain-reputation-safe volume planning (no sends here).

Nothing in this package sends, charges, or scrapes. Approved drafts only leave
through ``approval_center`` after founder review.
"""
from auto_client_acquisition.gtm_os.content_calendar import (
    ContentCalendarSlot,
    build_weekly_calendar,
)
from auto_client_acquisition.gtm_os.draft_quality_gate import (
    GateIssue,
    GateResult,
    summarize_gate_results,
    validate_outreach_draft,
)
from auto_client_acquisition.gtm_os.message_experiment import (
    MessageExperiment,
    draft_experiment,
)
from auto_client_acquisition.gtm_os.offer_catalog import (
    CATALOG_OFFER_IDS,
    is_catalog_offer,
    offer_label,
)
from auto_client_acquisition.gtm_os.outreach_draft import (
    DAILY_DRAFT_MIX,
    OutreachDraft,
)
from auto_client_acquisition.gtm_os.records import (
    CompanySignal,
    Prospect,
    Reply,
    SuppressionEntry,
    route_reply,
    score_prospect,
)
from auto_client_acquisition.gtm_os.sending_ramp import (
    ApprovedDraftRef,
    SendingPlan,
    plan_sending_batches,
    ramp_stage_for,
)

__all__ = [
    "CATALOG_OFFER_IDS",
    "DAILY_DRAFT_MIX",
    "ApprovedDraftRef",
    "CompanySignal",
    "ContentCalendarSlot",
    "GateIssue",
    "GateResult",
    "MessageExperiment",
    "OutreachDraft",
    "Prospect",
    "Reply",
    "SendingPlan",
    "SuppressionEntry",
    "build_weekly_calendar",
    "draft_experiment",
    "is_catalog_offer",
    "offer_label",
    "plan_sending_batches",
    "ramp_stage_for",
    "route_reply",
    "score_prospect",
    "summarize_gate_results",
    "validate_outreach_draft",
]
