#!/usr/bin/env python3
"""Run the safety & compliance audit over the latest draft queue.

Writes safety_audit.json into the latest run directory and prints PASS/FAIL.
Exit 0 on PASS, 1 on FAIL.

Usage:
    python scripts/commercial_safety_audit.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from launch_os import paths  # noqa: E402
from launch_os.safety import audit_queue  # noqa: E402


def main() -> int:
    run_dir = paths.latest_dir()
    queue = run_dir / "draft_queue.jsonl"
    if not queue.exists():
        print(f"[safety] FAIL: no draft queue at {paths.rel(queue)} — run the generator first")
        return 1

    result = audit_queue(queue)
    out = run_dir / "safety_audit.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    # Mirror to latest if run_dir is a timestamped dir.
    if run_dir != paths.COMMERCIAL_LATEST:
        paths.COMMERCIAL_LATEST.mkdir(parents=True, exist_ok=True)
        (paths.COMMERCIAL_LATEST / "safety_audit.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    print(f"[safety] drafts audited: {result['total_drafts']}")
    for k, v in result["checks"].items():
        print(f"[safety]   {'PASS' if v else 'FAIL'}  {k}")
    print(f"[safety] wrote {paths.rel(out)}")
    print("[safety] PASS" if result["pass"] else "[safety] FAIL")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
