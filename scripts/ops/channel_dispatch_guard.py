#!/usr/bin/env python3
"""Dealix channel dispatch guard.

Builds a guarded dispatch manifest from the daily commercial draft pack.
It only marks an item as dispatchable when a local contact registry explicitly
allows that account and channel. Without a local registry, everything remains
blocked and review-only.
"""

from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PACK_DIR = ROOT / "business" / "commercial" / "daily_channels"
REPORT_DIR = ROOT / "reports" / "commercial"
REGISTRY_PATH = ROOT / "data" / "outbound" / "consent_registry.json"

ALLOWED = {"opt_in", "customer", "existing_relationship", "inbound_request", "manual_allowlist"}
BLOCKED = {"unknown", "unsubscribed", "complained", "suppressed", "do_not_contact"}
DAILY_TOTAL_LIMIT = int(os.getenv("DEALIX_AUTONOMOUS_DAILY_TOTAL_LIMIT", "20"))
DAILY_PER_CHANNEL_LIMIT = int(os.getenv("DEALIX_AUTONOMOUS_DAILY_PER_CHANNEL_LIMIT", "5"))
LIVE_ENABLED = os.getenv("DEALIX_AUTONOMOUS_DISPATCH_ENABLED", "false").lower() == "true"


def read_json(path: Path) -> Any:
    if not path.exists():
        return {} if path == REGISTRY_PATH else []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {} if path == REGISTRY_PATH else []


def latest_pack() -> Path | None:
    if not PACK_DIR.exists():
        return None
    files = sorted(PACK_DIR.glob("commercial-draft-pack-*.json"), reverse=True)
    return files[0] if files else None


def load_registry() -> dict[str, Any]:
    registry = read_json(REGISTRY_PATH)
    contacts = registry.get("contacts", []) if isinstance(registry, dict) else []
    suppression = registry.get("suppression", []) if isinstance(registry, dict) else []
    by_account = {str(item.get("account_id")): item for item in contacts if isinstance(item, dict)}
    suppressed = {str(item.get("account_id")) for item in suppression if isinstance(item, dict)}
    return {"contacts": by_account, "suppressed": suppressed}


def evaluate(draft: dict[str, Any], registry: dict[str, Any], counts: dict[str, int]) -> dict[str, Any]:
    account_id = str(draft.get("account_id") or draft.get("company") or "")
    channel = str(draft.get("channel") or "")
    contact = registry["contacts"].get(account_id)
    reasons: list[str] = []

    if account_id in registry["suppressed"]:
        reasons.append("suppressed")
    if not contact:
        reasons.append("missing_local_contact_registry_record")
    else:
        status = str(contact.get("consent_status", "unknown"))
        if status in BLOCKED or status not in ALLOWED:
            reasons.append(f"consent_status_not_allowed:{status}")
        channels = contact.get("channels", {}) if isinstance(contact.get("channels"), dict) else {}
        if not channels.get(channel):
            reasons.append(f"missing_channel_address:{channel}")

    if counts.get("total", 0) >= DAILY_TOTAL_LIMIT:
        reasons.append("daily_total_limit_reached")
    if counts.get(channel, 0) >= DAILY_PER_CHANNEL_LIMIT:
        reasons.append(f"daily_channel_limit_reached:{channel}")

    ready = not reasons and LIVE_ENABLED
    status = "ready_for_autonomous_dispatch" if ready else "blocked_or_manifest_only"
    if ready:
        counts["total"] = counts.get("total", 0) + 1
        counts[channel] = counts.get(channel, 0) + 1

    return {
        "date": dt.date.today().isoformat(),
        "account_id": account_id,
        "company": draft.get("company"),
        "channel": channel,
        "language": draft.get("language"),
        "status": status,
        "reasons": reasons,
        "subject": draft.get("subject"),
        "body": draft.get("body"),
        "live_enabled": LIVE_ENABLED,
    }


def main() -> int:
    pack = latest_pack()
    if not pack:
        print(f"missing daily commercial pack under {PACK_DIR}")
        return 1
    drafts = read_json(pack)
    registry = load_registry()
    counts: dict[str, int] = {"total": 0}
    manifest = [evaluate(draft, registry, counts) for draft in drafts if isinstance(draft, dict)]

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    out = REPORT_DIR / f"channel-dispatch-manifest-{today}.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    ready = sum(1 for item in manifest if item["status"] == "ready_for_autonomous_dispatch")
    print(f"built dispatch manifest: {out}")
    print(f"ready={ready} total={len(manifest)} live_enabled={LIVE_ENABLED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
