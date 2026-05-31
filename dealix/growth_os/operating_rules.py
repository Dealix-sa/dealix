"""Top-level wrapper around the marketing operating rules + `enforce_all`.

Re-exports the rule catalogue for callers and offers a convenience
function that runs the appropriate per-asset checks for a batch.
"""

from __future__ import annotations

from typing import Any

from dealix.growth_os.content_engine.operating_rules import (
    MARKETING_OPERATING_RULES,
    MarketingRule,
    RuleViolation,
    check_asset,
)


def enforce_all(batch: dict[str, list[dict[str, Any]]]) -> dict[str, list[RuleViolation]]:
    """Run rules across a batch of assets grouped by kind.

    Example payload::

        {
          "campaign": [{...}, {...}],
          "content": [{...}],
          "deal": [{...}],
          "revenue": [{...}],
          "lead": [{...}],
          "offer": [{...}],
        }
    """
    out: dict[str, list[RuleViolation]] = {}
    for kind, assets in batch.items():
        violations: list[RuleViolation] = []
        for asset in assets:
            violations.extend(check_asset(kind, asset))
        if violations:
            out[kind] = violations
    return out


def list_rules() -> list[MarketingRule]:
    return list(MARKETING_OPERATING_RULES)


__all__ = [
    "MARKETING_OPERATING_RULES",
    "MarketingRule",
    "RuleViolation",
    "check_asset",
    "enforce_all",
    "list_rules",
]
