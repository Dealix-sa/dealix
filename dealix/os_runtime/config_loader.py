"""
config_loader.py — Reads os/*.yml and os/growth/*.yml into typed dicts.

Usage:
    loader = OSConfigLoader()
    loader.load_all()
    offers = loader.offers
    channels = loader.channels
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class OSConfigLoader:
    """Loads and caches all Dealix OS configuration files."""

    def __init__(self, os_dir: Path | None = None) -> None:
        if os_dir is None:
            os_dir = Path(__file__).resolve().parent.parent.parent / "os"
        self.os_dir: Path = os_dir
        self.growth_dir: Path = os_dir / "growth"

        # Raw data caches
        self._offers_raw: dict[str, Any] = {}
        self._markets_raw: dict[str, Any] = {}
        self._scoring_raw: dict[str, Any] = {}
        self._approval_gates_raw: dict[str, Any] = {}
        self._channel_router_raw: dict[str, Any] = {}
        self._anti_ban_raw: dict[str, Any] = {}
        self._gcc_sectors_raw: dict[str, Any] = {}

        self._loaded = False

    # ------------------------------------------------------------------
    # Public accessors
    # ------------------------------------------------------------------

    @property
    def offers(self) -> dict[str, Any]:
        self._ensure_loaded()
        return self._offers_raw.get("offers", {})

    @property
    def markets(self) -> dict[str, Any]:
        self._ensure_loaded()
        return self._markets_raw.get("primary_markets", {})

    @property
    def scoring_dimensions(self) -> dict[str, Any]:
        self._ensure_loaded()
        return self._scoring_raw.get("scoring_dimensions", {})

    @property
    def decision_thresholds(self) -> dict[str, Any]:
        self._ensure_loaded()
        return self._scoring_raw.get("decision_thresholds", {})

    @property
    def approval_gates(self) -> dict[str, Any]:
        self._ensure_loaded()
        return self._approval_gates_raw.get("gates", {})

    @property
    def channels(self) -> dict[str, Any]:
        self._ensure_loaded()
        return self._channel_router_raw.get("channels", {})

    @property
    def anti_ban_rules(self) -> dict[str, Any]:
        self._ensure_loaded()
        return self._anti_ban_raw.get("rules", {})

    @property
    def gcc_sectors(self) -> dict[str, Any]:
        self._ensure_loaded()
        return self._gcc_sectors_raw.get("sectors", {})

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load_all(self) -> None:
        """Load all OS config files. Idempotent."""
        self._offers_raw = self._load_yaml(self.os_dir / "03_OFFERS.yml")
        self._markets_raw = self._load_yaml(self.os_dir / "04_MARKETS.yml")
        self._scoring_raw = self._load_yaml(self.os_dir / "05_SCORING.yml")
        self._approval_gates_raw = self._load_yaml(self.os_dir / "06_APPROVAL_GATES.yml")
        self._channel_router_raw = self._load_yaml(
            self.growth_dir / "CHANNEL_ROUTER.yml"
        )
        self._anti_ban_raw = self._load_yaml(self.growth_dir / "ANTI_BAN_GUARDIAN.yml")
        self._gcc_sectors_raw = self._load_yaml(self.growth_dir / "GCC_SECTOR_OFFERS.yml")
        self._loaded = True

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.load_all()

    @staticmethod
    def _load_yaml(path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        try:
            with path.open(encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            return data if isinstance(data, dict) else {}
        except yaml.YAMLError:
            return {}

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def get_offer(self, offer_id: str) -> dict[str, Any] | None:
        """Return a single offer by ID, or None if not found."""
        for key, val in self.offers.items():
            if isinstance(val, dict) and val.get("id") == offer_id:
                return val
        return None

    def get_channel(self, channel_name: str) -> dict[str, Any] | None:
        """Return channel config by name."""
        return self.channels.get(channel_name)

    def get_sector(self, sector_id: str) -> dict[str, Any] | None:
        """Return GCC sector config by ID."""
        for key, val in self.gcc_sectors.items():
            if isinstance(val, dict) and val.get("id") == sector_id:
                return val
        return None

    def score_company(self, signals: dict[str, str]) -> dict[str, Any]:
        """
        Score a company based on signals dict.

        signals: {dimension_id: level}
        e.g. {"operations_complexity": "high", "reporting_burden": "medium"}

        Returns scoring output conforming to 05_SCORING.yml output format.
        """
        self._ensure_loaded()
        dims = self.scoring_dimensions
        total_score = 0
        dimension_scores = []
        strengths = []
        weaknesses = []

        for dim_id, dim_config in dims.items():
            if not isinstance(dim_config, dict):
                continue
            level = signals.get(dim_id, "low")
            levels = dim_config.get("levels", {})
            level_config = levels.get(level, {})
            score = level_config.get("score", 0)
            total_score += score
            dimension_scores.append(
                {
                    "dimension_id": dim_id,
                    "score": score,
                    "level": level,
                    "max": dim_config.get("weight", 0),
                }
            )
            if score >= dim_config.get("weight", 0) * 0.8:
                strengths.append(dim_id)
            elif score <= dim_config.get("weight", 0) * 0.3:
                weaknesses.append(dim_id)

        tier = self._get_tier(total_score)
        recommended_offer = self._recommend_offer(tier, signals)

        return {
            "total_score": total_score,
            "tier": tier,
            "dimension_scores": dimension_scores,
            "top_strengths": strengths[:3],
            "top_weaknesses": weaknesses[:3],
            "recommended_offer": recommended_offer,
            "next_action": self.decision_thresholds.get(tier, {}).get("action", ""),
            "scored_at": "",
            "scored_by": "dealix.os_runtime",
            "governance_decision": {
                "scored_by": "dealix.os_runtime",
                "no_live_action": True,
            },
        }

    def _get_tier(self, score: int) -> str:
        thresholds = self.decision_thresholds
        if score >= thresholds.get("priority_high", {}).get("min_score", 80):
            return "priority_high"
        if score >= thresholds.get("priority_medium", {}).get("min_score", 60):
            return "priority_medium"
        if score >= thresholds.get("nurture", {}).get("min_score", 40):
            return "nurture"
        return "disqualified"

    def _recommend_offer(self, tier: str, signals: dict[str, str]) -> str:
        if tier == "disqualified":
            return ""
        if signals.get("maintenance_or_field_ops") in ("yes", "partial"):
            return "maintenance_intelligence_os"
        if signals.get("operations_complexity") == "high":
            return "ai_workflow_audit"
        return "ai_workflow_audit"

    def route_offer(self, company_profile: dict[str, Any]) -> dict[str, Any]:
        """
        Given a company profile, return the best offer and channel routing.

        Returns:
            {
                "best_offer": str,
                "best_channel": str,
                "reasoning": str,
                "requires_approval": bool,
                "governance_decision": dict,
            }
        """
        self._ensure_loaded()
        sector = company_profile.get("sector", "")
        score = company_profile.get("score", 0)

        # Find sector config
        sector_config = None
        for key, val in self.gcc_sectors.items():
            if isinstance(val, dict) and (
                val.get("name", "").lower() in sector.lower()
                or sector.lower() in val.get("name", "").lower()
                or sector.lower() in val.get("name_ar", "").lower()
            ):
                sector_config = val
                break

        best_offer = (
            sector_config.get("best_offer", "ai_workflow_audit")
            if sector_config
            else "ai_workflow_audit"
        )
        best_channel = (
            sector_config.get("preferred_channel", "Email")
            if sector_config
            else "Email"
        )

        # Override for low scores
        if score < 60:
            best_offer = "ai_workflow_audit"

        channel_config = self.get_channel(best_channel) or {}
        requires_approval = channel_config.get("approval_required", True)

        return {
            "best_offer": best_offer,
            "best_channel": best_channel,
            "requires_approval": requires_approval,
            "reasoning": (
                f"Sector '{sector}' matched to offer '{best_offer}' via "
                f"GCC_SECTOR_OFFERS; channel '{best_channel}' selected. "
                f"Approval required: {requires_approval}."
            ),
            "governance_decision": {
                "routed_by": "dealix.os_runtime",
                "no_live_action": True,
                "requires_founder_approval_before_send": requires_approval,
            },
        }
