"""Sovereignty + Identity & Access (sections 51, 52)."""

from __future__ import annotations

import pytest

from dealix.control_plane.identity_access import (
    Identity,
    IdentityKind,
    IdentityRegistry,
    Permission,
)
from dealix.control_plane.sovereignty import (
    SOVEREIGNTY_ORDER,
    SovereigntyTier,
    assert_sovereignty,
)


def test_sovereignty_order_is_canonical() -> None:
    assert SOVEREIGNTY_ORDER[0] is SovereigntyTier.SAMI
    assert SOVEREIGNTY_ORDER[-1] is SovereigntyTier.TOOL
    assert SovereigntyTier.SAMI.outranks(SovereigntyTier.INTERNAL)
    assert not SovereigntyTier.AGENT.outranks(SovereigntyTier.SAMI)


def test_assert_sovereignty_raises_for_lower_tier() -> None:
    with pytest.raises(PermissionError):
        assert_sovereignty(SovereigntyTier.AGENT, SovereigntyTier.SAMI)
    assert_sovereignty(SovereigntyTier.SAMI, SovereigntyTier.AGENT)


def test_identity_kind_maps_to_tier() -> None:
    assert IdentityKind.SAMI.tier is SovereigntyTier.SAMI
    assert IdentityKind.AGENT.tier is SovereigntyTier.AGENT


def test_sami_holds_all_permissions() -> None:
    sami = Identity(identity_id="sami", kind=IdentityKind.SAMI, display_name="Sami")
    for permission in Permission:
        assert sami.has(permission)


def test_agent_cannot_enable_tool_without_delegation() -> None:
    agent = Identity(
        identity_id="agent_x", kind=IdentityKind.AGENT, display_name="Agent X"
    )
    assert not agent.has(Permission.ENABLE_TOOL)
    with pytest.raises(PermissionError):
        agent.require(Permission.ENABLE_TOOL)


def test_identity_registry_delegation_requires_sami() -> None:
    registry = IdentityRegistry()
    sami = registry.register(
        Identity(identity_id="sami", kind=IdentityKind.SAMI, display_name="Sami")
    )
    operator = registry.register(
        Identity(
            identity_id="op_1",
            kind=IdentityKind.INTERNAL_OPERATOR,
            display_name="Internal Op",
        )
    )
    not_sami = registry.register(
        Identity(identity_id="agent_y", kind=IdentityKind.AGENT, display_name="Agent Y")
    )
    registry.delegate(
        sami_id=sami.identity_id,
        delegate_id=operator.identity_id,
        permissions=[Permission.APPROVE_EXTERNAL_ACTION],
    )
    delegated = registry.get(operator.identity_id)
    assert delegated.has(Permission.APPROVE_EXTERNAL_ACTION)
    assert delegated.delegated_by == sami.identity_id

    with pytest.raises(PermissionError):
        registry.delegate(
            sami_id=not_sami.identity_id,
            delegate_id=operator.identity_id,
            permissions=[Permission.ENABLE_TOOL],
        )
