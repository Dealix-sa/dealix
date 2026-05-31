"""Saudi sector registry — canonical taxonomy for ICP, prospector, proposal.

Loads from saudi_taxonomy.yaml. Exposes lookup helpers used by:
  - auto_client_acquisition/icp_scorer.py (sector-aware weights)
  - auto_client_acquisition/agents/prospector.py (sector validation)
  - auto_client_acquisition/agents/proposal.py (sector-specific pricing)
  - api/routers/research.py (sector enrichment)
"""

from __future__ import annotations

from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path
from typing import Any

_TAXONOMY_PATH = Path(__file__).parent / "saudi_taxonomy.yaml"


@lru_cache(maxsize=1)
def load_taxonomy() -> dict[str, Any]:
    """Load + cache the Saudi sector taxonomy YAML."""
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        return {"sectors": {}}
    if not _TAXONOMY_PATH.is_file():
        return {"sectors": {}}
    return yaml.safe_load(_TAXONOMY_PATH.read_text(encoding="utf-8")) or {"sectors": {}}


def get_sector(code: str) -> dict[str, Any] | None:
    """Look up a sector by code (case-insensitive)."""
    if not code:
        return None
    code_norm = code.upper().strip()
    sectors = load_taxonomy().get("sectors", {})
    return sectors.get(code_norm)


def list_sectors() -> Iterable[dict[str, Any]]:
    """Yield all sectors with code embedded."""
    sectors = load_taxonomy().get("sectors", {})
    for code, data in sectors.items():
        yield {"code": code, **data}


def sector_codes() -> list[str]:
    """Return all sector codes."""
    return list(load_taxonomy().get("sectors", {}).keys())


def is_known_sector(code: str) -> bool:
    """Return True if the sector code is in the registry."""
    return get_sector(code) is not None


def normalize_hint(hint: str) -> str | None:
    """Convert a free-text sector hint to canonical code, or None.

    Accepts common shorthand: 'saas', 'fintech', 'logistics', etc.
    """
    if not hint:
        return None
    hint_lower = hint.lower().strip()
    aliases = {
        "saas": "TECHNOLOGY",
        "tech": "TECHNOLOGY",
        "software": "TECHNOLOGY",
        "fintech": "FINANCE",
        "finance": "FINANCE",
        "banking": "FINANCE",
        "logistics": "LOGISTICS",
        "shipping": "LOGISTICS",
        "supply chain": "LOGISTICS",
        "healthcare": "HEALTHCARE",
        "health": "HEALTHCARE",
        "medical": "HEALTHCARE",
        "real estate": "REAL_ESTATE",
        "realestate": "REAL_ESTATE",
        "proptech": "REAL_ESTATE",
        "education": "EDUCATION",
        "edtech": "EDUCATION",
        "retail": "RETAIL",
        "ecommerce": "RETAIL",
        "e-commerce": "RETAIL",
        "manufacturing": "MANUFACTURING",
        "construction": "CONSTRUCTION",
        "contech": "CONSTRUCTION",
        "consulting": "CONSULTING",
        "tourism": "TOURISM",
        "hospitality": "TOURISM",
        "agency": "AGENCIES",
        "agencies": "AGENCIES",
        "marketplace": "MARKETPLACES",
        "marketplaces": "MARKETPLACES",
    }
    if hint_lower in aliases:
        return aliases[hint_lower]
    # Try direct match
    code = hint_lower.upper().replace(" ", "_").replace("-", "_")
    if is_known_sector(code):
        return code
    return None


__all__ = [
    "get_sector",
    "is_known_sector",
    "list_sectors",
    "load_taxonomy",
    "normalize_hint",
    "sector_codes",
]
