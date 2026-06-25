#!/usr/bin/env python3
from __future__ import annotations

from scripts.commercial.generate_command_room_snapshot import main as command_snapshot
from scripts.commercial.generate_founder_daily_brief import main as founder_brief
from scripts.commercial.generate_startup_command_center import main as startup_center
from scripts.commercial.generate_startup_proof_pack import main as proof_pack
from scripts.commercial.prepare_review_actions import main as review_actions
from scripts.commercial.run_sales_agent_company_brain_day import main as commercial_day


def main() -> int:
    commercial_day()
    review_actions()
    command_snapshot()
    startup_center()
    founder_brief()
    proof_pack()
    print("STARTUP_OS_DAY_READY")
    print("REPORTS_READY=reports/startup_command_center/latest.md,reports/founder_daily_brief/latest.md,reports/startup_proof_pack/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
