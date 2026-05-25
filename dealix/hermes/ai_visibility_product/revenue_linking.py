"""Link AI visibility events to leads and verified revenue."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass

_LINKS: list["VisibilityRevenueLink"] = []


@dataclass(frozen=True)
class VisibilityRevenueLink:
    link_id: str
    customer_id: str
    engine: str
    query: str
    lead_id: str
    verified_revenue_sar: float
    evidence_pack_id: str
    linked_at: float = 0.0


def link(
    customer_id: str,
    engine: str,
    query: str,
    lead_id: str,
    verified_revenue_sar: float,
    evidence_pack_id: str,
) -> VisibilityRevenueLink:
    """Link a visibility event chain (engine, query, lead) to verified revenue."""
    if not evidence_pack_id:
        raise ValueError("evidence_pack_id required to link visibility -> revenue")
    record = VisibilityRevenueLink(
        link_id=f"vrl_{uuid.uuid4().hex[:10]}",
        customer_id=customer_id,
        engine=engine,
        query=query,
        lead_id=lead_id,
        verified_revenue_sar=float(verified_revenue_sar),
        evidence_pack_id=evidence_pack_id,
        linked_at=time.time(),
    )
    _LINKS.append(record)
    return record


def total_for_customer(customer_id: str) -> float:
    """Return total verified revenue linked to visibility events for a customer."""
    return sum(l.verified_revenue_sar for l in _LINKS if l.customer_id == customer_id)


def reset() -> None:
    """Clear visibility-revenue links (test helper)."""
    _LINKS.clear()
