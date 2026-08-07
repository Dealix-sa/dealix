from __future__ import annotations

import asyncio

from api.routers import command_bus
from core.config.models import Task
from core.llm.base import LLMResponse


def test_command_bus_calls_model_router_run_contract(monkeypatch) -> None:
    class FakeRouter:
        async def run(self, task, messages, **kwargs):
            assert task == Task.ARABIC_TASKS
            assert len(messages) == 1
            assert messages[0].role == "user"
            assert kwargs["system"] == "system"
            return LLMResponse(
                content='{"action_type":"note"}',
                provider="fake",
                model="fake-model",
            )

    monkeypatch.setattr("core.llm.router.get_router", lambda: FakeRouter())
    content, model = asyncio.run(command_bus._call_llm("system", "user"))
    assert content == '{"action_type":"note"}'
    assert model == "fake-model"
