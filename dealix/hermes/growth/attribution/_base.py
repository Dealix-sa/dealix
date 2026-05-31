"""Shared in-memory store for verified-revenue attribution dimensions."""

from __future__ import annotations

from dataclasses import dataclass, field

_RECORDS: dict[str, list["AttributionRecord"]] = {}


@dataclass(frozen=True)
class AttributionRecord:
    dimension: str
    key: str
    revenue_sar: float
    evidence_pack_id: str
    metadata: dict[str, str] = field(default_factory=dict)


def attribute(dimension: str, key: str, revenue_sar: float, evidence_pack_id: str, metadata: dict[str, str] | None = None) -> AttributionRecord:
    """Add an attribution record to a dimension; evidence_pack_id is mandatory."""
    if not evidence_pack_id:
        raise ValueError("evidence_pack_id required for any attribution")
    rec = AttributionRecord(
        dimension=dimension,
        key=key,
        revenue_sar=float(revenue_sar),
        evidence_pack_id=evidence_pack_id,
        metadata=dict(metadata or {}),
    )
    _RECORDS.setdefault(dimension, []).append(rec)
    return rec


def total_for(dimension: str, key: str) -> float:
    """Return total verified revenue attributed to (dimension, key)."""
    return sum(r.revenue_sar for r in _RECORDS.get(dimension, []) if r.key == key)


def records(dimension: str) -> list[AttributionRecord]:
    """Return all records for a dimension."""
    return list(_RECORDS.get(dimension, []))


def reset() -> None:
    """Clear the attribution store (test helper)."""
    _RECORDS.clear()
