#!/usr/bin/env python3
"""Run a deterministic, network-free synthetic Dealix company loop."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = REPO_ROOT / "dealix/registers/company_loops_registry.json"


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


def run_loop(
    loop_id: str,
    *,
    mode: str = "synthetic",
    approve_external: bool = False,
    registry_path: Path = DEFAULT_REGISTRY,
) -> dict[str, Any]:
    if mode not in {"synthetic", "draft_only"}:
        raise ValueError("mode must be synthetic or draft_only")

    registry = load_registry(registry_path)
    loop = get_loop(registry, loop_id)
    if loop["status"] != "executable_synthetic":
        raise ValueError(f"loop is not executable yet: {loop_id}")

    run_id = hashlib.sha256(f"dealix:{loop_id}:{mode}:v1".encode()).hexdigest()[:20]
    result: dict[str, Any] = {
        "schema_version": "1.0",
        "run_id": run_id,
        "tenant_id": "synthetic-tenant",
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
        "daily_command": None,
    }

    for stage in sorted(loop["stages"], key=lambda item: item["order"]):
        if stage["external_effect"] and mode == "draft_only" and not approve_external:
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

        outcome_id = _record_id(run_id, stage["id"], "outcome")
        if "OutcomeEvent" in stage["outputs"]:
            result["outcome_events"].append(
                {
                    "id": outcome_id,
                    "stage_id": stage["id"],
                    "event_type": stage["event_type"],
                    "is_synthetic": mode == "synthetic",
                }
            )

        for proof_type in stage["proof_requirements"]:
            result["proof_events"].append(
                {
                    "id": _record_id(run_id, stage["id"], f"proof:{proof_type}"),
                    "stage_id": stage["id"],
                    "proof_type": proof_type,
                    "verified": True,
                    "is_synthetic": mode == "synthetic",
                }
            )

        if "LearningEvent" in stage["outputs"]:
            result["learning_events"].append(
                {
                    "id": _record_id(run_id, stage["id"], "learning"),
                    "stage_id": stage["id"],
                    "event_type": stage["event_type"],
                    "confidence": 0.5,
                    "status": "hypothesis",
                    "is_synthetic": mode == "synthetic",
                }
            )

        if "DailyCommand" in stage["outputs"]:
            result["daily_command"] = {
                "id": _record_id(run_id, stage["id"], "daily-command"),
                "loop_id": loop_id,
                "status": "synthetic_complete" if mode == "synthetic" else "complete",
                "approval_count": len(result["approvals"]),
                "proof_count": len(result["proof_events"]),
                "learning_count": len(result["learning_events"]),
            }

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
    parser.add_argument("--approve-external", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = run_loop(
        args.loop,
        mode=args.mode,
        approve_external=args.approve_external,
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
