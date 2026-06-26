#!/usr/bin/env python3
"""Dealix Agentic Commercial OS control-plane runner.

This script does not send externally. It reads the operating registry,
normalizes the current commercial loop contract, and writes review-ready
reports that a founder can inspect before touching any external channel.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "data" / "commercial" / "agentic_commercial_os_registry.json"
REPORT_DIR = ROOT / "reports" / "agentic_commercial_os"
LATEST_JSON = REPORT_DIR / "latest.json"
LATEST_MD = REPORT_DIR / "latest.md"

SAFE_DEFAULTS = {
    "EXTERNAL_SEND_ENABLED": "false",
    "EMAIL_SEND_ENABLED": "false",
    "WHATSAPP_SEND_ENABLED": "false",
    "WHATSAPP_ALLOW_LIVE_SEND": "false",
    "SMS_SEND_ENABLED": "false",
    "OUTBOUND_MODE": "draft_only",
}


def _env_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _load_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Missing registry: {REGISTRY_PATH}")
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _safety_status() -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []

    external = _env_truthy("EXTERNAL_SEND_ENABLED")
    email = _env_truthy("EMAIL_SEND_ENABLED")
    whatsapp = _env_truthy("WHATSAPP_SEND_ENABLED")
    whatsapp_live = _env_truthy("WHATSAPP_ALLOW_LIVE_SEND")
    sms = _env_truthy("SMS_SEND_ENABLED")
    mode = os.getenv("OUTBOUND_MODE", "draft_only")

    if external and mode != "controlled_live":
        failures.append("EXTERNAL_SEND_ENABLED=true requires OUTBOUND_MODE=controlled_live")
    if email and not external:
        failures.append("EMAIL_SEND_ENABLED=true requires EXTERNAL_SEND_ENABLED=true")
    if whatsapp and not external:
        failures.append("WHATSAPP_SEND_ENABLED=true requires EXTERNAL_SEND_ENABLED=true")
    if whatsapp and not whatsapp_live:
        failures.append("WHATSAPP_SEND_ENABLED=true requires WHATSAPP_ALLOW_LIVE_SEND=true")
    if sms:
        failures.append("SMS_SEND_ENABLED=true is blocked by this control plane")
    if mode not in {"draft_only", "review_only", "controlled_live", "disabled"}:
        failures.append(f"Unsupported OUTBOUND_MODE={mode}")
    if mode == "controlled_live":
        warnings.append("controlled_live requested; verify DNS, opt-out, suppression, approval, and channel-specific gates before any send")

    return {
        "status": "blocked" if failures else "safe",
        "mode": mode,
        "failures": failures,
        "warnings": warnings,
        "defaults": SAFE_DEFAULTS,
    }


def _build_founder_actions(registry: dict[str, Any]) -> list[dict[str, str]]:
    actions: list[dict[str, str]] = []
    for product in registry.get("commercial_products", []):
        actions.append(
            {
                "owner": "founder",
                "action": f"Prepare one sales proof note for {product['name']}",
                "why": product.get("promise", "Commercial product requires proof language."),
                "mode": "manual_review",
            }
        )
    for loop in registry.get("loops", []):
        actions.append(
            {
                "owner": "operator",
                "action": f"Run or verify loop: {loop['loop_id']}",
                "why": loop.get("goal", "Loop must produce a safe operating output."),
                "mode": "draft_only",
            }
        )
    return actions[:10]


def _write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    safety = payload["safety"]
    lines = [
        "# Dealix Agentic Commercial OS — Latest Control Plane Report",
        "",
        f"Generated: `{payload['generated_at']}`",
        f"Mode: `{safety['mode']}`",
        f"Safety status: `{safety['status']}`",
        "",
        "## Founder actions",
    ]
    for idx, action in enumerate(payload["founder_actions"], start=1):
        lines.append(f"{idx}. **{action['action']}** — {action['why']} (`{action['mode']}`)")

    lines.extend(["", "## Commercial products"])
    for product in payload["commercial_products"]:
        lines.append(f"- **{product['name']}** (`{product['priority']}`): {product['promise']}")

    lines.extend(["", "## Loops"])
    for loop in payload["loops"]:
        lines.append(f"- `{loop['loop_id']}` — {loop['goal']} / stop: {loop['stop_condition']}")

    if safety["failures"]:
        lines.extend(["", "## Safety failures"])
        for failure in safety["failures"]:
            lines.append(f"- {failure}")

    if safety["warnings"]:
        lines.extend(["", "## Safety warnings"])
        for warning in safety["warnings"]:
            lines.append(f"- {warning}")

    lines.extend(
        [
            "",
            "## Next step",
            "Review the generated actions manually. Do not send externally from this report.",
        ]
    )
    LATEST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    registry = _load_registry()
    safety = _safety_status()
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "company_positioning": registry.get("company_positioning"),
        "safety": safety,
        "commercial_products": registry.get("commercial_products", []),
        "loops": registry.get("loops", []),
        "founder_actions": _build_founder_actions(registry),
        "reports": {
            "json": str(LATEST_JSON.relative_to(ROOT)),
            "markdown": str(LATEST_MD.relative_to(ROOT)),
        },
    }
    _write_reports(payload)

    print("AGENTIC_COMMERCIAL_OS_CONTROL_PLANE_READY")
    print(f"SAFETY_STATUS={safety['status']}")
    print(f"OUTBOUND_MODE={safety['mode']}")
    print(f"REPORT_JSON={payload['reports']['json']}")
    print(f"REPORT_MD={payload['reports']['markdown']}")
    return 1 if safety["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
