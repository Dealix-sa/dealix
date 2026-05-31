"""CRUD + scoring for Ideal Customer Profile (ICP) records."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

_ICPS: dict[str, "ICP"] = {}


@dataclass(frozen=True)
class ICP:
    icp_id: str
    name: str
    industry: str
    region: str
    company_size: str
    pain_points: tuple[str, ...] = ()
    weight: float = 1.0
    attributes: dict[str, Any] = field(default_factory=dict)


def upsert(icp: ICP) -> ICP:
    """Create or replace an ICP record by icp_id."""
    _ICPS[icp.icp_id] = icp
    return icp


def get(icp_id: str) -> ICP | None:
    """Return the ICP with icp_id, or None if absent."""
    return _ICPS.get(icp_id)


def list_all() -> list[ICP]:
    """Return every registered ICP."""
    return list(_ICPS.values())


def score_account(icp_id: str, account: dict[str, Any]) -> float:
    """Score an account against an ICP across industry, region, size, pain alignment."""
    icp = _ICPS.get(icp_id)
    if icp is None:
        return 0.0
    score = 0.0
    if account.get("industry") == icp.industry:
        score += 0.3
    if account.get("region") == icp.region:
        score += 0.2
    if account.get("company_size") == icp.company_size:
        score += 0.2
    pains = set(account.get("pain_points", []))
    overlap = len(pains.intersection(icp.pain_points))
    if icp.pain_points:
        score += 0.3 * (overlap / len(icp.pain_points))
    return round(min(1.0, score) * icp.weight, 4)


def reset() -> None:
    """Clear the ICP registry (test helper)."""
    _ICPS.clear()
