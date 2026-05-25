"""Alert rules — fire when the platform sees something it must not."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class AlertRule:
    rule_id: str
    description: str
    severity: str  # "info" | "warn" | "critical"


ALERT_RULES: tuple[AlertRule, ...] = (
    AlertRule("external_action_without_approval", "External action attempted without approval", "critical"),
    AlertRule("mcp_descriptor_changed", "MCP descriptor changed unexpectedly", "warn"),
    AlertRule("agent_incident_rate_high", "Agent incident rate above threshold", "warn"),
    AlertRule("campaign_spend_without_attribution", "Campaign spend with no attribution", "warn"),
    AlertRule("revenue_paid_without_verification", "Revenue marked paid without verification events", "critical"),
    AlertRule("customer_missing_value_report", "Customer missing value report this period", "warn"),
    AlertRule("tool_used_by_unauthorized_agent", "Tool used by an agent without the capability", "critical"),
)


@dataclass
class AlertEvent:
    rule_id: str
    fired_at: datetime
    context: dict[str, str] = field(default_factory=dict)


ALERT_LOG: list[AlertEvent] = []


def fire_alert(rule_id: str, **context: str) -> AlertEvent:
    if not any(r.rule_id == rule_id for r in ALERT_RULES):
        raise KeyError(f"unknown alert rule {rule_id!r}")
    event = AlertEvent(rule_id=rule_id, fired_at=datetime.now(UTC), context=context)
    ALERT_LOG.append(event)
    return event
