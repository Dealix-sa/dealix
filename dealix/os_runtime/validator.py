"""
validator.py — Cross-consistency validator for Dealix OS configs.

Runs structural checks against loaded OS config data and returns a
ValidationResult so callers can decide how to handle errors.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.os_runtime.config_loader import OSConfigLoader


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)

    def __str__(self) -> str:
        lines = [
            f"ValidationResult: {len(self.errors)} errors, {len(self.warnings)} warnings"
        ]
        for e in self.errors:
            lines.append(f"  ERROR: {e}")
        for w in self.warnings:
            lines.append(f"  WARN:  {w}")
        return "\n".join(lines)


class OSValidator:
    """Validates the Dealix OS configuration for internal consistency."""

    def __init__(self, loader: OSConfigLoader | None = None) -> None:
        self.loader = loader or OSConfigLoader()

    def validate(self) -> ValidationResult:
        self.loader.load_all()
        result = ValidationResult()
        self._check_offers(result)
        self._check_markets(result)
        self._check_scoring(result)
        self._check_approval_gates(result)
        self._check_channels(result)
        self._check_anti_ban(result)
        self._check_cross_channel_offer_consistency(result)
        return result

    def validate_or_raise(self) -> None:
        result = self.validate()
        if not result.is_valid:
            raise RuntimeError(
                f"OS config validation failed with {len(result.errors)} error(s):\n"
                + "\n".join(f"  - {e}" for e in result.errors)
            )

    # ------------------------------------------------------------------
    # Checkers
    # ------------------------------------------------------------------

    def _check_offers(self, result: ValidationResult) -> None:
        offers = self.loader.offers
        if not offers:
            result.add_error("03_OFFERS.yml: no offers found or file missing")
            return
        seen_ids: set[str] = set()
        for key, val in offers.items():
            if not isinstance(val, dict):
                result.add_error(f"03_OFFERS.yml: offer '{key}' is not a mapping")
                continue
            for f_name in ("id", "name", "category"):
                if f_name not in val:
                    result.add_error(
                        f"03_OFFERS.yml: offer '{key}' missing required field '{f_name}'"
                    )
            offer_id = val.get("id", "")
            if offer_id in seen_ids:
                result.add_error(f"03_OFFERS.yml: duplicate offer id '{offer_id}'")
            seen_ids.add(offer_id)

    def _check_markets(self, result: ValidationResult) -> None:
        markets = self.loader.markets
        if not markets:
            result.add_warning("04_MARKETS.yml: no markets found or file missing")
            return
        for key, val in markets.items():
            if not isinstance(val, dict):
                continue
            for f_name in ("id", "priority"):
                if f_name not in val:
                    result.add_error(f"04_MARKETS.yml: market '{key}' missing '{f_name}'")

    def _check_scoring(self, result: ValidationResult) -> None:
        dims = self.loader.scoring_dimensions
        thresholds = self.loader.decision_thresholds
        if not dims:
            result.add_error("05_SCORING.yml: no scoring_dimensions found or file missing")
            return
        total = sum(v.get("weight", 0) for v in dims.values() if isinstance(v, dict))
        if total != 100:
            result.add_error(
                f"05_SCORING.yml: dimension weights sum to {total}, expected 100"
            )
        if len(thresholds) < 3:
            result.add_error(
                f"05_SCORING.yml: need at least 3 decision_thresholds, found {len(thresholds)}"
            )

    def _check_approval_gates(self, result: ValidationResult) -> None:
        gates = self.loader.approval_gates
        if not gates:
            result.add_error("06_APPROVAL_GATES.yml: no gates found or file missing")
            return
        for key, val in gates.items():
            if not isinstance(val, dict):
                continue
            if "id" not in val:
                result.add_error(f"06_APPROVAL_GATES.yml: gate '{key}' missing 'id'")
            if "requires_human_approval" not in val:
                result.add_error(
                    f"06_APPROVAL_GATES.yml: gate '{key}' missing 'requires_human_approval'"
                )
            if val.get("allowed") is False and val.get("requires_human_approval") is True:
                result.add_error(
                    f"06_APPROVAL_GATES.yml: gate '{key}' is permanently forbidden "
                    f"(allowed=false) but also has requires_human_approval=true"
                )

    def _check_channels(self, result: ValidationResult) -> None:
        channels = self.loader.channels
        if not channels:
            result.add_warning("CHANNEL_ROUTER.yml: no channels found or file missing")
            return
        for key, val in channels.items():
            if not isinstance(val, dict):
                continue
            for f_name in ("priority", "approval_required"):
                if f_name not in val:
                    result.add_error(
                        f"CHANNEL_ROUTER.yml: channel '{key}' missing '{f_name}'"
                    )

    def _check_anti_ban(self, result: ValidationResult) -> None:
        rules = self.loader.anti_ban_rules
        if not rules:
            result.add_warning("ANTI_BAN_GUARDIAN.yml: no rules found or file missing")
            return
        for key, val in rules.items():
            if not isinstance(val, dict):
                continue
            for f_name in ("daily_limit", "hourly_limit", "required_opt_in"):
                if f_name not in val:
                    result.add_error(
                        f"ANTI_BAN_GUARDIAN.yml: rule '{key}' missing '{f_name}'"
                    )

    def _check_cross_channel_offer_consistency(self, result: ValidationResult) -> None:
        sectors = self.loader.gcc_sectors
        channels = self.loader.channels
        if not sectors or not channels:
            return
        valid_channels = set(channels.keys())
        for sector_key, sector_val in sectors.items():
            if not isinstance(sector_val, dict):
                continue
            pref_ch = sector_val.get("preferred_channel")
            if pref_ch and pref_ch not in valid_channels:
                result.add_warning(
                    f"GCC_SECTOR_OFFERS.yml: sector '{sector_key}' preferred_channel "
                    f"'{pref_ch}' not found in CHANNEL_ROUTER.yml"
                )
