#!/usr/bin/env python3
"""Generate local Hermes agent reports from repository configuration."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
AGENTS_FILE = ROOT / "dealix" / "hermes" / "agents.yaml"
POLICY_FILE = ROOT / "dealix" / "hermes" / "policy.yaml"
OUTPUT_DIR = ROOT / "docs" / "generated" / "hermes"


def agent_ids(text: str) -> list[str]:
    ids: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("id: "):
            ids.append(s.split("id: ", 1)[1].strip())
    return ids


def write_agent_report(agent_id: str, mode: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{agent_id}.md"
    now = datetime.now(timezone.utc).isoformat()
    path.write_text(
        f"""# Hermes Agent Report — {agent_id}

- generated_at: {now}
- agent_id: {agent_id}
- mode: {mode}
- registry: `dealix/hermes/agents.yaml`
- policy: `dealix/hermes/policy.yaml`

## Summary

This is a local repository report for the Hermes agent registry.

## Current operating mode

Hermes starts in dry-run mode. Reports are generated for review before any higher-privilege workflow is considered.

## Review checklist

- [ ] Agent mission is clear.
- [ ] Agent owner is clear.
- [ ] Outputs are useful.
- [ ] Stop rules are understood.
- [ ] Human approval expectations are clear.

## Recommended next action

Review this report and keep the agent in dry-run until production gates are green.
""",
        encoding="utf-8",
    )
    return path


def main() -> int:
    mode = "enabled" if os.getenv("HERMES_AGENTS_ENABLED") in {"1", "true", "yes"} else "dry_run"
    text = AGENTS_FILE.read_text(encoding="utf-8")
    ids = agent_ids(text)
    if not ids:
        raise SystemExit("No Hermes agents found")
    for agent_id in ids:
        print(f"Wrote {write_agent_report(agent_id, mode).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
