#!/usr/bin/env python3
"""Run the Dealix Revenue Lab against supplied signals in draft-only mode."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.proof_ledger.file_backend import FileProofLedger
from auto_client_acquisition.proof_ledger.schemas import ProofEvent
from dealix.revenue_lab import CompanySignal, OutcomeEvent, run_revenue_lab
from dealix.revenue_lab.artifacts import write_bundle


def _load(path: Path) -> tuple[list[CompanySignal], list[OutcomeEvent]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        signal_rows = payload
        outcome_rows: list[dict] = []
    elif isinstance(payload, dict):
        signal_rows = payload.get("signals") or []
        outcome_rows = payload.get("outcomes") or []
    else:
        raise ValueError("input must be a JSON list or object")
    return (
        [CompanySignal.from_dict(item) for item in signal_rows],
        [OutcomeEvent.from_dict(item) for item in outcome_rows],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the evidence-first Dealix Revenue Lab")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--mode", default="draft-only", choices=("draft-only",))
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--proof-ledger-dir", type=Path)
    args = parser.parse_args()

    if args.demo and args.input:
        parser.error("use either --demo or --input, not both")
    input_path = args.input
    if args.demo:
        input_path = ROOT / "data" / "examples" / "revenue_lab_signals.demo.json"
    if input_path is None:
        parser.error("--input is required unless --demo is used")

    signals, outcomes = _load(input_path)
    bundle = run_revenue_lab(signals, outcomes=outcomes)
    output_dir = args.output_dir or (
        ROOT / "reports" / "revenue_lab" / datetime.now(UTC).strftime("%Y-%m-%d")
    )
    paths = write_bundle(output_dir, bundle)

    if args.proof_ledger_dir:
        ledger = FileProofLedger(base_dir=args.proof_ledger_dir)
        for event in bundle.proof_events:
            ledger.record(ProofEvent.model_validate(event))

    print(f"REVENUE_LAB_RUN_ID={bundle.run_id}")
    print(f"REVENUE_LAB_MODE={bundle.mode}")
    print(f"REVENUE_LAB_OPPORTUNITIES={bundle.summary['opportunities']}")
    print(f"REVENUE_LAB_EXTERNAL_ACTIONS={bundle.summary['external_actions_executed']}")
    print(f"REVENUE_LAB_VERIFIED_OUTCOMES={bundle.summary['verified_customer_outcomes']}")
    print(f"REVENUE_LAB_REPORT={paths['latest_md']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
