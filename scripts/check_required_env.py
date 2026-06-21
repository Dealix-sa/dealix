#!/usr/bin/env python3
"""Check required environment variables for a given mode.

Modes:
- demo: zero required env vars (operates fully on local demo data).
- production: full env required.

Exit codes: 0 if all required are set or mode=demo, 1 otherwise.
Output: a deterministic report; never prints variable values.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_BY_MODE = {
    "demo": [],
    "production": [
        "DATABASE_URL",
        "JWT_SECRET_KEY",
        "DEALIX_ADMIN_PASSWORD",
        "DEALIX_ADMIN_TOKEN",
    ],
}

OPTIONAL = [
    "OPENAI_API_KEY",
    "MINIMAX_API_KEY",
    "KIMI_API_KEY",
    "DEEPSEEK_API_KEY",
    "OPENROUTER_API_KEY",
    "MOYASAR_SECRET_KEY",
    "STRIPE_SECRET_KEY",
    "AI_PROVIDER_DEFAULT",
    "AI_MODE_DEMO",
    "NEXT_PUBLIC_DEMO_MODE",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=list(REQUIRED_BY_MODE), default="demo")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    required = REQUIRED_BY_MODE[args.mode]
    missing = [k for k in required if not os.environ.get(k)]
    present_optional = [k for k in OPTIONAL if os.environ.get(k)]

    payload = {
        "mode": args.mode,
        "required": required,
        "missing": missing,
        "optional_present": present_optional,
        "ok": not missing,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Mode: {args.mode}")
        if not required:
            print("Required: (none — demo mode operates on local demo data)")
        else:
            print(f"Required: {len(required)}")
            for k in required:
                state = "OK" if os.environ.get(k) else "MISSING"
                print(f"  - {k}: {state}")
        print(f"Optional present: {len(present_optional)}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
