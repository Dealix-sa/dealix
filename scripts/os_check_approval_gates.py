#!/usr/bin/env python3
"""CLI: check whether an action requires human approval per 06_APPROVAL_GATES.yml.

Usage:
    python scripts/os_check_approval_gates.py --action "send_first_email"
    python scripts/os_check_approval_gates.py --action "read_file"

Exit code: 1 if approval is required, 0 if the action is free.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from os_runtime.approval_gate import check_action


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check approval gate status for a given action"
    )
    parser.add_argument("--action", type=str, required=True, help="Action key to check")
    args = parser.parse_args()

    result = check_action(args.action)
    output = {
        "action": result.action,
        "requires_approval": result.requires_approval,
        "gate_id": result.gate_id,
        "reason": result.reason,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))

    return 1 if result.requires_approval else 0


if __name__ == "__main__":
    sys.exit(main())
