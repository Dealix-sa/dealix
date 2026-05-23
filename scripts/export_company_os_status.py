#!/usr/bin/env python3
"""
export_company_os_status.py — write a JSON snapshot of the company OS
state to evals/results/. Consumed by the scorecard workflow.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from control_plane.company_state import snapshot  # noqa: E402
from control_plane.risk_engine import RiskEngine  # noqa: E402
from control_plane.system_scorecard import score_system  # noqa: E402


def main() -> int:
    state = snapshot(
        as_of=datetime.now(timezone.utc),
        stage="0-founder-clarity",
    )
    risks = RiskEngine().assess(state)
    trust_score = score_system("trust", signals={
        "approval_matrix_loaded": 1.0,
        "claim_guard_loaded": 1.0,
        "suppression_loaded": 1.0,
    })

    payload = {
        "as_of": state.as_of.isoformat(),
        "stage": state.stage,
        "company_health_score": state.company_health_score,
        "risks": [
            {"code": r.code, "title": r.title, "severity": r.severity}
            for r in risks
        ],
        "trust_score": trust_score.score,
    }

    out_dir = REPO / "evals" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "company_os_status.json"
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[OK] export_company_os_status: wrote {target.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
