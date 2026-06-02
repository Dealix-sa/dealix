#!/usr/bin/env python3
"""Draft Queue Review (Revenue Execution OS) — the founder's approval list.

Lists pending drafts and writes reports/distribution/DRAFT_QUEUE_REVIEW.md so the
founder can approve / edit / reject, then copy + send manually. Optional
``--approve`` / ``--reject`` / ``--mark-copied`` transition a single draft.

Usage:
    python scripts/review_draft_queue.py
    python scripts/review_draft_queue.py --approve draft_xxx
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from dealix.distribution import drafts  # noqa: E402
from dealix.distribution.paths import REPORTS_DIR  # noqa: E402
from dealix.distribution.reports import render_queue  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description="Review the draft approval queue.")
    p.add_argument("--approve", metavar="DRAFT_ID")
    p.add_argument("--reject", metavar="DRAFT_ID")
    p.add_argument("--reason", default="")
    p.add_argument("--mark-copied", metavar="DRAFT_ID", dest="mark_copied")
    args = p.parse_args(argv)

    if args.approve:
        rec = drafts.approve_draft(args.approve)
        print(f"APPROVED: {args.approve} -> {rec['status'] if rec else 'NOT FOUND'}")
    if args.reject:
        rec = drafts.reject_draft(args.reject, args.reason)
        print(f"REJECTED: {args.reject} -> {rec['status'] if rec else 'NOT FOUND'}")
    if args.mark_copied:
        rec = drafts.mark_copied(args.mark_copied)
        print(f"COPIED: {args.mark_copied} -> {rec['status'] if rec else 'NOT FOUND'}")

    pending = drafts.pending_drafts()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "DRAFT_QUEUE_REVIEW.md").write_text(render_queue(pending), encoding="utf-8")

    print(f"DRAFT_QUEUE: {len(pending)} pending (awaiting approval)")
    for d in pending:
        print(f"  - {d['id']} | {d['company']} | {d['sector']} | {d['channel']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"DRAFT_QUEUE: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
