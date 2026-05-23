"""Founder CLI command implementations."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def ensure_private_ops(private_ops: str) -> Path:
    """Resolve and validate the private ops root."""
    path = Path(private_ops).expanduser().resolve()
    if not path.exists():
        raise SystemExit(
            f"FAIL: private ops path does not exist: {path}"
        )
    if not path.is_dir():
        raise SystemExit(
            f"FAIL: private ops path is not a directory: {path}"
        )
    return path


def run_command(cmd: list[str]) -> None:
    """Run a subprocess and raise SystemExit on failure."""
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def mission_control(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    run_command([
        sys.executable,
        "scripts/generate_mission_control.py",
        "--private-ops",
        str(private_ops_path),
    ])
    print("\nPASS: mission-control command completed.")
