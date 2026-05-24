"""Reserve outreach queue correlation id for LeadOps spine (no auto-send)."""
from __future__ import annotations


def reserve_outreach_queue_id(*, leadops_id: str) -> str:
    """Deterministic queue correlation id for founder UI + outreach meta."""
    return f"leadops_{leadops_id}"
