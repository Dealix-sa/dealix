"""Adapter registry: maps canonical entity types to their normalize functions.

Provides a single lookup table from entity names (as defined in the
entity ownership registry) to their adapter functions. Entities that
have no operational source (no adapter by design) are explicitly marked.

No database, network, or LLM calls.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AdapterStatus(StrEnum):
    """Whether an adapter exists for a given entity type."""

    ACTIVE = "active"
    NO_OPERATIONAL_SOURCE = "no_operational_source"
    BUILDER_ONLY = "builder_only"


@dataclass(frozen=True)
class AdapterEntry:
    """One entry in the adapter registry."""

    entity_name: str
    status: AdapterStatus
    adapter_functions: tuple[str, ...] = ()
    module: str = ""
    notes: str = ""


def _build_registry() -> dict[str, AdapterEntry]:
    """Build the registry lazily to avoid circular imports at module level."""
    from dealix.company_intelligence.action_adapter import normalize_next_best_action
    from dealix.company_intelligence.consent_adapter import normalize_consent
    from dealix.company_intelligence.execution_contracts import (
        normalize_approval,
        normalize_draft,
        normalize_opportunity,
    )
    from dealix.company_intelligence.graph_adapter import (
        normalize_lead_to_company,
        normalize_lead_to_contact,
    )
    from dealix.company_intelligence.learning_adapter import (
        normalize_learning_event,
        normalize_win_loss,
    )
    from dealix.company_intelligence.offer_adapter import (
        normalize_catalog,
        normalize_service_offering,
    )
    from dealix.company_intelligence.pipeline_adapter import normalize_pipeline_lead
    from dealix.company_intelligence.playbook_adapter import normalize_sector_playbook
    from dealix.company_intelligence.proof_adapter import normalize_proof_event
    from dealix.company_intelligence.proposal_adapter import normalize_proposal
    from dealix.company_intelligence.revenue_graph_adapter import normalize_graph_edge
    from dealix.company_intelligence.signal_adapter import normalize_signal
    from dealix.company_intelligence.source_adapter import normalize_source_passport

    _ = (  # reference to suppress unused-import warnings; functions stored by name
        normalize_next_best_action, normalize_consent, normalize_approval,
        normalize_draft, normalize_opportunity, normalize_lead_to_company,
        normalize_lead_to_contact, normalize_learning_event, normalize_win_loss,
        normalize_catalog, normalize_service_offering, normalize_pipeline_lead,
        normalize_sector_playbook, normalize_proof_event, normalize_proposal,
        normalize_graph_edge, normalize_signal, normalize_source_passport,
    )

    entries: list[AdapterEntry] = [
        # Entities with active adapters
        AdapterEntry(
            entity_name="Company",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_lead_to_company",),
            module="graph_adapter",
        ),
        AdapterEntry(
            entity_name="Contact",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_lead_to_contact",),
            module="graph_adapter",
        ),
        AdapterEntry(
            entity_name="Signal",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_signal",),
            module="signal_adapter",
        ),
        AdapterEntry(
            entity_name="Source",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_source_passport",),
            module="source_adapter",
        ),
        AdapterEntry(
            entity_name="ConsentBasis",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_consent",),
            module="consent_adapter",
        ),
        AdapterEntry(
            entity_name="Relationship",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_graph_edge",),
            module="revenue_graph_adapter",
        ),
        AdapterEntry(
            entity_name="Opportunity",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_pipeline_lead", "normalize_opportunity"),
            module="pipeline_adapter, execution_contracts",
        ),
        AdapterEntry(
            entity_name="Action",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_next_best_action",),
            module="action_adapter",
        ),
        AdapterEntry(
            entity_name="Draft",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_draft",),
            module="execution_contracts",
        ),
        AdapterEntry(
            entity_name="Approval",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_approval",),
            module="execution_contracts",
        ),
        AdapterEntry(
            entity_name="Offer",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_service_offering", "normalize_catalog"),
            module="offer_adapter",
        ),
        AdapterEntry(
            entity_name="Proposal",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_proposal",),
            module="proposal_adapter",
        ),
        AdapterEntry(
            entity_name="ProofEvent",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_proof_event",),
            module="proof_adapter",
        ),
        AdapterEntry(
            entity_name="LearningEvent",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_learning_event", "normalize_win_loss"),
            module="learning_adapter",
        ),
        AdapterEntry(
            entity_name="PlaybookVersion",
            status=AdapterStatus.ACTIVE,
            adapter_functions=("normalize_sector_playbook",),
            module="playbook_adapter",
        ),
        # Entities with builder-only contracts (built directly, not adapted)
        AdapterEntry(
            entity_name="OutcomeEvent",
            status=AdapterStatus.BUILDER_ONLY,
            notes="Built via build_outcome_event; no operational legacy source",
        ),
        AdapterEntry(
            entity_name="DailyCommand",
            status=AdapterStatus.BUILDER_ONLY,
            notes="Built via build_daily_command; aggregates other entities",
        ),
        AdapterEntry(
            entity_name="CompanyBrain",
            status=AdapterStatus.BUILDER_ONLY,
            notes="Built via build_customer_company_brain/build_internal_company_brain",
        ),
        # Entities without operational sources (no adapter by design)
        AdapterEntry(
            entity_name="Tenant",
            status=AdapterStatus.NO_OPERATIONAL_SOURCE,
            notes="Tenant context from auth layer; no external normalization needed",
        ),
        AdapterEntry(
            entity_name="Persona",
            status=AdapterStatus.NO_OPERATIONAL_SOURCE,
            notes="Defined in company brain; no legacy source to adapt",
        ),
        AdapterEntry(
            entity_name="PartnershipOpportunity",
            status=AdapterStatus.NO_OPERATIONAL_SOURCE,
            notes="New entity; no legacy source exists yet",
        ),
        AdapterEntry(
            entity_name="DepartmentPlan",
            status=AdapterStatus.NO_OPERATIONAL_SOURCE,
            notes="New entity; no legacy source exists yet",
        ),
    ]

    return {entry.entity_name: entry for entry in entries}


_REGISTRY: dict[str, AdapterEntry] | None = None


def get_adapter_registry() -> dict[str, AdapterEntry]:
    """Return the adapter registry, building it lazily on first call."""
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = _build_registry()
    return _REGISTRY


def get_adapter_entry(entity_name: str) -> AdapterEntry | None:
    """Look up one adapter entry by entity name."""
    return get_adapter_registry().get(entity_name)


def get_active_adapters() -> list[AdapterEntry]:
    """Return only entries with active adapters."""
    return [
        entry for entry in get_adapter_registry().values()
        if entry.status == AdapterStatus.ACTIVE
    ]


def get_all_normalize_functions() -> list[str]:
    """Return a sorted list of all normalize function names across all adapters."""
    functions: set[str] = set()
    for entry in get_adapter_registry().values():
        functions.update(entry.adapter_functions)
    return sorted(functions)


def validate_coverage(entity_names: list[str]) -> list[str]:
    """Check that every entity name has a registry entry. Returns missing names."""
    registry = get_adapter_registry()
    return [name for name in entity_names if name not in registry]
