#!/usr/bin/env python3
"""Generate 400+ review-only commercial drafts for the founder review queue.

Review-only. Nothing is sent. Every draft carries send_allowed=false,
external_send_blocked=true, no_auto_send=true, requires_founder_approval=true.

Usage:
    python scripts/commercial_generate_400_drafts.py --target 400
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from launch_os import paths  # noqa: E402
from launch_os.drafts import generate_drafts, write_run  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate review-only commercial drafts.")
    ap.add_argument("--target", type=int, default=400, help="Minimum number of drafts.")
    args = ap.parse_args(argv)

    paths.ensure_dirs()
    drafts = generate_drafts(target=args.target)
    summary = write_run(drafts, paths.COMMERCIAL_OUT, paths.COMMERCIAL_LATEST)

    count = summary["count"]
    ok = count >= args.target
    print(f"[drafts] generated {count} drafts (target {args.target})")
    print(f"[drafts] queue: {paths.rel(summary['queue_path'])}")
    print(f"[drafts] latest: {paths.rel(summary['latest_dir'])}")
    print("[drafts] PASS" if ok else "[drafts] FAIL: below target")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
