"""Tests for the Full Ops agent hierarchy (the governed agent pyramid)."""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os.agent_registry import clear_for_test
from auto_client_acquisition.full_ops.agent_hierarchy import (
    HIERARCHY_MAX_AUTONOMY_LEVEL,
    HierarchyNode,
    all_nodes,
    get_hierarchy,
    hierarchy_status,
    seed_hierarchy,
)


@pytest.fixture(autouse=True)
def _isolated_registry(monkeypatch, tmp_path):
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_all_nodes_shape() -> None:
    nodes = all_nodes()
    tiers = {n.tier for n in nodes}
    assert tiers == {"orchestrator", "director", "operator"}
    orchestrators = [n for n in nodes if n.tier == "orchestrator"]
    directors = [n for n in nodes if n.tier == "director"]
    operators = [n for n in nodes if n.tier == "operator"]
    assert len(orchestrators) == 1
    assert len(directors) == 5
    assert 15 <= len(operators) <= 25


def test_every_node_at_or_below_l3() -> None:
    for node in all_nodes():
        assert isinstance(node, HierarchyNode)
        assert 0 <= node.autonomy_level <= HIERARCHY_MAX_AUTONOMY_LEVEL == 3


def test_seed_hierarchy_registers_every_node() -> None:
    cards = seed_hierarchy()
    expected = {n.agent_id for n in all_nodes()}
    assert {c.agent_id for c in cards} == expected
    for card in cards:
        assert card.autonomy_level <= 3
        assert card.owner == "founder"
        assert card.kill_switch_owner
        assert card.purpose.strip()


def test_seed_hierarchy_is_idempotent() -> None:
    first = seed_hierarchy()
    second = seed_hierarchy()
    assert {c.agent_id for c in first} == {c.agent_id for c in second}
    assert len(second) == len(all_nodes())


def test_get_hierarchy_tree_shape() -> None:
    tree = get_hierarchy()
    assert set(tree) == {"orchestrator", "directors", "totals"}
    assert tree["orchestrator"]["tier"] == "orchestrator"
    assert len(tree["directors"]) == 5
    operator_total = 0
    for director in tree["directors"]:
        assert director["tier"] == "director"
        assert isinstance(director["operators"], list)
        assert len(director["operators"]) >= 3
        operator_total += len(director["operators"])
    totals = tree["totals"]
    assert totals["directors"] == 5
    assert totals["operators"] == operator_total
    assert totals["max_autonomy_level"] == 3


def test_hierarchy_status_reflects_registration() -> None:
    seed_hierarchy()
    tree = hierarchy_status()
    assert tree["orchestrator"]["status"] != "unregistered"
    for director in tree["directors"]:
        assert director["status"] != "unregistered"
        for op in director["operators"]:
            assert op["status"] != "unregistered"
            assert "capabilities" in op
