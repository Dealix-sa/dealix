#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "data" / "commercial" / "startup_os_product_matrix.json"
COMMERCIAL = ROOT / "reports" / "commercial" / "sales_agent_company_brain" / "latest.json"
REVIEW = ROOT / "reports" / "commercial" / "review_actions" / "latest.json"
OUT = ROOT / "reports" / "startup_command_center"
WEB_SNAPSHOT = ROOT / "apps" / "web" / "lib" / "startup-command-snapshot.ts"


def load_json(path: Path, fallback: dict) -> dict:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def product_rows(products: list[dict]) -> list[str]:
    rows = ["| Product | First offer | Setup SAR | Retainer SAR | Proof |", "|---|---|---:|---:|---|"]
    for product in products:
        rows.append(
            f"| {product['name']} | {product['first_offer']} | {product['setup_range_sar']} | {product['retainer_range_sar']} | {product['proof']} |"
        )
    return rows


def priority_rows(queue: list[dict]) -> list[str]:
    rows = ["| Priority | Score | Company | Sector | Offer |", "|---|---:|---|---|---|"]
    for item in queue[:12]:
        rows.append(
            f"| {item.get('priority','P3')} | {item.get('priority_value',0)} | {item.get('company_name','')} | {item.get('sector','')} | {item.get('recommended_offer','')} |"
        )
    return rows


def build_markdown(matrix: dict, commercial: dict, review: dict) -> str:
    products = matrix.get("products", [])
    queue = commercial.get("priority_queue", [])
    actions = review.get("actions", [])
    lines = [
        "# Dealix Startup Command Center",
        "",
        "## Executive verdict",
        "",
        "Dealix is operating as a founder-led Saudi B2B AI Operating Systems company. This command center joins products, target priority, sales packs, Company Brain decisions, review actions, and proof work into one operating view.",
        "",
        "## Safety state",
        "",
        f"- Mode: {matrix.get('mode', 'founder_led_review_first')}",
        "- External communication remains draft/review-first by default.",
        "- No live WhatsApp, SMS, or automatic cold email is enabled by this command center.",
        "",
        "## Product system",
        "",
    ]
    lines.extend(product_rows(products))
    lines += [
        "",
        "## Commercial queue",
        "",
        f"- Targets loaded: {commercial.get('targets_loaded', 0)}",
        f"- Packs generated: {commercial.get('packs_generated', 0)}",
        f"- Queue items: {len(queue)}",
        "",
    ]
    lines.extend(priority_rows(queue))
    lines += [
        "",
        "## Founder review actions",
        "",
    ]
    for action in actions[:10]:
        lines.append(f"- {action.get('title', 'Review account')} — {action.get('next_step', 'review')}")
    lines += [
        "",
        "## Next operating moves",
        "",
        "1. Review the top P1 accounts.",
        "2. Select three accounts for discovery preparation.",
        "3. Create one scoped diagnostic proposal after qualification.",
        "4. Update HubSpot or local ledgers after every founder action.",
        "5. Produce a proof pack for every paid sprint.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    matrix = load_json(MATRIX, {})
    commercial = load_json(COMMERCIAL, {"priority_queue": [], "packs": []})
    review = load_json(REVIEW, {"actions": []})
    products = matrix.get("products", [])
    queue = commercial.get("priority_queue", [])
    actions = review.get("actions", [])
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "company": matrix.get("company", "Dealix"),
        "positioning": matrix.get("positioning", "Saudi B2B AI Operating Systems company"),
        "mode": matrix.get("mode", "founder_led_review_first"),
        "products": products,
        "targets_loaded": commercial.get("targets_loaded", 0),
        "packs_generated": commercial.get("packs_generated", 0),
        "priority_queue": queue[:12],
        "review_actions": actions[:12],
        "commands": [
            "python scripts/commercial/run_command_room_day.py",
            "python scripts/commercial/generate_startup_command_center.py",
            "npm --prefix apps/web run verify",
        ],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "latest.md").write_text(build_markdown(matrix, commercial, review), encoding="utf-8")
    WEB_SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    WEB_SNAPSHOT.write_text(
        "export const startupCommandSnapshot = " + json.dumps(payload, ensure_ascii=False, indent=2) + " as const;\n",
        encoding="utf-8",
    )
    print("STARTUP_COMMAND_CENTER=reports/startup_command_center/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
