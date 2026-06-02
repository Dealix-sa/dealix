"""Sector prioritization — load + score sectors from data/distribution/sectors.yaml.

Priority is *computed* from weighted component scores so it is reproducible and
auditable (the OS never hard-codes a magic number). Each sector also references
a canonical offer id (``offer_ref``) in os/03_OFFERS.yml so pricing lives in one
place.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from dealix.distribution.paths import SECTORS_YAML


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


@lru_cache(maxsize=1)
def _raw() -> dict[str, Any]:
    return _load_yaml(SECTORS_YAML)


def weights() -> dict[str, int]:
    return dict(_raw().get("weights") or {})


def entry_gate() -> list[str]:
    return list(_raw().get("entry_gate") or [])


def compute_priority(scores: dict[str, Any], wts: dict[str, int] | None = None) -> int:
    """Sum of component scores, clamped to each component's weight ceiling.

    Components are already expressed on the same scale as the weight (max
    points), so the priority is simply the bounded sum → 0–100.
    """
    w = wts or weights()
    total = 0
    for component, ceiling in w.items():
        raw = scores.get(component, 0)
        try:
            val = int(raw)
        except (TypeError, ValueError):
            val = 0
        total += max(0, min(val, int(ceiling)))
    return total


def load_sectors() -> list[dict[str, Any]]:
    """Return sectors enriched with a computed ``priority``, ranked desc."""
    raw = _raw()
    wts = dict(raw.get("weights") or {})
    out: list[dict[str, Any]] = []
    for key, body in (raw.get("sectors") or {}).items():
        if not isinstance(body, dict):
            continue
        scores = dict(body.get("scores") or {})
        out.append(
            {
                "key": key,
                "name_ar": body.get("name_ar", ""),
                "name_en": body.get("name_en", ""),
                "pain": body.get("pain", ""),
                "offer": body.get("offer", ""),
                "offer_ref": body.get("offer_ref", ""),
                "first_workflow": body.get("first_workflow", ""),
                "proof_speed_days": body.get("proof_speed_days"),
                "scores": scores,
                "priority": compute_priority(scores, wts),
            }
        )
    out.sort(key=lambda s: s["priority"], reverse=True)
    return out


def get_sector(key: str) -> dict[str, Any] | None:
    for s in load_sectors():
        if s["key"] == key:
            return s
    return None


__all__ = [
    "compute_priority",
    "entry_gate",
    "get_sector",
    "load_sectors",
    "weights",
]
