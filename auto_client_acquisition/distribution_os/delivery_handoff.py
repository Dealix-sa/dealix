"""Delivery Handoff — turns a closed sale into a structured delivery start.

Prevents the classic "we sold, then delivery became chaos" failure (plan
section 11) by capturing scope, timeline, success metric, first workflow,
required access, and owner at the moment of handoff.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4

from auto_client_acquisition.distribution_os import catalog
from auto_client_acquisition.distribution_os._store import JsonlStore, now_iso


class DeliveryHandoffStatus(StrEnum):
    QUEUED = "queued"
    IN_ONBOARDING = "in_onboarding"
    ACTIVE = "active"
    BLOCKED = "blocked"
    COMPLETED = "completed"


@dataclass
class DeliveryHandoff:
    id: str = field(default_factory=lambda: f"deliv_{uuid4().hex[:12]}")
    customer_id: str = ""
    product_sold: str = ""  # catalog product id
    scope: list[str] = field(default_factory=list)
    timeline: str = ""
    success_metric: str = ""
    first_workflow: str = ""
    required_access: list[str] = field(default_factory=list)
    owner: str = ""
    risks: list[str] = field(default_factory=list)
    next_meeting: str = ""
    status: str = DeliveryHandoffStatus.QUEUED.value
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_store = JsonlStore(
    env_var="DEALIX_DELIVERY_HANDOFFS_PATH",
    default_rel="var/delivery_handoffs.jsonl",
    id_field="id",
)


def create_handoff(
    *,
    customer_id: str,
    product_sold: str,
    scope: list[str] | None = None,
    timeline: str = "",
    success_metric: str = "",
    first_workflow: str = "",
    required_access: list[str] | None = None,
    owner: str = "",
    risks: list[str] | None = None,
    next_meeting: str = "",
) -> DeliveryHandoff:
    if not catalog.is_valid_product_id(product_sold):
        raise ValueError(f"unknown_product_id:{product_sold}")
    if not success_metric.strip():
        raise ValueError("success_metric is required for a clean handoff")
    handoff = DeliveryHandoff(
        customer_id=customer_id,
        product_sold=product_sold,
        scope=scope or [],
        timeline=timeline,
        success_metric=success_metric,
        first_workflow=first_workflow,
        required_access=required_access or [],
        owner=owner,
        risks=risks or [],
        next_meeting=next_meeting,
    )
    _store.append(handoff.to_dict())
    return handoff


def get_handoff(handoff_id: str) -> DeliveryHandoff | None:
    rec = _store.get(handoff_id)
    return DeliveryHandoff(**rec) if rec else None


def list_handoffs(*, status: str | None = None) -> list[DeliveryHandoff]:
    latest: dict[str, dict[str, Any]] = {}
    for rec in _store.list():
        latest[str(rec.get("id"))] = rec
    handoffs = [DeliveryHandoff(**rec) for rec in latest.values()]
    if status is not None:
        handoffs = [h for h in handoffs if h.status == status]
    return handoffs


def update_status(handoff_id: str, status: str | DeliveryHandoffStatus) -> DeliveryHandoff | None:
    value = status.value if isinstance(status, DeliveryHandoffStatus) else str(status)
    if value not in {s.value for s in DeliveryHandoffStatus}:
        raise ValueError(f"invalid_status:{value}")
    rec = _store.patch(handoff_id, {"status": value})
    return DeliveryHandoff(**rec) if rec else None


def clear_for_test() -> None:
    _store.clear_for_test()


__all__ = [
    "DeliveryHandoff",
    "DeliveryHandoffStatus",
    "clear_for_test",
    "create_handoff",
    "get_handoff",
    "list_handoffs",
    "update_status",
]
