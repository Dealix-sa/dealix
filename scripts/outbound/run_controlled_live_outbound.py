#!/usr/bin/env python3
"""Run the controlled live outbound engine.

Examples:
    DRY_RUN=true python scripts/outbound/run_controlled_live_outbound.py
    APPROVED_BY=sami python scripts/outbound/run_controlled_live_outbound.py
    CHANNEL=email LIMIT=10 python scripts/outbound/run_controlled_live_outbound.py
"""

from __future__ import annotations

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

from app.outbound.config import OutboundSettings  # noqa: E402
from app.outbound.models import Channel  # noqa: E402
from app.outbound.runner import ControlledOutboundRunner  # noqa: E402


def main() -> int:
    settings = OutboundSettings()
    dry_run = os.getenv("DRY_RUN", "false").lower() in ("1", "true", "yes")
    approved_by = os.getenv("APPROVED_BY") or ("system" if not settings.outbound_require_approval else None)
    channel_str = os.getenv("CHANNEL", "")
    channel = Channel(channel_str) if channel_str else None
    limit = int(os.getenv("LIMIT", "1000"))

    runner = ControlledOutboundRunner(settings=settings)

    print("=== Dealix Controlled Live Outbound Runner ===")
    print(f"Mode: {'DRY-RUN' if dry_run else 'LIVE'}")
    print(f"Outbound mode: {settings.outbound_mode}")
    print(f"Channel: {channel or 'all'}")
    print(f"Approved by: {approved_by or 'REQUIRED'}")
    print()

    if not dry_run and settings.outbound_require_approval and not approved_by:
        print("❌ Live send requires APPROVED_BY=<operator>")
        return 1

    result = runner.run_drafts(channel=channel, dry_run=dry_run, approved_by=approved_by, limit=limit)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
