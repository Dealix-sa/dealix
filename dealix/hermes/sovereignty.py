"""
Sami Sovereign Layer — the apex authority.

No agent, no partner, no customer sees this layer. It is the only authority
that can:
  - approve / reject any action above S1
  - flip the global kill switch
  - allocate capital
  - override agent decisions
  - grant or revoke permissions

S4 — Sovereign Only:
  - open Public API
  - launch Marketplace
  - enable an MCP server
  - sign a strategic partnership
  - approve an Enterprise price
  - export sensitive data
  - change company strategy
  - grant agent permissions
  - run external automation
  - launch a new venture

S5 — Never Autonomous:
  - money transfer
  - signing on Sami's behalf
  - data exfiltration
  - claiming a fake partnership
  - external legal commitment
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Any

from dealix.hermes.core.schemas import RiskLevel, SovereigntyLevel
from dealix.hermes.trust.approvals import get_approval_center
from dealix.hermes.trust.audit import get_audit_log


# Canonical S4 / S5 sets — kept here as the single source of truth.
S4_SOVEREIGN_ACTIONS: frozenset[str] = frozenset(
    {
        "open_public_api",
        "launch_marketplace",
        "enable_mcp_server",
        "sign_strategic_partnership",
        "approve_enterprise_pricing",
        "export_sensitive_data",
        "change_company_strategy",
        "grant_agent_permission",
        "run_external_automation",
        "launch_venture",
    }
)

S5_NEVER_AUTONOMOUS_ACTIONS: frozenset[str] = frozenset(
    {
        "money_transfer",
        "sign_on_sami_behalf",
        "leak_data",
        "claim_nonexistent_partnership",
        "external_legal_commitment",
    }
)


@dataclass
class SovereignVerdict:
    allowed: bool
    requires_approval: bool
    sovereignty_level: SovereigntyLevel
    reason: str
    approval_id: str | None = None


def classify_action(action_type: str) -> SovereigntyLevel:
    """Map any action_type string to a sovereignty level."""
    if action_type in S5_NEVER_AUTONOMOUS_ACTIONS:
        return SovereigntyLevel.S5_NEVER_AUTONOMOUS
    if action_type in S4_SOVEREIGN_ACTIONS:
        return SovereigntyLevel.S4_SOVEREIGN_ONLY
    if action_type.startswith("send_external") or action_type.startswith("publish_"):
        return SovereigntyLevel.S2_SAMI_APPROVAL
    if action_type.startswith("draft_") or action_type.startswith("read_"):
        return SovereigntyLevel.S0_AGENT_FREE
    return SovereigntyLevel.S1_INTERNAL


class SovereignLayer:
    """The single arbiter of every consequential action."""

    def __init__(self) -> None:
        self._kill_switch_engaged = False
        self._lock = RLock()

    # ── Kill switch ────────────────────────────────────────────
    @property
    def kill_switch_engaged(self) -> bool:
        with self._lock:
            return self._kill_switch_engaged

    def engage_kill_switch(self, reason: str = "manual_engage") -> None:
        with self._lock:
            self._kill_switch_engaged = True
        get_audit_log().record(
            action_type="kill_switch_engaged",
            risk_level=RiskLevel.CRITICAL,
            sovereignty_level=SovereigntyLevel.S4_SOVEREIGN_ONLY,
            result=reason,
        )

    def disengage_kill_switch(self, reason: str = "manual_disengage") -> None:
        with self._lock:
            self._kill_switch_engaged = False
        get_audit_log().record(
            action_type="kill_switch_disengaged",
            risk_level=RiskLevel.HIGH,
            sovereignty_level=SovereigntyLevel.S4_SOVEREIGN_ONLY,
            result=reason,
        )

    # ── Decision gate ──────────────────────────────────────────
    def evaluate(
        self,
        *,
        action_type: str,
        agent_id: str,
        payload: dict[str, Any] | None = None,
        sovereignty_override: SovereigntyLevel | str | None = None,
        risk_level: RiskLevel | str = RiskLevel.MEDIUM,
    ) -> SovereignVerdict:
        if self.kill_switch_engaged:
            get_audit_log().record(
                action_type=action_type,
                agent_id=agent_id,
                risk_level=RiskLevel(risk_level),
                sovereignty_level=SovereigntyLevel.S4_SOVEREIGN_ONLY,
                result="blocked_kill_switch",
            )
            return SovereignVerdict(
                allowed=False,
                requires_approval=False,
                sovereignty_level=SovereigntyLevel.S4_SOVEREIGN_ONLY,
                reason="kill_switch_engaged",
            )

        sov = (
            SovereigntyLevel(sovereignty_override)
            if sovereignty_override
            else classify_action(action_type)
        )

        if sov == SovereigntyLevel.S5_NEVER_AUTONOMOUS:
            get_audit_log().record(
                action_type=action_type,
                agent_id=agent_id,
                risk_level=RiskLevel(risk_level),
                sovereignty_level=sov,
                result="blocked_s5_never_autonomous",
            )
            return SovereignVerdict(
                allowed=False,
                requires_approval=False,
                sovereignty_level=sov,
                reason="s5_never_autonomous",
            )

        if sov in {
            SovereigntyLevel.S2_SAMI_APPROVAL,
            SovereigntyLevel.S4_SOVEREIGN_ONLY,
        }:
            req = get_approval_center().request(
                requested_by_agent=agent_id,
                action_type=action_type,
                payload=payload,
                sovereignty_level=sov,
                risk_level=RiskLevel(risk_level),
            )
            get_audit_log().record(
                action_type=action_type,
                agent_id=agent_id,
                payload=payload,
                risk_level=RiskLevel(risk_level),
                sovereignty_level=sov,
                approval_id=req.id,
                result="approval_requested",
            )
            return SovereignVerdict(
                allowed=False,
                requires_approval=True,
                sovereignty_level=sov,
                reason="approval_required",
                approval_id=req.id,
            )

        get_audit_log().record(
            action_type=action_type,
            agent_id=agent_id,
            payload=payload,
            risk_level=RiskLevel(risk_level),
            sovereignty_level=sov,
            result="allowed",
        )
        return SovereignVerdict(
            allowed=True,
            requires_approval=False,
            sovereignty_level=sov,
            reason="ok",
        )


_default_layer: SovereignLayer | None = None


def get_sovereign_layer() -> SovereignLayer:
    global _default_layer
    if _default_layer is None:
        _default_layer = SovereignLayer()
    return _default_layer
