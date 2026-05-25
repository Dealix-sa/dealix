"""
Agent Runtime — كل agent يمر بنفس الـ pipeline:

    load agent card
    load context packet
    check permissions (via runtime gates)
    run model (يحقن من الخارج → قابل للاختبار بدون LLM)
    validate structured output
    trust check (في الـ runtime، ليس هنا)
    approval if needed
    trace
    outcome required

`AgentRuntime` لا يعرف أي شيء عن مزود LLM. يستلم `model_fn` كحقن. الإنتاج
يستبدله بـ Claude/OpenAI adapter؛ الاختبار يستبدله بـ stub deterministic.
"""

from __future__ import annotations

import threading
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from ..contracts import ContextPacket
from ..control_plane.kill_switch import KillSwitch, KillTargetKind
from .output_validator import OutputValidator, ValidationReport
from .run_state import RunState, RunStatus
from .tool_gateway import ToolGateway


@dataclass(frozen=True)
class AgentCard:
    """عقد الـ agent — يتطابق مع جدول `hermes_agents`."""

    agent_id: str
    role: str  # eg "SignalClassifier", "ProposalFactory"
    owner: str  # human owner (CTRL-GOV-001)
    purpose: str
    allowed_tools: tuple[str, ...] = ()
    required_output_fields: tuple[str, ...] = ("text",)
    max_text_chars: int = 8000
    can_call_external: bool = False
    locale: str = "ar"

    def validate(self) -> None:
        if not self.owner:
            raise ValueError(
                f"agent `{self.agent_id}` missing owner (CTRL-GOV-001)"
            )


ModelFn = Callable[[ContextPacket, AgentCard, dict[str, Any]], dict[str, Any]]


@dataclass
class AgentRunResult:
    run_id: str
    agent_id: str
    request_id: str
    output: dict[str, Any]
    validation: ValidationReport
    status: RunStatus
    started_at: datetime
    finished_at: datetime
    error: str | None = None


class AgentRuntime:
    def __init__(
        self,
        *,
        tool_gateway: ToolGateway | None = None,
        kill_switch: KillSwitch | None = None,
    ) -> None:
        self._cards: dict[str, AgentCard] = {}
        self._lock = threading.Lock()
        self._runs: list[RunState] = []
        self._tools = tool_gateway or ToolGateway(kill_switch=kill_switch)
        self._kill = kill_switch or KillSwitch()

    def register(self, card: AgentCard) -> None:
        card.validate()
        with self._lock:
            if card.agent_id in self._cards:
                raise ValueError(f"agent `{card.agent_id}` already registered")
            self._cards[card.agent_id] = card

    def get_card(self, agent_id: str) -> AgentCard | None:
        with self._lock:
            return self._cards.get(agent_id)

    def run(
        self,
        agent_id: str,
        *,
        context: ContextPacket,
        prompt_payload: dict[str, Any],
        model_fn: ModelFn,
    ) -> AgentRunResult:
        run_id = f"agr_{uuid.uuid4().hex[:14]}"
        started = datetime.now(timezone.utc)
        card = self.get_card(agent_id)
        if card is None:
            return self._error(
                run_id, agent_id, context.request_id, started, "agent not registered"
            )

        if not self._kill.is_active(KillTargetKind.AGENT, agent_id):
            return self._error(
                run_id,
                agent_id,
                context.request_id,
                started,
                f"agent `{agent_id}` is killed",
            )

        state = RunState(
            run_id=run_id,
            kind="agent",
            target_id=agent_id,
            request_id=context.request_id,
            status=RunStatus.RUNNING,
        )
        with self._lock:
            self._runs.append(state)

        try:
            output = model_fn(context, card, prompt_payload) or {}
        except Exception as exc:  # noqa: BLE001 — boundary
            state.transition(RunStatus.FAILED, error=str(exc))
            return self._error(
                run_id,
                agent_id,
                context.request_id,
                started,
                f"model_fn failed: {exc}",
            )

        validator = OutputValidator(
            required_fields=list(card.required_output_fields),
            max_text_chars=card.max_text_chars,
        )
        report = validator.validate(output)
        if not report.valid:
            state.transition(RunStatus.FAILED, error="; ".join(report.issues))
            return AgentRunResult(
                run_id=run_id,
                agent_id=agent_id,
                request_id=context.request_id,
                output=output,
                validation=report,
                status=RunStatus.FAILED,
                started_at=started,
                finished_at=datetime.now(timezone.utc),
                error="output validation failed",
            )

        state.transition(RunStatus.SUCCEEDED)
        return AgentRunResult(
            run_id=run_id,
            agent_id=agent_id,
            request_id=context.request_id,
            output=output,
            validation=report,
            status=RunStatus.SUCCEEDED,
            started_at=started,
            finished_at=datetime.now(timezone.utc),
        )

    def list_runs(self, limit: int = 100) -> list[RunState]:
        with self._lock:
            return list(self._runs)[-limit:]

    def tools(self) -> ToolGateway:
        return self._tools

    def _error(
        self,
        run_id: str,
        agent_id: str,
        request_id: str,
        started: datetime,
        reason: str,
    ) -> AgentRunResult:
        return AgentRunResult(
            run_id=run_id,
            agent_id=agent_id,
            request_id=request_id,
            output={},
            validation=ValidationReport(valid=False, issues=[reason]),
            status=RunStatus.FAILED,
            started_at=started,
            finished_at=datetime.now(timezone.utc),
            error=reason,
        )


__all__ = ["AgentCard", "AgentRunResult", "AgentRuntime", "ModelFn"]
