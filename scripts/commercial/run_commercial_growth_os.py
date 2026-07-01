#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.commercial.growth_os_v2 import run_growth_os


def main() -> int:
    snapshot = run_growth_os()
    summary = snapshot["summary"]
    print("COMMERCIAL_GROWTH_OS_READY=1")
    print(f"ACCOUNTS={summary['accounts']}")
    print(f"CARDS={summary['cards']}")
    print(f"REPLIES={summary['replies']}")
    print(f"BOOKING_OPTIONS={summary['booking_options']}")
    print(f"PROPOSALS={summary['proposal_briefs']}")
    print(f"FOLLOWUPS={summary['followup_tasks']}")
    print(f"DECISIONS_REQUIRED={len(snapshot['decision_queue'])}")
    print("REPORT_JSON=reports/commercial/growth_os/latest.json")
    print("REPORT_MD=reports/commercial/growth_os/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
