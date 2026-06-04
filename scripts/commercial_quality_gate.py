#!/usr/bin/env python3
"""Quality gate CLI / module. Scores a draft (or a day's queue) for quality.

A draft fails quality if score < 70 or any structural rule trips (missing
pain/vertical, not exactly one CTA, missing opt-out where required, sensitive
vertical without human-approval language, overlength, generic agency language,
or more than one offer).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import commercial_launch_core as core  # noqa: E402


def evaluate(draft: dict, configs: dict | None = None) -> dict:
    configs = configs or core.load_all_configs()
    passed, score, reasons = core.quality_gate(draft, configs)
    return {"passed": passed, "score": score, "reasons": reasons}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Quality gate over a day's queue.")
    parser.add_argument("--date", default=None)
    args = parser.parse_args(argv)
    date_str = args.date or core.today_str()
    configs = core.load_all_configs()
    path = core.output_dir_for(date_str) / "draft_queue.jsonl"
    if not path.exists():
        print("No draft_queue.jsonl found.", file=sys.stderr)
        return 1
    total = passed = 0
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            total += 1
            if evaluate(json.loads(line), configs)["passed"]:
                passed += 1
    print(f"Quality gate: {passed}/{total} pass (>= {configs['quality']['min_quality_score']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
