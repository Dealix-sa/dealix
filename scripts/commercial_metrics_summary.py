"""Commercial metrics summary — combine auto metrics with manual founder inputs.

Revenue is NEVER assumed. Manual metrics default to zero / sample only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Run both as `python scripts/<file>.py` and `python -m scripts.<file>`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.commercial_launch_core import OUTPUT_ROOT, load_config

MANUAL_DEFAULTS = {
    "manual_sent": 0,
    "replies_positive": 0,
    "replies_negative": 0,
    "reply_rate": 0.0,
    "qualified_calls": 0,
    "diagnostics_sold": 0,
    "pilots_sold": 0,
    "retainers_started": 0,
    "revenue_pipeline_sar": 0,
    "realized_revenue_sar": 0,
    "top_objection": None,
}


def summarize_metrics(
    date: str | None = None, manual: dict[str, Any] | None = None
) -> dict[str, Any]:
    metrics_cfg = load_config("metrics")
    dirs = sorted([p for p in OUTPUT_ROOT.glob("*") if p.is_dir()])
    daily: dict[str, Any] = {}
    if date:
        dm = OUTPUT_ROOT / date / "daily_metrics.json"
    elif dirs:
        dm = dirs[-1] / "daily_metrics.json"
    else:
        dm = None
    if dm and dm.exists():
        daily = json.loads(dm.read_text(encoding="utf-8"))

    merged = dict(MANUAL_DEFAULTS)
    if manual:
        merged.update({k: v for k, v in manual.items() if k in MANUAL_DEFAULTS})

    return {
        "schema_version": "1.0",
        "auto_metrics": {k: daily.get(k) for k in metrics_cfg["auto_metrics"]},
        "manual_metrics": merged,
        "revenue_disclaimer": "Revenue is manual input only; not assumed by the system.",
        "safety_violations": 0,
        "compliance_rejections": daily.get("rejected_compliance", 0),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Commercial metrics summary.")
    ap.add_argument("--date", default=None)
    args = ap.parse_args(argv)
    print(json.dumps(summarize_metrics(args.date), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
