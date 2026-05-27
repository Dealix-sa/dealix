"""Core Module — universal kernel of Hermes.

Everything in Hermes — money, products, partners, ventures, customers — is
shaped as the same six-step pipeline:

    Signal → Opportunity → Decision → Execution → Outcome → Asset

Core does not know the domain (customer, partner, venture, ...). It only
guarantees the pipeline is well-formed and that no object is orphaned.
"""

from dealix.hermes.core.assets import AssetRegistry
from dealix.hermes.core.decisions import DecisionLog
from dealix.hermes.core.events import Event, EventBus, EventKind
from dealix.hermes.core.executions import ExecutionPlanner
from dealix.hermes.core.opportunities import OpportunityBook
from dealix.hermes.core.outcomes import OutcomeLedger
from dealix.hermes.core.scale import ScaleKillEvaluator, ScaleVerdict
from dealix.hermes.core.schemas import (
    Asset,
    AssetStatus,
    CoreObject,
    Decision,
    DecisionStatus,
    Execution,
    ExecutionStatus,
    Opportunity,
    OpportunityStatus,
    Outcome,
    OutcomeStatus,
    Signal,
    SignalStatus,
    StructuredOutput,
)
from dealix.hermes.core.scoring import OpportunityScorer
from dealix.hermes.core.signals import SignalInbox

__all__ = [
    "AssetRegistry",
    "DecisionLog",
    "Event",
    "EventBus",
    "EventKind",
    "ExecutionPlanner",
    "OpportunityBook",
    "OutcomeLedger",
    "ScaleKillEvaluator",
    "ScaleVerdict",
    "Asset",
    "AssetStatus",
    "CoreObject",
    "Decision",
    "DecisionStatus",
    "Execution",
    "ExecutionStatus",
    "Opportunity",
    "OpportunityStatus",
    "Outcome",
    "OutcomeStatus",
    "Signal",
    "SignalStatus",
    "StructuredOutput",
    "OpportunityScorer",
    "SignalInbox",
]
