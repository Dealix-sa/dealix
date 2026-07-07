"""
Model Router — local-first model selection with fallbacks.

Prefers a self-hosted Ollama endpoint (privacy, cost, Saudi-data locality),
falling back to configured hosted providers only when a local model is not
available. The router is *declarative*: it selects a target, it does not make
network calls here. Actual inference is done by callers that already hold the
right client and credentials, keeping this package dependency-light and safe
to import in CI.

Selection order (first available wins):
  1. Local Ollama (OLLAMA_HOST set, or default localhost)  -> is_local=True
  2. Configured hosted fallbacks (only if their API key env is present)

No secret values are read or printed — only the *presence* of an env var is
checked to decide availability.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

DEFAULT_OLLAMA_HOST = "http://localhost:11434"

# task_kind -> preferred local model tag (self-hosted defaults, overridable).
LOCAL_MODEL_BY_TASK = {
    "strategy": "llama3.1",
    "draft": "llama3.1",
    "classify": "llama3.1",
    "summarize": "llama3.1",
    "arabic": "qwen2.5",
    "code": "qwen2.5-coder",
    "default": "llama3.1",
}

# Ordered hosted fallbacks: (provider, env var that must be present, model).
HOSTED_FALLBACKS: list[tuple[str, str, str]] = [
    ("deepseek", "DEEPSEEK_API_KEY", "deepseek-chat"),
    ("groq", "GROQ_API_KEY", "llama-3.1-70b-versatile"),
    ("openai", "OPENAI_API_KEY", "gpt-4o-mini"),
]


@dataclass(frozen=True)
class ModelChoice:
    provider: str
    model: str
    endpoint: str
    is_local: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "endpoint": self.endpoint,
            "is_local": self.is_local,
            "reason": self.reason,
        }


class ModelRouter:
    def __init__(self, env: dict[str, str] | None = None, prefer_local: bool = True) -> None:
        self._env = env if env is not None else dict(os.environ)
        self.prefer_local = prefer_local

    def _get(self, name: str) -> str:
        return (self._env.get(name) or "").strip()

    def local_available(self) -> bool:
        # Local Ollama is considered available if a host is configured, or if
        # the caller has explicitly opted into local via ENABLE_LOCAL_LLM.
        return bool(self._get("OLLAMA_HOST")) or self._get("ENABLE_LOCAL_LLM").lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

    def _local_model(self, task_kind: str) -> str:
        override = self._get(f"OLLAMA_MODEL_{task_kind.upper()}")
        if override:
            return override
        return LOCAL_MODEL_BY_TASK.get(task_kind, LOCAL_MODEL_BY_TASK["default"])

    def route(self, task_kind: str = "default") -> ModelChoice:
        if self.prefer_local and self.local_available():
            host = self._get("OLLAMA_HOST") or DEFAULT_OLLAMA_HOST
            return ModelChoice(
                provider="ollama",
                model=self._local_model(task_kind),
                endpoint=host,
                is_local=True,
                reason="local-first: self-hosted Ollama available",
            )

        for provider, env_key, model in HOSTED_FALLBACKS:
            if self._get(env_key):
                return ModelChoice(
                    provider=provider,
                    model=model,
                    endpoint=f"env:{env_key}",
                    is_local=False,
                    reason=f"fallback: {provider} credentials present",
                )

        # Nothing configured — still return a deterministic local target so the
        # OS can plan drafts; execution will no-op until a model is wired.
        return ModelChoice(
            provider="ollama",
            model=self._local_model(task_kind),
            endpoint=self._get("OLLAMA_HOST") or DEFAULT_OLLAMA_HOST,
            is_local=True,
            reason="no provider configured — defaulting to local target (draft planning only)",
        )
