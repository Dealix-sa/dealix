import argparse
import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ops_runtime.business_audit import calculate_business_score
from control_plane.strategic_decision_engine import recommend_strategic_decision


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    score = calculate_business_score(str(root))
    decision = recommend_strategic_decision(score)
    content = f"""# Strategic Decision Report

## Date
{date.today().isoformat()}

## CEO Business Score
{score['total_score']} / 100

## Decision
{decision['decision']}

## Area
{decision['area']}

## Reason
{decision['reason']}

## Action
{decision['action']}

## CEO Rule
Do not override this decision without new evidence.

## Review
- Did we act on this?
- What changed?
- What should be killed or deferred?
"""
    out_dir = root / "founder"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "strategic_decision_report.md"
    out.write_text(content, encoding="utf-8")
    print("PASS: strategic decision report generated.")
    print(f"Decision: {decision['decision']} / {decision['area']}")
    print(f"Action: {decision['action']}")
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
