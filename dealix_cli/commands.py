"""Founder-facing commands for the Dealix CLI."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parent.parent


def ensure_private_ops(private_ops: str) -> Path:
    path = Path(private_ops).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_command(cmd: List[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=REPO_ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def business_score(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    run_command(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "generate_ceo_business_score.py"),
            "--private-ops",
            str(private_ops_path),
        ]
    )
    print("\nPASS: business-score command completed.")


def audit(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    run_command([sys.executable, str(REPO_ROOT / "scripts" / "verify_ceo_business_systems.py")])
    run_command([sys.executable, str(REPO_ROOT / "scripts" / "verify_ceo_business_score.py")])
    run_command(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "generate_ceo_business_score.py"),
            "--private-ops",
            str(private_ops_path),
        ]
    )
    print("\nPASS: audit command completed.")
