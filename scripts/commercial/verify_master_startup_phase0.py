#!/usr/bin/env python3
"""Verify the master-startup Phase-0 consolidation contract."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NoReturn

REQUIRED_OUTPUTS = {
    "latest.json",
    "latest.md",
    "current_state_and_drift.md",
    "blockers.json",
    "proof_log.json",
    "capability_reality_matrix.csv",
    "approval_queue.csv",
    "opportunity_graph.csv",
    "claim_and_proof_registry.csv",
    "claim_and_proof_registry.md",
}


def fail(message: str) -> NoReturn:
    print(f"MASTER_STARTUP_PHASE0_VERDICT=FAIL reason={message}", file=sys.stderr)
    raise SystemExit(1)


def _verify(output_dir: Path) -> None:
    missing = sorted(name for name in REQUIRED_OUTPUTS if not (output_dir / name).is_file())
    if missing:
        fail("missing_outputs:" + ",".join(missing))

    latest = json.loads((output_dir / "latest.json").read_text(encoding="utf-8"))
    summary = latest.get("summary") or {}
    if summary.get("external_actions_executed") != 0:
        fail("external_actions_must_be_zero")
    if summary.get("production_changes") != 0:
        fail("production_changes_must_be_zero")

    for item in latest.get("opportunities") or []:
        if item.get("conversion_probability") is not None:
            fail("uncalibrated_conversion_probability_must_be_null")
        if item.get("prediction_status") != "not_calibrated":
            fail("prediction_status_must_be_not_calibrated")

    for item in latest.get("approval_requests") or []:
        if item.get("status") == "approved" or item.get("action_mode") == "approved_execute":
            fail("phase0_cannot_preapprove_external_actions")

    proof = json.loads((output_dir / "proof_log.json").read_text(encoding="utf-8"))
    if latest.get("mode") == "mixed_or_demo" and proof.get("events"):
        fail("demo_inputs_must_not_create_proof_events")

    blockers = json.loads((output_dir / "blockers.json").read_text(encoding="utf-8"))
    if blockers.get("external_actions_executed") != 0:
        fail("blocker_report_external_actions_must_be_zero")

    with (output_dir / "capability_reality_matrix.csv").open(encoding="utf-8") as handle:
        capabilities = list(csv.DictReader(handle))
    if not capabilities or any(row.get("production_claim_allowed") != "no" for row in capabilities):
        fail("capability_matrix_must_block_unverified_production_claims")

    with (output_dir / "opportunity_graph.csv").open(encoding="utf-8") as handle:
        opportunities = list(csv.DictReader(handle))
    if not opportunities:
        fail("opportunity_graph_is_empty")
    if any(row.get("conversion_probability") for row in opportunities):
        fail("opportunity_csv_contains_uncalibrated_probability")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Dealix Phase-0 consolidation")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()

    if args.output_dir:
        output_dir = args.output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        temporary = None
    else:
        temporary = tempfile.TemporaryDirectory(prefix="dealix-phase0-")
        output_dir = Path(temporary.name)

    command = [
        sys.executable,
        str(root / "scripts" / "commercial" / "run_master_startup_phase0.py"),
        "--root",
        str(root),
        "--output-dir",
        str(output_dir),
        "--demo",
    ]
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        fail("generator_failed:" + (result.stderr.strip() or result.stdout.strip())[-500:])
    _verify(output_dir)
    print("MASTER_STARTUP_PHASE0_VERDICT=PASS")
    print("EXTERNAL_ACTIONS_EXECUTED=0")
    print("DEMO_PROOF_EVENTS=0")
    if args.output_dir:
        print(f"REPORT_DIR={output_dir}")
    if temporary is not None:
        temporary.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
