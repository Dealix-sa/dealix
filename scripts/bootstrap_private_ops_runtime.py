#!/usr/bin/env python3
"""Bootstrap the /opt/dealix-ops-private/ runtime tree.

Safety:
  * NEVER writes inside the repo.
  * NEVER prints secrets.
  * Refuses to overwrite existing files (idempotent create-only).
  * Uses --dry-run by default; pass --apply to actually create the tree.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

DEFAULT_ROOT = Path("/opt/dealix-ops-private")


SKELETON = {
    "README.md": (
        "# Dealix Private Ops Runtime\n\n"
        "Founder-only. Never commit. Created by "
        "scripts/bootstrap_private_ops_runtime.py.\n\n"
        "Layout documented in docs/runtime/PRIVATE_OPS_LAYOUT.md.\n"
    ),
    "warm_list/warm_list.csv": (
        "company,contact_name,email,phone,sector,city,owner,source_ref,notes\n"
    ),
    "value_ledger/events.jsonl": "",
    "approvals/pending/.keep": "",
    "approvals/decided/.keep": "",
    "audit_log/.keep": "",
    "proof_packs/.keep": "",
    "secrets/.keep": "",
    "backups/.keep": "",
}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=str(DEFAULT_ROOT),
                   help="Runtime root path (default /opt/dealix-ops-private).")
    p.add_argument("--apply", action="store_true",
                   help="Actually create files (default dry-run).")
    p.add_argument("--check", action="store_true",
                   help="Verifier mode: print OK and exit 0 if script importable.")
    args = p.parse_args()

    if args.check:
        print("bootstrap_private_ops_runtime: OK")
        return 0

    root = Path(args.root)
    # Defensive: never bootstrap inside this repo.
    repo_root = Path(__file__).resolve().parents[1]
    try:
        root.resolve().relative_to(repo_root.resolve())
        print("REFUSED: runtime root must not live inside the repo.")
        return 2
    except ValueError:
        pass  # good — outside repo

    action = "WOULD CREATE" if not args.apply else "CREATED"
    for rel, body in SKELETON.items():
        full = root / rel
        if full.exists():
            print(f"SKIP (exists): {full}")
            continue
        if args.apply:
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text(body, encoding="utf-8")
            try:
                os.chmod(full.parent, 0o750)
                os.chmod(full, 0o640)
            except PermissionError:
                pass
        print(f"{action}: {full}")
    if not args.apply:
        print("Re-run with --apply on the runtime host to create the tree.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
