"""Offline tests for the Founder First-Revenue Cockpit.

No network, no real ledger reads: the pipeline side is injected as an empty
stub so the build is deterministic and we can assert that absent data renders as
honest zeros (never fabricated). The warm-list fixture has exactly one
ready-to-close row (warm owner -> ACCEPT), one reject row, and one
doctrine-violating row, so the ready count must be exactly 1.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import scripts.dealix_first_revenue_cockpit as cockpit_mod

_HEADER = ["name", "role", "company", "sector", "relationship", "city", "linkedin_url", "notes"]

# One ACCEPT (warm owner), one REJECT (high client-risk / refer-out style),
# one doctrine-violating row (cold-whatsapp language in notes).
_ROWS: list[dict[str, str]] = [
    {
        "name": "Ready Owner",
        "role": "COO",
        "company": "Ready Co",
        "sector": "b2b_services",
        "relationship": "warm",
        "city": "Riyadh",
        "linkedin_url": "",
        "notes": "warm intro at LEAP",
    },
    {
        "name": "Cold Analyst",
        "role": "Analyst",
        "company": "Cold Co",
        "sector": "b2b_services",
        "relationship": "cold",
        "city": "Riyadh",
        "linkedin_url": "",
        "notes": "",
    },
    {
        "name": "Doctrine Breaker",
        "role": "CEO",
        "company": "Spam Co",
        "sector": "b2b_services",
        "relationship": "warm",
        "city": "Riyadh",
        "linkedin_url": "",
        "notes": "wants cold whatsapp blast leads",
    },
]


def _empty_pipeline(_customer_id: str) -> dict[str, Any]:
    """A pipeline reader with every ledger empty (honest zeros)."""
    return {
        "leads_waiting_24h_plus": {"count": 0, "items": []},
        "recent_proof_events": {"count": 0, "items": []},
        "capital_assets_this_week": {"count": 0, "items": []},
        "renewals_due_next_7d": {"count": 0, "items": []},
        "friction_high_7d": {"total": 0, "high": 0, "top_3_kinds": []},
        "retainer_eligible": {"count": 0, "items": [], "note": "no_adoption_ledger_wired"},
    }


def _write_csv(tmp_path: Path) -> Path:
    path = tmp_path / "warm_list.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_HEADER)
        writer.writeheader()
        for row in _ROWS:
            writer.writerow(row)
    return path


def test_assess_warm_list_ready_count_is_one() -> None:
    warm = cockpit_mod.assess_warm_list(_ROWS)
    assert warm["ready_count"] == 1
    assert warm["total"] == 3
    # The two non-ready rows are skips (reject + doctrine), none diagnostic-only.
    assert warm["skip_count"] == 2
    assert warm["diagnostic_count"] == 0
    ready_names = {r["name"] for r in warm["ready"]}
    assert ready_names == {"Ready Owner"}


def test_reject_and_doctrine_rows_not_in_ready() -> None:
    warm = cockpit_mod.assess_warm_list(_ROWS)
    ready_companies = {r["company"] for r in warm["ready"]}
    assert "Spam Co" not in ready_companies  # doctrine violation
    assert "Cold Co" not in ready_companies  # refer-out
    # The doctrine-violating row is recorded with its violation, in skip.
    skip_breaker = [r for r in warm["skip"] if r["company"] == "Spam Co"]
    assert skip_breaker and skip_breaker[0]["doctrine_violations"]


def test_build_cockpit_has_three_sections_and_disclaimer() -> None:
    cockpit = cockpit_mod.build_cockpit(
        _ROWS,
        csv_label="data/warm_list.csv.template",
        is_demo=True,
        pipeline_reader=_empty_pipeline,
    )
    board = cockpit["markdown"]
    assert cockpit_mod._SECTION_WARM in board
    assert cockpit_mod._SECTION_PIPELINE in board
    assert cockpit_mod._SECTION_ACTIONS in board
    # Bilingual disclaimer present.
    assert "Estimated value is not Verified value" in board
    assert "القيمة التقديرية ليست قيمة مُتحقَّقة" in board
    # Demo label surfaced.
    assert "DEMO DATA" in board


def test_top_actions_present_and_lead_with_ready_close() -> None:
    cockpit = cockpit_mod.build_cockpit(
        _ROWS,
        csv_label="data/warm_list.csv.template",
        is_demo=True,
        pipeline_reader=_empty_pipeline,
    )
    actions = cockpit["top_actions"]
    assert 1 <= len(actions) <= 3
    # The first action must be to generate close packets for the 1 ready contact,
    # and it must point to the warm-list packet generator command.
    first = actions[0]
    assert "1 ready warm contact" in first["en"]
    assert "dealix_warm_list_packets.py" in first["command"]


def test_no_fabricated_pipeline_numbers_when_ledgers_empty() -> None:
    cockpit = cockpit_mod.build_cockpit(
        _ROWS,
        csv_label="data/warm_list.csv.template",
        is_demo=True,
        pipeline_reader=_empty_pipeline,
    )
    pipe = cockpit["pipeline"]
    assert pipe["leads_waiting_24h_plus"]["count"] == 0
    assert pipe["recent_proof_events"]["count"] == 0
    assert pipe["capital_assets_this_week"]["count"] == 0
    assert pipe["renewals_due_next_7d"]["count"] == 0
    assert pipe["friction_high_7d"]["high"] == 0
    assert pipe["retainer_eligible"]["count"] == 0
    board = cockpit["markdown"]
    # The board explicitly states the zeros are honest, not fabricated.
    assert "honest zeros" in board
    # The retainer line carries its honest "not wired" note rather than a number.
    assert "no_adoption_ledger_wired" in board


def test_render_is_deterministic_for_same_input() -> None:
    a = cockpit_mod.render_markdown(
        cockpit_mod.build_cockpit(
            _ROWS,
            csv_label="x.csv",
            pipeline_reader=_empty_pipeline,
        )
    )
    b = cockpit_mod.render_markdown(
        cockpit_mod.build_cockpit(
            _ROWS,
            csv_label="x.csv",
            pipeline_reader=_empty_pipeline,
        )
    )
    # Strip the only non-deterministic lines (timestamps) before comparing.
    def _strip(md: str) -> list[str]:
        return [ln for ln in md.splitlines() if "Generated:" not in ln]

    assert _strip(a) == _strip(b)


def test_main_writes_board_from_template(tmp_path: Path) -> None:
    out = tmp_path / "board.md"
    # Point at a missing csv so it falls back to the repo template (DEMO).
    rc = cockpit_mod.main(
        ["--csv", str(tmp_path / "does_not_exist.csv"), "--out", str(out)]
    )
    assert rc == 0
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert cockpit_mod._SECTION_WARM in text
    assert "Estimated value is not Verified value" in text


def test_main_with_real_csv(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path)
    out = tmp_path / "real_board.md"
    rc = cockpit_mod.main(["--csv", str(csv_path), "--out", str(out)])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    # Exactly the one ready contact should be listed in the ready table.
    assert "Ready Co" in text
    assert "Spam Co" not in text.split(_section_marker := cockpit_mod._SECTION_PIPELINE)[0]
