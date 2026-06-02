"""Sector prioritization — a deterministic 100-point weighted model.

Criteria and weights mirror the distribution doctrine. Ratings are fractions
in ``[0, 1]``; the weighted sum yields a 0-100 priority score. Built-in
defaults can be overridden by ``data/distribution/sectors.yaml``.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

# criterion -> weight (must sum to 100)
SECTOR_WEIGHTS: dict[str, int] = {
    "pain": 20,
    "lead_flow": 15,
    "decision_access": 15,
    "ability_to_pay": 15,
    "speed_to_prove": 15,
    "ease_of_execution": 10,
    "local_edge": 10,
}
CRITERIA: tuple[str, ...] = tuple(SECTOR_WEIGHTS.keys())
assert sum(SECTOR_WEIGHTS.values()) == 100


@dataclass(frozen=True, slots=True)
class SectorScore:
    key: str
    name_ar: str
    name_en: str
    total: float
    entry_offer: str
    first_paid_offer: str
    breakdown: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "key": self.key,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "total": round(self.total, 1),
            "entry_offer": self.entry_offer,
            "first_paid_offer": self.first_paid_offer,
            "breakdown": {k: round(v, 1) for k, v in self.breakdown.items()},
        }


def _clamp01(x: float) -> float:
    return 0.0 if x < 0 else 1.0 if x > 1 else float(x)


def score_sector(ratings: Mapping[str, float]) -> float:
    """Weighted 0-100 score. Missing criteria count as 0; values clamped to [0,1]."""
    return round(sum(_clamp01(float(ratings.get(c, 0.0))) * SECTOR_WEIGHTS[c] for c in CRITERIA), 1)


def score_breakdown(ratings: Mapping[str, float]) -> dict[str, float]:
    """Per-criterion contribution to the total score."""
    return {c: round(_clamp01(float(ratings.get(c, 0.0))) * SECTOR_WEIGHTS[c], 1) for c in CRITERIA}


# Built-in defaults. Ratings are deliberate, conservative starting estimates;
# the founder should override them from real data via sectors.yaml.
DEFAULT_SECTORS: dict[str, dict] = {
    "marketing_agencies": {
        "name_ar": "وكالات التسويق",
        "name_en": "Marketing agencies",
        "entry_offer": "free_diagnostic",
        "first_paid_offer": "revenue_sprint",
        "ratings": {
            "pain": 0.9,
            "lead_flow": 0.9,
            "decision_access": 0.9,
            "ability_to_pay": 0.8,
            "speed_to_prove": 0.9,
            "ease_of_execution": 0.8,
            "local_edge": 0.8,
        },
    },
    "training_companies": {
        "name_ar": "شركات التدريب",
        "name_en": "Training companies",
        "entry_offer": "free_diagnostic",
        "first_paid_offer": "revenue_sprint",
        "ratings": {
            "pain": 0.9,
            "lead_flow": 0.8,
            "decision_access": 0.8,
            "ability_to_pay": 0.8,
            "speed_to_prove": 0.9,
            "ease_of_execution": 0.8,
            "local_edge": 0.8,
        },
    },
    "clinics": {
        "name_ar": "العيادات",
        "name_en": "Clinics",
        "entry_offer": "free_diagnostic",
        "first_paid_offer": "revenue_sprint",
        "ratings": {
            "pain": 0.9,
            "lead_flow": 0.8,
            "decision_access": 0.7,
            "ability_to_pay": 0.8,
            "speed_to_prove": 0.8,
            "ease_of_execution": 0.8,
            "local_edge": 0.8,
        },
    },
    "real_estate_teams": {
        "name_ar": "فرق العقار",
        "name_en": "Real estate teams",
        "entry_offer": "free_diagnostic",
        "first_paid_offer": "data_revenue_pack",
        "ratings": {
            "pain": 0.9,
            "lead_flow": 0.9,
            "decision_access": 0.7,
            "ability_to_pay": 0.8,
            "speed_to_prove": 0.7,
            "ease_of_execution": 0.7,
            "local_edge": 0.8,
        },
    },
    "recruitment_agencies": {
        "name_ar": "وكالات التوظيف",
        "name_en": "Recruitment agencies",
        "entry_offer": "free_diagnostic",
        "first_paid_offer": "data_revenue_pack",
        "ratings": {
            "pain": 0.8,
            "lead_flow": 0.8,
            "decision_access": 0.7,
            "ability_to_pay": 0.7,
            "speed_to_prove": 0.8,
            "ease_of_execution": 0.7,
            "local_edge": 0.7,
        },
    },
    "professional_services": {
        "name_ar": "الخدمات المهنية",
        "name_en": "Professional services",
        "entry_offer": "free_diagnostic",
        "first_paid_offer": "revenue_sprint",
        "ratings": {
            "pain": 0.8,
            "lead_flow": 0.7,
            "decision_access": 0.7,
            "ability_to_pay": 0.8,
            "speed_to_prove": 0.7,
            "ease_of_execution": 0.7,
            "local_edge": 0.7,
        },
    },
    "restaurant_groups": {
        "name_ar": "مجموعات المطاعم",
        "name_en": "Restaurant groups",
        "entry_offer": "free_diagnostic",
        "first_paid_offer": "revenue_sprint",
        "ratings": {
            "pain": 0.7,
            "lead_flow": 0.8,
            "decision_access": 0.6,
            "ability_to_pay": 0.7,
            "speed_to_prove": 0.7,
            "ease_of_execution": 0.6,
            "local_edge": 0.8,
        },
    },
    "education_providers": {
        "name_ar": "مزودو التعليم",
        "name_en": "Education providers",
        "entry_offer": "free_diagnostic",
        "first_paid_offer": "revenue_sprint",
        "ratings": {
            "pain": 0.7,
            "lead_flow": 0.7,
            "decision_access": 0.6,
            "ability_to_pay": 0.7,
            "speed_to_prove": 0.7,
            "ease_of_execution": 0.7,
            "local_edge": 0.7,
        },
    },
    "logistics_companies": {
        "name_ar": "شركات اللوجستيات",
        "name_en": "Logistics companies",
        "entry_offer": "free_diagnostic",
        "first_paid_offer": "data_revenue_pack",
        "ratings": {
            "pain": 0.7,
            "lead_flow": 0.6,
            "decision_access": 0.6,
            "ability_to_pay": 0.7,
            "speed_to_prove": 0.6,
            "ease_of_execution": 0.6,
            "local_edge": 0.7,
        },
    },
    "local_saas_service": {
        "name_ar": "شركات SaaS/خدمات محلية",
        "name_en": "Local SaaS / service companies",
        "entry_offer": "free_diagnostic",
        "first_paid_offer": "revenue_sprint",
        "ratings": {
            "pain": 0.7,
            "lead_flow": 0.6,
            "decision_access": 0.7,
            "ability_to_pay": 0.7,
            "speed_to_prove": 0.7,
            "ease_of_execution": 0.7,
            "local_edge": 0.6,
        },
    },
}


def _sectors_yaml_path() -> Path:
    return Path(os.getenv("DEALIX_REVX_SECTORS_PATH", "data/distribution/sectors.yaml"))


def load_sector_overrides() -> dict[str, dict]:
    """Load sector overrides from YAML if present; otherwise built-in defaults.

    The YAML must map sector keys to ``{name_ar, name_en, entry_offer,
    first_paid_offer, ratings}``. Falls back to defaults on any parse issue.
    """
    path = _sectors_yaml_path()
    if not path.exists():
        return dict(DEFAULT_SECTORS)
    try:
        import yaml

        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return dict(DEFAULT_SECTORS)
    sectors = raw.get("sectors", raw) if isinstance(raw, dict) else {}
    return sectors if isinstance(sectors, dict) and sectors else dict(DEFAULT_SECTORS)


def rank_sectors(sectors: Mapping[str, dict] | None = None) -> list[SectorScore]:
    """Rank sectors by priority score (highest first)."""
    source = sectors if sectors is not None else load_sector_overrides()
    scored: list[SectorScore] = []
    for key, spec in source.items():
        ratings = spec.get("ratings", {}) if isinstance(spec, dict) else {}
        scored.append(
            SectorScore(
                key=key,
                name_ar=str(spec.get("name_ar", key)),
                name_en=str(spec.get("name_en", key)),
                total=score_sector(ratings),
                entry_offer=str(spec.get("entry_offer", "free_diagnostic")),
                first_paid_offer=str(spec.get("first_paid_offer", "revenue_sprint")),
                breakdown=score_breakdown(ratings),
            )
        )
    scored.sort(key=lambda s: (-s.total, s.key))
    return scored


def top_sector(sectors: Mapping[str, dict] | None = None) -> SectorScore | None:
    """The highest-priority sector, or ``None`` when no sectors are configured."""
    ranked = rank_sectors(sectors)
    return ranked[0] if ranked else None


__all__ = [
    "CRITERIA",
    "DEFAULT_SECTORS",
    "SECTOR_WEIGHTS",
    "SectorScore",
    "load_sector_overrides",
    "rank_sectors",
    "score_breakdown",
    "score_sector",
    "top_sector",
]
