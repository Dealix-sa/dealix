from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

_MODULE_PATH = Path(__file__).resolve().parents[1] / "core" / "observability" / "langfuse_integration.py"
_SPEC = importlib.util.spec_from_file_location("_dealix_langfuse_hardening", _MODULE_PATH)
assert _SPEC and _SPEC.loader
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)

LLMCall = _MODULE.LLMCall
LangfuseTracker = _MODULE.LangfuseTracker


class CaptureTracker(LangfuseTracker):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(public_key="pk-test", secret_key="sk-test", **kwargs)
        self.sent: list[dict[str, Any]] = []
        self.attempts = 0
        self.failures_before_success = 0

    async def _post_payload(self, data: dict[str, Any]) -> None:
        self.attempts += 1
        if self.attempts <= self.failures_before_success:
            raise RuntimeError("transient export failure")
        self.sent.append(data)


@pytest.mark.asyncio
async def test_export_is_disabled_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEALIX_LANGFUSE_EXPORT_ENABLED", raising=False)
    tracker = CaptureTracker()

    await tracker.trace_llm_call(LLMCall(prompt="hello", response="world"))

    assert tracker.sent == []
    assert tracker.get_export_status()["enabled"] is False
    assert tracker.get_export_status()["queued"] == 0


@pytest.mark.asyncio
async def test_recursive_redaction_happens_before_transport() -> None:
    tracker = CaptureTracker(enabled=True)
    call = LLMCall(
        prompt="Email sami@example.com and call +966501234567",
        response="Bearer abcdefghijklmnopqrstuvwxyz",
        session_id="session-raw-value",
        error="token-test_abcdefghijklmnop",
        metadata={
            "api_key": "must-never-leave",
            "nested": {"email": "owner@dealix.me", "safe": "kept"},
        },
    )

    await tracker.trace_llm_call(call)
    assert await tracker.flush()

    payload = tracker.sent[0]
    assert payload["input"] == "Email [REDACTED_EMAIL] and call [REDACTED_PHONE]"
    assert payload["output"] == "[REDACTED_BEARER]"
    assert payload["session_id"] == "[REDACTED]"
    assert payload["error"] == "[REDACTED_SECRET]"
    assert payload["metadata"]["api_key"] == "[REDACTED]"
    assert payload["metadata"]["nested"]["email"] == "[REDACTED_EMAIL]"
    assert payload["metadata"]["nested"]["safe"] == "kept"
    assert payload["usage"]["prompt_tokens"] == 0
    assert call.prompt == "Email sami@example.com and call +966501234567"


@pytest.mark.asyncio
async def test_unapproved_or_insecure_export_target_fails_closed() -> None:
    unapproved = CaptureTracker(enabled=True, host="https://collector.example.com")
    insecure = CaptureTracker(
        enabled=True,
        host="http://cloud.langfuse.com",
        allowed_hosts={"cloud.langfuse.com"},
    )

    await unapproved.trace_llm_call(LLMCall(prompt="a", response="b"))
    await insecure.trace_llm_call(LLMCall(prompt="a", response="b"))

    assert unapproved.get_export_status()["export_allowed"] is False
    assert "allowlist" in str(unapproved.get_export_status()["block_reason"])
    assert insecure.get_export_status()["export_allowed"] is False
    assert "https" in str(insecure.get_export_status()["block_reason"])
    assert unapproved.sent == insecure.sent == []


@pytest.mark.asyncio
async def test_export_retries_without_raising_into_business_flow() -> None:
    tracker = CaptureTracker(enabled=True, max_retries=2)
    tracker.failures_before_success = 1

    trace_id = await tracker.trace_llm_call(LLMCall(prompt="safe", response="safe"))
    assert trace_id
    assert await tracker.flush()

    status = tracker.get_export_status()
    assert tracker.attempts == 2
    assert status["exported"] == 1
    assert status["failed"] == 0
    assert status["last_error_type"] is None


@pytest.mark.asyncio
async def test_bounded_queue_drops_oldest_payload_deterministically() -> None:
    tracker = CaptureTracker(enabled=True, max_queue_size=2)

    for index in range(5):
        await tracker.trace_llm_call(LLMCall(prompt=f"prompt-{index}", response="safe"))

    status_before_flush = tracker.get_export_status()
    assert status_before_flush["queued"] == 2
    assert status_before_flush["dropped"] == 3
    assert await tracker.flush()

    assert [payload["input"] for payload in tracker.sent] == ["prompt-3", "prompt-4"]
