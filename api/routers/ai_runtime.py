"""
Dealix AI runtime HTTP surface — MiniMax-first (env: AI_PRIMARY_PROVIDER=minimax).

Keys live in .env.local only. Responses never include API keys or raw upstream bodies.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from core.llm.runtime_router import RuntimeLLMRouter, get_runtime_router

router = APIRouter(
    prefix="/api/v1/ai-runtime",
    tags=["AI Runtime"],
    dependencies=[Depends(require_admin_key)],
)


class ChatRequest(BaseModel):
    """Minimal chat request for runtime router smoke / founder tools."""

    message: str = Field(..., min_length=1, max_length=32_000)
    system: str | None = Field(default=None, max_length=8_000)
    max_tokens: int = Field(default=1024, ge=16, le=8192)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    content: str
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    finish_reason: str | None = None
    used_fallback: bool = False


@router.get("/status")
async def ai_runtime_status() -> dict[str, Any]:
    """Provider chain + configuration (no secrets)."""
    return get_runtime_router().status()


@router.post("/chat", response_model=ChatResponse)
async def ai_runtime_chat(body: ChatRequest) -> ChatResponse:
    """
    Execute a single-turn chat via env-configured primary → fallback chain.
    Admin key required — incurs provider cost.
    """
    runtime: RuntimeLLMRouter = get_runtime_router()
    chain = runtime.provider_chain()
    if not any(runtime.settings.has_llm_provider(p.value) for p in chain):
        raise HTTPException(
            status_code=503,
            detail=(
                "No AI providers configured. Set MINIMAX_API_KEY (and optional "
                "AI_FALLBACK_PROVIDER key) in .env.local or Railway"
            ),
        )

    try:
        response = await runtime.chat(
            body.message,
            system=body.system,
            max_tokens=body.max_tokens,
            temperature=body.temperature,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    used_fallback = response.provider != runtime.primary.value
    return ChatResponse(
        content=response.content,
        provider=response.provider,
        model=response.model,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        finish_reason=response.finish_reason,
        used_fallback=used_fallback,
    )
