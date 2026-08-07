from __future__ import annotations

import asyncio
import base64
import logging
import os
import re
import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

_DEFAULT_LANGFUSE_HOST = "https://cloud.langfuse.com"
_DEFAULT_ALLOWED_HOSTS = frozenset({"cloud.langfuse.com"})
_TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
_SENSITIVE_KEYS = frozenset({
    "api_key",
    "apikey",
    "authorization",
    "cookie",
    "credential",
    "password",
    "secret",
    "session_id",
    "token",
})
_SENSITIVE_KEY_SUFFIXES = ("_api_key", "_cookie", "_credential", "_password", "_secret", "_token")
_EMAIL_RE = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
_SAUDI_PHONE_RE = re.compile(r"(?<!\d)(?:\+?966|00966|0)?5\d{8}(?!\d)")
_BEARER_RE = re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}")
_JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")
_LONG_SECRET_RE = re.compile(r"\b(?:sk|pk|rk|key|token)[-_][A-Za-z0-9_-]{12,}\b", re.IGNORECASE)


def _env_enabled(name: str, *, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in _TRUE_VALUES


def _redact_text(value: str) -> str:
    value = _BEARER_RE.sub("[REDACTED_BEARER]", value)
    value = _JWT_RE.sub("[REDACTED_JWT]", value)
    value = _LONG_SECRET_RE.sub("[REDACTED_SECRET]", value)
    value = _EMAIL_RE.sub("[REDACTED_EMAIL]", value)
    return _SAUDI_PHONE_RE.sub("[REDACTED_PHONE]", value)


def redact_trace_value(value: Any, *, key: str | None = None, depth: int = 0) -> Any:
    """Return a JSON-safe, recursively redacted copy for network export.

    Local in-memory objects are left untouched. Redaction happens when the export
    payload is created, which guarantees that raw prompts and metadata never reach
    the network transport.
    """
    normalized_key = (key or "").lower().replace("-", "_")
    if normalized_key in _SENSITIVE_KEYS or normalized_key.endswith(_SENSITIVE_KEY_SUFFIXES):
        return "[REDACTED]"
    if depth >= 8:
        return "[TRUNCATED_DEPTH]"
    if isinstance(value, str):
        return _redact_text(value)
    if isinstance(value, dict):
        return {
            str(item_key): redact_trace_value(item_value, key=str(item_key), depth=depth + 1)
            for item_key, item_value in value.items()
        }
    if isinstance(value, (list, tuple, set, frozenset)):
        return [redact_trace_value(item, depth=depth + 1) for item in value]
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return _redact_text(str(value))


def _validate_export_target(host: str, allowed_hosts: frozenset[str]) -> tuple[str, str | None]:
    """Normalize an explicitly allowed HTTPS Langfuse endpoint or fail closed."""
    try:
        parsed = urlparse(host)
        hostname = (parsed.hostname or "").lower().rstrip(".")
        port = parsed.port
    except (TypeError, ValueError):
        return host, "invalid Langfuse host"

    if parsed.scheme.lower() != "https":
        return host, "Langfuse export requires https"
    if not hostname or parsed.username or parsed.password:
        return host, "Langfuse host must not contain credentials"
    if port not in (None, 443):
        return host, "Langfuse export only allows the default HTTPS port"
    if hostname not in allowed_hosts:
        return host, f"Langfuse host {hostname!r} is not in the explicit egress allowlist"
    if parsed.query or parsed.fragment:
        return host, "Langfuse host must not contain a query or fragment"
    return host.rstrip("/"), None


@dataclass
class LLMCall:
    call_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    provider: str = ""
    model: str = ""
    prompt: str = ""
    response: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0
    latency_ms: float = 0.0
    status: str = "success"
    error: str | None = None
    agent_id: str | None = None
    session_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AgentAction:
    action_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    action_type: str = ""
    input: dict[str, Any] = field(default_factory=dict)
    output: dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0
    status: str = "success"
    error: str | None = None
    trace_id: str | None = None
    parent_action_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CostReport:
    period_days: int = 30
    total_cost: float = 0.0
    by_provider: dict[str, float] = field(default_factory=dict)
    by_model: dict[str, float] = field(default_factory=dict)
    by_agent: dict[str, float] = field(default_factory=dict)
    daily_costs: list[dict[str, Any]] = field(default_factory=list)
    total_calls: int = 0
    avg_cost_per_call: float = 0.0


class LangfuseTracker:
    def __init__(
        self,
        public_key: str | None = None,
        secret_key: str | None = None,
        host: str | None = None,
        enabled: bool | None = None,
        allowed_hosts: set[str] | frozenset[str] | None = None,
        max_queue_size: int = 256,
        max_retries: int = 2,
        request_timeout_seconds: float = 2.0,
    ):
        if max_queue_size < 1:
            raise ValueError("max_queue_size must be at least 1")
        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        if request_timeout_seconds <= 0:
            raise ValueError("request_timeout_seconds must be positive")

        self._public_key = public_key or os.getenv("LANGFUSE_PUBLIC_KEY")
        self._secret_key = secret_key or os.getenv("LANGFUSE_SECRET_KEY")
        self._enabled = (
            _env_enabled("DEALIX_LANGFUSE_EXPORT_ENABLED", default=False)
            if enabled is None
            else enabled
        )
        if allowed_hosts is None:
            configured_hosts = frozenset(
                item.strip().lower().rstrip(".")
                for item in os.getenv(
                    "DEALIX_LANGFUSE_ALLOWED_HOSTS",
                    ",".join(sorted(_DEFAULT_ALLOWED_HOSTS)),
                ).split(",")
                if item.strip()
            )
        else:
            configured_hosts = frozenset(item.lower().rstrip(".") for item in allowed_hosts)
        configured_host = host or os.getenv("LANGFUSE_HOST", _DEFAULT_LANGFUSE_HOST)
        self._host, self._target_error = _validate_export_target(configured_host, configured_hosts)
        self._credentials_error = (
            None
            if self._public_key and self._secret_key
            else "Langfuse export credentials are incomplete"
        )
        self._max_retries = max_retries
        self._request_timeout_seconds = request_timeout_seconds
        self._export_queue: deque[dict[str, Any]] = deque(maxlen=max_queue_size)
        self._worker_task: asyncio.Task[None] | None = None
        self._exported_count = 0
        self._failed_count = 0
        self._dropped_count = 0
        self._last_error: str | None = None
        self._calls: list[LLMCall] = []
        self._actions: list[AgentAction] = []
        self._traces: dict[str, dict[str, Any]] = {}

        if self._enabled and not self._export_block_reason:
            logger.info("Langfuse export enabled (host: %s)", self._host)
        elif self._enabled:
            logger.warning("Langfuse export blocked: %s", self._export_block_reason)

    async def trace_llm_call(self, call: LLMCall) -> str:
        trace_id = call.call_id
        self._calls.append(call)

        if not self._enabled:
            return trace_id

        self._enqueue_export({
            "schema_version": "dealix.trace.v1",
            "id": trace_id,
            "type": "llm_call",
            "provider": call.provider,
            "model": call.model,
            "input": call.prompt[:1000],
            "output": call.response[:1000],
            "usage": {
                "prompt_tokens": call.prompt_tokens,
                "completion_tokens": call.completion_tokens,
                "total_tokens": call.total_tokens,
            },
            "cost": call.cost,
            "latency_ms": call.latency_ms,
            "status": call.status,
            "error": call.error,
            "agent_id": call.agent_id,
            "session_id": call.session_id,
            "metadata": call.metadata,
            "lineage": {"trace_id": trace_id, "parent_action_id": None},
            "timestamp": call.timestamp.isoformat(),
        })

        if trace_id not in self._traces:
            self._traces[trace_id] = {"calls": [], "actions": [], "started_at": call.timestamp}
        self._traces[trace_id]["calls"].append(call.call_id)

        return trace_id

    async def trace_agent_action(self, action: AgentAction) -> str:
        trace_id = action.action_id
        self._actions.append(action)

        if not self._enabled:
            return trace_id

        self._enqueue_export({
            "schema_version": "dealix.trace.v1",
            "id": trace_id,
            "type": "agent_action",
            "agent_id": action.agent_id,
            "action_type": action.action_type,
            "input": action.input,
            "output": action.output,
            "duration_ms": action.duration_ms,
            "status": action.status,
            "error": action.error,
            "trace_id": action.trace_id,
            "parent_action_id": action.parent_action_id,
            "metadata": action.metadata,
            "lineage": {
                "trace_id": action.trace_id or trace_id,
                "parent_action_id": action.parent_action_id,
            },
            "timestamp": action.timestamp.isoformat(),
        })

        parent_trace = action.trace_id or trace_id
        if parent_trace not in self._traces:
            self._traces[parent_trace] = {"calls": [], "actions": [], "started_at": action.timestamp}
        self._traces[parent_trace]["actions"].append(action.action_id)

        return trace_id

    async def create_trace(
        self,
        name: str,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        trace_id = str(uuid.uuid4())
        self._traces[trace_id] = {
            "name": name,
            "calls": [],
            "actions": [],
            "metadata": metadata or {},
            "started_at": datetime.utcnow(),
        }

        if self._enabled:
            self._enqueue_export({
                "schema_version": "dealix.trace.v1",
                "id": trace_id,
                "type": "trace",
                "name": name,
                "metadata": metadata or {},
                "lineage": {"trace_id": trace_id, "parent_action_id": None},
                "timestamp": datetime.utcnow().isoformat(),
            })

        return trace_id

    async def get_cost_report(self, days: int = 30) -> CostReport:
        cutoff = datetime.utcnow() - timedelta(days=days)
        calls = [c for c in self._calls if c.timestamp >= cutoff]

        report = CostReport(period_days=days, total_calls=len(calls))

        daily: dict[str, float] = {}
        for call in calls:
            report.total_cost += call.cost
            report.by_provider[call.provider] = (
                report.by_provider.get(call.provider, 0) + call.cost
            )
            report.by_model[call.model] = (
                report.by_model.get(call.model, 0) + call.cost
            )
            if call.agent_id:
                report.by_agent[call.agent_id] = (
                    report.by_agent.get(call.agent_id, 0) + call.cost
                )

            day_key = call.timestamp.strftime("%Y-%m-%d")
            daily[day_key] = daily.get(day_key, 0) + call.cost

        report.daily_costs = [
            {"date": date, "cost": round(cost, 4)}
            for date, cost in sorted(daily.items())
        ]
        report.avg_cost_per_call = (
            round(report.total_cost / len(calls), 6) if calls else 0.0
        )

        return report

    async def get_trace(self, trace_id: str) -> dict[str, Any] | None:
        return self._traces.get(trace_id)

    async def get_llm_calls(
        self,
        limit: int = 100,
        agent_id: str | None = None,
        model: str | None = None,
    ) -> list[LLMCall]:
        calls = list(self._calls)
        if agent_id:
            calls = [c for c in calls if c.agent_id == agent_id]
        if model:
            calls = [c for c in calls if c.model == model]
        return sorted(calls, key=lambda c: c.timestamp, reverse=True)[:limit]

    async def get_agent_actions(
        self,
        agent_id: str | None = None,
        limit: int = 100,
    ) -> list[AgentAction]:
        actions = list(self._actions)
        if agent_id:
            actions = [a for a in actions if a.agent_id == agent_id]
        return sorted(actions, key=lambda a: a.timestamp, reverse=True)[:limit]

    @property
    def _export_block_reason(self) -> str | None:
        return self._target_error or self._credentials_error

    def _enqueue_export(self, data: dict[str, Any]) -> None:
        """Queue a redacted payload without awaiting network I/O."""
        if not self._enabled or self._export_block_reason:
            return
        if len(self._export_queue) == self._export_queue.maxlen:
            self._export_queue.popleft()
            self._dropped_count += 1
        self._export_queue.append(redact_trace_value(data))
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(
                self._drain_export_queue(),
                name="dealix-langfuse-export",
            )

    async def _drain_export_queue(self) -> None:
        try:
            while self._export_queue:
                payload = self._export_queue.popleft()
                delivered = await self._deliver_with_retry(payload)
                if delivered:
                    self._exported_count += 1
                else:
                    self._failed_count += 1
        finally:
            self._worker_task = None

    async def _deliver_with_retry(self, payload: dict[str, Any]) -> bool:
        for attempt in range(self._max_retries + 1):
            try:
                await self._post_payload(payload)
                self._last_error = None
                return True
            except Exception as exc:
                self._last_error = type(exc).__name__
                if attempt < self._max_retries:
                    await asyncio.sleep(min(0.05 * (2**attempt), 0.5))
        logger.debug("Langfuse export failed after retries: %s", self._last_error)
        return False

    async def _post_payload(self, data: dict[str, Any]) -> None:
        """Perform one export attempt. Override in tests; never pass raw data here."""
        import aiohttp

        auth = base64.b64encode(f"{self._public_key}:{self._secret_key}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
        }
        async with (
            aiohttp.ClientSession() as session,
            session.post(
                f"{self._host}/api/public/observations",
                json=data,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self._request_timeout_seconds),
            ) as response,
        ):
            if response.status not in (200, 201, 202):
                raise RuntimeError(f"Langfuse API returned {response.status}")

    async def flush(self, timeout_seconds: float = 5.0) -> bool:
        """Wait for queued exports during graceful shutdown or deterministic tests."""
        task = self._worker_task
        if task is None:
            return not self._export_queue
        try:
            await asyncio.wait_for(asyncio.shield(task), timeout=timeout_seconds)
        except TimeoutError:
            return False
        return not self._export_queue

    def get_export_status(self) -> dict[str, Any]:
        """Return non-secret operational evidence for health/proof logs."""
        return {
            "enabled": self._enabled,
            "export_allowed": self._enabled and self._export_block_reason is None,
            "block_reason": self._export_block_reason,
            "queued": len(self._export_queue),
            "queue_capacity": self._export_queue.maxlen,
            "exported": self._exported_count,
            "failed": self._failed_count,
            "dropped": self._dropped_count,
            "last_error_type": self._last_error,
        }
