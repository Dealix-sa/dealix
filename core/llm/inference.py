"""Safe application-facing entry point for routed LLM inference.

Application code must call ``ModelRouter.run`` rather than a provider-client
method. Keeping this adapter in one place also gives operators an explicit,
machine-readable failure when no provider is configured; callers must not
replace that failure with canned text presented as model output.
"""

from __future__ import annotations

import asyncio

from core.config.models import Provider, Task
from core.llm.base import Message
from core.llm.router import get_router


class NoLLMProviderConfigured(RuntimeError):
    """Raised when inference is requested without a configured provider."""


async def complete_with_router(
    system_prompt: str,
    user_input: str,
    *,
    task: Task = Task.ARABIC_TASKS,
    max_tokens: int = 400,
    temperature: float = 0.4,
    timeout_seconds: float = 12.0,
) -> tuple[str, str]:
    """Run one completion through the configured model router.

    Prefer GLM for Arabic work when available. Otherwise select the first
    configured provider explicitly, so an OpenAI-only deployment remains
    usable even when OpenAI is absent from the task's default fallback chain.
    """

    router = get_router()
    providers = router.available_providers()
    if not providers:
        raise NoLLMProviderConfigured("no_llm_provider_configured")

    preferred = Provider.GLM if Provider.GLM in providers else providers[0]
    response = await asyncio.wait_for(
        router.run(
            task=task,
            messages=[Message(role="user", content=user_input)],
            system=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            preferred_provider=preferred,
        ),
        timeout=timeout_seconds,
    )
    return response.content, response.model


__all__ = ["NoLLMProviderConfigured", "complete_with_router"]
