#!/usr/bin/env python3
"""Create a Command Sprint customer workspace from customers/_template.

Usage:
    python scripts/create_customer_workspace.py --name "test-command-sprint-client"

Copies every file in customers/_template/ into customers/<slug>/, substituting
{{CLIENT_NAME}} and {{DATE}} placeholders. Idempotent-safe: refuses to
overwrite an existing workspace unless --force is given. Pure stdlib.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "customers" / "_template"

EXPECTED = [
    "00_intake.md", "01_company_intelligence.md", "02_diagnostic_summary.md",
    "03_command_sprint_scope.md", "04_revenue_map.md", "05_proof_register.md",
    "06_approval_register.md", "07_next_action_board.md",
    "08_executive_command_brief.md", "09_delivery_log.md",
    "10_proof_pack.md", "11_upsell_recommendation.md",
]


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    return s or "client"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--name", required=True, help="Customer / company name")
    ap.add_argument("--slug", help="Override the folder slug")
    ap.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = ap.parse_args()

    if not TEMPLATE.is_dir():
        print(f"ERROR: template not found at {TEMPLATE}", file=sys.stderr)
        return 1

    missing = [f for f in EXPECTED if not (TEMPLATE / f).is_file()]
    if missing:
        print("ERROR: template is incomplete, missing: " + ", ".join(missing), file=sys.stderr)
        return 1

    slug = args.slug or slugify(args.name)
    dest = ROOT / "customers" / slug
    if dest.exists() and not args.force:
        print(f"ERROR: {dest} already exists (use --force to overwrite)", file=sys.stderr)
        return 1
    dest.mkdir(parents=True, exist_ok=True)

    today = _dt.date.today().isoformat()
    created = []
    for src in sorted(TEMPLATE.iterdir()):
        if not src.is_file():
            continue
        text = src.read_text(encoding="utf-8")
        text = text.replace("{{CLIENT_NAME}}", args.name).replace("{{DATE}}", today)
        (dest / src.name).write_text(text, encoding="utf-8")
        created.append(src.name)

    print(f"Created workspace: {dest.relative_to(ROOT)}")
    for name in created:
        print(f"  + {name}")
    print(f"\n{len(created)} files created for '{args.name}'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
