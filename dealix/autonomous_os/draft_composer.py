"""
Draft Composer — turns a planned step into actual draft text.

Uses the ModelRouter to pick a target and the local-first OllamaAdapter to
generate content, falling back to a deterministic template when no model is
available. The composer is the bridge between "planning" and "prepared draft".

It only ever produces text for review. It does not send, post, or approve.
All prompts steer toward hypothesis language ("we expect / the goal is / we
will measure") and forbid fabricated metrics or guarantees.
"""

from __future__ import annotations

from typing import Any

from .adapters.ollama_adapter import OllamaAdapter
from .model_router import ModelRouter

_SYSTEM_PROMPT = (
    "You are Dealix's draft assistant for a Saudi B2B AI operating-system company. "
    "You produce DRAFTS ONLY for founder review — never final sends. "
    "Rules: no fabricated metrics, no fake clients/testimonials, no guaranteed-ROI "
    "claims. Use hypothesis language (we expect / the goal is / we will measure). "
    "Keep drafts concise and professional. Default to the requested language."
)


class DraftComposer:
    def __init__(
        self,
        env: dict[str, str] | None = None,
        router: ModelRouter | None = None,
        ollama: OllamaAdapter | None = None,
    ) -> None:
        self.router = router or ModelRouter(env=env)
        self.ollama = ollama or OllamaAdapter(env=env)

    def _task_kind(self, action: str) -> str:
        a = action.lower()
        if "proposal" in a or "sprint" in a:
            return "draft"
        if "post" in a or "content" in a or "case_study" in a:
            return "draft"
        if "research" in a or "map" in a:
            return "summarize"
        if "classify" in a or "flag" in a:
            return "classify"
        return "draft"

    def compose(
        self,
        *,
        action: str,
        strategy_id: str,
        language: str = "ar",
        offer: str | None = None,
        description: str = "",
    ) -> dict[str, Any]:
        choice = self.router.route(self._task_kind(action))
        prompt = (
            f"Draft for strategy '{strategy_id}', action '{action}'.\n"
            f"Language: {language}.\n"
            f"Offer context: {offer or 'n/a'}.\n"
            f"Intent: {description or action}.\n"
            "Produce a short, review-ready draft. Mark it clearly as a draft."
        )
        # Local-first, and *only* local: the composer never calls a public model
        # endpoint (safety doctrine). If the router selected a hosted provider
        # because no local model is available, we still generate locally/offline
        # and report that honestly rather than naming a provider we never call.
        if choice.is_local:
            result = self.ollama.generate(prompt, model=choice.model, system=_SYSTEM_PROMPT)
            generation_mode = result.mode
            draft_text = result.data
        else:
            generation_mode = "local_unavailable_template"
            draft_text = self.ollama._fallback_text(prompt)
        return {
            "action": action,
            "strategy_id": strategy_id,
            "language": language,
            "offer": offer,
            "model": choice.to_dict(),
            "model_used_for_generation": choice.provider if choice.is_local else "none_local_only",
            "generation_mode": generation_mode,
            "draft_text": draft_text,
            "is_draft": True,
            "will_send": False,
        }
