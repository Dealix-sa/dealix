"""Deterministic AI router (V14).

Single entry point — ``route(task, prompt, lang, use_ai)`` — that:

1. Runs the inbound prompt through the safety gate. Banned requests
   (guaranteed outcomes, scraping, cold/mass outreach, auto-send) are
   **refused** without generating anything.
2. Resolves the task's prompt template from the registry.
3. Generates a draft with the selected provider (deterministic by default).
4. Re-scans the output; any banned claim flips the result to **refused**.
5. Returns a typed result that is always ``pending_human_review`` when it
   passes — nothing is ever auto-approved or auto-sent.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import ai_providers, ai_safety, prompt_registry
from .ai_memory import RouterMemory


@dataclass
class RouteResult:
    task: str
    lang: str
    output: str
    provider: str
    deterministic: bool
    safety_passed: bool
    review_status: str  # "pending_human_review" | "refused"
    reasons: list[str] = field(default_factory=list)


def route(
    task: str,
    prompt: str,
    lang: str = "en",
    use_ai: bool = False,
    memory: RouterMemory | None = None,
) -> RouteResult:
    lang = "ar" if str(lang).lower().startswith("ar") else "en"

    inbound = ai_safety.scan_prompt(prompt)
    if not inbound.passed:
        result = RouteResult(
            task=task, lang=lang, output="", provider="none",
            deterministic=True, safety_passed=False,
            review_status="refused", reasons=inbound.reasons,
        )
        if memory is not None:
            memory.record(_audit(result))
        return result

    template = prompt_registry.get_prompt(task, lang)
    provider = ai_providers.get_provider(use_ai=use_ai)
    output = provider.generate(task=task, prompt=prompt, lang=lang, template=template)

    outbound = ai_safety.scan_output(output)
    if not outbound.passed:
        result = RouteResult(
            task=task, lang=lang, output=output, provider=provider.name,
            deterministic=provider.deterministic, safety_passed=False,
            review_status="refused", reasons=outbound.reasons,
        )
        if memory is not None:
            memory.record(_audit(result))
        return result

    result = RouteResult(
        task=task, lang=lang, output=output, provider=provider.name,
        deterministic=provider.deterministic, safety_passed=True,
        review_status="pending_human_review", reasons=[],
    )
    if memory is not None:
        memory.record(_audit(result))
    return result


def _audit(r: RouteResult) -> dict[str, object]:
    return {
        "task": r.task,
        "lang": r.lang,
        "provider": r.provider,
        "review_status": r.review_status,
        "safety_passed": r.safety_passed,
        "reasons": r.reasons,
    }
