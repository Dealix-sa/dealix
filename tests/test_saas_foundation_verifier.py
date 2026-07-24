"""Regression coverage for the repository-level SaaS verifier."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_saas_foundation.py"


def test_saas_foundation_verifier_reports_ready_with_operator_gates() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(ROOT), "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)

    assert result["foundation_status"] == "READY"
    assert result["production_activation_status"] == "OPERATOR_GATES_REQUIRED"
    assert all(check["passed"] for check in result["checks"])
    assert [gate["issue"] for gate in result["operator_gates"]] == [898, 884, 894]
    assert "production-ready requires" in result["claim_boundary"]
