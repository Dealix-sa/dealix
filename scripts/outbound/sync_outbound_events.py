#!/usr/bin/env python3
"""Sync outbound events from provider webhooks / CSV into command-room reports."""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from app.outbound.storage import CSVOutboundStorage


def build_summary(storage: CSVOutboundStorage) -> dict:
    messages = storage.list_messages(limit=10000)
    total = len(messages)
    sent = sum(1 for m in messages if m.status == "sent")
    failed = sum(1 for m in messages if m.status == "failed")
    replied = sum(1 for m in messages if m.status == "replied")
    drafts = sum(1 for m in messages if m.status == "draft")
    queued = sum(1 for m in messages if m.status == "queued")
    email_count = sum(1 for m in messages if m.channel == "email")
    wa_count = sum(1 for m in messages if m.channel == "whatsapp")
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "total_messages": total,
        "by_status": {
            "draft": drafts,
            "queued": queued,
            "sent": sent,
            "failed": failed,
            "replied": replied,
        },
        "by_channel": {"email": email_count, "whatsapp": wa_count},
    }


def main() -> int:
    storage = CSVOutboundStorage()
    summary = build_summary(storage)

    reports_dir = Path("reports/command_room")
    reports_dir.mkdir(parents=True, exist_ok=True)

    out_path = reports_dir / "outbound_events.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)

    print(f"✅ Synced outbound events to {out_path}")
    print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
