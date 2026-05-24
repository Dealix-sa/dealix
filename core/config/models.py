"""
Model routing configuration — maps tasks to the best LLM provider.
توجيه النماذج — يربط كل مهمة بأفضل مزود نموذج.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.config.settings import Settings


class Provider(StrEnum):
    """Supported LLM providers | المزودون المدعومون."""

    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    GLM = "glm"
    GEMINI = "gemini"
    GROQ = "groq"
    OPENAI = "openai"
    MINIMAX = "minimax"


class Task(StrEnum):
    """Task categories — route each to the best provider | أنواع المهام."""

    # Reasoning / writing → Claude
    REASONING = "reasoning"
    SUMMARY = "summary"
    PROPOSAL = "proposal"
    PAGE_COPY = "page_copy"
    ORCHESTRATION = "orchestration"

    # Research / multimodal → Gemini
    RESEARCH = "research"
    MULTIMODAL = "multimodal"
    SOURCE_ANALYSIS = "source_analysis"

    # Fast classification → Groq
    CLASSIFICATION = "classification"
    TAGGING = "tagging"
    FAST_VARIANTS = "fast_variants"
    TRIAGE = "triage"

    # Code → DeepSeek
    CODE = "code"
    IMPLEMENTATION = "implementation"
    DEBUG = "debug"

    # Arabic / bulk → GLM
    ARABIC_TASKS = "arabic_tasks"
    CHINESE_TASKS = "chinese_tasks"
    BULK_TASKS = "bulk_tasks"


@dataclass(frozen=True)
class ModelConfig:
    """Immutable model configuration | إعدادات نموذج ثابتة."""

    provider: Provider
    model_id: str
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 60


# ═══════════════════════════════════════════════════════════════
# TASK → PROVIDER ROUTING TABLE
# جدول توجيه المهام إلى المزودين
# ═══════════════════════════════════════════════════════════════

TASK_ROUTING: dict[Task, Provider] = {
    # Claude — reasoning, writing, orchestration
    Task.REASONING: Provider.ANTHROPIC,
    Task.SUMMARY: Provider.ANTHROPIC,
    Task.PROPOSAL: Provider.ANTHROPIC,
    Task.PAGE_COPY: Provider.ANTHROPIC,
    Task.ORCHESTRATION: Provider.ANTHROPIC,
    # Gemini — research, multimodal, sources
    Task.RESEARCH: Provider.GEMINI,
    Task.MULTIMODAL: Provider.GEMINI,
    Task.SOURCE_ANALYSIS: Provider.GEMINI,
    # Groq — fast, cheap
    Task.CLASSIFICATION: Provider.GROQ,
    Task.TAGGING: Provider.GROQ,
    Task.FAST_VARIANTS: Provider.GROQ,
    Task.TRIAGE: Provider.GROQ,
    # DeepSeek — code
    Task.CODE: Provider.DEEPSEEK,
    Task.IMPLEMENTATION: Provider.DEEPSEEK,
    Task.DEBUG: Provider.DEEPSEEK,
    # GLM — Arabic, Chinese, bulk
    Task.ARABIC_TASKS: Provider.GLM,
    Task.CHINESE_TASKS: Provider.GLM,
    Task.BULK_TASKS: Provider.GLM,
}


# Fallback chain — if primary provider fails, try these in order
# سلسلة الاحتياط — إذا فشل المزود الرئيسي جرّب هؤلاء
FALLBACK_CHAIN: dict[Provider, list[Provider]] = {
    Provider.ANTHROPIC: [Provider.OPENAI, Provider.GLM],
    Provider.DEEPSEEK: [Provider.MINIMAX, Provider.ANTHROPIC, Provider.OPENAI],
    Provider.MINIMAX: [Provider.OPENAI, Provider.DEEPSEEK],
    Provider.GLM: [Provider.ANTHROPIC, Provider.GROQ],
    Provider.GEMINI: [Provider.ANTHROPIC, Provider.OPENAI],
    Provider.GROQ: [Provider.GLM, Provider.DEEPSEEK],
    Provider.OPENAI: [Provider.ANTHROPIC, Provider.GLM],
}

# When DEALIX_LLM_PROFILE=minimax — reasoning/copy/Arabic → MiniMax
MINIMAX_TASK_ROUTING: dict[Task, Provider] = {
    Task.REASONING: Provider.MINIMAX,
    Task.SUMMARY: Provider.MINIMAX,
    Task.PROPOSAL: Provider.MINIMAX,
    Task.PAGE_COPY: Provider.MINIMAX,
    Task.ORCHESTRATION: Provider.MINIMAX,
    Task.ARABIC_TASKS: Provider.MINIMAX,
    Task.CHINESE_TASKS: Provider.GLM,
    Task.BULK_TASKS: Provider.GLM,
    Task.CODE: Provider.DEEPSEEK,
    Task.IMPLEMENTATION: Provider.DEEPSEEK,
    Task.DEBUG: Provider.DEEPSEEK,
    Task.RESEARCH: Provider.GEMINI,
    Task.MULTIMODAL: Provider.GEMINI,
    Task.SOURCE_ANALYSIS: Provider.GEMINI,
    Task.CLASSIFICATION: Provider.GROQ,
    Task.TAGGING: Provider.GROQ,
    Task.FAST_VARIANTS: Provider.GROQ,
    Task.TRIAGE: Provider.GROQ,
}


def effective_dealix_llm_profile(settings: Settings | None = None) -> str:
    """
    Resolved LLM profile: minimax | default.

    Auto-selects minimax when MINIMAX_API_KEY is set, ANTHROPIC_API_KEY is not,
    and DEALIX_LLM_PROFILE is unset. Explicit DEALIX_LLM_PROFILE wins.
    """
    if settings is None:
        from core.config.settings import get_settings

        settings = get_settings()

    explicit = (settings.dealix_llm_profile or "").strip().lower()
    if explicit in {"minimax", "default"}:
        return explicit
    if explicit:
        return "default"

    if settings.has_llm_provider("minimax") and not settings.has_llm_provider("anthropic"):
        return "minimax"
    if (settings.ai_primary_provider or "").strip().lower() == "minimax":
        return "minimax"
    return "default"


def _code_provider_for_profile(settings: Settings) -> Provider:
    """CODE/DEBUG: DeepSeek when keyed, else MiniMax under minimax profile."""
    if settings.has_llm_provider("deepseek"):
        return Provider.DEEPSEEK
    if effective_dealix_llm_profile(settings) == "minimax":
        return Provider.MINIMAX
    return Provider.DEEPSEEK


def get_provider_for_task(task: Task, settings: Settings | None = None) -> Provider:
    """Get primary provider for a task | المزود الرئيسي للمهمة."""
    if settings is None:
        from core.config.settings import get_settings

        settings = get_settings()

    if effective_dealix_llm_profile(settings) == "minimax":
        if task in {Task.CODE, Task.IMPLEMENTATION, Task.DEBUG}:
            return _code_provider_for_profile(settings)
        return MINIMAX_TASK_ROUTING.get(task, Provider.MINIMAX)

    return TASK_ROUTING.get(task, Provider.ANTHROPIC)


def get_fallbacks(provider: Provider, settings: Settings | None = None) -> list[Provider]:
    """Get fallback chain for a provider | سلسلة الاحتياط للمزود."""
    return FALLBACK_CHAIN.get(provider, [Provider.ANTHROPIC])


# ═══════════════════════════════════════════════════════════════
# SMART MODEL ROUTING — cost-aware exact model per task
# توجيه ذكي يراعي التكلفة — نموذج محدد لكل مهمة
# ═══════════════════════════════════════════════════════════════

# Concrete model IDs per provider (cost-optimized picks)
PROVIDER_MODELS: dict[Provider, ModelConfig] = {
    Provider.ANTHROPIC: ModelConfig(
        provider=Provider.ANTHROPIC,
        model_id="claude-sonnet-4-5",
        max_tokens=4096,
        temperature=0.3,
    ),
    Provider.DEEPSEEK: ModelConfig(
        provider=Provider.DEEPSEEK,
        model_id="deepseek-chat",
        max_tokens=4096,
        temperature=0.2,
    ),
    Provider.GLM: ModelConfig(
        provider=Provider.GLM,
        model_id="glm-4",
        max_tokens=4096,
        temperature=0.3,
    ),
    Provider.GEMINI: ModelConfig(
        provider=Provider.GEMINI,
        model_id="gemini-2.5-flash",
        max_tokens=8192,
        temperature=0.3,
    ),
    Provider.GROQ: ModelConfig(
        provider=Provider.GROQ,
        model_id="llama-3.3-70b-versatile",
        max_tokens=2048,
        temperature=0.1,
    ),
    Provider.OPENAI: ModelConfig(
        provider=Provider.OPENAI,
        model_id="gpt-4o-mini",
        max_tokens=4096,
        temperature=0.3,
    ),
    Provider.MINIMAX: ModelConfig(
        provider=Provider.MINIMAX,
        model_id="MiniMax-M2.7",
        max_tokens=8192,
        temperature=0.3,
    ),
}


# Cost hints (USD per 1M tokens) — input/output. Used by smart router.
COST_HINTS: dict[Provider, tuple[float, float]] = {
    Provider.ANTHROPIC: (3.00, 15.00),
    Provider.DEEPSEEK: (0.14, 0.28),
    Provider.GLM: (0.14, 0.28),
    Provider.GEMINI: (0.075, 0.30),
    Provider.GROQ: (0.00, 0.00),
    Provider.OPENAI: (0.15, 0.60),
    Provider.MINIMAX: (0.30, 1.20),
}


# Feature flags for Arabic-heavy content and token size thresholds
ARABIC_THRESHOLD = 0.30  # ratio of Arabic chars → prefer GLM
SHORT_EXTRACTION_TOKENS = 2000  # below this for code/extraction → DeepSeek
CRITICAL_TASKS = {
    Task.REASONING,
    Task.PROPOSAL,
    Task.ORCHESTRATION,
}


def _arabic_ratio(text: str) -> float:
    if not text:
        return 0.0
    arabic = sum(1 for c in text if "\u0600" <= c <= "\u06ff")
    return arabic / max(len(text), 1)


def smart_route(
    task: Task,
    *,
    text_sample: str = "",
    est_tokens: int = 0,
    critical: bool = False,
    settings: Settings | None = None,
) -> ModelConfig:
    """
    Cost-aware router | توجيه ذكي يراعي التكلفة.

    Rules:
      1. CLASSIFICATION/TRIAGE/TAGGING → Groq (free)
      2. Arabic content (>30%) for non-critical → GLM
      3. Short extraction/code → DeepSeek
      4. Research → Gemini Flash
      5. Critical reasoning/proposals → Anthropic (+ caching)
      6. Else → provider from TASK_ROUTING

    When DEALIX_LLM_PROFILE=minimax: critical + Arabic-heavy → MiniMax.
    """
    if settings is None:
        from core.config.settings import get_settings

        settings = get_settings()

    minimax_profile = effective_dealix_llm_profile(settings) == "minimax"

    # 1. Free tier for classification
    if task in {Task.CLASSIFICATION, Task.TRIAGE, Task.TAGGING, Task.FAST_VARIANTS}:
        return PROVIDER_MODELS[Provider.GROQ]

    if minimax_profile:
        if critical or task in CRITICAL_TASKS:
            return PROVIDER_MODELS[Provider.MINIMAX]
        if text_sample and _arabic_ratio(text_sample) >= ARABIC_THRESHOLD:
            if task not in {Task.RESEARCH, Task.MULTIMODAL}:
                return PROVIDER_MODELS[Provider.MINIMAX]
        if task in {Task.CODE, Task.IMPLEMENTATION, Task.DEBUG}:
            code_provider = _code_provider_for_profile(settings)
            return PROVIDER_MODELS[code_provider]
        if task in {Task.RESEARCH, Task.MULTIMODAL, Task.SOURCE_ANALYSIS}:
            return PROVIDER_MODELS[Provider.GEMINI]
        provider = get_provider_for_task(task, settings)
        return PROVIDER_MODELS[provider]

    # 2. Critical reasoning always Anthropic
    if critical or task in CRITICAL_TASKS:
        return PROVIDER_MODELS[Provider.ANTHROPIC]

    # 3. Arabic-heavy → GLM (keeps cost low while handling Arabic well)
    if text_sample and _arabic_ratio(text_sample) >= ARABIC_THRESHOLD:
        if task not in {Task.RESEARCH, Task.MULTIMODAL}:
            return PROVIDER_MODELS[Provider.GLM]

    # 4. Short code/extraction → DeepSeek
    if task in {Task.CODE, Task.IMPLEMENTATION, Task.DEBUG}:
        return PROVIDER_MODELS[Provider.DEEPSEEK]
    if task == Task.SUMMARY and 0 < est_tokens <= SHORT_EXTRACTION_TOKENS:
        return PROVIDER_MODELS[Provider.DEEPSEEK]

    # 5. Research → Gemini Flash
    if task in {Task.RESEARCH, Task.MULTIMODAL, Task.SOURCE_ANALYSIS}:
        return PROVIDER_MODELS[Provider.GEMINI]

    # 6. Default — use static routing table
    provider = get_provider_for_task(task, settings)
    return PROVIDER_MODELS[provider]


def ordered_providers(
    task: Task,
    *,
    text_sample: str = "",
    critical: bool = False,
    settings: Settings | None = None,
) -> list[Provider]:
    """Return primary + fallback chain after smart routing."""
    primary = smart_route(
        task, text_sample=text_sample, critical=critical, settings=settings
    ).provider
    chain = [primary] + [p for p in get_fallbacks(primary, settings) if p != primary]
    return chain
