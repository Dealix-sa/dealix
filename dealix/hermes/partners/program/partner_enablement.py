"""Enablement assets and certifications offered to partners."""

from __future__ import annotations

import time
from dataclasses import dataclass

_VALID_KINDS = {"playbook", "training", "certification", "demo_kit"}
_ASSETS: dict[str, "EnablementAsset"] = {}


@dataclass(frozen=True)
class EnablementAsset:
    asset_id: str
    kind: str
    title: str
    required_for_tiers: tuple[str, ...]
    created_at: float = 0.0


def publish(asset_id: str, kind: str, title: str, required_for_tiers: list[str]) -> EnablementAsset:
    """Publish an enablement asset bound to a list of partner tiers."""
    if kind not in _VALID_KINDS:
        raise ValueError(f"invalid enablement asset kind: {kind}")
    asset = EnablementAsset(
        asset_id=asset_id,
        kind=kind,
        title=title,
        required_for_tiers=tuple(required_for_tiers),
        created_at=time.time(),
    )
    _ASSETS[asset_id] = asset
    return asset


def required_for(tier: str) -> list[EnablementAsset]:
    """Return enablement assets required for a given partner tier."""
    return [a for a in _ASSETS.values() if tier in a.required_for_tiers]


def reset() -> None:
    """Clear enablement assets (test helper)."""
    _ASSETS.clear()
