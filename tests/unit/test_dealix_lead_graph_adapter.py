"""Unit tests for the Saudi Lead Graph adapter — doctrine-safe, no PII.

Guards the Article 4 / 8 invariants the adapter must never break:
- relationship-strength sources stay HONEST (never fabricated warmth);
- governance-held / high-risk rows are dropped;
- no contact PII ever leaves the CSV.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import dealix_lead_graph_adapter as adapter  # noqa: E402

MASTER = REPO_ROOT / "docs" / "ops" / "lead_machine" / "SAUDI_LEAD_GRAPH_MASTER.csv"

SAFE_SOURCES = {adapter.SOURCE_MANUAL_RESEARCH, adapter.SOURCE_PUBLIC_BUSINESS}
FORBIDDEN_SOURCES = {
    "warm_intro",
    "partner_referral",
    "founder_intro",
    "inbound_form",
    "cold_outreach",
    "scraping",
    "purchased_list",
    "linkedin_automation",
}

_HEADER = (
    "company,sector,website,country,opportunity_type,source,risk_score,priority,"
    "decision_roles,suggested_channel,recommended_action,first_message_angle,"
    "objection_prediction,offer_recommended,fit_score,intent_score\n"
)


def _write_csv(path: Path, rows: list[str]) -> Path:
    path.write_text(_HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    return path


# ── Real curated graph ────────────────────────────────────────────────


def test_real_graph_loads_and_sources_are_safe():
    candidates, _ = adapter.load_lead_graph_candidates(MASTER)
    assert len(candidates) > 0
    sources = {c.source for c in candidates}
    assert sources <= SAFE_SOURCES, f"unsafe source leaked: {sources - SAFE_SOURCES}"
    assert not (sources & FORBIDDEN_SOURCES)


def test_real_graph_never_emits_contact_pii():
    candidates, _ = adapter.load_lead_graph_candidates(MASTER)
    assert all(c.contact_name == "" for c in candidates)


def test_real_graph_is_deterministic():
    a, _ = adapter.load_lead_graph_candidates(MASTER)
    b, _ = adapter.load_lead_graph_candidates(MASTER)
    assert [c.name for c in a] == [c.name for c in b]


def test_rich_map_covers_every_candidate():
    candidates, rich = adapter.load_lead_graph_candidates(MASTER)
    names = {c.name for c in candidates}
    assert names <= set(rich), "rich_map must carry every surfaced candidate"
    # the call sheet relies on these keys existing (possibly empty strings)
    sample = next(iter(rich.values()))
    for key in ("suggested_channel", "first_message_angle", "offer_recommended", "fit_score"):
        assert key in sample


def test_exclude_held_reduces_the_set():
    kept, _ = adapter.load_lead_graph_candidates(MASTER, exclude_held=True)
    everything, _ = adapter.load_lead_graph_candidates(MASTER, exclude_held=False)
    assert len(kept) <= len(everything)
    # held rows must not appear in the kept set
    kept_names = {c.name for c in kept}
    assert "Herfy" not in kept_names  # known HOLD / governance-heavy row


# ── Synthetic rows (deterministic exclusion + mapping) ─────────────────


def test_hold_and_high_risk_rows_excluded(tmp_path):
    csv_path = _write_csv(
        tmp_path / "leads.csv",
        [
            "GoodCo,SaaS,goodco.sa,SA,DIRECT_CUSTOMER,public_page,15,P1,CEO,LINKEDIN_MANUAL,PREPARE_DM,angle,obj,offer,80,60",
            "HeldCo,Gov,heldco.sa,SA,DIRECT_CUSTOMER,public_page,20,P2,CEO,HOLD_FOR_APPROVAL,HOLD,angle,obj,offer,50,40",
            "RiskyCo,Bank,riskyco.sa,SA,DIRECT_CUSTOMER,public_page,85,P2,CEO,LINKEDIN_MANUAL,PREPARE_DM,angle,obj,offer,55,40",
        ],
    )
    kept, _ = adapter.load_lead_graph_candidates(csv_path, exclude_held=True)
    names = {c.name for c in kept}
    assert names == {"GoodCo"}

    everything, _ = adapter.load_lead_graph_candidates(csv_path, exclude_held=False)
    assert {c.name for c in everything} == {"GoodCo", "HeldCo", "RiskyCo"}


def test_channel_maps_to_honest_source(tmp_path):
    csv_path = _write_csv(
        tmp_path / "leads.csv",
        [
            "LinkedInCo,SaaS,li.sa,SA,DIRECT_CUSTOMER,public_page,10,P1,CEO,LINKEDIN_MANUAL,PREPARE_DM,a,o,off,70,50",
            "PartnerCo,Platform,p.sa,SA,STRATEGIC_PARTNER,public_page,10,P2,CEO,PARTNER_INTRO,PREPARE_PARTNER_PITCH,a,o,off,55,40",
        ],
    )
    kept, _ = adapter.load_lead_graph_candidates(csv_path)
    by_name = {c.name: c for c in kept}
    assert by_name["LinkedInCo"].source == adapter.SOURCE_MANUAL_RESEARCH
    assert by_name["PartnerCo"].source == adapter.SOURCE_PUBLIC_BUSINESS
    # neither is ever labelled "warm"
    assert all(c.source not in FORBIDDEN_SOURCES for c in kept)


def test_decision_role_maps_to_title_without_name(tmp_path):
    csv_path = _write_csv(
        tmp_path / "leads.csv",
        [
            "RoleCo,SaaS,r.sa,SA,DIRECT_CUSTOMER,public_page,10,P1,Founder,LINKEDIN_MANUAL,PREPARE_DM,a,o,off,70,50"
        ],
    )
    kept, _ = adapter.load_lead_graph_candidates(csv_path)
    assert kept[0].contact_title == "Founder"
    assert kept[0].contact_name == ""
