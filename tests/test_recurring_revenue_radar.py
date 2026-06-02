"""Tests for the Recurring Revenue Radar — engine, doctrine, ledger, and API.

The radar turns one-off Sprints into recurring retainers. These tests pin the
three non-negotiables it must honour:
  * no revenue before paid,
  * proof before upsell,
  * approval-first (draft_only) actions.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os import policy_check_draft
from dealix.revenue_ops_autopilot.recurring_revenue_radar import (
    RETAINER_TIER_MRR_SAR,
    RecurringRevenueRadarLedger,
    render_radar_markdown,
    run_radar,
)
from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerTier


def _eligible(account_id: str, **over) -> dict:
    base = {
        "account_id": account_id,
        "company_name": f"Co {account_id}",
        "proof_level": "L2",
        "satisfaction_score": 8.0,
        "measurable_result_achieved": True,
        "current_mrr_sar": 0.0,
        "latest_invoice_paid": False,
    }
    base.update(over)
    return base


# ── Engine: eligibility → opportunity ──────────────────────────────────


def test_eligible_account_becomes_opportunity_with_tier_and_incremental() -> None:
    summary = run_radar([_eligible("a1", proof_level="L2", satisfaction_score=8.0)])
    assert summary.opportunities_count == 1
    opp = summary.opportunities[0]
    assert opp.is_expansion_opportunity is True
    assert opp.recommended_tier == "growth_3999"  # L2 + sat>=8
    assert opp.recommended_tier_mrr_sar == 3999
    # No paid current MRR → full tier price is the incremental opportunity.
    assert opp.expected_incremental_mrr_sar == 3999
    assert opp.expected_incremental_arr_sar == 3999 * 12


def test_scale_tier_for_high_proof_and_satisfaction() -> None:
    summary = run_radar([_eligible("a1", proof_level="L3", satisfaction_score=9.0)])
    assert summary.opportunities[0].recommended_tier == "scale_4999"
    assert summary.opportunities[0].recommended_tier_mrr_sar == 4999


# ── Doctrine: proof before upsell ──────────────────────────────────────


@pytest.mark.parametrize(
    "over",
    [
        {"proof_level": "L0"},  # proof too low
        {"satisfaction_score": 6.0},  # satisfaction below threshold
        {"measurable_result_achieved": False},  # no measurable result
    ],
)
def test_ineligible_accounts_are_not_opportunities(over: dict) -> None:
    summary = run_radar([_eligible("a1", **over)])
    opp = summary.opportunities[0]
    assert opp.is_expansion_opportunity is False
    assert opp.expected_incremental_mrr_sar == 0.0
    assert opp.recommended_tier is None
    assert opp.blockers  # must explain why


# ── Doctrine: no revenue before paid ───────────────────────────────────


def test_unpaid_current_mrr_excluded_from_realised_and_baseline() -> None:
    # Account "pays" 2999 but the invoice is NOT paid → must not count as
    # realised revenue, and must not reduce the expansion baseline.
    summary = run_radar(
        [_eligible("a1", current_mrr_sar=2999.0, latest_invoice_paid=False)]
    )
    assert summary.realized_mrr_sar == 0.0
    opp = summary.opportunities[0]
    assert opp.current_mrr_sar == 0.0  # paid-only baseline
    assert "unverified_current_mrr_excluded_until_paid" in opp.blockers
    # Incremental computed against a zero baseline (not 2999).
    assert opp.expected_incremental_mrr_sar == opp.recommended_tier_mrr_sar


def test_paid_current_mrr_counts_and_reduces_incremental() -> None:
    # Paid 2999 today, eligible for growth_3999 → incremental is only 1000.
    summary = run_radar(
        [_eligible("a1", current_mrr_sar=2999.0, latest_invoice_paid=True)]
    )
    assert summary.realized_mrr_sar == 2999.0
    assert summary.realized_arr_sar == 2999.0 * 12
    opp = summary.opportunities[0]
    assert opp.current_mrr_sar == 2999.0
    assert opp.expected_incremental_mrr_sar == 3999 - 2999


def test_account_at_or_above_tier_is_retention_not_expansion() -> None:
    # Paid 4999 already and only eligible for growth_3999 → no upside.
    summary = run_radar(
        [_eligible("a1", current_mrr_sar=4999.0, latest_invoice_paid=True)]
    )
    opp = summary.opportunities[0]
    assert opp.is_expansion_opportunity is False
    assert opp.expected_incremental_mrr_sar == 0.0
    assert "already_at_or_above_recommended_tier" in opp.blockers


# ── Ranking + portfolio totals ─────────────────────────────────────────


def test_ranking_is_deterministic_and_by_incremental_mrr() -> None:
    accounts = [
        _eligible("low", proof_level="L1", satisfaction_score=7.0),  # starter 2999
        _eligible("high", proof_level="L3", satisfaction_score=9.0),  # scale 4999
        _eligible("mid", proof_level="L2", satisfaction_score=8.0),  # growth 3999
    ]
    s1 = run_radar(accounts)
    s2 = run_radar(list(reversed(accounts)))
    order1 = [o.account_id for o in s1.opportunities]
    order2 = [o.account_id for o in s2.opportunities]
    assert order1 == order2 == ["high", "mid", "low"]
    assert s1.pipeline_incremental_mrr_sar == 4999 + 3999 + 2999
    assert s1.by_tier == {"scale_4999": 1, "growth_3999": 1, "starter_2999": 1}


def test_empty_portfolio_is_all_zeros() -> None:
    summary = run_radar([])
    assert summary.accounts_total == 0
    assert summary.opportunities_count == 0
    assert summary.realized_mrr_sar == 0.0
    assert summary.pipeline_incremental_mrr_sar == 0.0
    assert summary.opportunities == []


# ── Invariants that protect against silent drift ───────────────────────


def test_tier_mrr_map_matches_tier_identifiers() -> None:
    # The tier id embeds its price; the map must never drift from it.
    for tier, mrr in RETAINER_TIER_MRR_SAR.items():
        assert tier.endswith(str(mrr)), f"{tier} price drifted from {mrr}"
    assert set(RETAINER_TIER_MRR_SAR) == set(RetainerTier.__args__)  # type: ignore[attr-defined]


def test_every_opportunity_is_draft_only_and_approval_first() -> None:
    summary = run_radar([_eligible("a1"), _eligible("a2", proof_level="L0")])
    for opp in summary.opportunities:
        assert opp.requires_approval is True
        assert opp.mode == "draft_only"
    assert summary.guardrails["no_revenue_before_paid"] is True
    assert summary.guardrails["approval_first"] is True


def test_generated_drafts_pass_doctrine_policy_check() -> None:
    # Every AR/EN next-action must survive the non-negotiables policy gate
    # (no guarantees, no cold-channel language, etc.).
    summary = run_radar(
        [
            _eligible("a1", proof_level="L3", satisfaction_score=9.0),
            _eligible("a2", proof_level="L0"),
            _eligible("a3", current_mrr_sar=4999, latest_invoice_paid=True),
        ]
    )
    for opp in summary.opportunities:
        assert policy_check_draft(opp.next_action_ar).allowed is True
        assert policy_check_draft(opp.next_action_en).allowed is True


# ── Markdown render ────────────────────────────────────────────────────


def test_markdown_render_contains_key_sections() -> None:
    summary = run_radar([_eligible("a1", proof_level="L2", satisfaction_score=8.0)])
    md = render_radar_markdown(summary)
    assert "Recurring Revenue Radar" in md
    assert "PIPELINE" in md
    assert "Governance" in md
    assert "draft_only" in md
    # The pipeline figure must be visible.
    assert "3,999" in md


def test_markdown_handles_no_opportunities() -> None:
    md = render_radar_markdown(run_radar([_eligible("a1", proof_level="L0")]))
    assert "No expansion opportunities today" in md


# ── Ledger round-trip ──────────────────────────────────────────────────


def test_ledger_append_and_read(tmp_path) -> None:
    ledger = RecurringRevenueRadarLedger(ledger_path=tmp_path / "radar_log.json")
    assert ledger.latest() is None
    summary = run_radar([_eligible("a1", proof_level="L2", satisfaction_score=8.0)])
    rec = ledger.append_run(summary)
    assert rec["opportunities_count"] == 1
    assert rec["pipeline_incremental_mrr_sar"] == 3999
    assert len(rec["top"]) == 1
    ledger.append_run(summary)  # exercise append path twice
    assert len(ledger.history(limit=10)) == 2
    assert ledger.latest()["pipeline_incremental_mrr_sar"] == 3999


# ── API surface ────────────────────────────────────────────────────────

# Admin-guarded endpoints: configure a key and send it (dev-mode would reject a
# *missing* key). This mirrors the pattern in test_enterprise_pmo.py.
_ADMIN = {"X-Admin-API-Key": "test_radar_admin_key"}


@pytest.fixture
def _admin_env(monkeypatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEYS", "test_radar_admin_key")


@pytest.mark.asyncio
async def test_api_radar_returns_ranked_summary(async_client, _admin_env) -> None:
    payload = {
        "accounts": [
            _eligible("high", proof_level="L3", satisfaction_score=9.0),
            _eligible("low", proof_level="L1", satisfaction_score=7.0),
        ]
    }
    resp = await async_client.post(
        "/api/v1/recurring-revenue/radar", json=payload, headers=_ADMIN
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["opportunities_count"] == 2
    assert data["pipeline_incremental_mrr_sar"] == 4999 + 2999
    assert data["opportunities"][0]["account_id"] == "high"
    assert data["guardrails"]["no_revenue_before_paid"] is True


@pytest.mark.asyncio
async def test_api_doctrine_exposes_tiers_and_guardrails(async_client, _admin_env) -> None:
    resp = await async_client.get("/api/v1/recurring-revenue/doctrine", headers=_ADMIN)
    assert resp.status_code == 200
    data = resp.json()
    assert data["tier_mrr_sar"]["growth_3999"] == 3999
    assert data["eligibility"]["min_proof_level"] == "L1"
    assert data["guardrails"]["proof_before_upsell"] is True


@pytest.mark.asyncio
async def test_api_markdown_endpoint(async_client, _admin_env) -> None:
    payload = {"accounts": [_eligible("a1", proof_level="L2", satisfaction_score=8.0)]}
    resp = await async_client.post(
        "/api/v1/recurring-revenue/radar/markdown", json=payload, headers=_ADMIN
    )
    assert resp.status_code == 200
    assert "Recurring Revenue Radar" in resp.json()["markdown"]


@pytest.mark.asyncio
async def test_api_rejects_unknown_fields(async_client, _admin_env) -> None:
    # extra="forbid" guards against typo'd / injected fields.
    payload = {"accounts": [{**_eligible("a1"), "surprise": 1}]}
    resp = await async_client.post(
        "/api/v1/recurring-revenue/radar", json=payload, headers=_ADMIN
    )
    assert resp.status_code == 422
