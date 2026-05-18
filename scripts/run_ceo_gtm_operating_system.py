#!/usr/bin/env python3
"""CEO GTM operating system CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.ceo_gtm_operating_system import (  # noqa: E402
    run_mode,
    verdict_from_payload,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "mode",
        choices=("status", "railway", "daily", "weekly", "gates", "agents"),
        nargs="?",
        default="status",
    )
    p.add_argument("--json", action="store_true")
    p.add_argument("--skip-live", action="store_true")
    p.add_argument("--api-base", default="https://api.dealix.me")
    p.add_argument("--ui-start-command", default="")
    p.add_argument("--ui-predeploy", default="")
    args = p.parse_args()

    blob = run_mode(
        args.mode,
        api_base=args.api_base,
        ui_start=args.ui_start_command,
        ui_predeploy=args.ui_predeploy,
        skip_live_railway=args.skip_live,
    )
    verdict = verdict_from_payload(blob)
    print(f"CEO_GTM_OS_VERDICT={verdict}")
    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        blockers = blob.get("blockers") or blob.get("status", {}).get("blockers") or []
        for b in blockers[:15]:
            print(f"  BLOCKER: {b}")
        ui = blob.get("railway_ui") or blob.get("status", {}).get("railway_ui")
        if ui:
            print(f"  RAILWAY_UI: {ui.get('founder_railway_ui_action')}")
    return 0 if verdict in ("PASS", "OK", "WARN") else 1


if __name__ == "__main__":
    raise SystemExit(main())
