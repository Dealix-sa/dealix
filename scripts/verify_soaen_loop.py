#!/usr/bin/env python3
"""Verify SOAEN loop hygiene."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.soaen_loop import analyze_soaen_loop  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict-board", action="store_true")
    args = p.parse_args()

    payload = analyze_soaen_loop()
    verdict = payload["verdict"]
    if args.strict_board and payload.get("weekly_board", {}).get("gaps"):
        verdict = "ACTION_REQUIRED"

    print(f"SOAEN_LOOP_VERDICT={verdict}")
    for b in payload.get("blockers_ar") or []:
        print(f"  BLOCKER: {b}")
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
