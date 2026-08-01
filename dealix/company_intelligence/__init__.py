"""Canonical Company Intelligence contracts and compatibility adapters."""

from . import outcome_contracts as _outcome_contracts
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
from dealix.company_intelligence.proof_adapter import normalize_proof_event

CanonicalDailyCommand = _outcome_contracts.CanonicalDailyCommand
CanonicalLearningEvent = _outcome_contracts.CanonicalLearningEvent
CanonicalOutcomeEvent = _outcome_contracts.CanonicalOutcomeEvent
CanonicalProofEvent = _outcome_contracts.CanonicalProofEvent
EvidenceState = _outcome_contracts.EvidenceState
LearningEventType = _outcome_contracts.LearningEventType
OutcomeEventType = _outcome_contracts.OutcomeEventType
ProofSourceEventType = _outcome_contracts.ProofSourceEventType
ProofType = _outcome_contracts.ProofType
build_daily_command = _outcome_contracts.build_daily_command
build_learning_event = _outcome_contracts.build_learning_event
build_outcome_event = _outcome_contracts.build_outcome_event
build_proof_event = _outcome_contracts.build_proof_event

# Preserve the legacy direct-import path while routing it to the fail-closed
# compatibility adapter. The module is loaded once above, so this does not
# create a competing implementation or import path.
_outcome_contracts.normalize_proof_event = normalize_proof_event

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
    "ProofSourceEventType",
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
