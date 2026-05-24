"""
Hermes Universal Kernel — Dealix Sovereign OS.

Modular sovereign operating layer that converts signals into governed
outcomes and reusable assets. All modules share the same six core objects
(Signal → Opportunity → Decision → Execution → Outcome → Asset) and route
sensitive actions through the Sovereignty + Trust layers before any tool
is invoked.

Module map (matches section 111 of the sovereign spec):

    core         — universal kernel (signals → ... → assets)
    sovereignty  — S0..S5 levels, classifier, kill switch, sovereign memory
    trust        — agent / tool registries, MCP gateway, evidence, audit
    money        — cash + revenue engine (proposals, follow-ups, dashboard)
    products     — offer factory + scale/kill lifecycle
    partners     — distribution network + revenue share
    intelligence — market / sector / tender / competitor radars
    training     — knowledge-as-product (workshops, prompt packs)
    customer     — onboarding, health, value reports, renewals
    ventures     — vertical launcher + kill/scale rules
    api          — capability gateway for future internal/public APIs
    marketplace  — internal/external asset marketplace
    events       — event bus that ties all modules together
"""

__version__ = "0.1.0"

# Re-export the canonical kernel primitives so callers can write
# `from dealix.hermes import Signal, Opportunity, ...` without caring
# which sub-module owns them.
from dealix.hermes.core.schemas import (  # noqa: F401
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
)
from dealix.hermes.sovereignty.levels import SovereigntyLevel  # noqa: F401

__all__ = [
    "__version__",
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
    "SovereigntyLevel",
]
