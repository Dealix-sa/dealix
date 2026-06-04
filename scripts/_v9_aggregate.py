#!/usr/bin/env python3
"""Helper to aggregate V9 verifier verdicts into a themed roll-up report."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

# Map of short keys -> verify module names.
V9_MODULES = {
    "strategic_moat": "strategic_moat_verify",
    "enterprise_readiness": "enterprise_readiness_verify",
    "trust_center": "trust_center_verify",
    "demo_os": "demo_os_verify",
    "customer_lifecycle": "customer_lifecycle_verify",
    "agent_governance": "agent_governance_verify",
    "agent_registry": "agent_registry_verify",
    "cost_control": "cost_control_verify",
    "data_room": "data_room_verify",
    "procurement": "procurement_verify",
    "qms": "qms_verify",
    "docs_governance": "docs_governance_verify",
    "deployment_static": "deployment_static_verify",
}


def run_subset(keys: list[str]) -> dict:
    results: dict[str, str] = {}
    for key in keys:
        mod = importlib.import_module(V9_MODULES[key])
        report = mod.verify()
        results[key] = report.get("verdict", "FAIL")
    return results


def aggregate(name: str, keys: list[str], output_name: str) -> dict:
    results = run_subset(keys)
    verdict = "PASS" if all(v == "PASS" for v in results.values()) else "FAIL"
    report = {
        "aggregate": name,
        "verdict": verdict,
        "checked": results,
    }
    v9_lib.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (v9_lib.OUTPUT_DIR / f"{output_name}.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def print_aggregate(report: dict) -> int:
    print(f"[{report['aggregate']}] verdict={report['verdict']}")
    for k, v in report["checked"].items():
        print(f"  - {k}: {v}")
    print(f"{report['aggregate'].upper()}_VERDICT={report['verdict']}")
    return 0 if report["verdict"] == "PASS" else 1
