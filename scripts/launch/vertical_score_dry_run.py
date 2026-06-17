"""Dry-run: print ranked Saudi market verticals and top wedge recommendation.

Usage:
    python scripts/launch/vertical_score_dry_run.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow running directly without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dealix.launch_os.vertical_scorer import rank_verticals, top_wedge


def main() -> None:
    ranked = rank_verticals()

    print("=" * 70)
    print("DEALIX — Saudi Market Vertical Scores (15 Sectors)")
    print("تقييم القطاعات السعودية الخمسة عشر")
    print("=" * 70)
    print(
        f"{'#':<3} {'Sector':<25} {'Rev':<5} {'Pain':<5} {'Reg':<5} "
        f"{'AI':<5} {'Gap':<5} {'TOTAL':<6}"
    )
    print("-" * 70)

    for rank, v in enumerate(ranked, 1):
        print(
            f"{rank:<3} {v.sector:<25} {v.revenue_potential:<5} {v.pain_clarity:<5} "
            f"{v.regulatory_ease:<5} {v.ai_readiness:<5} {v.competition_gap:<5} "
            f"{v.total_score:<6}"
        )

    wedge = top_wedge()
    print()
    print("=" * 70)
    print(f"TOP WEDGE RECOMMENDATION: {wedge.sector.upper()}")
    print(f"الوتد الرئيسي الموصى به: {wedge.sector}")
    print(f"Total Score: {wedge.total_score}/100")
    print()
    print(f"Notes (EN): {wedge.notes_en}")
    print(f"Notes (AR): {wedge.notes_ar}")
    print("=" * 70)


if __name__ == "__main__":
    main()
