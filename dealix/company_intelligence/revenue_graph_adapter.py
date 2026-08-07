"""Fail-closed adapter from Revenue Graph edges to canonical Relationship truth.

Bridges ``auto_client_acquisition.revenue_graph.graph.GraphEdge``
into ``CanonicalRelationship`` without escalating authority. The operational
Revenue Graph carries typed, weighted edges between nodes; this adapter
normalises relevant edges into the tenant-scoped, evidence-graded,
deduplicated shape the Company Intelligence relationship layer expects.

Key constraints:
  - Only company-to-company and company-to-contact edge types are bridged.
    Non-relationship edges (e.g. ``shows_signal``, ``received``, ``led_to``)
    are filtered out — they map to other canonical entities (Signal, Draft,
    Outcome).
  - Edge types map to canonical ``RelationshipType`` via an explicit mapping;
    unknown types fail-closed to ``OTHER``.
  - Strength is derived from the edge weight: < 0.3 → unknown,
    < 0.5 → cold, < 0.7 → warm, < 0.9 → active, ≥ 0.9 → strong.
  - The adapter never escalates relationship status above ``DISCOVERED``.
"""
from __future__ import annotations

from typing import Any

from dealix.company_intelligence.relationship_contracts import (
    CanonicalRelationship,
    EntityType,
    RelationshipStatus,
    RelationshipType,
    build_relationship,
)

# ---------------------------------------------------------------------------
# Edge type → relationship mapping
# ---------------------------------------------------------------------------

_EDGE_TYPE_MAP: dict[str, RelationshipType] = {
    "similar_to": RelationshipType.OTHER,
    "decides_at": RelationshipType.CUSTOMER,
    "operates_in": RelationshipType.OTHER,
    "engaged_via": RelationshipType.CHANNEL_PARTNER,
    "matches_playbook": RelationshipType.OTHER,
}

# Edge types that represent relationships between graph entities.
# Other edge types (shows_signal, received, responded_with, originated,
# led_to) represent actions, signals, or outcomes — not relationships.
_RELATIONSHIP_EDGE_TYPES = frozenset(_EDGE_TYPE_MAP.keys())


def _resolve_relationship_type(edge_type: str) -> RelationshipType:
    """Map an operational edge type to a canonical RelationshipType.

    Unknown types fail-closed to ``OTHER``.
    """
    return _EDGE_TYPE_MAP.get(edge_type.lower().strip(), RelationshipType.OTHER)


def _weight_to_strength(weight: float) -> str:
    """Derive relationship strength from edge weight.

    Weight thresholds:
      < 0.3 → unknown
      < 0.5 → cold
      < 0.7 → warm
      < 0.9 → active
      ≥ 0.9 → strong
    """
    if weight < 0.3:
        return "unknown"
    if weight < 0.5:
        return "cold"
    if weight < 0.7:
        return "warm"
    if weight < 0.9:
        return "active"
    return "strong"


def is_relationship_edge(edge_type: str) -> bool:
    """Check whether an edge type represents a relationship.

    Non-relationship edges (signals, messages, outcomes) return False.
    """
    return edge_type.lower().strip() in _RELATIONSHIP_EDGE_TYPES


def normalize_graph_edge(
    edge: Any,
    *,
    tenant_id: str,
    source_id: str,
    from_type: EntityType = EntityType.COMPANY,
    to_type: EntityType = EntityType.COMPANY,
) -> CanonicalRelationship:
    """Normalize a Revenue Graph ``GraphEdge`` into a ``CanonicalRelationship``.

    Parameters
    ----------
    edge:
        A ``GraphEdge`` or any duck-typed object with ``src_id``, ``dst_id``,
        ``edge_type``, ``weight``, and optionally ``properties``.
    tenant_id:
        The tenant scope for the resulting canonical relationship.
    source_id:
        Source identity for provenance tracking.
    from_type:
        Entity type of the source node (default: COMPANY).
    to_type:
        Entity type of the destination node (default: COMPANY).
    """
    src_id = str(getattr(edge, "src_id", "") or "").strip()
    dst_id = str(getattr(edge, "dst_id", "") or "").strip()
    if not src_id:
        raise ValueError("edge must have a non-empty src_id")
    if not dst_id:
        raise ValueError("edge must have a non-empty dst_id")
    if src_id == dst_id:
        raise ValueError("edge src_id and dst_id must differ")

    edge_type_raw = str(getattr(edge, "edge_type", "") or "").strip()
    relationship_type = _resolve_relationship_type(edge_type_raw)

    raw_weight = getattr(edge, "weight", 0.5)
    weight = float(raw_weight if raw_weight is not None else 0.5)
    weight = max(0.0, min(1.0, weight))  # clamp
    strength = _weight_to_strength(weight)

    # Use weight as confidence (clamped to 0.0–1.0)
    confidence = weight

    # Description from edge properties
    properties = dict(getattr(edge, "properties", {}) or {})
    description = str(properties.get("description", ""))
    if not description and edge_type_raw:
        description = f"Revenue graph edge: {edge_type_raw}"

    return build_relationship(
        tenant_id=tenant_id,
        from_id=src_id,
        from_type=from_type,
        to_id=dst_id,
        to_type=to_type,
        relationship_type=relationship_type,
        source_id=source_id,
        status=RelationshipStatus.DISCOVERED,
        strength=strength,
        description=description,
        confidence=confidence,
    )
