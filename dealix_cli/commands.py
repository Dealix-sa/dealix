"""Commands for the Dealix founder CLI.

Each command is a thin, read-only wrapper that points the founder at the
right private files and the right next action. None of these commands
send external messages or take destructive actions.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Sequence


def ensure_private_ops(private_ops: str) -> Path:
    """Return the private ops directory, creating it if missing.

    The private ops directory lives outside this repo by default
    (see ``.gitignore``). When pointed at a fresh location, scaffold
    the directories the playbook expects so daily commands don't error.
    """
    path = Path(private_ops).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    for sub in (
        "icp",
        "acquisition",
        "sales/proposal_notes",
        "pipeline",
        "delivery/samples",
        "clients/_template",
        "experiments",
        "revenue",
    ):
        (path / sub).mkdir(parents=True, exist_ok=True)
    return path


def run_command(cmd: Sequence[str]) -> int:
    """Run a subprocess and stream output. Returns the exit code."""
    result = subprocess.run(list(cmd), check=False)
    return result.returncode


def revenue_ops(private_ops: str) -> None:
    """Print the revenue ops file map and refresh the CEO action queue."""
    private_ops_path = ensure_private_ops(private_ops)
    print("\nDealix Revenue Operations")
    print("=" * 40)
    print("Review these private files:")
    print(f"- {private_ops_path / 'pipeline/pipeline_tracker.csv'}")
    print(f"- {private_ops_path / 'revenue/revenue_action_log.csv'}")
    print(f"- {private_ops_path / 'sales/proposal_tracker.csv'}")
    print(f"- {private_ops_path / 'delivery/sample_quality_log.csv'}")
    print(f"- {private_ops_path / 'pipeline/win_loss_log.md'}")
    run_command([
        sys.executable,
        "scripts/generate_ceo_action_queue.py",
        "--private-ops",
        str(private_ops_path),
    ])
    print("\nRevenue Rule:")
    print(
        "Do the action that moves cash, proof, retention, trust, or learning."
    )
