#!/usr/bin/env python3
"""Re-score an existing day's draft_queue.jsonl (quality + compliance) and print
a summary. Review-only; sends nothing."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import commercial_launch_core as core  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Re-score a day's drafts.")
    parser.add_argument("--date", default=None)
    args = parser.parse_args(argv)
    date_str = args.date or core.today_str()
    configs = core.load_all_configs()
    path = core.output_dir_for(date_str) / "draft_queue.jsonl"
    if not path.exists():
        print("No draft_queue.jsonl found.", file=sys.stderr)
        return 1
    q_total = c_total = n = 0
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            _, q, _ = core.quality_gate(d, configs)
            _, c, _ = core.compliance_gate(d, configs)
            q_total += q
            c_total += c
            n += 1
    if n:
        print(f"Scored {n} drafts. avg_quality={q_total / n:.1f} avg_compliance={c_total / n:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
