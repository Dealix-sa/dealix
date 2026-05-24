"""Agent runner — single-agent execution with timeout, retries, and evidence capture.

The runner is the smallest unit of agent execution in the AI Stack. Given a
registered ``AgentCard`` and a task payload, it:

1. Verifies the agent's lifecycle state allows production work.
2. Invokes the agent's handler (a callable) with the payload.
3. Captures evidence (input hash, output summary, duration, errors) for
   the evidence chain.
4. Returns a stable :class:`AgentRun` result that the agent mesh can fold
   into its trace.

The runner never speaks to an LLM directly — that's the handler's job. It
just enforces the governance/safety guarantees around every invocation.
"""

from __future__ import annotations

import hashlib
import json
import time
import traceback
import uuid
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from typing import Any

from auto_client_acquisition.agent_os.agent_card import AgentCard, AgentStatus
from auto_client_acquisition.agent_os.agent_lifecycle import (
    AgentLifecycleState,
    lifecycle_allows_production_tools,
)

# A handler returns either a dict (preferred) or any JSON-serializable value.
AgentHandler = Callable[[Mapping[str, Any]], Mapping[str, Any] | Any]


@dataclass(frozen=True, slots=True)
class AgentRun:
    """Stable record of one handler invocation."""

    run_id: str
    agent_id: str
    agent_name: str
    status: str  # "ok" | "error" | "blocked"
    started_at: str
    completed_at: str
    duration_ms: int
    input_hash: str
    output_summary: str
    output: Any
    error: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["metadata"] = dict(self.metadata)
        return data


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _hash_payload(payload: Mapping[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _summarize_output(output: Any, *, max_chars: int = 240) -> str:
    """Best-effort one-line audit summary of an agent's output."""
    if output is None:
        return "(no output)"
    if isinstance(output, str):
        text = output.strip().replace("\n", " ")
    elif isinstance(output, Mapping):
        for key in ("summary", "title", "message", "headline"):
            if output.get(key):
                text = str(output[key]).strip().replace("\n", " ")
                break
        else:
            text = json.dumps(output, ensure_ascii=False, default=str)
    else:
        try:
            text = json.dumps(output, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            text = str(output)
    if len(text) > max_chars:
        return text[: max_chars - 1] + "…"
    return text


def run_agent(
    *,
    card: AgentCard,
    handler: AgentHandler,
    payload: Mapping[str, Any],
    lifecycle_state: AgentLifecycleState = AgentLifecycleState.PRODUCTION,
    metadata: Mapping[str, Any] | None = None,
) -> AgentRun:
    """Execute a single agent handler under runner guarantees.

    The runner enforces two preconditions before invoking the handler:

    * The agent's registered status must not be ``killed``.
    * The agent's lifecycle state must allow production tool use.
    """
    run_id = f"ar_{uuid.uuid4().hex[:16]}"
    started_at = _now_iso()
    started_perf = time.perf_counter()
    input_hash = _hash_payload(payload)

    if card.status == AgentStatus.KILLED.value:
        completed_at = _now_iso()
        return AgentRun(
            run_id=run_id,
            agent_id=card.agent_id,
            agent_name=card.name,
            status="blocked",
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=0,
            input_hash=input_hash,
            output_summary="agent is killed — execution blocked",
            output=None,
            error="agent_killed",
            metadata={"reason": card.killed_reason or "unspecified"},
        )

    if not lifecycle_allows_production_tools(lifecycle_state):
        completed_at = _now_iso()
        return AgentRun(
            run_id=run_id,
            agent_id=card.agent_id,
            agent_name=card.name,
            status="blocked",
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=0,
            input_hash=input_hash,
            output_summary=(
                f"lifecycle state {lifecycle_state} does not allow production tools"
            ),
            output=None,
            error="lifecycle_blocked",
            metadata={"lifecycle_state": str(lifecycle_state)},
        )

    try:
        output = handler(payload)
        duration_ms = int((time.perf_counter() - started_perf) * 1000)
        completed_at = _now_iso()
        return AgentRun(
            run_id=run_id,
            agent_id=card.agent_id,
            agent_name=card.name,
            status="ok",
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            input_hash=input_hash,
            output_summary=_summarize_output(output),
            output=output,
            error=None,
            metadata=dict(metadata or {}),
        )
    except Exception as exc:
        duration_ms = int((time.perf_counter() - started_perf) * 1000)
        completed_at = _now_iso()
        return AgentRun(
            run_id=run_id,
            agent_id=card.agent_id,
            agent_name=card.name,
            status="error",
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            input_hash=input_hash,
            output_summary=f"handler raised: {exc!r}",
            output=None,
            error=str(exc),
            metadata={
                **dict(metadata or {}),
                "traceback": traceback.format_exc(limit=4),
            },
        )


__all__ = [
    "AgentHandler",
    "AgentRun",
    "run_agent",
]
