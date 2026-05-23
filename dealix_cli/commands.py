"""Founder CLI command implementations."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def ensure_private_ops(private_ops: str) -> Path:
    path = Path(private_ops).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    for sub in (
        "business_audit",
        "founder",
        "stage",
        "finance",
        "pipeline",
        "revenue",
        "delivery",
    ):
        (path / sub).mkdir(parents=True, exist_ok=True)
    return path


def run_command(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def control_tower(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    run_command([
        sys.executable,
        "scripts/generate_control_tower_brief.py",
        "--private-ops",
        str(private_ops_path),
    ])
    print("\nControl Tower Files:")
    print(f"- {private_ops_path / 'founder/control_tower_brief.md'}")
    print(f"- {private_ops_path / 'business_audit/ceo_business_score.md'}")
    print(f"- {private_ops_path / 'founder/ceo_action_queue.md'}")
    print(f"- {private_ops_path / 'stage/evidence_report.md'}")
    print("\nPASS: control-tower command completed.")
