"""
Ollama adapter — local-first text generation.

Calls a self-hosted Ollama endpoint when configured and reachable; otherwise
degrades to a deterministic templated fallback so the OS can still compose
drafts in CI/cron with no model available. Never raises, never sends anything.

Availability is opt-in via `OLLAMA_HOST` or `ENABLE_LOCAL_LLM=true`, so a CI
run with neither set will always take the offline path — no network calls.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from .base import Adapter, AdapterResult, AdapterStatus

DEFAULT_OLLAMA_HOST = "http://localhost:11434"
REQUEST_TIMEOUT_SECONDS = 20


class OllamaAdapter(Adapter):
    name = "ollama"

    def __init__(self, env: dict[str, str] | None = None) -> None:
        self._env = env if env is not None else dict(os.environ)

    def _get(self, key: str) -> str:
        return (self._env.get(key) or "").strip()

    @property
    def host(self) -> str:
        return self._get("OLLAMA_HOST") or DEFAULT_OLLAMA_HOST

    def is_available(self) -> bool:
        return bool(self._get("OLLAMA_HOST")) or self._get("ENABLE_LOCAL_LLM").lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

    def status(self) -> AdapterStatus:
        available = self.is_available()
        return AdapterStatus(
            name=self.name,
            available=available,
            mode="live" if available else "offline_fallback",
            detail=f"host={self.host}" if available else "local model not configured",
        )

    @staticmethod
    def _fallback_text(prompt: str) -> str:
        # Deterministic, honest placeholder draft. Framed as a draft to review,
        # using hypothesis language, never a finished claim.
        head = prompt.strip().splitlines()[0][:180] if prompt.strip() else "draft"
        return (
            "[DRAFT — offline template, no model connected]\n"
            f"Topic: {head}\n"
            "We expect this draft to be refined by a local model or the founder "
            "before any use. The goal is to prepare, not to send."
        )

    def generate(
        self,
        prompt: str,
        *,
        model: str = "llama3.1",
        system: str | None = None,
    ) -> AdapterResult:
        if not self.is_available():
            return AdapterResult(
                ok=True,
                mode="offline_fallback",
                data=self._fallback_text(prompt),
                meta={"model": model, "reason": "local model not configured"},
            )

        payload: dict[str, Any] = {"model": model, "prompt": prompt, "stream": False}
        if system:
            payload["system"] = system
        body = json.dumps(payload).encode("utf-8")
        url = f"{self.host.rstrip('/')}/api/generate"
        req = urllib.request.Request(
            url, data=body, headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                raw = resp.read().decode("utf-8")
            parsed = json.loads(raw)
            text = str(parsed.get("response", "")).strip()
            if not text:
                raise ValueError("empty response from ollama")
            return AdapterResult(ok=True, mode="live", data=text, meta={"model": model})
        except (urllib.error.URLError, ValueError, json.JSONDecodeError, OSError) as exc:
            # Degrade gracefully — never break the cycle on model failure.
            return AdapterResult(
                ok=True,
                mode="offline_fallback",
                data=self._fallback_text(prompt),
                error=f"{type(exc).__name__}: {exc}",
                meta={"model": model, "reason": "ollama call failed"},
            )
