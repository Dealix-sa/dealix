"""Custom Systems OS — Proof Pack v2 section assembly.

Maps a custom-system engagement onto the 14 canonical Proof Pack v2 sections
using the real ``merge_proof_pack_v2`` helper, so every section is non-empty
and ``proof_pack_v2_sections_complete`` returns ``(True, ())``.
"""

from __future__ import annotations

from auto_client_acquisition.custom_systems_os.schemas import (
    CustomDesignProfile,
    CustomStructureBlueprint,
)
from auto_client_acquisition.proof_os.proof_pack import (
    build_empty_proof_pack_v2,
    merge_proof_pack_v2,
)


def build_proof_sections(
    *,
    customer_name: str,
    passport_valid: bool,
    governance_decision: str,
    profile: CustomDesignProfile,
    blueprint: CustomStructureBlueprint,
    spec_artifact_ref: str,
    capital_asset_refs: list[str],
    retainer_recommendation: str,
) -> dict[str, str]:
    module_names = ", ".join(m["name"] for m in blueprint.modules) or "(none declared)"
    updates: dict[str, str] = {
        "executive_summary": (
            f"Governed custom internal system for {customer_name}: a client design "
            f"profile, a structure blueprint, and a complete bilingual spec."
        ),
        "problem": (
            "Client needs a bespoke internal system with a custom design and "
            "structure, delivered under Dealix governance."
        ),
        "inputs": (
            f"Declared modules and workflows; design direction "
            f"`{profile.direction_name}`; Source Passport."
        ),
        "source_passports": (f"Source Passport validated: {passport_valid}."),
        "work_completed": (
            f"Built custom design profile, structure blueprint ({module_names}), "
            f"and the bilingual internal-system specification."
        ),
        "outputs": f"Specification artifact written to: {spec_artifact_ref or '(not exported)'}.",
        "quality_scores": (
            f"Design direction `{profile.direction_name}`; "
            f"{len(blueprint.governance_gates)} governance gates embedded."
        ),
        "governance_decisions": f"Runtime governance decision: {governance_decision}.",
        "blocked_risks": ("No automated external send; no full white-label; no outcome promises."),
        "value_metrics": (
            "Estimated delivery acceleration from a reusable, governed system "
            "blueprint (methodology estimate, not a verified figure)."
        ),
        "limitations": ("Founder-assisted delivery. PDF export deferred; markdown/html/json only."),
        "recommended_next_step": "Founder review, then deliver the spec to the client.",
        "retainer_expansion_path": f"Recommended next offer: {retainer_recommendation}.",
        "capital_assets_created": (
            ", ".join(capital_asset_refs) if capital_asset_refs else "(none)"
        ),
    }
    return merge_proof_pack_v2(build_empty_proof_pack_v2(), updates)


__all__ = ["build_proof_sections"]
