"""Command implementations for the dealix_cli package."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def ensure_private_ops(private_ops: str) -> Path:
    """Resolve the private ops root and create it if missing."""
    path = Path(private_ops).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_command(cmd: list[str]) -> None:
    """Run a subprocess, streaming output and raising on failure."""
    print("$", " ".join(cmd))
    result = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def assurance(private_ops: str) -> None:
    """Generate the execution assurance report from real evidence."""
    private_ops_path = ensure_private_ops(private_ops)
    run_command([
        sys.executable,
        str(REPO_ROOT / "scripts" / "generate_execution_assurance_report.py"),
        "--private-ops",
        str(private_ops_path),
    ])
    print("\nPASS: assurance command completed.")
    print(
        "Review: "
        f"{private_ops_path / 'evidence' / 'execution_assurance_report.md'}"
    )
