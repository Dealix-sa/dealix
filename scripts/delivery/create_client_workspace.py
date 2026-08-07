#!/usr/bin/env python3
"""Create a client delivery workspace from the _template directory.

Doctrine: Map -> Design -> Build -> Operate -> Scale.

Usage:
    python scripts/delivery/create_client_workspace.py --client-slug acme --client-name "Acme Co"
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLIENTS_DIR = REPO_ROOT / "clients"
TEMPLATE_DIR = CLIENTS_DIR / "_template"

# Ordered delivery phases and the files each must contain.
# Used by tests and by the build-plan / proof scripts.
PHASES: dict[str, list[str]] = {
    "00_intake": [
        "intake_form.md",
        "stakeholder_map.md",
        "access_checklist.md",
    ],
    "01_diagnosis": [
        "current_state.md",
        "pain_map.md",
        "bottlenecks.md",
        "opportunity_map.md",
        "risk_register.md",
    ],
    "02_solution": [
        "system_blueprint.md",
        "workflow_map.md",
        "data_model.md",
        "ai_policy.md",
        "acceptance_criteria.md",
    ],
    "03_delivery": [
        "sprint_plan.md",
        "test_plan.md",
        "uat_notes.md",
    ],
    "04_training": [
        "user_guide.md",
        "admin_guide.md",
        "sop.md",
    ],
    "05_proof": [
        "before_after.md",
        "weekly_command_report.md",
        "decisions_log.md",
        "actions_completed.md",
        "open_risks.md",
        "client_feedback.md",
        "next_30_days.md",
    ],
}

# Phases that must exist before the workspace is considered "created".
REQUIRED_PHASES = list(PHASES.keys())


def expected_files() -> list[Path]:
    """Return every expected template file path relative to the template dir."""
    files: list[Path] = []
    for phase, names in PHASES.items():
        for name in names:
            files.append(Path(phase) / name)
    return files


def template_complete() -> bool:
    """True if the _template directory contains every expected file."""
    for rel in expected_files():
        if not (TEMPLATE_DIR / rel).exists():
            return False
    return True


def create_workspace(client_slug: str, client_name: str | None = None, overwrite: bool = False) -> Path:
    """Create clients/<client_slug>/ by copying the phase subdirectories from _template.

    Only the numbered phase subdirectories are copied (00_intake .. 05_proof).
    The legacy flat files in _TEMPLATE are intentionally left untouched.
    """
    if not template_complete():
        raise RuntimeError(
            "clients/_template is incomplete — missing one or more phase files. "
            "Run the delivery setup before creating client workspaces."
        )

    target = CLIENTS_DIR / client_slug
    if target.exists() and not overwrite:
        raise FileExistsError(
            f"Client workspace already exists: {target}. Pass --overwrite to replace."
        )
    if target.exists():
        shutil.rmtree(target)

    target.mkdir(parents=True, exist_ok=True)

    for phase in REQUIRED_PHASES:
        src = TEMPLATE_DIR / phase
        dst = target / phase
        if src.exists():
            shutil.copytree(src, dst)
        else:
            # Defensive: create empty dir so downstream scripts do not crash.
            dst.mkdir(parents=True, exist_ok=True)

    # Write a small manifest so scripts can detect a Dealix-created workspace.
    manifest_lines = [
        f"# {client_name or client_slug}",
        "",
        "Client delivery workspace. Doctrine: Map -> Design -> Build -> Operate -> Scale.",
        "",
        "Created by: scripts/delivery/create_client_workspace.py",
        f"Slug: {client_slug}",
    ]
    (target / "README.md").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a client delivery workspace.")
    parser.add_argument("--client-slug", required=True, help="Folder slug under clients/")
    parser.add_argument("--client-name", default=None, help="Human-readable client name")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing workspace")
    args = parser.parse_args()

    try:
        path = create_workspace(args.client_slug, args.client_name, args.overwrite)
    except (FileExistsError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"created client workspace: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
