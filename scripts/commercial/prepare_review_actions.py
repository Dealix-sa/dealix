#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "reports" / "commercial" / "sales_agent_company_brain" / "latest.json"
OUT_DIR = ROOT / "reports" / "commercial" / "review_actions"


def load_source() -> dict:
    if not SOURCE.exists():
        raise FileNotFoundError("run scripts/commercial/run_sales_agent_company_brain_day.py first")
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def build_actions(data: dict) -> list[dict[str, str]]:
    actions = []
    for item in data.get("priority_queue", [])[:10]:
        company = str(item.get("company_name", "Unknown"))
        offer = str(item.get("recommended_offer", "Revenue Command Room OS"))
        priority = str(item.get("priority", "P3"))
        actions.append(
            {
                "kind": "account_review",
                "company_name": company,
                "priority": priority,
                "title": f"Review {company} for {offer}",
                "next_step": "verify source, confirm pain hypothesis, prepare discovery notes",
            }
        )
    return actions


def markdown(actions: list[dict[str, str]]) -> str:
    lines = [
        "# Founder Review Actions",
        "",
        "Local review queue only. No external system was changed.",
        "",
        "| Priority | Company | Title | Next step |",
        "|---|---|---|---|",
    ]
    for action in actions:
        lines.append(
            f"| {action['priority']} | {action['company_name']} | {action['title']} | {action['next_step']} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    data = load_source()
    actions = build_actions(data)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "review_only",
        "external_mutation_performed": False,
        "actions": actions,
    }
    (OUT_DIR / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT_DIR / "latest.md").write_text(markdown(actions), encoding="utf-8")
    print("REVIEW_ACTIONS=reports/commercial/review_actions/latest.md")
    print(f"ACTIONS_PREPARED={len(actions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
