#!/usr/bin/env python3
"""Generate Dealix Strategic Command Center reports.

Local-only. No external requests and no outbound actions.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = ROOT / "data" / "commercial" / "strategic_command_center_template.json"
OUT_DIR = ROOT / "reports" / "command_center"


def load_template() -> dict:
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


def build_markdown(payload: dict) -> str:
    today = date.today().isoformat()
    lines = [
        f"# Dealix Strategic Command Center — {today}",
        "",
        f"## Executive verdict",
        "",
        payload["executive_verdict"],
        "",
        "## North star",
        "",
        f"- Metric: {payload['north_star']['metric']}",
        f"- Daily target: {payload['north_star']['daily_target']}",
        f"- Weekly target: {payload['north_star']['weekly_target']}",
        "",
        "## Command lanes",
        "",
        "| Lane | Status | Strategic question | Actions |",
        "|---|---|---|---|",
    ]
    for lane in payload["lanes"]:
        actions = "<br>".join(lane["daily_actions"])
        lines.append(f"| {lane['title']} | {lane['status']} | {lane['primary_question']} | {actions} |")

    numbers = payload["daily_numbers"]
    lines += [
        "",
        "## Daily operating numbers",
        "",
        "| Activity | Target |",
        "|---|---:|",
        f"| Research companies | {numbers['research_companies']} |",
        f"| Verify targets | {numbers['verify_targets']} |",
        f"| Draft messages | {numbers['draft_messages']} |",
        f"| Manual contacts | {numbers['manual_contacts']} |",
        f"| Call attempts | {numbers['call_attempts']} |",
        f"| Discovery calls | {numbers['discovery_calls']} |",
        f"| Proposals | {numbers['proposals']} |",
        "",
        "## Service stack",
        "",
    ]
    lines.extend(f"- {service}" for service in payload["service_stack"])
    lines += [
        "",
        "## Baseline safety",
        "",
        "- Outbound mode: draft_only",
        "- External sends: disabled in baseline",
        "- Sales agent: authorized assistant only",
        "- Named executive identity: requires explicit approval",
        "- WhatsApp live use: requires opt-in and approved template",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    payload = load_template()
    payload["generated_at"] = datetime.now(timezone.utc).isoformat()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "latest.md").write_text(build_markdown(payload), encoding="utf-8")
    (OUT_DIR / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("STRATEGIC_COMMAND_CENTER_GENERATED=reports/command_center/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
