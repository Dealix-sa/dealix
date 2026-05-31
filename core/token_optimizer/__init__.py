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
from core.token_optimizer.counter import (
    count_tokens,
    count_messages_tokens,
    estimate_cost,
    token_summary,
    CostEstimate,
    COST_TABLE,
)
from core.token_optimizer.budget import (
    BudgetConfig,
    BudgetGuard,
    BudgetExceededError,
    SessionUsage,
    get_default_guard,
    budget_check,
)
from core.token_optimizer.tracker import (
    LangfuseTracker,
    TokenUsageMiddleware,
    TraceContext,
    get_tracker,
)

__all__ = [
    # counter
    "count_tokens",
    "count_messages_tokens",
    "estimate_cost",
    "token_summary",
    "CostEstimate",
    "COST_TABLE",
    # budget
    "BudgetConfig",
    "BudgetGuard",
    "BudgetExceededError",
    "SessionUsage",
    "get_default_guard",
    "budget_check",
    # tracker
    "LangfuseTracker",
    "TokenUsageMiddleware",
    "TraceContext",
    "get_tracker",
]
