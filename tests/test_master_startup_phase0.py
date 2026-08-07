from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_phase0_verifier_builds_and_checks_complete_pack(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "commercial" / "verify_master_startup_phase0.py"),
            "--root",
            str(ROOT),
            "--output-dir",
            str(tmp_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    assert "MASTER_STARTUP_PHASE0_VERDICT=PASS" in result.stdout
    assert "EXTERNAL_ACTIONS_EXECUTED=0" in result.stdout
    assert (tmp_path / "capability_reality_matrix.csv").is_file()
    assert (tmp_path / "claim_and_proof_registry.csv").is_file()
