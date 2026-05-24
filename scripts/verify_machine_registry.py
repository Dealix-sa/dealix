#!/usr/bin/env python3
"""Verify the machine registry."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, print_and_exit, repo_root  # noqa: E402


def main() -> int:
    result = VerifyResult(name="Machine Registry", passed=True)
    path = repo_root() / "registries" / "machine_registry.yaml"
    if not path.exists():
        result.passed = False
        result.missing.append(str(path.relative_to(repo_root())))
        return print_and_exit(result)
    text = path.read_text(encoding="utf-8")
    machine_count = 0
    for match in re.finditer(r"-\s+id:\s*(\S+)[\s\S]+?(?=\n\s*-\s+id:|\Z)", text):
        block = match.group(0)
        machine_count += 1
        mid = match.group(1)
        if "kill_switch:" not in block:
            result.passed = False
            result.notes.append(f"{mid}: missing kill_switch")
        if "state_file:" not in block:
            result.passed = False
            result.notes.append(f"{mid}: missing state_file")
    if machine_count == 0:
        result.passed = False
        result.notes.append("no machines registered")
    result.notes.append(f"machines registered: {machine_count}")
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
