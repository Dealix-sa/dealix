import argparse
import sys
from pathlib import Path
from datetime import date

# Ensure project root is importable regardless of invocation cwd.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ops_runtime.business_audit import calculate_business_score  # noqa: E402
from control_plane.control_tower import build_control_tower_signal  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    private_root = Path(args.private_ops).resolve()
    private_root.mkdir(parents=True, exist_ok=True)
    (private_root / "founder").mkdir(parents=True, exist_ok=True)
    score = calculate_business_score(str(private_root))
    tower = build_control_tower_signal(score)
    signal_rows = "\n".join(
        f"| {s['area']} | {s['level']} | {s['message']} | {s['action']} |"
        for s in tower["signals"]
    ) or "| None | green | No major signal | Continue cadence |"
    content = f"""# Dealix Control Tower Brief
## Date
{date.today().isoformat()}
## Company Posture
{tower['posture']}
## CEO Business Score
{score['total_score']} / 100
## Top CEO Action
{tower['top_action']}
## Signals
| Area | Level | Message | Action |
|---|---|---|---|
{signal_rows}
## CEO Rule
Do the top CEO action before building new systems, dashboards, agents, or features.
## Review Files
- business_audit/ceo_business_score.md
- founder/ceo_action_queue.md
- stage/evidence_report.md
- founder/weekly_war_room.md
- finance/monthly_finance_review.md
"""
    out = private_root / "founder/control_tower_brief.md"
    out.write_text(content, encoding="utf-8")
    print("PASS: Control Tower brief generated.")
    print(f"Posture: {tower['posture']}")
    print(f"Top action: {tower['top_action']}")
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
