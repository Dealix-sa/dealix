"""Content engine — content types, CTA matrix, marketing operating rules."""

from __future__ import annotations

from dealix.growth_os.content_engine.content_types import (
    CONTENT_TYPE_DESCRIPTIONS,
    ContentType,
    describe_content_type,
)
from dealix.growth_os.content_engine.cta_matrix import (
    CONTENT_TO_CASH,
    CTAMapping,
    cta_for,
)
from dealix.growth_os.content_engine.operating_rules import (
    MARKETING_OPERATING_RULES,
    MarketingRule,
    RuleViolation,
    check_asset,
    enforce_marketing_rules,
)

__all__ = [
    "CONTENT_TO_CASH",
    "CONTENT_TYPE_DESCRIPTIONS",
    "MARKETING_OPERATING_RULES",
    "CTAMapping",
    "ContentType",
    "MarketingRule",
    "RuleViolation",
    "check_asset",
    "cta_for",
    "describe_content_type",
    "enforce_marketing_rules",
]
