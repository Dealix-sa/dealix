"""Custom Systems OS — governed per-client custom design + structure + spec.

A bespoke internal-system builder that produces, under full Dealix governance:

  1. a per-client custom design profile (tokens/theme overriding Dealix defaults),
  2. a per-client custom structure/architecture blueprint, and
  3. a complete bilingual internal-system specification,

flowing through the existing governance -> Proof Pack -> Capital Asset ->
retainer-readiness machinery. Pure-function core + JSONL ledger; the FastAPI
router (``api/routers/custom_systems.py``) is a thin wrapper.

The capability is GATED: ``entry_gate.check_entry`` encodes the doctrine rule
"no customization before 3 paid pilots" and delivery is always founder-assisted.
"""

from __future__ import annotations

from auto_client_acquisition.custom_systems_os.design_profile import build_design_profile
from auto_client_acquisition.custom_systems_os.engagement_runner import (
    run_custom_system_engagement,
)
from auto_client_acquisition.custom_systems_os.entry_gate import MIN_PAID_PILOTS, check_entry
from auto_client_acquisition.custom_systems_os.schemas import (
    CustomDesignProfile,
    CustomStructureBlueprint,
    CustomSystemEngagementResult,
    CustomSystemEntryDecision,
    CustomSystemRecord,
)
from auto_client_acquisition.custom_systems_os.spec_document import build_spec_document
from auto_client_acquisition.custom_systems_os.structure_blueprint import build_structure_blueprint

__all__ = [
    "MIN_PAID_PILOTS",
    "CustomDesignProfile",
    "CustomStructureBlueprint",
    "CustomSystemEngagementResult",
    "CustomSystemEntryDecision",
    "CustomSystemRecord",
    "build_design_profile",
    "build_spec_document",
    "build_structure_blueprint",
    "check_entry",
    "run_custom_system_engagement",
]
