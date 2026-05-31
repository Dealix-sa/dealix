"""Registry of campaigns linked to offers."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field

_CAMPAIGNS: dict[str, "Campaign"] = {}


@dataclass(frozen=True)
class Campaign:
    campaign_id: str
    name: str
    offer_id: str
    icp_id: str
    channels: tuple[str, ...]
    status: str = "draft"
    created_at: float = 0.0
    tags: tuple[str, ...] = field(default_factory=tuple)


def register(name: str, offer_id: str, icp_id: str, channels: list[str], tags: list[str] | None = None) -> Campaign:
    """Create a draft campaign linked to an offer + ICP."""
    cam = Campaign(
        campaign_id=f"cam_{uuid.uuid4().hex[:10]}",
        name=name,
        offer_id=offer_id,
        icp_id=icp_id,
        channels=tuple(channels),
        created_at=time.time(),
        tags=tuple(tags or ()),
    )
    _CAMPAIGNS[cam.campaign_id] = cam
    return cam


def get(campaign_id: str) -> Campaign | None:
    """Return a campaign by id or None."""
    return _CAMPAIGNS.get(campaign_id)


def list_all() -> list[Campaign]:
    """Return all registered campaigns."""
    return list(_CAMPAIGNS.values())


def reset() -> None:
    """Clear the campaign registry (test helper)."""
    _CAMPAIGNS.clear()
