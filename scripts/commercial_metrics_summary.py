#!/usr/bin/env python3
"""Commercial metrics summary.

Combines today's draft metrics with manual-input metrics (defaults to sample
zeros). Revenue and reply numbers are NEVER assumed by the system.
"""

from __future__ import annotations

import json
from pathlib import Path

import commercial_launch_lib as lib


def main(argv: list[str] | None = None) -> int:
    metrics_cfg = lib.load_config("commercial_metrics.json")
    out = lib.output_dir()
    daily_path = out / "daily_metrics.json"
    if daily_path.exists():
        daily = json.loads(daily_path.read_text(encoding="utf-8"))
    else:
        drafts = lib.generate_drafts(target=400)
        daily = {k: v for k, v in lib.summarize(drafts).items() if isinstance(v, int)}

    summary = {m: daily.get(m, 0) for m in metrics_cfg["metrics"]}
    summary["_manual_input_metrics"] = metrics_cfg["manual_input_metrics"]
    summary["_note"] = metrics_cfg["note"]
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
