#!/usr/bin/env python3
"""Generate Hermes Agent OS reports and action queues.

Default behavior is safe: read repository files and write internal Markdown reports
under docs/hermes/runtime. It does not send messages, deploy, mutate production, or
call external APIs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AGENTS_FILE = ROOT / "dealix/hermes/agents.yaml"
POLICIES_FILE = ROOT / "dealix/hermes/policies.yaml"
TOOLS_FILE = ROOT / "dealix/hermes/tools.yaml"
RUNTIME_DIR = ROOT / "docs/hermes/runtime"


def _simple_yaml_agents(text: str) -> list[dict[str, Any]]:
    """Very small fallback parser for the specific agents.yaml structure."""
    agents: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    in_agents = False
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.strip() == "agents:":
            in_agents = True
            continue
        if not in_agents:
            continue
        if re.match(r"^\s*- id:\s*", line):
            if current:
                agents.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
            continue
        if current is None:
            continue
        match = re.match(r"^\s{4}([a-zA-Z_]+):\s*(.*)$", line)
        if match:
            key, value = match.group(1), match.group(2).strip()
            if value:
                current[key] = value.strip('"')
    if current:
        agents.append(current)
    return agents


def load_agents() -> list[dict[str, Any]]:
    text = AGENTS_FILE.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        agents = data.get("agents", []) if isinstance(data, dict) else []
        return [agent for agent in agents if isinstance(agent, dict)]
    except Exception:
        return _simple_yaml_agents(text)


def load_text(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        return f"MISSING: {path}"
    return target.read_text(encoding="utf-8", errors="replace")[:4000]


def bullet_list(items: list[str]) -> str:
    if not items:
        return "- none"
    return "\n".join(f"- {item}" for item in items)


def agent_summary(agent: dict[str, Any]) -> str:
    owns = agent.get("owns") if isinstance(agent.get("owns"), list) else []
    inputs = agent.get("inputs") if isinstance(agent.get("inputs"), list) else []
    approvals = agent.get("approval_required_for") if isinstance(agent.get("approval_required_for"), list) else []
    return f"""# {agent.get('name', agent.get('id', 'Hermes Agent'))}

Generated: {dt.datetime.now(dt.UTC).isoformat()}

## Purpose

{agent.get('purpose', 'No purpose defined.')}

## Tier and risk

- Tier: `{agent.get('tier', 'unknown')}`
- Risk class: `{agent.get('risk_class', 'unknown')}`

## Owns

{bullet_list([str(x) for x in owns])}

## Inputs reviewed

{bullet_list([str(x) for x in inputs])}

## Approval required for

{bullet_list([str(x) for x in approvals])}

## Recommended operating stance

- Work in dry-run mode by default.
- Produce internal evidence before recommending action.
- Route external messages, production changes, vendor spend, and security-sensitive work to the action queue for founder approval.
"""


def write_runtime_file(name: str, content: str) -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    (RUNTIME_DIR / name).write_text(content, encoding="utf-8")


def generate_digest(agents: list[dict[str, Any]]) -> str:
    lines = [
        "# Hermes Daily Digest",
        "",
        f"Generated: {dt.datetime.now(dt.UTC).isoformat()}",
        "",
        "## Active agents",
        "",
    ]
    for agent in agents:
        lines.append(
            f"- **{agent.get('name', agent.get('id'))}** — tier `{agent.get('tier', 'unknown')}`, risk `{agent.get('risk_class', 'unknown')}`"
        )
    lines.extend(
        [
            "",
            "## Founder priorities today",
            "",
            "1. Keep production deploy surfaces healthy.",
            "2. Convert pipeline activity into a paid next step.",
            "3. Capture evidence for any customer, deployment, or security decision.",
            "",
            "## Required approvals queue summary",
            "",
            "All high/critical actions remain approval-gated. See `hermes_action_queue.md`.",
        ]
    )
    return "\n".join(lines) + "\n"


def generate_action_queue(agents: list[dict[str, Any]]) -> str:
    actions = []
    for agent in agents:
        risk = str(agent.get("risk_class", "medium"))
        if risk in {"high", "critical"}:
            actions.append(
                {
                    "agent": agent.get("id"),
                    "risk": risk,
                    "recommended_action": "Review latest evidence and approve/deny any external or production-side work.",
                    "approval_required": True,
                }
            )
    return "# Hermes Action Queue\n\n```json\n" + json.dumps(actions, ensure_ascii=False, indent=2) + "\n```\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Hermes Agent OS reports")
    parser.add_argument("--agent", help="Generate a single agent report by id", default=None)
    args = parser.parse_args()

    if not AGENTS_FILE.exists():
        raise SystemExit(f"missing {AGENTS_FILE}")
    agents = load_agents()
    if args.agent:
        agents = [agent for agent in agents if agent.get("id") == args.agent]
        if not agents:
            raise SystemExit(f"agent not found: {args.agent}")

    for agent in agents:
        agent_id = str(agent.get("id", "agent"))
        write_runtime_file(f"{agent_id}.md", agent_summary(agent))

    write_runtime_file("hermes_digest.md", generate_digest(agents))
    write_runtime_file("hermes_action_queue.md", generate_action_queue(agents))

    print(f"HERMES_REPORTS_OK agents={len(agents)} dir={RUNTIME_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
