#!/usr/bin/env python3
"""Distribution Metrics — write the daily + weekly KPI snapshot report.

Read-only. Aggregates the distribution_os JSONL stores into
reports/distribution/DISTRIBUTION_METRICS.md (numbers are never invented).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.distribution_os import metrics  # noqa: E402

_REPORT = ROOT / "reports" / "distribution" / "DISTRIBUTION_METRICS.md"


def _render(snapshot: dict) -> str:
    daily = snapshot["daily"]
    weekly = snapshot["weekly"]
    today = datetime.now(UTC).date().isoformat()
    lines = [
        "# Distribution Metrics — مقاييس التوزيع",
        "",
        f"التاريخ / Date: {today}",
        "",
        "## يومي / Daily",
    ]
    lines += [f"- {k}: {v}" for k, v in daily.items()]
    lines += ["", "## أسبوعي / Weekly"]
    lines += [f"- {k}: {v}" for k, v in weekly.items()]
    lines += [
        "",
        "> القراءة لا تُنشر خارجياً. الأرقام من السجلات فقط ولا تُخترع.",
        "> Read-only. Numbers come only from the ledgers; never invented.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    snapshot = metrics.snapshot()
    if args.json:
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
        return 0

    _REPORT.parent.mkdir(parents=True, exist_ok=True)
    _REPORT.write_text(_render(snapshot), encoding="utf-8")
    print(f"Wrote {_REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
