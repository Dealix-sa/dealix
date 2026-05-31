"""Execution plane — agent runtime, output validator, tool gateway, kill switch."""

from __future__ import annotations

from typing import Any

import pytest

from dealix.hermes.contracts import (
    Actor,
    ActorKind,
    ContextPacket,
)
from dealix.hermes.control_plane.kill_switch import KillSwitch, KillTargetKind
from dealix.hermes.execution import (
    AgentCard,
    AgentRuntime,
    RunStatus,
    ToolDescriptor,
    ToolGateway,
)


def _context() -> ContextPacket:
    return ContextPacket(
        actor=Actor(actor_id="founder_1", kind=ActorKind.FOUNDER),
        intent="internal.draft.test",
    )


# ────────────────────────────────────────────────────────────────
# Agent runtime
# ────────────────────────────────────────────────────────────────


def test_agent_run_succeeds_with_valid_output() -> None:
    runtime = AgentRuntime()
    card = AgentCard(
        agent_id="t",
        role="Test",
        owner="founder",
        purpose="t",
    )
    runtime.register(card)

    def model_fn(
        ctx: ContextPacket, card: AgentCard, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return {"text": "ok"}

    result = runtime.run(
        "t",
        context=_context(),
        prompt_payload={},
        model_fn=model_fn,
    )
    assert result.status == RunStatus.SUCCEEDED
    assert result.output == {"text": "ok"}
    assert result.validation.valid is True


def test_agent_run_fails_validation_when_required_field_missing() -> None:
    runtime = AgentRuntime()
    card = AgentCard(
        agent_id="t2",
        role="Test",
        owner="founder",
        purpose="t",
    )
    runtime.register(card)

    def model_fn(
        ctx: ContextPacket, card: AgentCard, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return {}

    result = runtime.run(
        "t2",
        context=_context(),
        prompt_payload={},
        model_fn=model_fn,
    )
    assert result.status == RunStatus.FAILED
    assert result.validation.valid is False
    assert any("text" in issue for issue in result.validation.issues)


# ────────────────────────────────────────────────────────────────
# Tool gateway
# ────────────────────────────────────────────────────────────────


def test_tool_registration_without_owner_raises() -> None:
    gateway = ToolGateway()
    descriptor = ToolDescriptor(
        tool_id="search",
        description="search tool",
        sensitivity="read",
        owner="",
    )
    with pytest.raises(ValueError):
        gateway.register(descriptor, lambda args: {"ok": True})


def test_tool_call_fails_when_kill_switch_tripped() -> None:
    kill = KillSwitch()
    gateway = ToolGateway(kill_switch=kill)
    descriptor = ToolDescriptor(
        tool_id="echo",
        description="echo back",
        sensitivity="read",
        owner="founder",
    )
    gateway.register(descriptor, lambda args: {"echo": args})

    kill.trip(
        KillTargetKind.TOOL,
        "echo",
        tripped_by="founder",
        reason="incident",
    )
    result = gateway.call(
        "echo",
        args={"hello": "world"},
        actor_kind=ActorKind.FOUNDER.value,
    )
    assert result.success is False
    assert result.error is not None
    assert "killed" in result.error
