#!/usr/bin/env python3
"""Client proof pack — assemble the 05_proof directory into a single proof pack document.

Usage:
    python scripts/delivery/client_proof.py --client-slug acme
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLIENTS_DIR = REPO_ROOT / "clients"

PROOF_FILES = [
    "before_after.md",
    "weekly_command_report.md",
    "decisions_log.md",
    "actions_completed.md",
    "open_risks.md",
    "client_feedback.md",
    "next_30_days.md",
]


def proof_pack(slug: str) -> Path:
    """Concatenate every 05_proof file into clients/<slug>/proof_pack.md."""
    ws = CLIENTS_DIR / slug
    if not ws.exists():
        raise FileNotFoundError(f"client workspace not found: {ws}")

    proof_dir = ws / "05_proof"
    parts: list[str] = [f"# Proof Pack — {slug}", "", "Doctrine: Map -> Design -> Build -> Operate -> Scale.", ""]
    missing: list[str] = []
    for name in PROOF_FILES:
        f = proof_dir / name
        if not f.exists():
            missing.append(name)
            continue
        parts.append(f"\n---\n\n# {name}\n")
        parts.append(f.read_text(encoding="utf-8").rstrip())
        parts.append("")

    if missing:
        parts.append("")
        parts.append("## Missing proof files")
        for m in missing:
            parts.append(f"- {m}")

    pack_path = ws / "proof_pack.md"
    pack_path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return pack_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble client proof pack.")
    parser.add_argument("--client-slug", required=True)
    args = parser.parse_args()

    try:
        path = proof_pack(args.client_slug)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"proof pack written: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())