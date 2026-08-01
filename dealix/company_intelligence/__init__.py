"""Canonical Company Intelligence contracts and compatibility adapters."""

import sys

from dealix.company_intelligence.company_brain import (
    CanonicalCompanyBrain,
    build_customer_company_brain,
    build_internal_company_brain,
)
from dealix.company_intelligence.contracts import CompanyBrainSource, ProvenanceRef
from dealix.company_intelligence.execution_contracts import (
    CanonicalApproval,
    CanonicalDraft,
    CanonicalOpportunity,
    DraftChannel,
    LawfulContactBasis,
    build_draft,
    normalize_approval,
    normalize_opportunity,
)
from dealix.company_intelligence.outcome_contracts import (
    CanonicalDailyCommand,
    CanonicalLearningEvent,
    CanonicalOutcomeEvent,
    CanonicalProofEvent,
    EvidenceState,
    LearningEventType,
    OutcomeEventType,
    ProofType,
    build_daily_command,
    build_learning_event,
    build_outcome_event,
    build_proof_event,
)
from dealix.company_intelligence.proof_adapter import normalize_proof_event

# Preserve the legacy direct-import path while routing it to the fail-closed
# compatibility adapter. The module is already loaded by the imports above, so
# this avoids importing the same module with both ``import`` and ``from``.
_outcome_module = sys.modules.get(f"{__name__}.outcome_contracts")
if _outcome_module is not None:
    setattr(_outcome_module, "normalize_proof_event", normalize_proof_event)

__all__ = [
    "CanonicalApproval",
    "CanonicalCompanyBrain",
    "CanonicalDailyCommand",
    "CanonicalDraft",
    "CanonicalLearningEvent",
    "CanonicalOpportunity",
    "CanonicalOutcomeEvent",
    "CanonicalProofEvent",
    "CompanyBrainSource",
    "DraftChannel",
    "EvidenceState",
    "LawfulContactBasis",
    "LearningEventType",
    "OutcomeEventType",
    "ProofType",
    "ProvenanceRef",
    "build_customer_company_brain",
    "build_daily_command",
    "build_draft",
    "build_internal_company_brain",
    "build_learning_event",
    "build_outcome_event",
    "build_proof_event",
    "normalize_approval",
    "normalize_opportunity",
    "normalize_proof_event",
]
