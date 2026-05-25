from __future__ import annotations

import pytest

from dealix.hermes.control_plane import ControlPlane
from dealix.hermes.identity import (
    IdentityStatus,
    SessionPolicy,
    build_identity,
)


def _seed_identity(plane: ControlPlane):
    identity = build_identity(
        "proposal_factory",
        "Sami",
        capability_scope=["read_approved_opportunity", "draft_proposal", "flag_risk"],
        forbidden_capabilities=["send_external", "sign_contract"],
    )
    identity.status = IdentityStatus.ACTIVE
    plane.register_identity(identity)
    return identity


def test_open_session_and_authorize_capability():
    plane = ControlPlane()
    _seed_identity(plane)
    session = plane.open_session(
        "proposal_factory",
        SessionPolicy(ttl_seconds=60, idle_timeout_seconds=60, max_operations=5),
    )
    decision = plane.authorize_capability(session.session_id, "draft_proposal")
    assert decision.allowed is True

    decision = plane.authorize_capability(session.session_id, "send_external")
    assert decision.allowed is False
    assert "capability" in decision.reason


def test_revoked_identity_blocks_session_open():
    plane = ControlPlane()
    identity = _seed_identity(plane)
    plane.revocation.revoke(identity, revoked_by="sami", reason="rotated")
    with pytest.raises(PermissionError):
        plane.open_session(
            "proposal_factory",
            SessionPolicy(ttl_seconds=60, idle_timeout_seconds=60, max_operations=5),
        )


def test_unknown_session_denied():
    plane = ControlPlane()
    decision = plane.authorize_capability("fake-session", "draft_proposal")
    assert decision.allowed is False
    assert decision.reason == "unknown_session"
