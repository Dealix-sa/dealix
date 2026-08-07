from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_company_day_guards_removed_legacy_runner() -> None:
    script = ROOT / "scripts" / "dealix_company_day.sh"
    text = script.read_text(encoding="utf-8")

    assert "if [ -x ./scripts/dealix_secret_aware_company_day.sh ]; then" in text
    assert "external execution remains disabled" in text

    result = subprocess.run(
        ["bash", "-n", str(script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_v16_readiness_contract_is_complete() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/dealix_v16_readiness_check.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert "Checked: 11 critical files" in result.stdout
