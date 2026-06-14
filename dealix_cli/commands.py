"""CLI command implementations."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def ensure_private_ops(private_ops: str) -> Path:
    path = Path(private_ops).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    for sub in ("founder", "business_audit", "stage", "pipeline", "finance"):
        (path / sub).mkdir(parents=True, exist_ok=True)
    return path


def run_command(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(REPO_ROOT), check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def ceo(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    run_command([
        sys.executable,
        "scripts/generate_ceo_business_score.py",
        "--private-ops",
        str(private_ops_path),
    ])
    run_command([
        sys.executable,
        "scripts/generate_ceo_action_queue.py",
        "--private-ops",
        str(private_ops_path),
    ])
    print("\nCEO Command Files:")
    print(f"- {private_ops_path / 'business_audit/ceo_business_score.md'}")
    print(f"- {private_ops_path / 'founder/ceo_action_queue.md'}")
    print(f"- {private_ops_path / 'founder/ceo_command.md'}")
    print(f"- {private_ops_path / 'founder/decision_queue.md'}")
    print("\nPASS: CEO command completed.")


def monthly(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    run_command([
        sys.executable,
        "scripts/generate_monthly_strategy_review.py",
        "--private-ops",
        str(private_ops_path),
    ])
    run_command([
        sys.executable,
        "scripts/generate_finance_review.py",
        "--private-ops",
        str(private_ops_path),
    ])
    print("\nPASS: monthly command completed.")
