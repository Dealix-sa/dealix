#!/usr/bin/env python3
"""
generate_ceo_brief.py — render today's CEO brief from the default
CompanyState. Replace defaults with a real source when a metrics
adapter is wired.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from control_plane import generate_ceo_brief, snapshot  # noqa: E402


def main() -> int:
    state = snapshot(
        as_of=datetime.now(timezone.utc),
        stage="0-founder-clarity",
        leads_this_week=0,
        qualified_leads=0,
        proposals_out=0,
        paid_sprints=0,
        cash_collected_30d=0.0,
        mrr=0.0,
        runway_months=0.0,
        pending_approvals=0,
        company_health_score=0,
    )
    brief = generate_ceo_brief(state)
    out_dir = REPO / "evals" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"ceo_brief_{state.as_of.date().isoformat()}.md"
    target.write_text(brief.as_markdown(), encoding="utf-8")
    print(f"[OK] generate_ceo_brief: wrote {target.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
