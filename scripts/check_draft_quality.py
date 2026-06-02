#!/usr/bin/env python3
"""Draft Quality Gate — block any draft that violates doctrine before review.

Reuses ``governance_os`` (policy + claim safety) via the Distribution OS quality
gate. Writes ``reports/distribution/DRAFT_QUALITY_GATE.md`` and exits non-zero
if any violation is found, so CI / ``make draft-quality`` fails loud.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.distribution_os import check_drafts  # noqa: E402
from auto_client_acquisition.distribution_os.models import Draft  # noqa: E402
from auto_client_acquisition.distribution_os.report import render_quality_gate  # noqa: E402
from auto_client_acquisition.distribution_os.store import (  # noqa: E402
    drafts_path,
    read_jsonl,
    reports_dir,
    write_text,
)


def main() -> int:
    rows = read_jsonl(drafts_path())
    drafts = [Draft.from_dict(r) for r in rows]
    result = check_drafts(drafts)

    report = write_text(reports_dir() / "DRAFT_QUALITY_GATE.md", render_quality_gate(result))
    print(f"checked: {result.checked} | violations: {len(result.violations)}")
    print(f"wrote: {report.relative_to(ROOT)}")

    if not result.ok:
        for v in result.violations:
            print(f"  - {v.draft_id}: {v.code} — {v.detail}")
        print("DEALIX_DRAFT_QUALITY_GATE=FAIL")
        return 1
    print("DEALIX_DRAFT_QUALITY_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
