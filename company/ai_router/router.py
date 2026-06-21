#!/usr/bin/env python3
"""
Dealix AI Provider Router — multi-provider LLM routing with fallback.

Features:
  - Environment-driven provider order (no hardcoded keys)
  - Local-first (Ollama) option
  - Cloud fallback chain
  - Per-provider health checks
  - Daily budget guard (AI_DAILY_BUDGET_USD)
  - Timeout and retry handling
  - Task-based routing hints
  - Safe default: returns None when no provider is available (never crashes)

Usage:
    from company.ai_router.router import ai_complete

    response = ai_complete("Summarize this lead in Arabic", task="summarize")
    if response:
        print(response.text)
    else:
        print("No AI provider available — using template fallback")

Environment:
    OPENAI_API_KEY
    DEEPSEEK_API_KEY
    OPENROUTER_API_KEY
    MINIMAX_API_KEY
    KIMI_API_KEY
    GROQ_API_KEY
    OLLAMA_BASE_URL        (default: http://localhost:11434)
    AI_PROVIDER_ORDER      (default: local,deepseek,openrouter,openai,minimax,kimi,groq)
    AI_DAILY_BUDGET_USD    (default: 5.0)
    AI_TIMEOUT_SECONDS     (default: 60)
    AI_MAX_RETRIES         (default: 2)
"""
from __future__ import annotations

import json
import os
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
USAGE_LOG = ROOT / "company" / "runtime" / "ai_usage" / f"{date.today().isoformat()}_usage.json"


@dataclass
class AIResponse:
    text: str
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float = 0.0


@dataclass
class ProviderConfig:
    name: str
    api_key_env: str
    base_url: str
    default_model: str
    cost_per_1k_tokens: float = 0.001
    task_hints: list[str] = field(default_factory=list)


PROVIDERS: dict[str, ProviderConfig] = {
    "openai": ProviderConfig(
        name="openai",
        api_key_env="OPENAI_API_KEY",
        base_url="https://api.openai.com/v1",
        default_model="gpt-4o-mini",
        cost_per_1k_tokens=0.00015,
        task_hints=["complex", "multilingual", "code"],
    ),
    "deepseek": ProviderConfig(
        name="deepseek",
        api_key_env="DEEPSEEK_API_KEY",
        base_url="https://api.deepseek.com/v1",
        default_model="deepseek-chat",
        cost_per_1k_tokens=0.00014,
        task_hints=["code", "analysis", "arabic"],
    ),
    "openrouter": ProviderConfig(
        name="openrouter",
        api_key_env="OPENROUTER_API_KEY",
        base_url="https://openrouter.ai/api/v1",
        default_model="openai/gpt-4o-mini",
        cost_per_1k_tokens=0.00015,
        task_hints=["fallback", "multilingual"],
    ),
    "groq": ProviderConfig(
        name="groq",
        api_key_env="GROQ_API_KEY",
        base_url="https://api.groq.com/openai/v1",
        default_model="llama-3.1-8b-instant",
        cost_per_1k_tokens=0.00005,
        task_hints=["fast", "summarize"],
    ),
    "minimax": ProviderConfig(
        name="minimax",
        api_key_env="MINIMAX_API_KEY",
        base_url="https://api.minimax.chat/v1",
        default_model="abab6.5s-chat",
        cost_per_1k_tokens=0.00012,
        task_hints=["arabic", "chinese"],
    ),
    "kimi": ProviderConfig(
        name="kimi",
        api_key_env="KIMI_API_KEY",
        base_url="https://api.moonshot.cn/v1",
        default_model="moonshot-v1-8k",
        cost_per_1k_tokens=0.00012,
        task_hints=["long_context", "arabic"],
    ),
}


def _get_provider_order() -> list[str]:
    raw = os.environ.get("AI_PROVIDER_ORDER", "local,deepseek,openrouter,openai,minimax,kimi,groq")
    return [p.strip() for p in raw.split(",") if p.strip()]


def _budget_remaining() -> float:
    daily_limit = float(os.environ.get("AI_DAILY_BUDGET_USD", "5.0"))
    if not USAGE_LOG.exists():
        return daily_limit
    try:
        data = json.loads(USAGE_LOG.read_text())
        spent = sum(entry.get("cost_usd", 0) for entry in data.get("calls", []))
        return daily_limit - spent
    except Exception:
        return daily_limit


def _log_usage(response: AIResponse) -> None:
    USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
    data: dict = {"date": date.today().isoformat(), "calls": []}
    if USAGE_LOG.exists():
        try:
            data = json.loads(USAGE_LOG.read_text())
        except Exception:
            pass  # corrupted or empty usage log — start fresh for this run
    data.setdefault("calls", []).append({
        "provider": response.provider,
        "model": response.model,
        "prompt_tokens": response.prompt_tokens,
        "completion_tokens": response.completion_tokens,
        "cost_usd": response.cost_usd,
        "timestamp": time.time(),
    })
    USAGE_LOG.write_text(json.dumps(data, indent=2))


def _call_ollama(prompt: str, model: str, timeout: int) -> Optional[AIResponse]:
    base = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(
        f"{base}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
            text = data.get("response", "")
            if not text:
                return None
            return AIResponse(text=text, provider="local", model=model)
    except Exception:
        return None


def _call_openai_compat(
    prompt: str, config: ProviderConfig, timeout: int
) -> Optional[AIResponse]:
    api_key = os.environ.get(config.api_key_env, "")
    if not api_key:
        return None

    payload = json.dumps({
        "model": config.default_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
    }).encode()
    req = urllib.request.Request(
        f"{config.base_url}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
            text = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            pt = usage.get("prompt_tokens", 0)
            ct = usage.get("completion_tokens", 0)
            cost = (pt + ct) / 1000 * config.cost_per_1k_tokens
            return AIResponse(
                text=text,
                provider=config.name,
                model=config.default_model,
                prompt_tokens=pt,
                completion_tokens=ct,
                cost_usd=cost,
            )
    except Exception:
        return None


def ai_complete(
    prompt: str,
    task: str = "general",
    max_retries: int | None = None,
    timeout: int | None = None,
) -> Optional[AIResponse]:
    """
    Route prompt to best available provider.
    Returns None when no provider is available — callers must handle this.
    Never raises; never leaks API keys in logs.
    """
    if _budget_remaining() <= 0:
        return None

    timeout = timeout or int(os.environ.get("AI_TIMEOUT_SECONDS", "60"))
    retries = max_retries if max_retries is not None else int(os.environ.get("AI_MAX_RETRIES", "2"))
    order = _get_provider_order()

    for provider_name in order:
        for attempt in range(retries + 1):
            response: Optional[AIResponse] = None

            if provider_name == "local":
                ollama_model = os.environ.get("OLLAMA_MODEL", "llama3.2")
                response = _call_ollama(prompt, ollama_model, timeout)
            elif provider_name in PROVIDERS:
                response = _call_openai_compat(prompt, PROVIDERS[provider_name], timeout)

            if response:
                _log_usage(response)
                return response

            if attempt < retries:
                time.sleep(2 ** attempt)

    return None


def health_check() -> dict[str, str]:
    """Return which providers are configured (key present), without revealing key values."""
    status: dict[str, str] = {}
    for name, cfg in PROVIDERS.items():
        status[name] = "configured" if os.environ.get(cfg.api_key_env) else "no_key"
    ollama_base = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    try:
        urllib.request.urlopen(f"{ollama_base}/api/tags", timeout=2)
        status["local"] = "reachable"
    except Exception:
        status["local"] = "unreachable"
    status["budget_remaining_usd"] = str(round(_budget_remaining(), 4))
    return status


if __name__ == "__main__":
    import sys
    print("AI Provider Health Check:")
    for k, v in health_check().items():
        print(f"  {k}: {v}")
    sys.exit(0)
