"""Tests for the strategic agent tier."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os.agent_registry import clear_for_test
from auto_client_acquisition.strategy_autonomy.strategic_hierarchy import (
    OPERATIONAL_ORCHESTRATOR_ID,
    STRATEGIC_MAX_AUTONOMY_LEVEL,
    StrategicHierarchyNode,
    all_strategic_nodes,
    get_strategic_tier,
    seed_strategic_tier,
    strategic_tier_status,
)


@pytest.fixture(autouse=True)
def _isolated():
    clear_for_test()
    yield
    clear_for_test()


def test_tier_has_one_ceo_and_four_directors() -> None:
    nodes = all_strategic_nodes()
    ceos = [n for n in nodes if n.tier == "ceo"]
    directors = [n for n in nodes if n.tier == "director"]
    assert len(ceos) == 1
    assert len(directors) == 4
    assert ceos[0].agent_id == "sa_ceo_strategic_orchestrator"


def test_ceo_delegates_to_full_ops_orchestrator() -> None:
    ceo = next(n for n in all_strategic_nodes() if n.tier == "ceo")
    assert OPERATIONAL_ORCHESTRATOR_ID in ceo.delegates_to
    assert OPERATIONAL_ORCHESTRATOR_ID == "fo_orchestrator_chief_of_staff"


def test_all_nodes_l3_or_below() -> None:
    for node in all_strategic_nodes():
        assert node.autonomy_level <= STRATEGIC_MAX_AUTONOMY_LEVEL
        assert node.autonomy_level <= 3
        assert isinstance(node, StrategicHierarchyNode)


def test_all_nodes_use_sa_prefix() -> None:
    for node in all_strategic_nodes():
        assert node.agent_id.startswith("sa_")


def test_seed_is_idempotent() -> None:
    first = seed_strategic_tier()
    second = seed_strategic_tier()
    assert len(first) == len(second) == 5
    assert {c.agent_id for c in first} == {c.agent_id for c in second}


def test_get_strategic_tier_shape() -> None:
    tree = get_strategic_tier()
    assert "ceo" in tree
    assert len(tree["board_directors"]) == 4
    assert tree["delegates_to_operational"] == "fo_orchestrator_chief_of_staff"
    assert tree["totals"]["board_directors"] == 4
    assert tree["totals"]["max_autonomy_level"] == 3


def test_strategic_tier_status_annotates_registry() -> None:
    seed_strategic_tier()
    tree = strategic_tier_status()
    assert tree["ceo"]["status"] != "unregistered"
    for director in tree["board_directors"]:
        assert director["status"] != "unregistered"


def test_status_unregistered_before_seed() -> None:
    tree = strategic_tier_status()
    assert tree["ceo"]["status"] == "unregistered"
