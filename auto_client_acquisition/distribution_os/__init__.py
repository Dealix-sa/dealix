"""Distribution OS — approval-first product-distribution machine.

ماكينة تصريف المنتجات بالموافقة أولاً: Prospect → Draft → Approval → Manual send
→ Follow-up → Proposal → Proof → Payment → Delivery → Renewal.

Composition over reinvention: this package orchestrates existing platform
primitives rather than duplicating them —
  * ``governance_os`` — draft policy + claim safety (quality gate)
  * ``revenue_os.anti_waste`` — blocked ingestion sources (prospect intake)
  * ``sales_os`` — proposal skeleton (proposal factory)
  * ``proof_engine.evidence`` — evidence levels L0–L5

Nothing here sends anything externally. Every draft is ``pending_approval``.
"""

from __future__ import annotations

from auto_client_acquisition.distribution_os.draft_factory import build_draft, generate_drafts
from auto_client_acquisition.distribution_os.followup_engine import build_followups, due_followups
from auto_client_acquisition.distribution_os.metrics import compute_metrics
from auto_client_acquisition.distribution_os.models import (
    EVIDENCE_LEVELS,
    Channel,
    Draft,
    DraftStatus,
    DraftType,
    Followup,
    FollowupStatus,
    FollowupType,
    Language,
    Prospect,
    ProspectStatus,
    RiskLevel,
)
from auto_client_acquisition.distribution_os.proposal_factory import (
    ProposalDraft,
    build_proposal,
    generate_proposals,
    render_proposal_markdown,
)
from auto_client_acquisition.distribution_os.prospects import load_prospects, validate_prospect_dict
from auto_client_acquisition.distribution_os.quality_gate import (
    GateResult,
    GateViolation,
    check_draft,
    check_drafts,
)

__all__ = [
    "EVIDENCE_LEVELS",
    "Channel",
    "Draft",
    "DraftStatus",
    "DraftType",
    "Followup",
    "FollowupStatus",
    "FollowupType",
    "GateResult",
    "GateViolation",
    "Language",
    "ProposalDraft",
    "Prospect",
    "ProspectStatus",
    "RiskLevel",
    "build_draft",
    "build_followups",
    "build_proposal",
    "check_draft",
    "check_drafts",
    "compute_metrics",
    "due_followups",
    "generate_drafts",
    "generate_proposals",
    "load_prospects",
    "render_proposal_markdown",
    "validate_prospect_dict",
]
