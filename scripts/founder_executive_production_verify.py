#!/usr/bin/env python3
"""CEO/founder production verify — railway config + live healthz + version + GTM snapshot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.executive_production_snapshot import (  # noqa: E402
    build_executive_production_snapshot,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default="https://api.dealix.me")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    snap = build_executive_production_snapshot(api_base=args.api_base)
    print(f"FOUNDER_EXECUTIVE_PRODUCTION_VERDICT={snap['verdict']}")
    live = snap.get("live") or {}
    hz = live.get("healthz") or {}
    ver = live.get("version") or {}
    if hz.get("probed"):
        print(f"  /healthz -> {hz.get('status')} {hz.get('snippet', '')[:80]}")
    if ver.get("probed"):
        print(f"  /version -> {ver.get('status')} {ver.get('snippet', '')[:80]}")
    for b in snap.get("blockers_ar") or []:
        print(f"  BLOCKER: {b}")
    if args.json:
        print(json.dumps(snap, ensure_ascii=False, indent=2))
    return 0 if snap["verdict"] in ("PASS", "PARTIAL", "WARN") else 1


if __name__ == "__main__":
    raise SystemExit(main())
