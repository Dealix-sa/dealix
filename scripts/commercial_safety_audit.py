#!/usr/bin/env python3
"""Run the Commercial Launch safety audit.

Fails (non-zero) if any active external-send / automation / scraping code is
found in the commercial-launch source, or if any generated draft violates the
review-only invariants (send_allowed must be False, etc.).

Usage:
    python scripts/commercial_safety_audit.py
    python scripts/commercial_safety_audit.py --date 2026-06-04
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_launch.safety import (  # noqa: E402
    audit_outputs_dir,
    scan_files,
    write_safety_audit,
)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Commercial Launch safety audit")
    ap.add_argument("--date", type=str, default=None, help="Audit a specific day's draft queue")
    ap.add_argument("--scan-only", action="store_true", help="Static code scan only")
    args = ap.parse_args(argv)

    if args.scan_only:
        report = scan_files(ROOT)
    else:
        run_date = args.date or date.today().isoformat()
        report = audit_outputs_dir(run_date)
        write_safety_audit(report, run_date)

    print(f"[safety] scanned_files={report.scanned_files}")
    print(f"[safety] drafts_checked={report.drafts_checked}")
    print(f"[safety] findings={len(report.findings)} draft_violations={len(report.draft_violations)}")
    for f in report.findings:
        print(f"[safety][FINDING] {f.file}:{f.line} {f.rule} :: {f.snippet}")
    for v in report.draft_violations[:20]:
        print(f"[safety][VIOLATION] {v['draft_id']}: {v['problems']}")

    if not report.passed:
        print("[safety][FAIL] safety audit FAILED", file=sys.stderr)
        return 1
    print("[safety][OK] no external send, all drafts review-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
