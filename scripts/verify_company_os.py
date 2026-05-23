#!/usr/bin/env python3
"""Verify the Dealix Autonomous Company Control Plane v1 is in place.

This script is the executable definition of "Dealix Autonomous Company
Control Plane v1". It exits non-zero if any required artefact is
missing, so CI (GitHub Actions) can gate the company on it.

Usage:
    python scripts/verify_company_os.py
    python scripts/verify_company_os.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


REQUIRED_FILES: tuple[tuple[str, str], ...] = (
    # Control Plane code + schema
    ("control_plane/__init__.py", "Control Plane package"),
    ("control_plane/company_state.py", "Company State Schema"),
    ("control_plane/action_router.py", "Action Router"),
    ("docs/control_plane/COMPANY_STATE_SCHEMA.md", "Company State Schema doc"),
    ("docs/control_plane/ACTION_ROUTER.md", "Action Router doc"),
    # Operating doctrine
    ("docs/ops/OPERATING_LOOPS.md", "Operating Loops"),
    ("docs/ops/SYSTEM_OWNERS.md", "System Owners"),
    ("docs/ops/ESCALATION_MATRIX.md", "Escalation Matrix"),
    ("docs/ops/OPERATING_METRICS_CONTRACT.md", "Operating Metrics Contract"),
    # Founder OS
    ("docs/founder/FOUNDER_LEVERAGE_INDEX.md", "Founder Leverage Index"),
    ("docs/founder/BOARD_PACK_TEMPLATE.md", "Board Pack Template"),
    ("docs/founder/CEO_DASHBOARD_SPEC.md", "CEO Dashboard Spec"),
    ("docs/founder/KILL_LIST.md", "Kill List"),
    ("docs/founder/DECISION_QUEUE_TEMPLATE.md", "Decision Queue Template"),
    # Learning
    ("docs/learning/COMPANY_MEMORY.md", "Company Memory"),
    ("docs/learning/EXPERIMENT_SYSTEM.md", "Experiment System"),
    # Product / Revenue / CS / Finance / Strategy
    ("docs/product/PRODUCTIZATION_ENGINE.md", "Productization Engine"),
    ("docs/revenue/REVENUE_QUALITY.md", "Revenue Quality"),
    ("docs/client_success/CLIENT_TIERING.md", "Client Tiering"),
    ("docs/finance/CAPITAL_ALLOCATION.md", "Capital Allocation"),
    ("docs/strategy/MOAT_SYSTEM.md", "Moat System"),
)


def _check_file(rel_path: str) -> bool:
    path = REPO_ROOT / rel_path
    return path.is_file() and path.stat().st_size > 0


def _import_smoke() -> tuple[bool, str]:
    """Import the control_plane package end-to-end so a syntax error in
    company_state.py or action_router.py fails the verify."""

    sys.path.insert(0, str(REPO_ROOT))
    try:
        from control_plane import (  # noqa: F401  -- imported for side-effect
            ActionPath,
            ActionRouter,
            CompanyState,
        )

        router = ActionRouter()
        routed = router.route("send proposal to Acme")
        if routed.path is not ActionPath.APPROVE:
            return False, f"expected APPROVE for 'send proposal', got {routed.path}"

        blocked = router.route("guaranteed revenue claim")
        if blocked.path is not ActionPath.BLOCK:
            return False, f"expected BLOCK for 'guaranteed revenue', got {blocked.path}"

        state = CompanyState()
        state.to_dict()  # round-trip
        return True, "import + smoke OK"
    except Exception as exc:  # pragma: no cover -- only triggered on regressions
        return False, f"import failed: {exc!r}"


def verify() -> dict[str, object]:
    file_results: list[dict[str, object]] = []
    all_files_pass = True
    for rel_path, label in REQUIRED_FILES:
        ok = _check_file(rel_path)
        if not ok:
            all_files_pass = False
        file_results.append({"path": rel_path, "label": label, "pass": ok})

    import_ok, import_msg = _import_smoke()

    return {
        "all_pass": all_files_pass and import_ok,
        "files": file_results,
        "import_smoke": {"pass": import_ok, "message": import_msg},
    }


def _print_human(result: dict[str, object]) -> None:
    print("Dealix Autonomous Company Control Plane v1 -- verify")
    print("=" * 56)
    for entry in result["files"]:  # type: ignore[index]
        tag = "[PASS]" if entry["pass"] else "[FAIL]"
        print(f"{tag} {entry['label']:<32} {entry['path']}")
    smoke = result["import_smoke"]  # type: ignore[index]
    tag = "[PASS]" if smoke["pass"] else "[FAIL]"
    print(f"{tag} {'Control plane import + smoke':<32} {smoke['message']}")
    print("=" * 56)
    print("RESULT:", "PASS" if result["all_pass"] else "FAIL")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON to stdout")
    args = parser.parse_args()

    result = verify()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        _print_human(result)

    return 0 if result["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
