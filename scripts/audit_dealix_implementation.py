"""Master Dealix public-implementation audit.

Runs:
1. existence + minimum-size checks on every PUBLIC_REQUIRED path
2. every scripts/verify_*.py listed in VERIFY_SCRIPTS
3. `python -m compileall` on every code module we ship

Exits 0 only when all three layers are clean. Prints the punch list on failure.

This is the canonical answer to "is Dealix actually implemented?" — see
`DEALIX_IMPLEMENTATION_AUDIT.md` for the user-facing description.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PUBLIC_REQUIRED: tuple[tuple[str, int], ...] = (
    ("DEALIX_STAGE_GATED_ROADMAP.md", 500),
    ("DEALIX_30_DAY_EXECUTION_PLAN.md", 500),
    ("DEALIX_IMPLEMENTATION_AUDIT.md", 500),
    ("docs/revenue/REVENUE_COMMAND_CENTER.md", 500),
    ("docs/trust/TRUST_COMMAND_CENTER.md", 500),
    ("docs/delivery/revenue_sprint/REVENUE_SPRINT_FACTORY.md", 500),
    ("docs/offers/revenue_sprint/REVENUE_SPRINT_KIT.md", 500),
    ("docs/offers/revenue_sprint/founder_dm_pack.md", 200),
    ("docs/offers/revenue_sprint/sample_pack_template.md", 200),
    ("docs/offers/revenue_sprint/proposal_fast_template.md", 200),
    ("docs/offers/revenue_sprint/client_intake.md", 200),
    ("docs/offers/revenue_sprint/delivery_report_template.md", 200),
    ("docs/offers/revenue_sprint/qa_checklist.md", 200),
    ("docs/offers/revenue_sprint/handoff_template.md", 200),
    ("docs/offers/revenue_sprint/feedback_request.md", 200),
    ("docs/offers/revenue_sprint/retainer_ask.md", 200),
    ("docs/ops/OPERATING_READINESS_LEVELS.md", 500),
    ("docs/founder/GO_NO_GO_DECISION_SYSTEM.md", 500),
    ("docs/product/NO_OVERBUILD_POLICY.md", 500),
    ("docs/learning/LEARNING_LOOP.md", 500),
    ("execution_engine/__init__.py", 50),
    ("execution_engine/evidence_scanner.py", 500),
    ("execution_engine/stage_checklist_updater.py", 500),
    ("dealix_cli/__init__.py", 50),
    ("dealix_cli/__main__.py", 500),
    ("dealix_cli/commands.py", 500),
    ("templates/private_ops_audit_template.py", 500),
)

VERIFY_SCRIPTS: tuple[str, ...] = (
    "scripts/verify_tier0_safety.py",
    "scripts/verify_tier1_revenue.py",
    "scripts/verify_tier2_delivery.py",
    "scripts/verify_revenue_sprint_kit.py",
    "scripts/verify_execution_engine.py",
    "scripts/verify_stage_evidence_automation.py",
    "scripts/verify_stage_gated_roadmap.py",
    "scripts/verify_cli.py",
    "scripts/verify_dashboard_v2.py",
    "scripts/verify_weekly_automation.py",
    "scripts/verify_no_autonomous_external_actions.py",
    "scripts/verify_trust_boundary_terms.py",
)

COMPILE_TARGETS: tuple[str, ...] = (
    "dealix_cli",
    "execution_engine",
    "scripts",
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print a JSON summary to stdout instead of human-readable lines.",
    )
    return parser.parse_args()


def _check_files() -> list[str]:
    failures: list[str] = []
    for relative, min_size in PUBLIC_REQUIRED:
        path = REPO_ROOT / relative
        if not path.exists():
            failures.append(f"Missing required file: {relative}")
            continue
        if path.is_file() and path.stat().st_size < min_size:
            failures.append(
                f"Too short or empty: {relative} "
                f"({path.stat().st_size} < {min_size} bytes)"
            )
    return failures


def _run_verifiers() -> list[str]:
    failures: list[str] = []
    for relative in VERIFY_SCRIPTS:
        path = REPO_ROOT / relative
        if not path.exists():
            failures.append(f"Missing verifier: {relative}")
            continue
        print(f"\n== Running {relative} ==")
        result = subprocess.run([sys.executable, str(path)], cwd=REPO_ROOT)
        if result.returncode != 0:
            failures.append(f"Verifier failed: {relative}")
    return failures


def _run_compile() -> list[str]:
    print("\n== Compile Check ==")
    existing = [t for t in COMPILE_TARGETS if (REPO_ROOT / t).exists()]
    if not existing:
        return ["No compile targets found"]
    result = subprocess.run(
        [sys.executable, "-m", "compileall", "-q", *existing],
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        return ["Compile check failed"]
    return []


def main() -> None:
    args = _parse_args()
    print("== Dealix Public Implementation Audit ==")

    failures: list[str] = []
    failures.extend(_check_files())
    failures.extend(_run_verifiers())
    failures.extend(_run_compile())

    if args.json:
        import json

        print(json.dumps({"passed": not failures, "failures": failures}))

    if failures:
        print("\nIMPLEMENTATION AUDIT FAILED:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)

    print("\nPASS: Dealix public implementation audit passed.")


if __name__ == "__main__":
    main()
