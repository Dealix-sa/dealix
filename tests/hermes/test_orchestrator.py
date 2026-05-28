"""HermesOrchestrator end-to-end dispatch behavior."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

from dealix.hermes import (
    HermesOrchestrator,
    HermesTask,
    TaskClass,
)
from dealix.hermes.agents import route_to_agent_executor
from dealix.hermes.router import HermesRouter


@pytest.fixture
def isolated_audit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    audit = tmp_path / "hermes-runs.jsonl"
    monkeypatch.setenv("HERMES_AUDIT_PATH", str(audit))
    return audit


def _last_audit_entry(path: Path) -> dict[str, Any]:
    lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert lines, "audit ledger is empty"
    return json.loads(lines[-1])


def test_dispatch_classifies_engineering_intent_and_calls_executor(
    isolated_audit: Path,
) -> None:
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(HermesTask(intent="refactor the FastAPI router for /leads"))
    assert result.decision.decision == "approved"
    assert result.route is not None
    assert result.route.task_class == TaskClass.ENGINEERING
    assert result.route.sub_agent == "dealix-engineer"
    assert result.output["ok"] is True
    assert result.output["kind"] == "prompt_envelope"

    entry = _last_audit_entry(isolated_audit)
    assert entry["sub_agent"] == "dealix-engineer"
    assert entry["governance_decision"]["decision"] == "approved"
    assert entry["run_id"] == result.run_id


def test_dispatch_classifies_content_intent(isolated_audit: Path) -> None:
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(HermesTask(intent="Write bilingual case study markdown for sector report"))
    assert result.route is not None
    assert result.route.task_class == TaskClass.CONTENT
    assert result.route.sub_agent == "dealix-content"


def test_dispatch_classifies_delivery_intent(isolated_audit: Path) -> None:
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(
        HermesTask(intent="run source passport + DQ score for customer ACME")
    )
    assert result.route is not None
    assert result.route.task_class == TaskClass.DELIVERY


def test_dispatch_defaults_to_pm_when_ambiguous(isolated_audit: Path) -> None:
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(HermesTask(intent="hello"))
    assert result.route is not None
    assert result.route.task_class == TaskClass.PM


def test_dispatch_records_signature_with_agent_id(isolated_audit: Path) -> None:
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(HermesTask(intent="status check"))
    assert result.signature["agent_id"] == "hermes"
    assert result.signature["run_id"] == result.run_id


def test_dispatch_handles_executor_exception(
    isolated_audit: Path,
) -> None:
    def failing_executor(task, route):  # type: ignore[no-untyped-def]
        raise RuntimeError("boom")

    orch = HermesOrchestrator(executor=failing_executor)
    result = orch.dispatch(HermesTask(intent="status check"))
    assert result.output["ok"] is False
    assert result.output["kind"] == "executor_error"
    assert "boom" in result.output["error"]
