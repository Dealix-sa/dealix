"""Custom Systems OS — per-client structure / architecture blueprint.

Deterministic, ask-first composition of an internal-system architecture from
the client's DECLARED modules and workflows. Nothing is invented: when the
client has not declared modules/workflows the builder returns
``missing_context_questions`` (mirrors designops brief_builder semantics) so
the founder gathers context before any build proceeds.

Every blueprint carries the 11 non-negotiable governance gates so a custom
internal system inherits Dealix doctrine by construction.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.custom_systems_os.schemas import CustomStructureBlueprint

# The 11 non-negotiables, as machine-stable gate keys baked into every blueprint.
GOVERNANCE_GATES: tuple[str, ...] = (
    "source_passport_required_before_ai",
    "governance_decision_before_draft",
    "human_approval_for_external_send",
    "no_scraping",
    "no_cold_whatsapp",
    "no_linkedin_automation",
    "no_guaranteed_outcomes",
    "no_pii_in_logs",
    "every_answer_has_source",
    "proof_pack_required",
    "capital_asset_per_engagement",
)

# Default data-model spine every governed internal system needs.
_BASE_DATA_MODEL: tuple[dict[str, Any], ...] = (
    {"entity": "source_passport", "purpose": "data sovereignty gate before AI use"},
    {"entity": "approval_record", "purpose": "human sign-off for external actions"},
    {"entity": "proof_event", "purpose": "evidence ledger (L1-L5)"},
    {"entity": "capital_asset", "purpose": "reusable artifacts registry"},
    {"entity": "audit_log", "purpose": "PII-free action trail"},
)


def build_structure_blueprint(
    *,
    customer_id: str,
    declared_modules: list[str],
    declared_workflows: list[str],
    sector: str | None = None,
) -> CustomStructureBlueprint:
    if not customer_id:
        raise ValueError("customer_id is required")

    missing: list[str] = []
    if not declared_modules:
        missing.append("Which internal modules should the system include? (list)")
    if not declared_workflows:
        missing.append("Which workflows must the system run? (list)")

    modules = tuple(
        {
            "name": str(m).strip(),
            "governed": True,
            "owner": "founder_assisted",
        }
        for m in declared_modules
        if str(m).strip()
    )
    workflows = tuple(
        {
            "name": str(w).strip(),
            "requires_approval_for_external": True,
            "draft_only_default": True,
        }
        for w in declared_workflows
        if str(w).strip()
    )

    data_model = _BASE_DATA_MODEL
    if sector:
        data_model = (
            *_BASE_DATA_MODEL,
            {"entity": "sector_signal", "purpose": f"sector context: {sector}"},
        )

    return CustomStructureBlueprint(
        customer_id=customer_id,
        modules=modules,
        data_model=data_model,
        workflows=workflows,
        governance_gates=GOVERNANCE_GATES,
        missing_context_questions=tuple(missing),
    )


__all__ = ["GOVERNANCE_GATES", "build_structure_blueprint"]
