#!/usr/bin/env python3
"""Create a Command Sprint customer workspace from the canonical template.

Copies the full Command Sprint file set (``customers/_template/``) into a new
``customers/<slug>/`` folder so every account starts with the same governed
structure: intake → company intelligence → diagnostic → sprint scope →
revenue map → proof register → approval register → next-action board →
executive brief → delivery log → proof pack → upsell recommendation.

Usage:
    python scripts/create_customer_workspace.py --name "ACME Trading"
    python scripts/create_customer_workspace.py --name "dry-run-client" --force

Rules:
- Never overwrites an existing customer folder unless ``--force`` is passed.
- Touches only ``customers/<slug>/`` — no unrelated files.
- No external action of any kind; this is local scaffolding only.

Terminal markers (grep-friendly):
    CUSTOMER_WORKSPACE_CREATED
    CUSTOMER_WORKSPACE_FILES=<n>
    CUSTOMER_WORKSPACE_EXISTS
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = REPO / "customers" / "_template"
CUSTOMERS_DIR = REPO / "customers"

# Canonical Command Sprint file set. The dry run and template are validated
# against this exact list.
COMMAND_SPRINT_FILES = (
    "00_intake.md",
    "01_company_intelligence.md",
    "02_diagnostic_summary.md",
    "03_command_sprint_scope.md",
    "04_revenue_map.md",
    "05_proof_register.md",
    "06_approval_register.md",
    "07_next_action_board.md",
    "08_executive_command_brief.md",
    "09_delivery_log.md",
    "10_proof_pack.md",
    "11_upsell_recommendation.md",
)


def slugify(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-") or "customer"


def create_workspace(name: str, force: bool = False) -> tuple[Path, list[str]]:
    """Create the workspace; return (path, list of file names written)."""
    if not TEMPLATE_DIR.is_dir():
        raise FileNotFoundError(f"Template directory missing: {TEMPLATE_DIR}")

    slug = slugify(name)
    target = CUSTOMERS_DIR / slug

    if target.exists() and not force:
        print("CUSTOMER_WORKSPACE_EXISTS")
        raise FileExistsError(
            f"Customer folder already exists: {target} (use --force to overwrite)"
        )

    target.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for fname in COMMAND_SPRINT_FILES:
        src = TEMPLATE_DIR / fname
        if not src.is_file():
            raise FileNotFoundError(f"Template file missing: {src}")
        content = src.read_text(encoding="utf-8").replace("<<COMPANY_NAME>>", name)
        (target / fname).write_text(content, encoding="utf-8")
        written.append(fname)
    return target, written


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    parser = argparse.ArgumentParser(description="Create a Command Sprint customer workspace")
    parser.add_argument("--name", required=True, help="Customer / company name")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing customer folder (default: refuse)",
    )
    args = parser.parse_args(argv)

    try:
        target, written = create_workspace(args.name, force=args.force)
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    rel = target.relative_to(REPO)
    print(f"Created customer workspace: {rel}")
    for fname in written:
        print(f"  + {fname}")
    print("CUSTOMER_WORKSPACE_CREATED")
    print(f"CUSTOMER_WORKSPACE_FILES={len(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
