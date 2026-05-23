#!/usr/bin/env python3
"""
generate_weekly_review.py — render this week's CEO review from the
default CompanyState. Replace defaults with a real source when a
metrics adapter is wired.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from control_plane.company_state import snapshot  # noqa: E402
from operating_intelligence import (  # noqa: E402
    BottleneckDetector, LearningSynthesizer, generate_weekly_review,
)


def main() -> int:
    state = snapshot(
        as_of=datetime.now(timezone.utc),
        stage="0-founder-clarity",
    )
    bottleneck = BottleneckDetector().detect({})
    learning = LearningSynthesizer().summarize([], period=state.as_of.date().isoformat())
    review = generate_weekly_review(state, bottleneck=bottleneck, learning=learning)

    out_dir = REPO / "evals" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"weekly_review_{state.as_of.date().isoformat()}.md"
    target.write_text(review.as_markdown(), encoding="utf-8")
    print(f"[OK] generate_weekly_review: wrote {target.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
