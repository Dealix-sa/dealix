#!/usr/bin/env python3
"""Generate per-sector outreach DRAFTS (Revenue Execution OS) — never sends.

Reads founder-sourced prospects, builds one AR draft per prospect (de-duped),
appends them to data/drafts/drafts.jsonl as ``draft_pending_approval``.

Usage:
    python scripts/generate_distribution_drafts.py
    python scripts/generate_distribution_drafts.py --prospects path/to/prospects.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from dealix.distribution import drafts  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description="Generate distribution drafts (draft-only).")
    p.add_argument(
        "--prospects", type=Path, default=None, help="Prospects JSON (default: example)."
    )
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    summary = drafts.run_generation(args.prospects)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print("DISTRIBUTION_DRAFTS:")
        print(f"  prospects        : {summary['prospects']}")
        print(f"  existing drafts  : {summary['existing_drafts']}")
        print(f"  new drafts       : {summary['new_drafts']}")
        print(f"  policy           : {summary['policy']}")
        for did in summary["ids"]:
            print(f"    - {did}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"DISTRIBUTION_DRAFTS: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
