#!/usr/bin/env python3
"""Aggregate Dealix launch-readiness verifier.

Combines the three component verifiers (positioning, module status, growth
assets) with the presence of the governance approval doctrine document and the
private launch-readiness report. Prints a readiness score (X/Y) and a
PASS / NOT-READY verdict with the blockers list. Component verifiers are
imported defensively so a missing component is reported as a blocker rather than
crashing the aggregator.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

GOVERNANCE_DOC = ROOT / "docs" / "03_governance" / "NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md"
LAUNCH_REPORT = ROOT / "reports" / "launch" / "private_launch_readiness.md"


def _run_component(label: str, func_path: tuple[str, str]) -> dict[str, Any]:
    """Import and run a component verifier; degrade gracefully on failure."""
    module_name, func_name = func_path
    try:
        import importlib

        module = importlib.import_module(module_name)
        func: Callable[[], dict[str, Any]] = getattr(module, func_name)
        result = func()
        verdict = str(result.get("verdict", "FAIL"))
    except Exception as exc:  # pragma: no cover - defensive
        return {"label": label, "status": "FAIL", "detail": f"verifier error: {exc}"}
    return {
        "label": label,
        "status": "PASS" if verdict == "PASS" else "FAIL",
        "detail": f"{label} verdict {verdict}",
    }


def _check_doc(label: str, path: Path) -> dict[str, Any]:
    ok = path.is_file() and path.stat().st_size > 0
    return {
        "label": label,
        "status": "PASS" if ok else "FAIL",
        "detail": str(path.relative_to(ROOT)) + ("" if ok else " (missing)"),
    }


def check_launch_readiness() -> dict[str, Any]:
    """Aggregate all readiness checks. Returns a structured result."""
    checks: list[dict[str, Any]] = [
        _run_component("positioning", ("scripts.verify_dealix_positioning", "check_positioning")),
        _run_component("module_status", ("scripts.verify_dealix_module_status", "check_modules")),
        _run_component("growth_assets", ("scripts.verify_dealix_growth_assets", "check_growth_assets")),
        _check_doc("governance_approval_doc", GOVERNANCE_DOC),
        _check_doc("private_launch_readiness_report", LAUNCH_REPORT),
    ]
    passed = sum(1 for c in checks if c["status"] == "PASS")
    total = len(checks)
    blockers = [c["label"] for c in checks if c["status"] != "PASS"]
    verdict = "PASS" if not blockers else "NOT-READY"
    return {
        "checks": checks,
        "score": passed,
        "total": total,
        "blockers": blockers,
        "verdict": verdict,
    }


def _print_table(result: dict[str, Any]) -> None:
    print("== Dealix Launch Readiness ==")
    for c in result["checks"]:
        print(f"  [{c['status']}] {c['label']}: {c['detail']}")
    print(f"Score: {result['score']}/{result['total']}")
    if result["blockers"]:
        print(f"Blockers: {', '.join(result['blockers'])}")
    print(f"Verdict: {result['verdict']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    result = check_launch_readiness()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_table(result)
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
