"""
Token Optimizer — complete stack for reducing LLM token consumption.
محسّن التوكنز — مجموعة أدوات متكاملة لتقليل استهلاك النماذج اللغوية.

Stack:
  counter   -> tiktoken-based counting + cost estimation
  budget    -> per-call and per-session budget enforcement
  cache     -> Redis exact + semantic caching
  compressor -> context compression for long documents/RAG
  tracker   -> Langfuse observability integration
"""
from core.token_optimizer.budget import (
    BudgetConfig,
    BudgetExceededError,
    BudgetGuard,
    SessionUsage,
    budget_check,
    get_default_guard,
)
from core.token_optimizer.counter import (
    COST_TABLE,
    CostEstimate,
    count_messages_tokens,
    count_tokens,
    estimate_cost,
    token_summary,
)
from core.token_optimizer.tracker import (
    LangfuseTracker,
    TokenUsageMiddleware,
    TraceContext,
    get_tracker,
)

__all__ = [
    "COST_TABLE",
    "BudgetConfig",
    "BudgetExceededError",
    "BudgetGuard",
    "CostEstimate",
    "LangfuseTracker",
    "SessionUsage",
    "TokenUsageMiddleware",
    "TraceContext",
    "budget_check",
    "count_messages_tokens",
    "count_tokens",
    "estimate_cost",
    "get_default_guard",
    "get_tracker",
    "token_summary",
]
