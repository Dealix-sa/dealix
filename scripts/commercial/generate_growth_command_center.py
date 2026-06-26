#!/usr/bin/env python3
"""Generate Dealix Growth Command Center reports.

Local-only generator. It reads static service stack data and produces founder
review reports. It does not send messages, call external services, or mutate CRM.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "commercial" / "growth_command_center_stack.json"
OUT = ROOT / "reports" / "growth_command_center"


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Dealix Growth Command Center",
        "",
        "## Executive verdict",
        "",
        "Dealix should operate as a founder-led Saudi B2B AI Operating Systems company. The commercial motion is sprint-first, proof-led, and review-first.",
        "",
        "## North star",
        "",
        f"- Metric: {data['north_star']['metric']}",
        f"- Daily target: {data['north_star']['daily_target']}",
        f"- Weekly target: {data['north_star']['weekly_target']}",
        "",
        "## Service stack",
        "",
        "| Service | Buyer | Pain | Entry offer | Price range |",
        "|---|---|---|---|---:|",
    ]

    for item in data["service_stack"]:
        lines.append(
            f"| {item['name']} | {item['buyer']} | {item['pain']} | {item['entry_offer']} | {item['price_range_sar']} SAR |"
        )

    lines += [
        "",
        "## Daily operating targets",
        "",
    ]
    for key, value in data["daily_targets"].items():
        lines.append(f"- {key}: {value}")

    lines += [
        "",
        "## Sales Agent policy",
        "",
        "Allowed identities:",
    ]
    lines.extend(f"- {x}" for x in data["sales_agent_policy"]["allowed_identities"])
    lines += ["", "Blocked behaviors:"]
    lines.extend(f"- {x}" for x in data["sales_agent_policy"]["blocked_behaviors"])

    lines += [
        "",
        "## Safety state",
        "",
        "Live external communication remains disabled by default. The system generates drafts, reports, sales packs, and next actions for founder review.",
        "",
        "## Next founder actions",
        "",
        "1. Finish database foundation PR before merging this commercial layer.",
        "2. Generate ten company-specific sales packs from verified sectors.",
        "3. Book two discovery calls using founder-approved messages.",
        "4. Create one scoped sprint proposal after discovery qualification.",
        "5. Convert first sprint proof into a monthly managed OS retainer.",
    ]

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": data["mode"],
        "north_star": data["north_star"],
        "services_count": len(data["service_stack"]),
        "daily_targets": data["daily_targets"],
        "safety_defaults": data["safety_defaults"],
    }

    (OUT / "latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("GROWTH_COMMAND_CENTER_GENERATED=reports/growth_command_center/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
