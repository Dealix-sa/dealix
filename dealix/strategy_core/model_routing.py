"""Declarative model target selection without network calls or secret exposure.

A local model is executable only when the caller supplies an explicit healthy
signal. Hosted fallback is disabled unless explicitly allowed and both a model
name and credential presence are configured.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping

_TRUE = {"1", "true", "yes", "on"}
_LOCAL_DEFAULTS = {
    "classify": "qwen3:4b",
    "summarize": "qwen3:4b",
    "arabic": "qwen2.5-coder:7b-64k",
    "code": "qwen2.5-coder:7b-64k",
    "strategy": "qwen2.5-coder:7b-64k",
    "default": "qwen2.5-coder:7b-64k",
}
_HOSTED_PROVIDER_CONFIG = (
    ("openrouter", "OPENROUTER_API_KEY", "OPENROUTER_MODEL", "https://openrouter.ai/api/v1"),
    ("openai", "OPENAI_API_KEY", "OPENAI_MODEL", "https://api.openai.com/v1"),
    ("deepseek", "DEEPSEEK_API_KEY", "DEEPSEEK_MODEL", "https://api.deepseek.com"),
    ("groq", "GROQ_API_KEY", "GROQ_MODEL", "https://api.groq.com/openai/v1"),
)


@dataclass(frozen=True)
class ModelTarget:
    provider: str
    model: str | None
    endpoint: str | None
    is_local: bool
    executable: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class ModelRouter:
    def __init__(self, env: Mapping[str, str] | None = None) -> None:
        self._env = dict(env or {})

    def _get(self, key: str) -> str:
        return str(self._env.get(key) or "").strip()

    def _truthy(self, key: str) -> bool:
        return self._get(key).casefold() in _TRUE

    def _local_model(self, task_kind: str) -> str:
        normalized = task_kind.strip().casefold() or "default"
        override = self._get(f"LOCAL_MODEL_{normalized.upper()}")
        return override or _LOCAL_DEFAULTS.get(normalized, _LOCAL_DEFAULTS["default"])

    def route(self, task_kind: str = "default") -> ModelTarget:
        local_enabled = self._truthy("ENABLE_LOCAL_LLM")
        local_healthy = self._truthy("LOCAL_LLM_HEALTHY")
        if local_enabled and local_healthy:
            return ModelTarget(
                provider="ollama",
                model=self._local_model(task_kind),
                endpoint=self._get("OLLAMA_HOST") or "http://127.0.0.1:11434",
                is_local=True,
                executable=True,
                reason="explicit local enablement and health evidence are present",
            )

        if self._truthy("ALLOW_HOSTED_MODEL_FALLBACK"):
            for provider, credential_key, model_key, endpoint in _HOSTED_PROVIDER_CONFIG:
                if self._get(credential_key) and self._get(model_key):
                    return ModelTarget(
                        provider=provider,
                        model=self._get(model_key),
                        endpoint=endpoint,
                        is_local=False,
                        executable=True,
                        reason=f"explicit hosted fallback enabled; {provider} configuration present",
                    )

        reason_parts = []
        if local_enabled and not local_healthy:
            reason_parts.append("local model enabled but not proven healthy")
        elif not local_enabled:
            reason_parts.append("local model not explicitly enabled")
        if not self._truthy("ALLOW_HOSTED_MODEL_FALLBACK"):
            reason_parts.append("hosted fallback disabled")
        else:
            reason_parts.append("no hosted provider has both model and credential configuration")
        return ModelTarget(
            provider="none",
            model=None,
            endpoint=None,
            is_local=False,
            executable=False,
            reason="; ".join(reason_parts),
        )

    def public_summary(self, task_kind: str = "default") -> dict[str, object]:
        """Return a target summary that never contains credential values."""

        return self.route(task_kind).to_dict()
