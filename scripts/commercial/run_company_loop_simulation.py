#!/usr/bin/env python3
"""Run a deterministic, network-free synthetic Dealix company loop."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from dealix.company_intelligence.outcome_contracts import (
    LearningEventType,
    OutcomeEventType,
    ProofType,
    build_daily_command,
    build_learning_event,
    build_outcome_event,
    build_proof_event,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = REPO_ROOT / "dealix/registers/company_loops_registry.json"
SYNTHETIC_TIME = datetime(2026, 8, 2, 12, 0, tzinfo=UTC)

_OUTCOME_TYPE_BY_STAGE = {
    "discovery_contact_approved": OutcomeEventType.PROSPECT_REPLIED,
    "discovery_outcome_recorded": OutcomeEventType.PROSPECT_REPLIED,
    "proposal_approved": OutcomeEventType.PROPOSAL_REVIEWED,
    "commitment_recorded": OutcomeEventType.PROPOSAL_REVIEWED,
    "delivery_handoff": OutcomeEventType.PROPOSAL_REVIEWED,
    "invoice_approved": OutcomeEventType.PROPOSAL_REVIEWED,
}


def load_registry(path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def get_loop(registry: dict[str, Any], loop_id: str) -> dict[str, Any]:
    for loop in registry["loops"]:
        if loop["id"] == loop_id:
            return loop
    raise ValueError(f"unknown loop: {loop_id}")


def _record_id(run_id: str, stage_id: str, record_type: str) -> str:
    digest = hashlib.sha256(f"{run_id}:{stage_id}:{record_type}".encode()).hexdigest()
    return digest[:16]


def _canonical_outcome(
    *,
    tenant_id: str,
    run_id: str,
    stage: dict[str, Any],
    mode: str,
):
    event_type = _OUTCOME_TYPE_BY_STAGE.get(stage["id"])
    if event_type is None:
        return None
    evidence_ref = f"synthetic://company-loop/{run_id}/{stage['id']}"
    return build_outcome_event(
        tenant_id=tenant_id,
        action_id=f"action_{_record_id(run_id, stage['id'], 'action')}",
        event_type=event_type,
        occurred_at=SYNTHETIC_TIME,
        evidence_refs=[evidence_ref],
        confidence=0.5,
        is_synthetic=mode == "synthetic",
        notes=f"Synthetic company-loop checkpoint for {stage['id']}",
    )


def _canonical_non_financial_proofs(
    *,
    tenant_id: str,
    run_id: str,
    stage: dict[str, Any],
    mode: str,
):
    proofs = []
    for requirement in stage["proof_requirements"]:
        if requirement in {"payment_received", "delivery_completed"}:
            continue
        proofs.append(
            build_proof_event(
                tenant_id=tenant_id,
                entity_type="company_loop_stage",
                entity_id=stage["id"],
                proof_type=ProofType.OUTCOME_EVIDENCE,
                evidence_ref=f"synthetic://company-loop/{run_id}/{stage['id']}/{requirement}",
                verified_at=SYNTHETIC_TIME,
                verifier="company_loop_simulator",
                confidence=0.5,
                is_synthetic=mode == "synthetic",
                publication_approved=False,
            )
        )
    return proofs


def run_loop(
    loop_id: str,
    *,
    mode: str = "synthetic",
    registry_path: Path = DEFAULT_REGISTRY,
) -> dict[str, Any]:
    if mode not in {"synthetic", "draft_only"}:
        raise ValueError("mode must be synthetic or draft_only")

    registry = load_registry(registry_path)
    loop = get_loop(registry, loop_id)
    if loop["status"] != "executable_synthetic":
        raise ValueError(f"loop is not executable yet: {loop_id}")

    run_id = hashlib.sha256(f"dealix:{loop_id}:{mode}:v2".encode()).hexdigest()[:20]
    tenant_id = "synthetic-tenant"
    canonical_outcomes = []
    canonical_proofs = []
    canonical_learning = []
    withheld_claims = []
    result: dict[str, Any] = {
        "schema_version": "2.0",
        "run_id": run_id,
        "tenant_id": tenant_id,
        "loop_id": loop_id,
        "mode": mode,
        "is_synthetic": mode == "synthetic",
        "external_actions_executed": 0,
        "status": "running",
        "stages": [],
        "approvals": [],
        "outcome_events": [],
        "proof_events": [],
        "learning_events": [],
        "withheld_claims": withheld_claims,
        "daily_command": None,
    }

    for stage in sorted(loop["stages"], key=lambda item: item["order"]):
        if stage["external_effect"] and mode == "draft_only":
            result["status"] = "blocked_pending_approval"
            result["blocked_stage"] = stage["id"]
            result["stages"].append(
                {
                    "stage_id": stage["id"],
                    "status": "blocked_pending_approval",
                    "event_type": stage["event_type"],
                }
            )
            break

        if stage["approval_required"]:
            result["approvals"].append(
                {
                    "id": _record_id(run_id, stage["id"], "approval"),
                    "stage_id": stage["id"],
                    "status": "approved_synthetic" if mode == "synthetic" else "approved_input",
                    "risk_level": "controlled_external_effect",
                    "is_synthetic": mode == "synthetic",
                }
            )

        if "OutcomeEvent" in stage["outputs"]:
            outcome = _canonical_outcome(
                tenant_id=tenant_id,
                run_id=run_id,
                stage=stage,
                mode=mode,
            )
            if outcome is not None:
                canonical_outcomes.append(outcome)
                result["outcome_events"].append(outcome.model_dump(mode="json"))
            elif stage["event_type"] in {"payment_received", "delivery_completed"}:
                withheld_claims.append(
                    {
                        "stage_id": stage["id"],
                        "claim": stage["event_type"],
                        "reason": "synthetic financial and delivery outcomes are forbidden",
                    }
                )

        stage_proofs = _canonical_non_financial_proofs(
            tenant_id=tenant_id,
            run_id=run_id,
            stage=stage,
            mode=mode,
        )
        canonical_proofs.extend(stage_proofs)
        result["proof_events"].extend(
            proof.model_dump(mode="json") for proof in stage_proofs
        )

        if "LearningEvent" in stage["outputs"]:
            evidence_refs = sorted(
                {
                    *(
                        outcome.evidence_refs[0]
                        for outcome in canonical_outcomes
                        if outcome.evidence_refs
                    ),
                    *(
                        proof.evidence_ref
                        for proof in canonical_proofs
                    ),
                }
            ) or [f"synthetic://company-loop/{run_id}/no-recognized-value"]
            learning = build_learning_event(
                tenant_id=tenant_id,
                event_type=LearningEventType.OFFER,
                evidence_refs=evidence_refs,
                confidence=0.5,
                recommended_change=(
                    "Keep the loop approval-first and require real payment and delivery "
                    "evidence before recognizing value."
                ),
                created_at=SYNTHETIC_TIME,
            )
            canonical_learning.append(learning)
            result["learning_events"].append(learning.model_dump(mode="json"))

        if "DailyCommand" in stage["outputs"]:
            command = build_daily_command(
                tenant_id=tenant_id,
                command_date=date(2026, 8, 2),
                priorities=["collect real payment evidence", "collect real delivery evidence"],
                approval_items=["approve any external execution separately"],
                proofs=canonical_proofs,
                learning_events=canonical_learning,
                generated_at=SYNTHETIC_TIME,
            )
            result["daily_command"] = command.model_dump(mode="json")

        result["stages"].append(
            {
                "stage_id": stage["id"],
                "status": "completed_synthetic" if mode == "synthetic" else "completed",
                "event_type": stage["event_type"],
                "external_effect_simulated": bool(stage["external_effect"] and mode == "synthetic"),
            }
        )
    else:
        result["status"] = "completed_synthetic" if mode == "synthetic" else "completed"

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--loop", default="lead_to_cash")
    parser.add_argument("--mode", choices=("synthetic", "draft_only"), default="synthetic")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = run_loop(
        args.loop,
        mode=args.mode,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if result["status"].startswith("completed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
