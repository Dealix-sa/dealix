"""Loads strategy definitions from YAML files in the strategies/ folder."""

from __future__ import annotations

from pathlib import Path

import yaml

from .schemas import Strategy

STRATEGIES_DIR = Path(__file__).resolve().parent / "strategies"

# The 13 strategies the engine expects to find.
REQUIRED_STRATEGIES = (
    "technical_trust",
    "money_now_sprint",
    "revenue_sprint",
    "saudi_market_access",
    "foreign_company_targeting",
    "local_b2b_growth",
    "b2g_readiness",
    "content_factory",
    "proof_pack",
    "partner_growth",
    "referral_loop",
    "seo_market_reports",
    "founder_daily_ops",
)


def load_strategies(directory: Path | None = None) -> list[Strategy]:
    """Load and return all strategies sorted by priority (ascending = first)."""

    base = directory or STRATEGIES_DIR
    strategies: list[Strategy] = []
    for path in sorted(base.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:  # pragma: no cover - defensive
            raise ValueError(f"Invalid strategy YAML {path.name}: {exc}") from exc
        if not isinstance(data, dict):
            continue
        strategies.append(Strategy.from_dict(data, source_file=path.name))
    strategies.sort(key=lambda s: (s.priority, s.name))
    return strategies


def missing_required(directory: Path | None = None) -> list[str]:
    """Return the names of required strategy files that are absent."""

    base = directory or STRATEGIES_DIR
    present = {p.stem for p in base.glob("*.yaml")}
    return [name for name in REQUIRED_STRATEGIES if name not in present]
