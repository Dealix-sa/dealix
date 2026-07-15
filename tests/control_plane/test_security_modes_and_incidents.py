"""Security Modes + Incident Response (sections 64, 65)."""

from __future__ import annotations

import pytest

from dealix.control_plane.identity_access import Identity, IdentityKind
from dealix.control_plane.incident_response import (
    IncidentLog,
    IncidentSeverity,
    IncidentType,
)
from dealix.control_plane.security_modes import SecurityMode, SecurityModeManager


def _sami() -> Identity:
    return Identity(identity_id="sami", kind=IdentityKind.SAMI, display_name="Sami")


def _agent() -> Identity:
    return Identity(identity_id="ag", kind=IdentityKind.AGENT, display_name="ag")


def test_only_sami_switches_security_mode() -> None:
    mgr = SecurityModeManager(SecurityMode.DRAFT_ONLY)
    with pytest.raises(PermissionError):
        mgr.switch(actor=_agent(), target=SecurityMode.APPROVAL_GATED)
    mgr.switch(actor=_sami(), target=SecurityMode.APPROVAL_GATED, note="ready")
    assert mgr.mode is SecurityMode.APPROVAL_GATED
    assert mgr.history[-1].from_mode is SecurityMode.DRAFT_ONLY


def test_draft_only_blocks_external_sends() -> None:
    mgr = SecurityModeManager(SecurityMode.DRAFT_ONLY)
    assert mgr.allow_external_send() is False
    assert mgr.drafts_only() is True


def test_sovereign_lockdown_blocks_everything_high_risk() -> None:
    mgr = SecurityModeManager(SecurityMode.DRAFT_ONLY)
    mgr.switch(actor=_sami(), target=SecurityMode.SOVEREIGN_LOCKDOWN)
    assert mgr.allow_external_send() is False
    assert mgr.allow_tool(risk_high=True) is False
    assert mgr.allow_tool(risk_high=False) is False


def test_incident_log_notifies_subscribers() -> None:
    log = IncidentLog()
    received: list[str] = []
    log.subscribe(lambda inc: received.append(inc.incident_id))
    incident = log.report(
        type=IncidentType.OVERCLAIM,
        severity=IncidentSeverity.HIGH,
        agent_id="proposal_factory",
        action_id="exe_001",
        recommended_fix="Rewrite claim as non-guaranteed outcome.",
    )
    assert incident.notified is True
    assert received == [incident.incident_id]
    log.attach_policy_update(incident.incident_id, policy_update="overclaim_v2")
    log.resolve(incident.incident_id)
    assert log.get(incident.incident_id).resolved_at is not None
