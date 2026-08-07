#!/usr/bin/env python3
"""Dealix guarded action webhook executor.

Posts ready guarded actions to a server-side webhook when explicitly enabled.
This file is intentionally adapter-only: the receiving server owns the actual
channel provider integration and audit log.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ACTIONS_DIR = ROOT / "business" / "autonomy"
REPORT_DIR = ROOT / "reports" / "autonomy"
ENABLED = os.getenv("DEALIX_GUARDED_WEBHOOK_EXECUTOR_ENABLED", "false").lower() == "true"
WEBHOOK_URL = os.getenv("DEALIX_AUTONOMY_WEBHOOK_URL", "")
TOKEN = os.getenv("DEALIX_AUTONOMY_WEBHOOK_TOKEN", "")
DAILY_LIMIT = int(os.getenv("DEALIX_AUTONOMY_WEBHOOK_DAILY_LIMIT", "20"))


def latest_actions() -> Path | None:
    if not ACTIONS_DIR.exists():
        return None
    files = sorted(ACTIONS_DIR.glob("guarded-negotiation-actions-*.json"), reverse=True)
    return files[0] if files else None


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def post_action(action: dict[str, Any]) -> dict[str, Any]:
    if not ENABLED:
        return {"status": "skipped", "reason": "executor_disabled"}
    if not WEBHOOK_URL:
        return {"status": "skipped", "reason": "missing_webhook_url"}
    payload = json.dumps(action, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = urllib.request.Request(WEBHOOK_URL, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read(4000).decode("utf-8", errors="replace")
            return {"status": "sent_to_webhook", "code": response.status, "body_tail": body[-1000:]}
    except urllib.error.HTTPError as exc:
        return {"status": "webhook_http_error", "code": exc.code, "body_tail": exc.read(1000).decode("utf-8", errors="replace")}
    except Exception as exc:
        return {"status": "webhook_error", "error": str(exc)}


def main() -> int:
    path = latest_actions()
    if not path:
        print(f"missing guarded actions under {ACTIONS_DIR}")
        return 1
    payload = read_json(path)
    actions = payload.get("actions", [])
    ready = [item for item in actions if item.get("status") == "ready_for_guarded_execution"][:DAILY_LIMIT]
    results = []
    for action in ready:
        results.append({"action": action, "result": post_action(action)})
    today = dt.date.today().isoformat()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / f"guarded-webhook-executor-{today}.json"
    out.write_text(json.dumps({"date": today, "enabled": ENABLED, "count": len(results), "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"guarded webhook executor wrote {out}; count={len(results)} enabled={ENABLED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
