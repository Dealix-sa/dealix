"""Day-0 activation engine — scoring determinism + doctrine guards.

These tests are the enforcement contract for ``scripts/dealix_day0.py``:
the operator pack must never imply guaranteed outcomes, must carry the
bilingual disclaimer and a governance_decision, must take no external
action, and must score deterministically.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "dealix_day0", REPO_ROOT / "scripts" / "dealix_day0.py"
)
assert _spec and _spec.loader
day0 = importlib.util.module_from_spec(_spec)
# Register before exec so dataclasses(slots=True) can resolve the module dict.
sys.modules[_spec.name] = day0
_spec.loader.exec_module(day0)


def _sample() -> day0.Prospect:
    return day0.Prospect(
        name="Sample Co",
        sector="b2b_services",
        city="Riyadh",
        domain="sample.example.sa",
        contact_title="CEO",
        source="inbound_form",
        annual_turnover_sar=2_000_000,
        notes="wants help ranking inbound leads",
    )


def test_scoring_is_deterministic() -> None:
    p = _sample()
    a = day0.score_prospect(p)
    b = day0.score_prospect(p)
    assert a.icp == b.icp
    assert 0 <= a.icp <= 100
    assert a.decision == b.decision
    assert a.recommended_offer == b.recommended_offer


def test_seed_ships_and_is_labelled_sample() -> None:
    seed = REPO_ROOT / "data" / "prospects.seed.csv"
    assert seed.exists(), "the out-of-the-box seed must be committed"
    text = seed.read_text(encoding="utf-8")
    assert "SAMPLE" in text, "seed rows must be clearly labelled as samples"
    assert ".example." in text, "seed must use reserved example domains, never real ones"


def test_recommended_offers_stay_on_the_ladder() -> None:
    rows = day0.load_prospects(REPO_ROOT / "data" / "prospects.seed.csv")
    assert rows, "seed must contain prospects"
    for sp in (day0.score_prospect(p) for p in rows):
        assert sp.recommended_offer in day0.OFFER_LADDER


def test_operator_pack_carries_doctrine(tmp_path: Path) -> None:
    out = tmp_path / "day0"
    result = day0.run_day0(
        prospects_path=REPO_ROOT / "data" / "prospects.seed.csv",
        out_dir=out,
        warm_list_path=None,
        top=5,
        date_str="2026-06-07",
    )
    assert result["ok"] is True

    for name in (
        "OPERATOR_PACK.md",
        "prospects.md",
        "call_list.md",
        "draft_pack.md",
        "scorecard.md",
    ):
        text = (out / name).read_text(encoding="utf-8")
        # Bilingual disclaimer present on every customer-/founder-facing artifact.
        assert "القيمة التقديرية ليست قيمة مُتحقَّقة" in text
        assert "governance_decision" in text
        # No guaranteed-outcome language.
        lowered = text.lower()
        assert "guaranteed outcome" not in lowered or "not guaranteed" in lowered
        assert "we guarantee" not in lowered


def test_no_external_send_language_in_artifacts(tmp_path: Path) -> None:
    out = tmp_path / "day0"
    day0.run_day0(
        prospects_path=REPO_ROOT / "data" / "prospects.seed.csv",
        out_dir=out,
        warm_list_path=None,
        top=5,
        date_str="2026-06-07",
    )
    call_list = (out / "call_list.md").read_text(encoding="utf-8")
    draft_pack = (out / "draft_pack.md").read_text(encoding="utf-8")
    # The system must position the founder as the sender, never auto-send.
    assert (
        "system never dials" in call_list.lower() or "you make every contact" in call_list.lower()
    )
    assert "queued for your approval" in draft_pack.lower()


def test_doctrine_violation_in_notes_blocks_engagement() -> None:
    # A prospect explicitly requesting a forbidden method must not be "accept".
    p = day0.Prospect(
        name="Risky Co",
        sector="b2b_services",
        contact_title="CEO",
        source="inbound_form",
        annual_turnover_sar=3_000_000,
        notes="we want cold whatsapp blasts and scraping of competitor lists",
    )
    sp = day0.score_prospect(p)
    assert sp.decision in ("reject", "refer_out"), sp.decision
