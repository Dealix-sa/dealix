#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.commercial.growth_os_v2 import run_growth_os, verify_snapshot


def main() -> int:
    path = Path("reports/commercial/growth_os/latest.json")
    snapshot = json.loads(path.read_text(encoding="utf-8")) if path.exists() else run_growth_os()
    failures = verify_snapshot(snapshot)
    if failures:
        print("COMMERCIAL_GROWTH_OS_VERIFY=FAIL")
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("COMMERCIAL_GROWTH_OS_VERIFY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
