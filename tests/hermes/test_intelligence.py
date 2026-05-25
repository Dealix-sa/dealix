"""Intelligence plane graphs — signals, outcomes, revenue, attribution."""

from __future__ import annotations

import pytest

from dealix.hermes.intelligence_plane import (
    AttributionGraph,
    AttributionLink,
    Outcome,
    OutcomeGraph,
    RevenueGraph,
    Signal,
    SignalGraph,
)
from dealix.hermes.intelligence_plane.attribution_graph import (
    AttributionDimension,
)
from dealix.hermes.intelligence_plane.outcome_graph import OutcomeKind
from dealix.hermes.intelligence_plane.revenue_graph import RevenueRecord


# ────────────────────────────────────────────────────────────────
# Signal graph
# ────────────────────────────────────────────────────────────────


def test_signal_graph_link_and_query_for_opportunity() -> None:
    graph = SignalGraph()
    signal = Signal(
        signal_id="sig_1",
        source="website_form",
        payload={"email": "lead@example.com"},
    )
    graph.add(signal)
    graph.link_to_opportunity("sig_1", "opp_1")

    signals = graph.signals_for_opportunity("opp_1")
    assert len(signals) == 1
    assert signals[0].signal_id == "sig_1"


# ────────────────────────────────────────────────────────────────
# Outcome graph
# ────────────────────────────────────────────────────────────────


def test_outcome_graph_record_and_lookup() -> None:
    graph = OutcomeGraph()
    outcome = Outcome(
        outcome_id="out_1",
        execution_id="exe_1",
        kind=OutcomeKind.PROPOSAL_WON,
        value_sar=5000,
    )
    graph.record(outcome)
    assert [o.outcome_id for o in graph.for_execution("exe_1")] == ["out_1"]


def test_outcome_graph_win_loss_by_offer_counts_correctly() -> None:
    graph = OutcomeGraph()
    graph.record(Outcome("o1", "exe_w1", OutcomeKind.PROPOSAL_WON, value_sar=1))
    graph.record(Outcome("o2", "exe_w2", OutcomeKind.PROPOSAL_WON, value_sar=2))
    graph.record(Outcome("o3", "exe_l1", OutcomeKind.PROPOSAL_LOST, value_sar=0))
    graph.record(Outcome("o4", "exe_neut", OutcomeKind.NO_RESPONSE, value_sar=0))

    lookup = {
        "exe_w1": "offer_A",
        "exe_w2": "offer_A",
        "exe_l1": "offer_A",
        "exe_neut": "offer_A",
    }
    stats = graph.win_loss_by_offer(lookup)
    assert stats == {"offer_A": {"won": 2, "lost": 1}}


# ────────────────────────────────────────────────────────────────
# Revenue graph
# ────────────────────────────────────────────────────────────────


def test_revenue_graph_rejects_invalid_verification_source() -> None:
    graph = RevenueGraph()
    bad = RevenueRecord(
        revenue_id="r_bad",
        customer_id="cust_1",
        offer_id="offer_1",
        amount_sar=1000,
        verification_source="meeting_booked",
    )
    with pytest.raises(ValueError):
        graph.record(bad)


def test_revenue_graph_aggregates_totals() -> None:
    graph = RevenueGraph()
    graph.record(
        RevenueRecord(
            revenue_id="r1",
            customer_id="cust_1",
            offer_id="offer_A",
            amount_sar=3000,
            verification_source="payment",
        )
    )
    graph.record(
        RevenueRecord(
            revenue_id="r2",
            customer_id="cust_1",
            offer_id="offer_B",
            amount_sar=7000,
            verification_source="signed_agreement",
        )
    )
    graph.record(
        RevenueRecord(
            revenue_id="r3",
            customer_id="cust_2",
            offer_id="offer_A",
            amount_sar=2000,
            verification_source="invoice",
        )
    )

    assert graph.total_by_offer() == {"offer_A": 5000, "offer_B": 7000}
    assert graph.total_by_customer() == {"cust_1": 10000, "cust_2": 2000}


# ────────────────────────────────────────────────────────────────
# Attribution graph
# ────────────────────────────────────────────────────────────────


def test_attribution_graph_rejects_weight_above_one() -> None:
    graph = AttributionGraph()
    bad = AttributionLink(
        link_id="al_bad",
        revenue_id="r_1",
        dimension=AttributionDimension.CHANNEL,
        dimension_value="email",
        weight=1.5,
    )
    with pytest.raises(ValueError):
        graph.attribute(bad)


def test_attribution_graph_rejects_weights_exceeding_one_per_revenue() -> None:
    graph = AttributionGraph()
    first = AttributionLink(
        link_id="al_1",
        revenue_id="r_1",
        dimension=AttributionDimension.CHANNEL,
        dimension_value="email",
        weight=0.7,
    )
    second = AttributionLink(
        link_id="al_2",
        revenue_id="r_1",
        dimension=AttributionDimension.CHANNEL,
        dimension_value="referral",
        weight=0.4,
    )
    graph.attribute(first)
    with pytest.raises(ValueError):
        graph.attribute(second)
