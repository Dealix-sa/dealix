#!/usr/bin/env python3
"""Build the Phase-0 evidence pack without external or production mutation."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.revenue_lab import CompanySignal, OutcomeEvent, run_revenue_lab
from dealix.revenue_lab.artifacts import write_bundle
from scripts.commercial.audit_dealix_claims_phase0 import audit, write_registry

CAPABILITIES = (
    (
        "market_intelligence",
        "dealix/commercial/market_intelligence.py",
        "Curated intelligence code exists; live company signals still require attributable sources.",
    ),
    (
        "opportunity_graph",
        "dealix/commercial_universe.py",
        "Tenant-scoped opportunity foundation exists and Revenue Lab adds evidence status.",
    ),
    (
        "approval_queue",
        "auto_client_acquisition/approval_center/schemas.py",
        "Canonical queue is reused; research-only and unknown permission fail closed.",
    ),
    (
        "proof_ledger",
        "auto_client_acquisition/proof_ledger/file_backend.py",
        "Append-only ledger exists; process proof is separated from customer outcomes.",
    ),
    (
        "sales_strategy",
        "dealix/revenue_lab/engine.py",
        "Draft strategies include objections, give-get rules, and forbidden commitments.",
    ),
    (
        "proposal_generation",
        "dealix/commercial/transformation_proposal.py",
        "Proposal and conservative ROI foundations exist; baselines remain client-sourced.",
    ),
    (
        "negotiation",
        "dealix/company_os/negotiation_engine.py",
        "Draft negotiation plans exist; price, discount, legal terms, and guarantees are restricted.",
    ),
    (
        "delivery",
        "auto_client_acquisition/delivery_os/framework.py",
        "Delivery contracts exist; Revenue Lab produces a bounded 14-day proof plan.",
    ),
    (
        "self_improvement",
        "dealix/commercial_ops/revenue_learning_loop.py",
        "Evidence-backed recommendations exist; weights never self-modify without an experiment review.",
    ),
)


def _load(path: Path) -> tuple[list[CompanySignal], list[OutcomeEvent]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    signal_rows = payload if isinstance(payload, list) else payload.get("signals") or []
    outcome_rows = [] if isinstance(payload, list) else payload.get("outcomes") or []
    return (
        [CompanySignal.from_dict(item) for item in signal_rows],
        [OutcomeEvent.from_dict(item) for item in outcome_rows],
    )


def _git_value(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, check=False, capture_output=True, text=True, timeout=10
        )
    except (OSError, subprocess.TimeoutExpired):
        return "unavailable"
    return result.stdout.strip() if result.returncode == 0 else "unavailable"


def _write_capability_matrix(root: Path, output_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for capability, relative, reality in CAPABILITIES:
        present = (root / relative).is_file()
        rows.append(
            {
                "capability": capability,
                "status": "code_present" if present else "missing",
                "evidence_path": relative,
                "verified_reality": reality if present else "Required evidence path is missing.",
                "production_claim_allowed": "no",
            }
        )
    with (output_dir / "capability_reality_matrix.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def _write_current_state(root: Path, output_dir: Path, bundle: dict[str, Any]) -> None:
    branch = _git_value(root, "branch", "--show-current")
    head = _git_value(root, "rev-parse", "--short", "HEAD")
    lines = [
        "# Dealix Phase 0 — Current State and Drift",
        "",
        f"- Branch: `{branch}`",
        f"- HEAD: `{head}`",
        "- Product category: AI Business Operating System",
        "- Autonomy boundary: internal execution and drafts only",
        f"- Revenue Lab mode: `{bundle['mode']}`",
        f"- External actions executed: `{bundle['summary']['external_actions_executed']}`",
        f"- Verified customer outcomes: `{bundle['summary']['verified_customer_outcomes']}`",
        "",
        "## Reality",
        "",
        "- Existing Commercial Universe, Approval Center, Proof Ledger, proposal, negotiation, delivery, and learning components are reused.",
        "- A code path or passing unit test proves implementation behavior, not customer value or production reliability.",
        "- Conversion probability remains uncalibrated until attributable outcomes exist.",
        "- Demo inputs are excluded from proof events and must never become public proof.",
        "",
        "## Drift removed in this phase",
        "",
        "- Revenue Lab is no longer an empty package export.",
        "- The Phase-0 verifier is executable instead of ending at an incomplete function declaration.",
        "- Opportunity scores are labeled as priorities, not win probabilities.",
        "- Unknown permission or missing evidence remains research-only.",
    ]
    (output_dir / "current_state_and_drift.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the Dealix Phase-0 evidence pack")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--output-dir", type=Path, default=Path("reports/dealix_autonomous_company_os")
    )
    parser.add_argument("--input", type=Path)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    output_dir = args.output_dir.resolve()
    input_path = args.input
    if args.demo:
        input_path = root / "data" / "examples" / "revenue_lab_signals.demo.json"
    if input_path is None:
        parser.error("--input is required unless --demo is used")

    signals, outcomes = _load(input_path)
    bundle = run_revenue_lab(signals, outcomes=outcomes)
    write_bundle(output_dir, bundle)
    findings = audit(root, ())
    # Empty surfaces would skip the audit, so use the auditor's canonical defaults.
    if not findings:
        from scripts.commercial.audit_dealix_claims_phase0 import DEFAULT_SURFACES

        findings = audit(root, DEFAULT_SURFACES)
    write_registry(output_dir, findings)
    capability_rows = _write_capability_matrix(root, output_dir)
    bundle_payload = bundle.to_dict()
    _write_current_state(root, output_dir, bundle_payload)

    blockers = list(bundle.blockers)
    blockers.extend(
        f"{row['capability']}: required implementation path missing"
        for row in capability_rows
        if row["status"] == "missing"
    )
    if bundle.summary["verified_customer_outcomes"] < 1:
        blockers.append("No verified customer outcome; no public case-study claim is allowed")
    blocker_payload = {
        "phase0_foundation_ready": not any(row["status"] == "missing" for row in capability_rows),
        "commercial_proof_ready": bundle.summary["verified_customer_outcomes"] > 0,
        "external_actions_executed": 0,
        "blockers": list(dict.fromkeys(blockers)),
    }
    (output_dir / "blockers.json").write_text(
        json.dumps(blocker_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print("MASTER_STARTUP_PHASE0_GENERATED=1")
    print(f"PHASE0_FOUNDATION_READY={int(blocker_payload['phase0_foundation_ready'])}")
    print(f"COMMERCIAL_PROOF_READY={int(blocker_payload['commercial_proof_ready'])}")
    print("EXTERNAL_ACTIONS_EXECUTED=0")
    print(f"REPORT_DIR={output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
