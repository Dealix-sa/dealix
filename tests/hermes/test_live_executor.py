"""LiveLLMExecutor — wrapping logic without network calls.

The executor is sync and gated by ``HERMES_LIVE_LLM``. We verify that:
- When disabled it returns the envelope untouched.
- When enabled but the API key is missing it returns ``live_skipped``.
- When the base executor returns ``ok=False`` it does not call the LLM.
- The idempotency key is deterministic for same intent + customer + day.
- The cost-budget gate refuses when the day's count of successful runs
  exceeds the budget threshold (using a manually-seeded audit ledger).

Actual network calls live in ``scripts/hermes_smoke.py --live`` so they
do not gate CI.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from dealix.hermes import LiveLLMExecutor
from dealix.hermes.live_executor import _idempotency_key, _today_cost_usd
from dealix.hermes.router import HermesRouter


@pytest.fixture
def envelope_executor():
    def _exec(task, route):
        return {
            "ok": True,
            "kind": "prompt_envelope",
            "role": route.sub_agent,
            "intent": getattr(task, "intent", ""),
            "system_constraints": ["no scraping", "no fake claims"],
            "deliverable": "structured response",
            "model_id": route.gear_config.model_id,
            "provider": route.gear_config.provider,
            "timeout": route.gear_config.timeout,
            "max_tokens": route.gear_config.max_tokens,
            "customer_id": getattr(task, "customer_id", ""),
        }
    return _exec


class _FakeTask:
    def __init__(self, intent: str, customer_id: str = "cust_test"):
        self.intent = intent
        self.customer_id = customer_id


def test_live_disabled_returns_envelope_untouched(envelope_executor, monkeypatch) -> None:
    monkeypatch.delenv("HERMES_LIVE_LLM", raising=False)
    exe = LiveLLMExecutor(base_executor=envelope_executor)
    assert exe.enabled is False
    route = HermesRouter().route("status check")
    result = exe(_FakeTask("status check"), route)
    assert result["kind"] == "prompt_envelope"
    assert "content" not in result


def test_live_enabled_without_key_marks_skipped(envelope_executor, monkeypatch) -> None:
    monkeypatch.setenv("HERMES_LIVE_LLM", "1")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    exe = LiveLLMExecutor(base_executor=envelope_executor)
    route = HermesRouter().route("write docs for the bilingual report")
    result = exe(_FakeTask("write docs"), route)
    assert result.get("live_skipped") == "missing_api_key"


def test_live_skipped_when_base_returns_not_ok(monkeypatch) -> None:
    monkeypatch.setenv("HERMES_LIVE_LLM", "1")
    monkeypatch.setenv("OPENROUTER_API_KEY", "fake-key-not-used")

    def base(task, route):
        return {"ok": False, "kind": "refusal"}

    exe = LiveLLMExecutor(base_executor=base)
    route = HermesRouter().route("status")
    result = exe(_FakeTask("hello"), route)
    assert result["ok"] is False
    assert "content" not in result


def test_idempotency_key_stable_per_day_inputs() -> None:
    k1 = _idempotency_key("draft a proposal for ACME", "cust_123")
    k2 = _idempotency_key("draft a proposal for ACME", "cust_123")
    k3 = _idempotency_key("draft a proposal for ACME", "cust_other")
    assert k1 == k2
    assert k1 != k3


def test_cost_budget_blocks_live_call(envelope_executor, monkeypatch, tmp_path) -> None:
    audit = tmp_path / "hermes-runs.jsonl"
    today = "2099-01-01"
    rows = [
        {
            "occurred_at": f"{today}T00:00:00+00:00",
            "provider": "openrouter",
            "success": True,
        }
        for _ in range(50)
    ]
    audit.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")

    monkeypatch.setenv("HERMES_AUDIT_PATH", str(audit))
    monkeypatch.setenv("HERMES_LIVE_LLM", "1")
    monkeypatch.setenv("OPENROUTER_API_KEY", "fake-key-not-used")
    monkeypatch.setenv("HERMES_DAILY_BUDGET_USD", "0.05")  # < 50 * 0.005
    monkeypatch.setenv("HERMES_COST_PER_CALL_USD", "0.005")

    # Force "today" matching by freezing the date check inside the helper.
    import dealix.hermes.live_executor as live
    real_today_rows = live._today_audit_rows  # noqa: SLF001

    def fake_today_rows():
        return rows

    monkeypatch.setattr(live, "_today_audit_rows", fake_today_rows)

    exe = LiveLLMExecutor(base_executor=envelope_executor)
    route = HermesRouter().route("write docs")
    result = exe(_FakeTask("write docs"), route)
    assert result["ok"] is False
    assert result["kind"] == "cost_budget_exceeded"
    assert "budget_usd" in result
