"""
Unified Dealix chat entry — MiniMax-first runtime or task router fallback.

Use this for founder-facing narratives and high-value sales agents instead of
calling ModelRouter or RuntimeLLMRouter directly.
"""

from __future__ import annotations

import logging

from core.config.models import Task, effective_dealix_llm_profile
from core.config.settings import Settings, get_settings
from core.llm.base import LLMResponse, Message
from core.llm.runtime_router import get_runtime_router
from core.llm.router import get_router

logger = logging.getLogger(__name__)


def _should_use_runtime_router(settings: Settings) -> bool:
    """MiniMax-first path when profile or primary provider says minimax."""
    profile = effective_dealix_llm_profile(settings)
    if profile == "minimax":
        return True
    return (settings.ai_primary_provider or "").strip().lower() == "minimax"


def _runtime_chain_configured(settings: Settings) -> bool:
    for name in (settings.ai_primary_provider, settings.ai_fallback_provider):
        if settings.has_llm_provider(name):
            return True
    return False


async def dealix_chat(
    messages: list[Message] | str,
    *,
    system: str | None = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    task: Task | None = None,
) -> LLMResponse:
    """
    Run chat through Dealix AI stack.

    1) When profile=minimax or AI_PRIMARY=minimax → RuntimeLLMRouter (env chain).
    2) Otherwise → ModelRouter.run for the given task (default SUMMARY).
    """
    settings = get_settings()
    if isinstance(messages, str):
        messages = [Message(role="user", content=messages)]

    if _should_use_runtime_router(settings) and _runtime_chain_configured(settings):
        try:
            return await get_runtime_router().chat(
                messages,
                system=system,
                max_tokens=max_tokens,
                temperature=temperature,
            )
        except Exception as exc:
            logger.warning("dealix_chat runtime_router failed, falling back to task router: %s", exc)

    router = get_router()
    return await router.run(
        task or Task.SUMMARY,
        messages,
        system=system,
        max_tokens=max_tokens,
        temperature=temperature,
    )


async def agent_llm_run(
    task: Task,
    messages: list[Message] | str,
    *,
    system: str | None = None,
    max_tokens: int = 4096,
    temperature: float = 0.7,
    text_sample: str = "",
    critical: bool = False,
) -> LLMResponse:
    """
    Agent-facing LLM call — runtime when MiniMax-first, else smart task routing.

    Classification/triage tasks always use ModelRouter (Groq free tier).
    """
    if task in {Task.CLASSIFICATION, Task.TRIAGE, Task.TAGGING, Task.FAST_VARIANTS}:
        router = get_router()
        return await router.run(
            task,
            messages,
            system=system,
            max_tokens=max_tokens,
            temperature=temperature,
        )

    settings = get_settings()
    if _should_use_runtime_router(settings) and _runtime_chain_configured(settings):
        if isinstance(messages, str):
            messages = [Message(role="user", content=messages)]
        try:
            return await get_runtime_router().chat(
                messages,
                system=system,
                max_tokens=max_tokens,
                temperature=temperature,
            )
        except Exception as exc:
            logger.warning("agent_llm_run runtime_router failed: %s", exc)

    from core.config.models import smart_route

    if isinstance(messages, str):
        sample = messages
    elif messages:
        sample = messages[-1].content
    else:
        sample = text_sample

    cfg = smart_route(
        task,
        text_sample=sample or text_sample,
        critical=critical,
    )
    router = get_router()
    return await router.run(
        task,
        messages,
        system=system,
        max_tokens=max_tokens,
        temperature=temperature,
        preferred_provider=cfg.provider,
    )
