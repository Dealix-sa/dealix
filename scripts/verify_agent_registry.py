#!/usr/bin/env python3
"""Verify the agent registry is complete and every agent has a kill switch."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, print_and_exit, repo_root  # noqa: E402


def main() -> int:
    result = VerifyResult(name="Agent Registry", passed=True)
    path = repo_root() / "registries" / "agent_registry.yaml"
    if not path.exists():
        result.passed = False
        result.missing.append(str(path.relative_to(repo_root())))
        return print_and_exit(result)
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"- id:\s*(\w+)[\s\S]+?(?=\n  - id:|\Z)", text)
    if not blocks:
        result.passed = False
        result.notes.append("no agents listed")
        return print_and_exit(result)
    # Ensure every agent block has kill_switch + tier.
    agent_count = 0
    for match in re.finditer(r"-\s+id:\s*(\S+)[\s\S]+?(?=\n\s*-\s+id:|\Z)", text):
        block = match.group(0)
        agent_count += 1
        agent_id = match.group(1)
        if "tier:" not in block:
            result.passed = False
            result.notes.append(f"{agent_id}: missing tier")
        if "kill_switch:" not in block:
            result.passed = False
            result.notes.append(f"{agent_id}: missing kill_switch")
    result.notes.append(f"agents registered: {agent_count}")
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
