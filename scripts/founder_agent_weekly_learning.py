#!/usr/bin/env python3
"""Agent weekly learning log."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_agent_tasks import (  # noqa: E402
    apply_learning_hints_to_playbook_snippet,
    load_weekly_learning,
    seed_quarterly_external_refs,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apply-hints", action="store_true")
    p.add_argument("--seed-quarterly", action="store_true")
    args = p.parse_args()

    if args.seed_quarterly:
        seed_quarterly_external_refs()
        print("OK: quarterly external_refs seeded")
        return 0
    if args.apply_hints:
        block = apply_learning_hints_to_playbook_snippet()
        print(block or "لا توجد تلميحات بعد.")
        return 0
    data = load_weekly_learning()
    print(f"entries={len(data.get('entries') or [])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
