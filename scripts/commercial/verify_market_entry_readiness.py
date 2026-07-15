#!/usr/bin/env python3
"""Fail-closed verification for the Dealix market-entry decision layer."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        command = [
            sys.executable,
            str(ROOT / "scripts/commercial/run_founder_market_entry.py"),
            "--signals",
            "data/examples/dealix_market_entry_signals.demo.yaml",
            "--output-dir",
            tmp,
        ]
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            fail(result.stdout + result.stderr)
        snapshot = json.loads(
            (Path(tmp) / "market_entry_snapshot.json").read_text(encoding="utf-8")
        )
        if snapshot["external_actions_executed"] != 0:
            fail("market-entry runner executed an external action")
        if snapshot["stage"] not in {
            "evidence_required",
            "private_pilot_ready",
            "limited_launch_ready",
            "scale_ready",
        }:
            fail(f"unexpected stage: {snapshot['stage']}")
        if snapshot["stage"] == "evidence_required" and snapshot["public_claims_authorized"]:
            fail("public claims authorized without evidence")
        if not snapshot["pricing_audit"]["ok"]:
            fail("canonical pilot pricing drift detected")
        required = {
            "launch_gates.csv",
            "action_queue.csv",
            "approval_queue.csv",
            "strategy_backlog.csv",
            "opportunity_graph.csv",
            "proof_ledger.csv",
            "self_improvement.csv",
            "contacts_radar.csv",
            "90_day_milestones.csv",
            "slack_command_update.md",
        }
        missing = sorted(name for name in required if not (Path(tmp) / name).is_file())
        if missing:
            fail(f"missing operating artifacts: {missing}")
    print("DEALIX_MARKET_ENTRY_VERDICT=PASS")
    print("EXTERNAL_ACTIONS_EXECUTED=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
