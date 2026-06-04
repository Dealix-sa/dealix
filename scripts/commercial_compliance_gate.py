#!/usr/bin/env python3
"""Compliance gate CLI / module. Rejects a draft for banned phrases, missing
opt-out where required, sensitive-sector privacy gaps, multiple CTAs, or
WhatsApp without opt-in. Computes compliance_score / risk / rejection_reason."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import commercial_launch_core as core  # noqa: E402


def evaluate(draft: dict, configs: dict | None = None) -> dict:
    configs = configs or core.load_all_configs()
    passed, score, reasons = core.compliance_gate(draft, configs)
    return {"passed": passed, "score": score, "reasons": reasons}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compliance gate over a day's queue.")
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
    print(f"Compliance gate: {passed}/{total} pass (>= {configs['compliance']['min_compliance_score']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
