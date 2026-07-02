"""Sovereignty, permission, and trust routing for Hermes."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class SovereigntyLevel(StrEnum):
    S0_SAFE_INTERNAL = "S0_SAFE_INTERNAL"
    S1_INTERNAL = "S1_INTERNAL"
    S2_SAMI_APPROVAL = "S2_SAMI_APPROVAL"
    S3_HIGH_RISK_APPROVAL = "S3_HIGH_RISK_APPROVAL"
    S4_SOVEREIGN_ONLY = "S4_SOVEREIGN_ONLY"
    S5_BLOCKED_ALWAYS = "S5_BLOCKED_ALWAYS"


class ActionRoute(StrEnum):
    EXECUTE = "execute"
    HOLD_FOR_APPROVAL = "hold_for_approval"
    SOVEREIGN_ONLY = "sovereign_only"
    BLOCK = "block"


_ORDER = {
    SovereigntyLevel.S0_SAFE_INTERNAL: 0,
    SovereigntyLevel.S1_INTERNAL: 1,
    SovereigntyLevel.S2_SAMI_APPROVAL: 2,
    SovereigntyLevel.S3_HIGH_RISK_APPROVAL: 3,
    SovereigntyLevel.S4_SOVEREIGN_ONLY: 4,
    SovereigntyLevel.S5_BLOCKED_ALWAYS: 5,
}

S4_ACTIONS = {
    "open_public_api",
    "launch_marketplace",
    "enable_mcp_server",
    "approve_enterprise_pricing",
    "change_company_strategy",
    "grant_agent_permission",
    "run_external_automation",
    "launch_new_venture",
}

S5_ACTIONS = {
    "regulated_finance",
    "regulated_signature",
    "regulated_data",
    "regulated_claim",
    "regulated_legal",
    "regulated_outbound",
}

EXTERNAL_KEYWORDS = {"send", "publish", "post", "email", "linkedin", "whatsapp", "invoice", "proposal", "contract"}
SENSITIVE_KEYWORDS = {"restricted", "confidential", "pii", "personal_data", "customer_data", "export"}


@dataclass(slots=True)
class PermissionDecision:
    route: ActionRoute
    sovereignty_level: SovereigntyLevel
    requires_approval: bool
    allowed: bool
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class TrustCheckResult:
    passed: bool
    risk_level: str
    reasons: list[str] = field(default_factory=list)


def _normal(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def classify_action(
    action_type: str,
    *,
    external_action: bool = False,
    touches_sensitive_data: bool = False,
    changes_strategy: bool = False,
    grants_permissions: bool = False,
) -> SovereigntyLevel:
    action = _normal(action_type)
    if action in S5_ACTIONS:
        return SovereigntyLevel.S5_BLOCKED_ALWAYS
    if action in S4_ACTIONS or changes_strategy or grants_permissions:
        return SovereigntyLevel.S4_SOVEREIGN_ONLY
    if touches_sensitive_data or any(k in action for k in SENSITIVE_KEYWORDS):
        return SovereigntyLevel.S3_HIGH_RISK_APPROVAL
    if external_action or any(k in action for k in EXTERNAL_KEYWORDS):
        return SovereigntyLevel.S2_SAMI_APPROVAL
    if action.startswith(("draft", "score", "summarize")):
        return SovereigntyLevel.S0_SAFE_INTERNAL
    return SovereigntyLevel.S1_INTERNAL


def route_action(action_type: str, **kwargs: object) -> PermissionDecision:
    level = classify_action(action_type, **kwargs)  # type: ignore[arg-type]
    reasons = [f"classified:{level.value}"]
    if level == SovereigntyLevel.S5_BLOCKED_ALWAYS:
        return PermissionDecision(ActionRoute.BLOCK, level, False, False, reasons + ["blocked_always"])
    if level == SovereigntyLevel.S4_SOVEREIGN_ONLY:
        return PermissionDecision(ActionRoute.SOVEREIGN_ONLY, level, True, False, reasons + ["sami_only"])
    if level in {SovereigntyLevel.S2_SAMI_APPROVAL, SovereigntyLevel.S3_HIGH_RISK_APPROVAL}:
        return PermissionDecision(ActionRoute.HOLD_FOR_APPROVAL, level, True, False, reasons + ["approval_required"])
    return PermissionDecision(ActionRoute.EXECUTE, level, False, True, reasons + ["internal_safe_path"])


def permission_check(
    *,
    agent_id: str,
    agent_max_level: SovereigntyLevel | str,
    requested_level: SovereigntyLevel | str,
    tool_id: str | None = None,
    allowed_tools: list[str] | None = None,
    forbidden_tools: list[str] | None = None,
) -> PermissionDecision:
    max_level = SovereigntyLevel(agent_max_level)
    req_level = SovereigntyLevel(requested_level)
    allowed_tools = allowed_tools or []
    forbidden_tools = forbidden_tools or []
    reasons = [f"agent:{agent_id}", f"max:{max_level.value}", f"requested:{req_level.value}"]
    if tool_id and tool_id in forbidden_tools:
        return PermissionDecision(ActionRoute.BLOCK, req_level, False, False, reasons + ["tool_forbidden"])
    if tool_id and allowed_tools and tool_id not in allowed_tools:
        return PermissionDecision(ActionRoute.BLOCK, req_level, False, False, reasons + ["tool_not_allowed"])
    if _ORDER[req_level] > _ORDER[max_level]:
        return PermissionDecision(ActionRoute.HOLD_FOR_APPROVAL, req_level, True, False, reasons + ["above_agent_level"])
    return route_action(req_level.value)


def trust_check(
    *,
    agent_owner: str | None,
    agent_kpis: list[str] | None,
    tool_owner: str | None = None,
    tool_risk_level: str | None = None,
    mcp_reviewed: bool = True,
    data_scope: str | None = None,
) -> TrustCheckResult:
    reasons: list[str] = []
    risk_level = "low"
    if not agent_owner:
        reasons.append("agent_owner_missing")
        risk_level = "high"
    if not agent_kpis:
        reasons.append("agent_kpis_missing")
        risk_level = "medium" if risk_level == "low" else risk_level
    if tool_owner is not None and not tool_owner:
        reasons.append("tool_owner_missing")
        risk_level = "high"
    if tool_risk_level in {"high", "critical"}:
        reasons.append(f"tool_risk:{tool_risk_level}")
        risk_level = "high"
    if not mcp_reviewed:
        reasons.append("mcp_review_missing")
        risk_level = "high"
    if data_scope in {"all", "global", "unbounded"}:
        reasons.append("data_scope_too_broad")
        risk_level = "high"
    return TrustCheckResult(passed=not reasons, risk_level=risk_level, reasons=reasons or ["trust_passed"])
