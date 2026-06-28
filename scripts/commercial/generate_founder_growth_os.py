#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import UTC, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "commercial" / "founder_growth_os_2026.json"
OUT = ROOT / "reports" / "founder_growth_os"


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    products = data["created_hubspot_products"]
    tasks = data["created_hubspot_tasks"]
    total = sum(int(p["price_sar"]) for p in products)

    lines = [
        "# Dealix Founder Growth OS",
        "",
        "## Verdict",
        "",
        "Dealix has a practical operating base: HubSpot products, HubSpot tasks, command center, sales drafts, and communication gates.",
        "",
        "## HubSpot products",
        "",
        "| Product | HubSpot ID | Price SAR |",
        "|---|---:|---:|",
    ]
    for p in products:
        lines.append(f"| {p['name']} | {p['hubspot_object_id']} | {p['price_sar']} |")
    lines += ["", f"Total packaged setup value: {total} SAR", "", "## HubSpot tasks", "", "| Task | Task ID | Company ID |", "|---|---:|---:|"]
    for t in tasks:
        lines.append(f"| {t['subject']} | {t['hubspot_task_id']} | {t['company_id']} |")
    lines += [
        "",
        "## Next moves",
        "",
        "1. Finish the four HubSpot tasks.",
        "2. Generate ten company-specific sales packs.",
        "3. Book two discovery calls.",
        "4. Create one scoped sprint proposal after qualification.",
        "5. Keep communication in draft and approval mode until sender gates are complete.",
    ]

    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "mode": data["mode"],
        "products_count": len(products),
        "tasks_count": len(tasks),
        "total_packaged_setup_value_sar": total,
        "next_action": "Finish tasks, generate sales packs, qualify discovery calls.",
    }
    (OUT / "latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("FOUNDER_GROWTH_OS_GENERATED=reports/founder_growth_os/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
