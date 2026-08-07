"""Tests for the normalize_graph_edge adapter.

Verifies that operational Revenue Graph edges are correctly bridged to
CanonicalRelationship without escalating authority.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from dealix.company_intelligence import (
    CanonicalRelationship,
    EntityType,
    RelationshipStatus,
    RelationshipType,
)
from dealix.company_intelligence.revenue_graph_adapter import (
    is_relationship_edge,
    normalize_graph_edge,
)


def _edge(**overrides: object) -> SimpleNamespace:
    """Build a duck-typed GraphEdge-like object."""
    values: dict[str, object] = {
        "src_id": "company-001",
        "dst_id": "company-002",
        "edge_type": "similar_to",
        "weight": 0.75,
        "properties": {},
        "last_updated": None,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


# ---------------------------------------------------------------------------
# Basic normalization
# ---------------------------------------------------------------------------


class TestNormalizeGraphEdgeBasic:
    """Core normalization behavior."""

    def test_produces_canonical_relationship(self) -> None:
        rel = normalize_graph_edge(
            _edge(), tenant_id="tenant-a", source_id="revenue_graph"
        )
        assert isinstance(rel, CanonicalRelationship)
        assert rel.tenant_id == "tenant-a"
        assert rel.from_id == "company-001"
        assert rel.to_id == "company-002"
        assert rel.source_id == "revenue_graph"
        assert rel.status == RelationshipStatus.DISCOVERED

    def test_from_and_to_types_default_company(self) -> None:
        rel = normalize_graph_edge(
            _edge(), tenant_id="t", source_id="s"
        )
        assert rel.from_type == EntityType.COMPANY
        assert rel.to_type == EntityType.COMPANY

    def test_custom_entity_types(self) -> None:
        rel = normalize_graph_edge(
            _edge(), tenant_id="t", source_id="s",
            from_type=EntityType.CONTACT,
            to_type=EntityType.COMPANY,
        )
        assert rel.from_type == EntityType.CONTACT
        assert rel.to_type == EntityType.COMPANY

    def test_frozen_immutability(self) -> None:
        rel = normalize_graph_edge(
            _edge(), tenant_id="t", source_id="s"
        )
        with pytest.raises(Exception):
            rel.from_id = "tampered"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Edge type mapping
# ---------------------------------------------------------------------------


class TestEdgeTypeMapping:
    """Verify edge type → RelationshipType mapping."""

    @pytest.mark.parametrize(
        ("edge_type", "expected"),
        [
            ("similar_to", RelationshipType.OTHER),
            ("decides_at", RelationshipType.CUSTOMER),
            ("operates_in", RelationshipType.OTHER),
            ("engaged_via", RelationshipType.CHANNEL_PARTNER),
            ("matches_playbook", RelationshipType.OTHER),
        ],
    )
    def test_known_edge_type_mapping(
        self, edge_type: str, expected: RelationshipType
    ) -> None:
        rel = normalize_graph_edge(
            _edge(edge_type=edge_type), tenant_id="t", source_id="s"
        )
        assert rel.relationship_type == expected

    def test_unknown_type_fallback_to_other(self) -> None:
        rel = normalize_graph_edge(
            _edge(edge_type="unknown_future_edge"), tenant_id="t", source_id="s"
        )
        assert rel.relationship_type == RelationshipType.OTHER


# ---------------------------------------------------------------------------
# Weight → strength mapping
# ---------------------------------------------------------------------------


class TestWeightToStrength:
    """Verify edge weight → strength derivation."""

    @pytest.mark.parametrize(
        ("weight", "expected_strength"),
        [
            (0.0, "unknown"),
            (0.1, "unknown"),
            (0.29, "unknown"),
            (0.3, "cold"),
            (0.49, "cold"),
            (0.5, "warm"),
            (0.69, "warm"),
            (0.7, "active"),
            (0.89, "active"),
            (0.9, "strong"),
            (1.0, "strong"),
        ],
    )
    def test_weight_to_strength(self, weight: float, expected_strength: str) -> None:
        rel = normalize_graph_edge(
            _edge(weight=weight), tenant_id="t", source_id="s"
        )
        assert rel.strength == expected_strength

    def test_weight_used_as_confidence(self) -> None:
        rel = normalize_graph_edge(
            _edge(weight=0.85), tenant_id="t", source_id="s"
        )
        assert rel.confidence == 0.85

    def test_weight_clamped(self) -> None:
        rel = normalize_graph_edge(
            _edge(weight=1.5), tenant_id="t", source_id="s"
        )
        assert rel.confidence == 1.0
        assert rel.strength == "strong"


# ---------------------------------------------------------------------------
# is_relationship_edge filter
# ---------------------------------------------------------------------------


class TestIsRelationshipEdge:
    """Verify edge type filtering."""

    @pytest.mark.parametrize(
        "edge_type",
        ["similar_to", "decides_at", "operates_in", "engaged_via", "matches_playbook"],
    )
    def test_relationship_edges(self, edge_type: str) -> None:
        assert is_relationship_edge(edge_type) is True

    @pytest.mark.parametrize(
        "edge_type",
        ["shows_signal", "received", "responded_with", "originated", "led_to"],
    )
    def test_non_relationship_edges(self, edge_type: str) -> None:
        assert is_relationship_edge(edge_type) is False


# ---------------------------------------------------------------------------
# Description derivation
# ---------------------------------------------------------------------------


class TestDescription:
    """Verify description derivation from edge properties."""

    def test_description_from_properties(self) -> None:
        rel = normalize_graph_edge(
            _edge(properties={"description": "Strong partnership"}),
            tenant_id="t",
            source_id="s",
        )
        assert rel.description == "Strong partnership"

    def test_fallback_description(self) -> None:
        rel = normalize_graph_edge(
            _edge(edge_type="similar_to", properties={}),
            tenant_id="t",
            source_id="s",
        )
        assert "similar_to" in rel.description


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


class TestDeterminism:
    """Verify deterministic relationship_id generation."""

    def test_same_edge_same_id(self) -> None:
        a = normalize_graph_edge(_edge(), tenant_id="t", source_id="s")
        b = normalize_graph_edge(_edge(), tenant_id="t", source_id="s")
        assert a.relationship_id == b.relationship_id

    def test_different_tenant_different_id(self) -> None:
        a = normalize_graph_edge(_edge(), tenant_id="t1", source_id="s")
        b = normalize_graph_edge(_edge(), tenant_id="t2", source_id="s")
        assert a.relationship_id != b.relationship_id

    def test_reversed_edge_different_id(self) -> None:
        a = normalize_graph_edge(
            _edge(src_id="X", dst_id="Y"), tenant_id="t", source_id="s"
        )
        b = normalize_graph_edge(
            _edge(src_id="Y", dst_id="X"), tenant_id="t", source_id="s"
        )
        assert a.relationship_id != b.relationship_id


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidation:
    """Verify input validation."""

    def test_rejects_empty_src_id(self) -> None:
        with pytest.raises(ValueError, match="src_id"):
            normalize_graph_edge(
                _edge(src_id=""), tenant_id="t", source_id="s"
            )

    def test_rejects_empty_dst_id(self) -> None:
        with pytest.raises(ValueError, match="dst_id"):
            normalize_graph_edge(
                _edge(dst_id=""), tenant_id="t", source_id="s"
            )

    def test_rejects_self_loop(self) -> None:
        with pytest.raises(ValueError, match="differ"):
            normalize_graph_edge(
                _edge(src_id="same", dst_id="same"),
                tenant_id="t",
                source_id="s",
            )
