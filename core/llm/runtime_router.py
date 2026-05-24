"""
Dealix runtime AI router — env-driven primary + fallback providers.

Cursor is the IDE; Dealix runtime owns MiniMax / DeepSeek / OpenAI keys via
``.env.local``. Never log or return API keys from this module.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from core.config.models import Provider, effective_dealix_llm_profile
from core.config.settings import Settings, get_settings
from core.llm.base import LLMResponse, Message
from core.llm.router import ModelRouter, get_router

logger = logging.getLogger(__name__)

_SAFE_ERROR_RE = re.compile(
    r"(sk-[a-zA-Z0-9_-]{8,}|api[_-]?key|authorization|bearer\s+\S+)",
    re.IGNORECASE,
)


def _sanitize_error(exc: Exception) -> str:
    """Strip likely secret fragments from error messages."""
    msg = str(exc) or exc.__class__.__name__
    return _SAFE_ERROR_RE.sub("[redacted]", msg)[:500]


def parse_provider_name(name: str) -> Provider:
    """Map env string to Provider enum."""
    normalized = (name or "").strip().lower()
    try:
        return Provider(normalized)
    except ValueError as e:
        supported = ", ".join(p.value for p in Provider)
        raise ValueError(f"Unknown AI provider '{name}'. Supported: {supported}") from e


def _normalize_openai_base_url(base_url: str) -> str:
    """Ensure OpenAI-compatible base URLs end with /v1."""
    url = (base_url or "").rstrip("/")
    if not url:
        return "https://api.openai.com/v1"
    if url.endswith("/v1"):
        return url
    if url.endswith("/v1/"):
        return url.rstrip("/")
    return f"{url}/v1"


class RuntimeLLMRouter:
    """
    Primary/fallback chat router driven by AI_PRIMARY_PROVIDER and
    AI_FALLBACK_PROVIDER environment variables.
    """

    def __init__(
        self,
        settings: Settings | None = None,
        model_router: ModelRouter | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self._model_router = model_router or get_router()
        self.primary = parse_provider_name(self.settings.ai_primary_provider)
        self.fallback = parse_provider_name(self.settings.ai_fallback_provider)

    def provider_chain(self) -> list[Provider]:
        """Ordered providers: primary then fallback (deduplicated)."""
        chain: list[Provider] = []
        for provider in (self.primary, self.fallback):
            if provider not in chain:
                chain.append(provider)
        return chain

    def status(self) -> dict[str, Any]:
        """Safe status payload — no secrets."""
        chain = self.provider_chain()
        configured: dict[str, bool] = {}
        available: dict[str, bool] = {}
        for provider in chain:
            name = provider.value
            configured[name] = self.settings.has_llm_provider(name)
            available[name] = self._model_router.get_client(provider) is not None

        profile = effective_dealix_llm_profile(self.settings)
        minimax_hint = None
        if self.settings.has_llm_provider("minimax"):
            minimax_hint = (
                "Token Plan uses max_completion_tokens≤2048; "
                "insufficient_balance (1008) → add Credits at platform.minimax.io"
            )

        return {
            "service": "dealix_ai_runtime",
            "primary_provider": self.primary.value,
            "fallback_provider": self.fallback.value,
            "dealix_llm_profile": profile,
            "provider_chain": [p.value for p in chain],
            "configured": configured,
            "router_ready": available,
            "models": {
                Provider.DEEPSEEK.value: self.settings.deepseek_model,
                Provider.MINIMAX.value: self.settings.minimax_model,
                Provider.OPENAI.value: self.settings.openai_model,
            },
            "token_plan_hint": minimax_hint,
            "base_urls_normalized": {
                Provider.DEEPSEEK.value: _normalize_openai_base_url(
                    self.settings.deepseek_base_url
                ),
                Provider.MINIMAX.value: _normalize_openai_base_url(
                    self.settings.minimax_base_url
                ),
            },
        }

    async def chat(
        self,
        messages: list[Message] | str,
        *,
        system: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> LLMResponse:
        """
        Run chat on primary provider; on failure try fallback.
        Raises RuntimeError with sanitized message if all providers fail.
        """
        if isinstance(messages, str):
            messages = [Message(role="user", content=messages)]

        last_error: Exception | None = None
        chain = self.provider_chain()

        for idx, provider in enumerate(chain):
            client = self._model_router.get_client(provider)
            if client is None:
                logger.debug("Runtime router skip unconfigured provider=%s", provider.value)
                continue

            try:
                if idx > 0:
                    logger.warning(
                        "Runtime AI fallback %s → %s",
                        self.primary.value,
                        provider.value,
                    )
                return await client.chat(
                    messages=messages,
                    system=system,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "Runtime provider %s failed: %s",
                    provider.value,
                    _sanitize_error(exc),
                )
                continue

        detail = _sanitize_error(last_error) if last_error else "no providers configured"
        raise RuntimeError(
            f"AI runtime failed for chain {[p.value for p in chain]}. Last error: {detail}"
        )


_runtime_router: RuntimeLLMRouter | None = None


def get_runtime_router() -> RuntimeLLMRouter:
    """Singleton runtime router (rebuilt when settings cache is cleared)."""
    global _runtime_router
    if _runtime_router is None:
        _runtime_router = RuntimeLLMRouter()
    return _runtime_router


def reset_runtime_router() -> None:
    """Clear singleton — for tests after env changes."""
    global _runtime_router
    _runtime_router = None
