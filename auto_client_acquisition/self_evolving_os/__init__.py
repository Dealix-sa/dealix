"""Self-Evolving OS (L11) — shadow-mode feedback + improvement proposals.

This layer never mutates production behavior on its own. It:

1. **Ingests feedback** from value, adoption, and governance signals
   (:mod:`.feedback_ingestion`).
2. **Stores** every feedback event in an append-only learning ledger
   (:mod:`.learning_store`).
3. **Derives suggestions** from the ledger statistics
   (:mod:`.decision_improver`).
4. **Surfaces proposals** through a human-gated state machine
   (:mod:`.improvement_proposals`).

Approvals flow through ``governance_os``; only an approved + applied
proposal can change the AI Stack's behavior.

The legacy ``ImprovementProposal`` dataclass from :mod:`.repositories` is
re-exported as :class:`LegacyImprovementProposal` so older callers continue
to work while new callers prefer the strict state machine in
:mod:`.improvement_proposals`.
"""

from auto_client_acquisition.self_evolving_os.decision_improver import (
    SELF_EVOLVING_SHADOW_ONLY,
    ImprovementSuggestion,
    ShadowModeViolationError,
    assert_shadow_mode,
    derive_suggestions,
)
from auto_client_acquisition.self_evolving_os.feedback_ingestion import (
    FeedbackEvent,
    OutcomeKind,
    from_doctrine_violation,
    from_friction_log,
    from_governance_block,
    from_value_event,
    make_feedback_event,
)
from auto_client_acquisition.self_evolving_os.improvement_proposals import (
    IllegalProposalTransition,
    ImprovementProposal,
    InMemoryProposalRepository,
    ProposalState,
    get_default_repository,
    proposal_from_suggestion,
    reset_default_repository,
)
from auto_client_acquisition.self_evolving_os.learning_store import (
    InMemoryLearningStore,
    LayerOutcomeSummary,
    get_default_store,
    record_feedback,
    reset_default_store,
)
from auto_client_acquisition.self_evolving_os.repositories import (
    InMemorySelfEvolvingRepository,
    ProposalApprovalRequiredError,
)
from auto_client_acquisition.self_evolving_os.repositories import (
    ImprovementProposal as LegacyImprovementProposal,
)

__all__ = [
    "FeedbackEvent",
    "IllegalProposalTransition",
    "ImprovementProposal",
    "ImprovementSuggestion",
    "InMemoryLearningStore",
    "InMemoryProposalRepository",
    "InMemorySelfEvolvingRepository",
    "LayerOutcomeSummary",
    "LegacyImprovementProposal",
    "OutcomeKind",
    "ProposalApprovalRequiredError",
    "ProposalState",
    "SELF_EVOLVING_SHADOW_ONLY",
    "ShadowModeViolationError",
    "assert_shadow_mode",
    "derive_suggestions",
    "from_doctrine_violation",
    "from_friction_log",
    "from_governance_block",
    "from_value_event",
    "get_default_repository",
    "get_default_store",
    "make_feedback_event",
    "proposal_from_suggestion",
    "record_feedback",
    "reset_default_repository",
    "reset_default_store",
]
