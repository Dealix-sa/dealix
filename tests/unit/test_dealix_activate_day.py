"""Unit tests for the one-command daily activation runner.

Exercises the in-process pipeline (lead board → call sheet → index) hermetically
in a tmp dir, with subprocess steps disabled. Asserts the founder gets a single
ACTIVATION index that links the artifacts and reproduces the governance
invariants, and that the run degrades (never crashes) on bad input.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import dealix_activate_day as activate  # noqa: E402

_HEADER = (
    "company,sector,website,country,opportunity_type,source,risk_score,priority,"
    "decision_roles,suggested_channel,recommended_action,first_message_angle,"
    "objection_prediction,offer_recommended,fit_score,intent_score\n"
)
_ROWS = [
    "TestCo,SaaS,testco.sa,SA,DIRECT_CUSTOMER,public_page,15,P1,CEO,LINKEDIN_MANUAL,PREPARE_DM,زاوية تجريبية,price,Pilot 1 SAR,80,60",
    "MidCo,Fintech,midco.sa,SA,DIRECT_CUSTOMER,public_page,20,P2,Founder,LINKEDIN_MANUAL,PREPARE_DM,angle,fit,Pilot,60,40",
    "LowCo,Retail,lowco.sa,SA,DIRECT_CUSTOMER,public_page,25,P2,CEO,EMAIL,PREPARE_DM,angle,price,Starter,45,30",
]
ON_DATE = date(2026, 6, 7)


def _candidates_csv(tmp_path: Path) -> Path:
    p = tmp_path / "leads.csv"
    p.write_text(_HEADER + "\n".join(_ROWS) + "\n", encoding="utf-8")
    return p


def test_activation_writes_linked_index(tmp_path):
    briefs = tmp_path / "briefs"
    leads = tmp_path / "leads_out"
    rc = activate.run_activation(
        on_date=ON_DATE,
        top_n=3,
        candidates_path=_candidates_csv(tmp_path),
        briefs_dir=briefs,
        lead_out_dir=leads,
        run_subprocess_steps=False,
    )
    assert rc == 0

    index = briefs / "ACTIVATION_2026-06-07.md"
    call_sheet = briefs / "call_sheet_2026-06-07.md"
    board_md = leads / "2026-06-07.md"
    assert index.is_file()
    assert call_sheet.is_file()
    assert board_md.is_file()

    text = index.read_text(encoding="utf-8")
    # links resolve to real sibling files
    assert "call_sheet_2026-06-07.md" in text
    # governance invariants reproduced verbatim
    assert "no_live_send_called" in text
    assert "no_scraping_invoked" in text
    # true pool size surfaced
    assert "3" in text


def test_call_sheet_is_draft_only_and_ranked_by_fit(tmp_path):
    briefs = tmp_path / "briefs"
    activate.run_activation(
        on_date=ON_DATE,
        top_n=3,
        candidates_path=_candidates_csv(tmp_path),
        briefs_dir=briefs,
        lead_out_dir=tmp_path / "leads_out",
        run_subprocess_steps=False,
    )
    cs = (briefs / "call_sheet_2026-06-07.md").read_text(encoding="utf-8")
    assert "DRAFT-ONLY" in cs
    assert "TestCo" in cs
    # highest fit_score (TestCo=80) must appear before the lower one (LowCo=45)
    assert cs.index("TestCo") < cs.index("LowCo")


def test_activation_degrades_on_missing_candidates(tmp_path):
    briefs = tmp_path / "briefs"
    rc = activate.run_activation(
        on_date=ON_DATE,
        top_n=3,
        candidates_path=tmp_path / "does_not_exist.csv",
        briefs_dir=briefs,
        lead_out_dir=tmp_path / "leads_out",
        run_subprocess_steps=False,
    )
    assert rc == 0
    # index is still written even with zero candidates
    assert (briefs / "ACTIVATION_2026-06-07.md").is_file()


def test_build_call_sheet_pure_helper():
    # the pure builder works on an empty board without touching disk
    from dealix_daily_lead_prep import run_daily_prep

    board = run_daily_prep(candidates=[], on_date=ON_DATE, top_n=5)
    out = activate.build_call_sheet(board, {}, total_candidates=0)
    assert "DRAFT-ONLY" in out
    assert "2026-06-07" in out
