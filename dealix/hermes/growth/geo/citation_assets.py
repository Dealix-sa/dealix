"""Catalog of citation-grade assets (research, benchmarks, case studies) for GEO."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass

_VALID_KINDS = {"benchmark", "research", "case_study", "framework", "dataset"}
_ASSETS: dict[str, "CitationAsset"] = {}


@dataclass(frozen=True)
class CitationAsset:
    asset_id: str
    kind: str
    title: str
    url: str
    evidence_pack_id: str
    created_at: float = 0.0


def register(kind: str, title: str, url: str, evidence_pack_id: str) -> CitationAsset:
    """Register a citation-grade asset; evidence_pack_id is required for traceability."""
    if kind not in _VALID_KINDS:
        raise ValueError(f"invalid citation asset kind: {kind}")
    if not evidence_pack_id:
        raise ValueError("evidence_pack_id required to register citation asset")
    asset = CitationAsset(
        asset_id=f"cit_{uuid.uuid4().hex[:8]}",
        kind=kind,
        title=title,
        url=url,
        evidence_pack_id=evidence_pack_id,
        created_at=time.time(),
    )
    _ASSETS[asset.asset_id] = asset
    return asset


def list_assets() -> list[CitationAsset]:
    """Return all registered citation assets."""
    return list(_ASSETS.values())


def reset() -> None:
    """Clear citation asset registry (test helper)."""
    _ASSETS.clear()
