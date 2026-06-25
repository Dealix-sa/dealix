#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STARTUP = ROOT / "reports" / "startup_command_center" / "latest.json"
CONFIG = ROOT / "data" / "commercial" / "startup_os_operating_config.json"
OUT = ROOT / "reports" / "founder_daily_brief"


def load_json(path: Path, fallback: dict) -> dict:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def markdown(payload: dict) -> str:
    queue = payload.get("top_accounts", [])
    products = payload.get("products", [])
    actions = payload.get("founder_actions", [])
    rules = payload.get("hard_rules", [])
    lines = [
        "# Dealix Founder Daily Brief",
        "",
        "## Today's executive decision",
        "",
        payload.get("executive_decision", "Review top verified accounts and prepare one scoped diagnostic proposal."),
        "",
        "## Commercial state",
        "",
        f"- Targets loaded: {payload.get('targets_loaded', 0)}",
        f"- Packs generated: {payload.get('packs_generated', 0)}",
        f"- Products ready: {len(products)}",
        f"- Mode: {payload.get('mode', 'founder_led_review_first')}",
        "",
        "## Top founder actions",
        "",
    ]
    for action in actions:
        lines.append(f"- {action}")
    lines += ["", "## Top accounts", "", "| Priority | Company | Offer |", "|---|---|---|"]
    for item in queue[:8]:
        lines.append(f"| {item.get('priority', 'P3')} | {item.get('company_name', '')} | {item.get('recommended_offer', '')} |")
    lines += ["", "## Hard rules", ""]
    for rule in rules:
        lines.append(f"- {rule}")
    return "\n".join(lines) + "\n"


def main() -> int:
    startup = load_json(STARTUP, {})
    config = load_json(CONFIG, {})
    queue = startup.get("priority_queue", [])
    products = startup.get("products", [])
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": startup.get("mode", config.get("operating_mode", "founder_led_review_first")),
        "executive_decision": "Review the top P1 accounts, prepare three discovery notes, and create one scoped diagnostic proposal only after qualification.",
        "targets_loaded": startup.get("targets_loaded", 0),
        "packs_generated": startup.get("packs_generated", 0),
        "products": products,
        "top_accounts": queue[:8],
        "founder_actions": [
            "Open the Startup Command Center report.",
            "Review top P1 accounts first.",
            "Prepare three discovery notes.",
            "Create one scoped diagnostic proposal after qualification.",
            "Record every founder action in HubSpot or the local ledger.",
            "Do not expand delivery scope without a proof pack plan."
        ],
        "hard_rules": config.get("hard_rules", []),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "latest.md").write_text(markdown(payload), encoding="utf-8")
    print("FOUNDER_DAILY_BRIEF=reports/founder_daily_brief/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
