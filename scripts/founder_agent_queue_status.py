#!/usr/bin/env python3
"""Print / seed founder agent daily queue."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.agent_fleet_tasks import (  # noqa: E402
    build_agent_fleet_today_pack,
    load_unified_daily_tasks,
)
from dealix.commercial_ops.founder_agent_tasks import (  # noqa: E402
    build_queue_status,
    seed_today_queue,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed-today", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--unified", action="store_true", help="Include unified task templates")
    args = p.parse_args()

    if args.seed_today:
        seed_today_queue(force=True)
    status = build_queue_status()
    print(f"FOUNDER_AGENT_QUEUE_VERDICT={status.get('verdict')}")
    if args.unified:
        pack = build_agent_fleet_today_pack()
        if args.json:
            print(json.dumps(pack, ensure_ascii=False, indent=2))
        else:
            for t in load_unified_daily_tasks():
                print(f"  {t.get('priority')} · {t.get('agent')} · {t.get('title_ar') or t.get('id')}")
    elif args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        for agent, titles in (status.get("pending_by_agent") or {}).items():
            print(f"## {agent}")
            for title in titles:
                print(f"  - {title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
