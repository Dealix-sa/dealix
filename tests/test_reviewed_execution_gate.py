from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_reviewed_execution_gate_verifier_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/verify_reviewed_execution_gate.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS reviewed_execution_gate" in result.stdout
