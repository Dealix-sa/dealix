#!/usr/bin/env python3
"""Aggregate Dealix Private-Launch readiness gate.

Checks the Private Launch checklist from the Launch Control Tower:
  - /command-sprint and /start pages exist
  - sales kit (6 files) exists
  - customers/_template (12 files) exists
  - proof pack template exists
  - claims register + approval policy exist
  - positioning + cta + module-status + growth gates pass

Prints a verdict: PRIVATE_LAUNCH_READY=true/false and a Go/No-Go line.
Exit 0 if Private Launch ready, 1 otherwise.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

PAGES = [
    "frontend/src/app/[locale]/command-sprint/page.tsx",
    "frontend/src/app/[locale]/start/page.tsx",
]
SALES_KIT = [
    "sales/COMMAND_SPRINT_ONE_PAGER.md",
    "sales/DIAGNOSTIC_SCRIPT.md",
    "sales/OBJECTION_LIBRARY.md",
    "sales/PROPOSAL_TEMPLATE.md",
    "sales/FOLLOW_UP_SEQUENCE.md",
    "sales/PARTNER_ONE_PAGER.md",
]
CUSTOMER_TEMPLATE = [
    "customers/_template/00_intake.md",
    "customers/_template/01_company_intelligence.md",
    "customers/_template/02_diagnostic_summary.md",
    "customers/_template/03_command_sprint_scope.md",
    "customers/_template/04_revenue_map.md",
    "customers/_template/05_proof_register.md",
    "customers/_template/06_approval_register.md",
    "customers/_template/07_next_action_board.md",
    "customers/_template/08_executive_command_brief.md",
    "customers/_template/09_delivery_log.md",
    "customers/_template/10_proof_pack.md",
    "customers/_template/11_upsell_recommendation.md",
]
GOVERNANCE = [
    "customers/_template/10_proof_pack.md",
    "docs/governance/CLAIMS_REGISTER.md",
    "docs/governance/APPROVAL_MATRIX.md",
    "docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md",
]

SUB_GATES = [
    "scripts/verify_dealix_positioning.py",
    "scripts/verify_dealix_cta_map.py",
    "scripts/verify_dealix_module_status.py",
    "scripts/verify_dealix_growth_assets.py",
]


def _missing(paths: list[str]) -> list[str]:
    return [p for p in paths if not (REPO / p).exists()]


def _run_gate(rel: str) -> bool:
    try:
        res = subprocess.run(
            [sys.executable, str(REPO / rel)],
            capture_output=True, text=True, cwd=str(REPO),
        )
        return res.returncode == 0
    except Exception:  # noqa: BLE001
        return False


def main() -> int:
    failures: list[str] = []

    for label, paths in (
        ("pages", PAGES),
        ("sales_kit", SALES_KIT),
        ("customer_template", CUSTOMER_TEMPLATE),
        ("governance", GOVERNANCE),
    ):
        miss = _missing(paths)
        ok = not miss
        print(f"{label.upper()}_PASS={'true' if ok else 'false'}")
        for m in miss:
            failures.append(f"missing {label}: {m}")

    for gate in SUB_GATES:
        ok = _run_gate(gate)
        name = Path(gate).stem.replace("verify_dealix_", "").upper()
        print(f"GATE_{name}_PASS={'true' if ok else 'false'}")
        if not ok:
            failures.append(f"sub-gate failed: {gate}")

    ready = not failures
    print(f"PRIVATE_LAUNCH_READY={'true' if ready else 'false'}")
    print(f"VERDICT={'PRIVATE_LAUNCH_READY' if ready else 'NO_GO'}")

    if not ready:
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
