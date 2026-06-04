#!/usr/bin/env python3
"""Compute commercial launch readiness + daily metrics over the latest run.

Writes daily_metrics.json and readiness.json into the latest run directory.
Exit 0 if ready, 1 otherwise.

Usage:
    python scripts/commercial_launch_readiness.py [--target 400]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from launch_os import paths  # noqa: E402
from launch_os.readiness import readiness_report  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=400)
    args = ap.parse_args(argv)

    run_dir = paths.latest_dir()
    queue = run_dir / "draft_queue.jsonl"
    if not queue.exists():
        print(f"[readiness] FAIL: no draft queue at {paths.rel(queue)}")
        return 1

    report = readiness_report(queue, target=args.target)

    metrics_path = run_dir / "daily_metrics.json"
    metrics_path.write_text(json.dumps(report["metrics"], ensure_ascii=False, indent=2), encoding="utf-8")
    readiness_path = run_dir / "readiness.json"
    readiness_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if run_dir != paths.COMMERCIAL_LATEST:
        paths.COMMERCIAL_LATEST.mkdir(parents=True, exist_ok=True)
        (paths.COMMERCIAL_LATEST / "daily_metrics.json").write_text(
            json.dumps(report["metrics"], ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (paths.COMMERCIAL_LATEST / "readiness.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    print(f"[readiness] score: {report['score']}/100  ready={report['ready']}")
    for k, v in report["checks"].items():
        print(f"[readiness]   {'PASS' if v else 'FAIL'}  {k}")
    print(f"[readiness] wrote {paths.rel(metrics_path)}")
    return 0 if report["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
