#!/usr/bin/env python3
"""Print founder executive snapshot (Railway + GTM + first-paid + env)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_executive import build_founder_executive_snapshot  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default=os.getenv("DEALIX_API_BASE", "https://api.dealix.me"))
    p.add_argument("--skip-live", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    blob = build_founder_executive_snapshot(
        api_base=args.api_base,
        skip_live=args.skip_live,
    )

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("== founder_executive_snapshot ==")
        r = blob["railway"]
        print(f"  railway_verdict: {r['verdict']}")
        if r.get("deploy_note_ar"):
            print(f"  NOTE: {r['deploy_note_ar']}")
        for key in ("live_healthz", "live_version", "live_meta"):
            live = r.get(key) or {}
            if live.get("probed"):
                print(f"  {key}: {live.get('status')}")
        print(f"  first_paid: {blob['first_paid']['verdict']}")
        print(f"  gtm_surfaces: {'ok' if blob['gtm_surfaces']['ok'] else 'issues'}")
        print(f"  blockers: {len(blob['blockers'])}")
        for b in blob["blockers"][:12]:
            print(f"    - {b}")

    print(f"FOUNDER_EXECUTIVE_VERDICT={blob['verdict']}")
    return 0 if blob["verdict"] == "CLEAR" else 0


if __name__ == "__main__":
    raise SystemExit(main())
