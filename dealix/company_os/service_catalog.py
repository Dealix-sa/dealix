"""Canonical Dealix service catalog and deterministic evidence-first matcher."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class ServiceOffer:
    id: str
    name_ar: str
    department: str
    stage: str
    price_guidance_sar: str
    ideal_for: tuple[str, ...]
    pain_keywords: tuple[str, ...]
    value_outcomes: tuple[str, ...]
    proof_required: tuple[str, ...]
    forbidden_claims: tuple[str, ...] = (
        "guaranteed_revenue",
        "guaranteed