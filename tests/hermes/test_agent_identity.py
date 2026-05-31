from __future__ import annotations

import pytest

from dealix.hermes.identity import (
    IdentityStatus,
    RevocationLedger,
    SessionPolicy,
    build_identity,
    check_capability,
    enforce_workspace,
    revoke,
    start_session,
    validate_session,
)


def test_build_identity_rejects_overlap():
    with pytest.raises(ValueError):
        build_identity(
            "proposal_factory",
            "Sami",
            capability_scope=["draft_proposal", "send_external"],
            forbidden_capabilities=["send_external"],
        )


def test_capability_allowed_in_scope_only():
    identity = build_identity(
        "proposal_factory",
        "Sami",
        capability_scope=["draft_proposal", "flag_risk"],
        forbidden_capabilities=["send_external", "sign_contract"],
    )
    identity.status = IdentityStatus.ACTIVE
    assert check_capability(identity, "draft_proposal").allowed is True
    assert check_capability(identity, "send_external").allowed is False
    assert check_capability(identity, "modify_production_config").allowed is False


def test_revoked_identity_loses_all_capabilities():
    identity = build_identity(
        "proposal_factory",
        "Sami",
        capability_scope=["draft_proposal"],
    )
    identity.status = IdentityStatus.ACTIVE
    ledger = RevocationLedger()
    revoke(ledger, identity, revoked_by="sami", reason="rotation")
    assert ledger.is_revoked(identity.agent_id) is True
    assert check_capability(identity, "draft_proposal").allowed is False


def test_workspace_enforcement():
    identity = build_identity(
        "proposal_factory",
        "Sami",
        capability_scope=["draft_proposal"],
        workspace_scope=["dealix_internal"],
    )
    assert enforce_workspace(identity, "dealix_internal") is None
    violation = enforce_workspace(identity, "customer_xyz")
    assert violation is not None
    assert "customer_xyz" in violation.reason


def test_session_ttl_and_idle_timeout():
    policy = SessionPolicy(ttl_seconds=10, idle_timeout_seconds=2, max_operations=3)
    session = start_session("proposal_factory", policy)
    ok, reason = validate_session(session, now=session.started_at + 1)
    assert ok and reason == "ok"
    ok, reason = validate_session(session, now=session.started_at + 5)
    assert ok is False
    assert reason == "session_idle_timeout"


def test_session_max_operations():
    policy = SessionPolicy(ttl_seconds=60, idle_timeout_seconds=60, max_operations=2)
    session = start_session("proposal_factory", policy)
    assert validate_session(session)[0] is True
    assert validate_session(session)[0] is True
    ok, reason = validate_session(session)
    assert ok is False
    assert reason == "session_max_operations"
