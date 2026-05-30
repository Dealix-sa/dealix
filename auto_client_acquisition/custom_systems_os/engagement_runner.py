"""Custom Systems OS — the governed engagement orchestrator.

Sequences the 7-step Dealix delivery contract for a bespoke internal system:

    entry gate -> Source Passport -> build (design + structure + spec)
    -> governance decision -> safety gate -> local export (PDF-safe)
    -> Proof Pack -> Capital Assets -> retainer readiness -> ledger.

Every step short-circuits to a governed stop; nothing is sent externally and
the exporter is never called with ``pdf``/``pptx`` (which raise
``NotImplementedError``).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from auto_client_acquisition.adoption_os.retainer_readiness import evaluate as evaluate_retainer
from auto_client_acquisition.capital_os.asset_types import CapitalAssetType
from auto_client_acquisition.capital_os.capital_ledger import add_asset
from auto_client_acquisition.custom_systems_os import ledger as cs_ledger
from auto_client_acquisition.custom_systems_os.design_profile import build_design_profile
from auto_client_acquisition.custom_systems_os.entry_gate import check_entry
from auto_client_acquisition.custom_systems_os.proof_sections import build_proof_sections
from auto_client_acquisition.custom_systems_os.schemas import (
    CustomSystemEngagementResult,
    CustomSystemRecord,
)
from auto_client_acquisition.custom_systems_os.spec_document import build_spec_document
from auto_client_acquisition.custom_systems_os.structure_blueprint import build_structure_blueprint
from auto_client_acquisition.data_os.source_passport import SourcePassport, validate
from auto_client_acquisition.designops.exporter import export_artifact
from auto_client_acquisition.designops.safety_gate import check_artifact
from auto_client_acquisition.governance_os.runtime_decision import decide
from auto_client_acquisition.proof_os.proof_pack import proof_pack_v2_sections_complete
from auto_client_acquisition.proof_os.proof_score import (
    proof_pack_score_with_governance_penalty,
    proof_strength_band,
)

_SAFE_FORMATS = ["markdown", "html", "json"]


def _safe_artifact_id(engagement_id: str) -> str:
    return "custom-system-" + (re.sub(r"[^a-zA-Z0-9_-]", "-", engagement_id) or "engagement")


def _record_from(data: dict[str, Any]) -> CustomSystemRecord:
    retainer = data.get("retainer") or {}
    return CustomSystemRecord(
        engagement_id=data["engagement_id"],
        customer_id=data["customer_id"],
        entry_allowed=data["entry"].allowed,
        passport_valid=data["passport_valid"],
        governance_decision=data["governance_decision"],
        governance_blocked=data["governance_blocked"],
        safety_passed=data["safety_passed"],
        proof_score=data["proof_score"],
        proof_band=data["proof_band"],
        proof_complete=data["proof_complete"],
        capital_asset_ids=data["capital_assets"],
        spec_written_files=data["spec_written_files"],
        retainer_offer=str(retainer.get("recommended_offer", "")),
        next_step=data["next_step"],
        delivery_mode=data["delivery_mode"],
    )


def _finish(data: dict[str, Any], *, write_ledger: bool) -> CustomSystemEngagementResult:
    if write_ledger:
        try:
            cs_ledger.record_engagement(record=_record_from(data))
        except Exception:  # ledger must never break the governed result
            pass
    return CustomSystemEngagementResult(**data)


def run_custom_system_engagement(
    *,
    customer_id: str,
    customer_name: str,
    engagement_id: str,
    passport: SourcePassport,
    paid_pilots_completed: int,
    declared_modules: list[str],
    declared_workflows: list[str],
    direction_name: str = "saudi_executive_trust",
    client_overrides: dict[str, Any] | None = None,
    sector: str | None = None,
    workflow_owner_present: bool = False,
    adoption_score: float = 0.0,
    out_dir: Path | str | None = None,
    write_ledger: bool = True,
) -> CustomSystemEngagementResult:
    entry = check_entry(
        paid_pilots_completed=paid_pilots_completed,
        workflow_owner_present=workflow_owner_present,
    )
    data: dict[str, Any] = {
        "engagement_id": engagement_id,
        "customer_id": customer_id,
        "entry": entry,
        "passport_valid": False,
        "passport_reasons": (),
        "governance_decision": "not_evaluated",
        "governance_blocked": False,
        "safety_passed": False,
        "safety_blocked_reasons": (),
        "spec_written_files": (),
        "proof_score": 0,
        "proof_band": "weak_proof",
        "proof_complete": False,
        "capital_assets": (),
        "retainer": {},
        "blocked_reasons": (),
        "delivery_mode": entry.delivery_mode,
        "next_step": "",
    }

    # 1. Entry gate (the coded ">= 3 paid pilots" doctrine rule).
    if not entry.allowed:
        data["blocked_reasons"] = entry.blocked_reasons
        data["next_step"] = "blocked_entry_gate"
        return _finish(data, write_ledger=write_ledger)

    # 2. Source Passport — no AI/build before this passes.
    validation = validate(passport)
    data["passport_valid"] = validation.is_valid
    data["passport_reasons"] = tuple(validation.reasons)
    if not validation.is_valid:
        data["blocked_reasons"] = tuple(validation.reasons)
        data["next_step"] = "blocked_source_passport"
        return _finish(data, write_ledger=write_ledger)

    # 3. Build artifacts (deterministic, ask-first).
    profile = build_design_profile(
        customer_id=customer_id,
        direction_name=direction_name,
        client_overrides=client_overrides,
    )
    blueprint = build_structure_blueprint(
        customer_id=customer_id,
        declared_modules=declared_modules,
        declared_workflows=declared_workflows,
        sector=sector,
    )
    if blueprint.missing_context_questions:
        data["blocked_reasons"] = blueprint.missing_context_questions
        data["next_step"] = "ask_founder_for_missing_context"
        return _finish(data, write_ledger=write_ledger)

    spec_content = build_spec_document(
        profile=profile, blueprint=blueprint, customer_name=customer_name
    )

    # 4. Governance decision before any publish/claim.
    decision = decide(
        action_type="generate_custom_system_spec",
        context={"text": spec_content["markdown"]},
        actor="custom_systems_os",
    )
    governance_decision = str(decision.decision)
    governance_blocked = governance_decision in {"block", "escalate"}
    data["governance_decision"] = governance_decision
    data["governance_blocked"] = governance_blocked

    # 5. Safety gate (publish gate).
    safety = check_artifact(spec_content, language="bilingual")
    data["safety_passed"] = safety.passed
    data["safety_blocked_reasons"] = tuple(safety.blocked_reasons)

    blocked_reasons: list[str] = []
    if governance_blocked:
        blocked_reasons.append(f"governance:{governance_decision}")
    if not safety.passed:
        blocked_reasons.extend(safety.blocked_reasons)

    # 6. Local export (PDF-safe) — only when content is publishable.
    written_files: tuple[str, ...] = ()
    if safety.passed and not governance_blocked:
        try:
            export = export_artifact(
                manifest={"artifact_id": _safe_artifact_id(engagement_id), "safe_to_send": False},
                content=spec_content,
                out_dir=out_dir,
                formats=list(_SAFE_FORMATS),
            )
            written_files = tuple(export.get("written_files", ()))
        except Exception as exc:  # never crash the governed run
            blocked_reasons.append(f"export_error:{type(exc).__name__}")
    data["spec_written_files"] = written_files

    # 8. Capital assets (>= 1 per engagement) — built before proof so proof can cite them.
    asset_ref = written_files[0] if written_files else f"{_safe_artifact_id(engagement_id)}"
    capital_ids: list[str] = []
    for asset_type in (
        CapitalAssetType.CUSTOM_DESIGN_PROFILE,
        CapitalAssetType.STRUCTURE_BLUEPRINT,
        CapitalAssetType.SYSTEM_SPEC,
    ):
        try:
            asset = add_asset(
                customer_id=customer_id,
                engagement_id=engagement_id,
                asset_type=asset_type,
                owner=customer_name or customer_id,
                asset_ref=asset_ref,
                notes="custom_systems_os engagement",
            )
            capital_ids.append(asset.asset_id)
        except Exception:  # noqa: S112 — one bad asset write must not void the engagement
            continue
    data["capital_assets"] = tuple(capital_ids)

    # 9. Retainer readiness.
    retainer = evaluate_retainer(
        customer_id=customer_id,
        adoption_score=adoption_score,
        proof_score=0.0,  # set below after scoring
        workflow_owner_present=workflow_owner_present,
        governance_risk_controlled=not governance_blocked,
    )

    # 7. Proof Pack.
    sections = build_proof_sections(
        customer_name=customer_name,
        passport_valid=validation.is_valid,
        governance_decision=governance_decision,
        profile=profile,
        blueprint=blueprint,
        spec_artifact_ref=written_files[0] if written_files else "",
        capital_asset_refs=list(capital_ids),
        retainer_recommendation=retainer.recommended_offer,
    )
    complete, _missing = proof_pack_v2_sections_complete(sections)
    proof_score = proof_pack_score_with_governance_penalty(
        sections, governance_blocked=governance_blocked
    )
    data["proof_score"] = proof_score
    data["proof_band"] = proof_strength_band(proof_score)
    data["proof_complete"] = complete

    # Re-evaluate retainer now that we have the real proof score.
    retainer = evaluate_retainer(
        customer_id=customer_id,
        adoption_score=adoption_score,
        proof_score=float(proof_score),
        workflow_owner_present=workflow_owner_present,
        governance_risk_controlled=not governance_blocked,
    )
    data["retainer"] = retainer.to_dict()

    # 10. Resolve next step + blocked reasons.
    data["blocked_reasons"] = tuple(blocked_reasons)
    if not safety.passed:
        data["next_step"] = "blocked_safety_gate"
    elif governance_blocked:
        data["next_step"] = "blocked_governance"
    elif not complete:
        data["next_step"] = "incomplete_proof_pack"
    else:
        data["next_step"] = "deliver_for_founder_review"

    return _finish(data, write_ledger=write_ledger)


__all__ = ["run_custom_system_engagement"]
