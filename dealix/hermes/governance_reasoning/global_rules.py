"""Global, workspace-agnostic governance rules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

DEFAULT_SPEND_LIMIT_SAR: float = 500.0


@dataclass(frozen=True)
class GlobalRuleResult:
    allowed: bool
    reason: str = ""


def evaluate(action: str, context: dict[str, Any]) -> GlobalRuleResult:
    """Apply default global policy: no PII to external tool, spend caps, no live sends."""
    target = str(context.get("target", "internal"))
    if context.get("pii", False) and target == "external":
        return GlobalRuleResult(allowed=False, reason="global: PII may not leave workspace")

    spend = float(context.get("spend_sar", 0.0))
    if spend > DEFAULT_SPEND_LIMIT_SAR:
        return GlobalRuleResult(allowed=False, reason=f"global: spend {spend} exceeds {DEFAULT_SPEND_LIMIT_SAR} SAR")

    if action in {"send_whatsapp_cold", "scrape_linkedin", "scrape_engine"}:
        return GlobalRuleResult(allowed=False, reason=f"global: forbidden action {action}")

    return GlobalRuleResult(allowed=True)
