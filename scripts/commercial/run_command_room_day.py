#!/usr/bin/env python3
from __future__ import annotations

from scripts.commercial.generate_command_room_snapshot import main as snapshot
from scripts.commercial.prepare_review_actions import main as review_actions
from scripts.commercial.run_sales_agent_company_brain_day import main as commercial_day


def main() -> int:
    commercial_day()
    review_actions()
    snapshot()
    print("COMMAND_ROOM_DAY_READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
