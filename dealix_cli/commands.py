"""Dealix CEO operating commands.

Thin wrappers around the data-quality, snapshot, and (future) business-score,
assurance, and control-tower scripts. Every command takes --private-ops so
real customer data stays out of the public repo.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def ensure_private_ops(private_ops: str) -> Path:
    path = Path(private_ops).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Private ops path does not exist: {path}")
    if not path.is_dir():
        raise SystemExit(f"Private ops path is not a directory: {path}")
    return path


def run_command(cmd: list[str]) -> None:
    result = subprocess.run(cmd, cwd=REPO_ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def _script(name: str) -> str:
    return str(REPO_ROOT / "scripts" / name)


def data_quality(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    run_command([
        sys.executable,
        _script("audit_private_data_quality.py"),
        "--private-ops",
        str(private_ops_path),
    ])
    print("\nPASS: data-quality command completed.")


def snapshot(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    run_command([
        sys.executable,
        _script("export_company_snapshot.py"),
        "--private-ops",
        str(private_ops_path),
    ])
    print("\nPASS: snapshot command completed.")


def _optional(private_ops: str, script_name: str, label: str) -> None:
    """Run an ops script if it exists; otherwise warn and continue.

    Lets the master ceo-data / company-check flows degrade gracefully while
    the business-score, assurance, and control-tower modules are still
    being wired in.
    """
    script_path = REPO_ROOT / "scripts" / script_name
    if not script_path.exists():
        print(f"SKIP: {label} script not present yet ({script_name}).")
        return
    private_ops_path = ensure_private_ops(private_ops)
    run_command([sys.executable, str(script_path), "--private-ops", str(private_ops_path)])


def business_score(private_ops: str) -> None:
    _optional(private_ops, "compute_business_score.py", "business-score")


def assurance(private_ops: str) -> None:
    _optional(private_ops, "compute_execution_assurance.py", "assurance")


def control_tower(private_ops: str) -> None:
    _optional(private_ops, "compute_control_tower.py", "control-tower")
