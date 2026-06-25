import json
import subprocess
import sys
from pathlib import Path


def test_startup_os_release_gate_runs_and_reports():
    result = subprocess.run(
        [sys.executable, "scripts/commercial/verify_startup_os_release_gate.py"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "STARTUP_OS_RELEASE_GATE=PASS" in result.stdout

    report = Path("reports/startup_release_gate/latest.json")
    assert report.exists()
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["verdict"] == "PASS"
    assert not data["failures"]
