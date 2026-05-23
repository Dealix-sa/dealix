"""Render the CEO Business Score as a markdown brief."""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops_runtime.business_audit import calculate_business_score  # noqa: E402


def _render(score: dict) -> str:
    metrics = score["metrics"]
    rows = "\n".join(
        f"| {key} | {value} |" for key, value in sorted(metrics.items())
    )
    return f"""# CEO Business Score
## Date
{date.today().isoformat()}
## Total
{score['total_score']} / 100
## Status
{score['status']}
## Metrics
| Metric | Value |
|---|---:|
{rows}
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    (root / "business_audit").mkdir(parents=True, exist_ok=True)

    score = calculate_business_score(str(root))
    out = root / "business_audit/ceo_business_score.md"
    out.write_text(_render(score), encoding="utf-8")
    print(f"PASS: business score written: {out}")
    print(f"Score: {score['total_score']} / 100 ({score['status']})")


if __name__ == "__main__":
    main()
