"""Generate the CEO Action Queue from the current Business Score."""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops_runtime.business_audit import calculate_business_score  # noqa: E402
from control_plane.priority_router import route_priority  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    private_root = Path(args.private_ops).resolve()
    private_root.mkdir(parents=True, exist_ok=True)
    (private_root / "founder").mkdir(parents=True, exist_ok=True)

    score = calculate_business_score(str(private_root))
    priority = route_priority(score)

    content = f"""# CEO Action Queue
## Date
{date.today().isoformat()}
## Current Business Score
{score['total_score']} / 100
## Status
{score['status']}
## Top Priority
| Field | Value |
|---|---|
| Area | {priority['area']} |
| Priority | {priority['priority']} |
| Reason | {priority['reason']} |
| Action | {priority['action']} |
## CEO Rule
Do this priority before adding new features, dashboards, agents, or documentation.
## Secondary Checks
- Review approvals.
- Update pipeline.
- Log revenue action.
- Run close-day gate.
"""
    out = private_root / "founder/ceo_action_queue.md"
    out.write_text(content, encoding="utf-8")
    print("PASS: CEO action queue generated.")
    print(f"Top priority: {priority['priority']}")
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
