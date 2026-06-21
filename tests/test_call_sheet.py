"""Tests for the founder daily call-sheet generator (scripts/dealix_call_sheet.py).

Doctrine-critical invariants this guards:
- Warm/known contacts rank above cold ones (founder time goes to best fit).
- A recommendation off a *call* never jumps above the 499 SAR Sprint — the
  ladder is earned via Proof Pack, not pitched cold (non-negotiable: proof first).
- The rendered sheet states manual dialing / no automation and carries the
  bilingual value disclaimer.
- Empty input is safe (no fabrication, Article 8).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.dealix_call_sheet import (  # noqa: E402
    DISCLAIMER,
    build_call_sheet,
    render_markdown,
)

WARM_ROW = {
    "name": "Warm Contact",
    "role": "COO",
    "company": "Riyadh Co",
    "sector": "b2b_services",
    "relationship": "warm",
    "city": "Riyadh",
    "linkedin_url": "https://linkedin.com/in/x",
    "notes": "met at LEAP 2025",
}
COLD_ROW = {
    "name": "Cold Contact",
    "role": "Analyst",
    "company": "Jeddah LLC",
    "sector": "retail",
    "relationship": "cold",
    "city": "Jeddah",
    "linkedin_url": "",
    "notes": "",
}


def test_build_ranks_warm_above_cold():
    sheet = build_call_sheet([COLD_ROW, WARM_ROW])
    assert sheet[0]["row"]["name"] == "Warm Contact"
    assert sheet[0]["icp_total"] > 0


def test_recommendation_never_exceeds_sprint_from_a_call():
    sheet = build_call_sheet([WARM_ROW, COLD_ROW])
    for e in sheet:
        # diagnostic (0 SAR) or sprint (499 SAR) only — never managed/custom off a cold call
        assert e["rung"] in ("diagnostic", "sprint"), e["rung"]


def test_render_markdown_states_manual_and_has_disclaimer():
    sheet = build_call_sheet([WARM_ROW])
    md = render_markdown(sheet, "2026-06-07")
    assert DISCLAIMER in md
    assert "Manual dialing" in md
    assert "No automation" in md


def test_empty_list_is_safe():
    sheet = build_call_sheet([])
    assert sheet == []
    md = render_markdown(sheet, "2026-06-07")
    assert DISCLAIMER in md
