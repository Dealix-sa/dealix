#!/usr/bin/env python3
"""Rank the Dealix open-source tool stack.

This script intentionally uses only the Python standard library so it can run in
CI without installing dependencies.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def compute_score(tool: dict[str, Any]) -> int:
    scores = tool.get("scores", {})
    return int(
        scores.get("autonomy", 0)
        + scores.get("revenue", 0)
        + scores.get("safety", 0)
        + scores.get("locality", 0)
        + scores.get("compliance", 0)
        - scores.get("effort", 0)
        - scores.get("risk", 0)
    )


def render_report(registry: dict[str, Any]) -> str:
    tools = list(registry.get("tools", []))
    for tool in tools:
        tool["computed_score"] = compute_score(tool)
    tools.sort(key=lambda item: (item.get("priority", "P9"), -item["computed_score"], item["id"]))

    lines: list[str] = []
    lines.append("# Dealix Tool Stack Ranking")
    lines.append("")
    lines.append("Mode: draft-only, approval-first")
    lines.append("")
    lines.append("## Ranking")
    lines.append("")
    lines.append("| Rank | Priority | Score | Tool | Category | Safe next action |")
    lines.append("|---:|---|---:|---|---|---|")
    for rank, tool in enumerate(tools, start=1):
        lines.append(
            f"| {rank} | {tool.get('priority')} | {tool['computed_score']} | "
            f"[{tool.get('name')}]({tool.get('url')}) | {tool.get('category')} | {tool.get('next_action')} |"
        )

    lines.append("")
    lines.append("## P0 tools")
    lines.append("")
    for tool in [t for t in tools if t.get("priority") == "P0"]:
        lines.append(f"- **{tool['name']}**: {tool['dealix_use']}")

    lines.append("")
    lines.append("## Blocked by default")
    lines.append("")
    for action in registry.get("default_policy", {}).get("blocked_actions", []):
        lines.append(f"- {action}")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="dealix/strategy_execution/tool_registry.json")
    parser.add_argument("--output", default="reports/tool_stack/ranked_tool_stack.md")
    args = parser.parse_args()

    registry_path = Path(args.registry)
    output_path = Path(args.output)
    registry = json.loads(registry_path.read_text(encoding="utf-8"))

    if len(registry.get("tools", [])) != 50:
        raise SystemExit(f"Expected 50 tools, found {len(registry.get('tools', []))}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_report(registry), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
