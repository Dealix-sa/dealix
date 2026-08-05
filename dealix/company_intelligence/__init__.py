"""Canonical Company Intelligence contracts and compatibility adapters."""

from dealix.company_intelligence.action_contracts import (
    ActionStatus,
    ActionType,
    AutonomyLevel,
    CanonicalAction,
    RiskLevel,
    build_action,
    compute_priority_score,
    is_valid_transition,
    transition_action,
    valid_transitions_from,
)
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
from dealix.company_intelligence.graph_contracts import (
    CanonicalCompany,
    CanonicalContact,
    CompanyStatus,
    ContactRole,
    ContactStatus,
    RelationshipStrength,
    build_company,
    build_contact,
)
from dealix.company_intelligence.proof_adapter import normalize_proof_event
from dealix.company_intelligence.signal_contracts import (
    CanonicalSignal,
    ConsentStatus,
    SignalSensitivity,
    SignalStatus,
    SignalType,
    build_signal,
    is_signal_stale,
    is_valid_signal_transition,
    transition_signal,
    valid_signal_transitions_from,
)
from dealix.company_intelligence.source_contracts import (
    CanonicalSource,
    SourcePolicyStatus,
    SourceStatus,
    SourceType,
    build_source,
    compute_source_score,
    is_source_stale,
)

from . import outcome_contracts as _outcome_contracts

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
    "ActionStatus",
    "ActionType",
    "AutonomyLevel",
    "CanonicalAction",
    "CanonicalApproval",
    "CanonicalCompany",
    "CanonicalCompanyBrain",
    "CanonicalContact",
    "CanonicalDailyCommand",
    "CanonicalDraft",
    "CanonicalLearningEvent",
    "CanonicalOpportunity",
    "CanonicalOutcomeEvent",
    "CanonicalProofEvent",
    "CanonicalSignal",
    "CanonicalSource",
    "CompanyBrainSource",
    "CompanyStatus",
    "ConsentStatus",
    "ContactRole",
    "ContactStatus",
    "DraftChannel",
    "EvidenceState",
    "LawfulContactBasis",
    "LearningEventType",
    "OutcomeEventType",
    "ProofType",
    "ProofSourceEventType",
    "ProvenanceRef",
    "RelationshipStrength",
    "RiskLevel",
    "SignalSensitivity",
    "SignalStatus",
    "SignalType",
    "SourcePolicyStatus",
    "SourceStatus",
    "SourceType",
    "build_action",
    "build_company",
    "build_contact",
    "build_customer_company_brain",
    "build_daily_command",
    "build_draft",
    "build_internal_company_brain",
    "build_learning_event",
    "build_outcome_event",
    "build_proof_event",
    "build_signal",
    "build_source",
    "compute_priority_score",
    "compute_source_score",
    "is_signal_stale",
    "is_source_stale",
    "is_valid_signal_transition",
    "is_valid_transition",
    "normalize_approval",
    "normalize_opportunity",
    "normalize_proof_event",
    "transition_action",
    "transition_signal",
    "valid_signal_transitions_from",
    "valid_transitions_from",
]
