"""Trust Plane — policy, approval, authorization, audit, tool verification.

Two layers live here:

* The original Trust Plane (approval queue, audit sink, policy evaluator,
  tool verification) used by the existing decision pipeline.
* The Company OS Trust modules (approval matrix, claim guard, suppression,
  data retention, evidence pack, policy engine) used by external send
  paths per `docs/trust/`.

Both layers are independent and can be used together.
"""

from dealix.trust.approval import ApprovalCenter, ApprovalRequest, ApprovalStatus
from dealix.trust.approval_matrix import (
    ApprovalRequired,
    ApprovalTier,
    ProhibitedAction,
    require_approval,
    tier_for,
)
from dealix.trust.audit import AuditSink, InMemoryAuditSink
from dealix.trust.claim_guard import ClaimGuardReport, FlagSeverity
from dealix.trust.claim_guard import check as claim_guard_check
from dealix.trust.data_retention import (
    DataCategory,
    DeletionReport,
    RetentionRecord,
    build_deletion_report,
)
from dealix.trust.evidence_pack import EvidencePack, new_pack
from dealix.trust.policy import PolicyDecision, PolicyEvaluator, PolicyResult
from dealix.trust.policy_engine import (
    PolicyEvaluation,
    PolicyViolation,
    assert_send,
    evaluate_send,
)
from dealix.trust.suppression import (
    SuppressionEntry,
    SuppressionList,
    SuppressionViolation,
    assert_not_suppressed,
    is_suppressed,
)
from dealix.trust.tool_verification import ToolVerificationLedger

__all__ = [
    # Original Trust Plane
    "ApprovalCenter",
    "ApprovalRequest",
    # Company OS Trust (docs/trust/)
    "ApprovalRequired",
    "ApprovalStatus",
    "ApprovalTier",
    "AuditSink",
    "ClaimGuardReport",
    "DataCategory",
    "DeletionReport",
    "EvidencePack",
    "FlagSeverity",
    "InMemoryAuditSink",
    "PolicyDecision",
    "PolicyEvaluation",
    "PolicyEvaluator",
    "PolicyResult",
    "PolicyViolation",
    "ProhibitedAction",
    "RetentionRecord",
    "SuppressionEntry",
    "SuppressionList",
    "SuppressionViolation",
    "ToolVerificationLedger",
    "assert_not_suppressed",
    "assert_send",
    "build_deletion_report",
    "claim_guard_check",
    "evaluate_send",
    "is_suppressed",
    "new_pack",
    "require_approval",
    "tier_for",
]
