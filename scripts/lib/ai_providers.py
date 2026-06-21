"""AI providers for the router (V14).

Two providers share one interface:

* ``DeterministicProvider`` — no network, no model. Produces a safe, templated
  draft from the task + prompt. This is the default and the only provider used
  in CI / demo mode.
* ``LiveProvider`` — a thin placeholder that would call a real model when keys
  are configured. It deliberately falls back to the deterministic provider
  unless explicitly wired, so nothing leaves the workspace by accident.

Every generated draft ends with a human-review banner and never contains a
guaranteed-outcome claim or an auto-send instruction.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

_REVIEW_BANNER = {
    "ar": "— مسودة للمراجعة البشرية فقط. الإرسال يتطلب موافقة بشرية صريحة. لا وعود نتائج.",
    "en": "— Draft for human review only. Sending requires explicit human approval. No outcome promises.",
}


def _summarise(prompt: str, limit: int = 240) -> str:
    text = " ".join((prompt or "").split())
    return text[:limit]


@dataclass
class Provider:
    name: str
    deterministic: bool

    def generate(self, *, task: str, prompt: str, lang: str = "en", template: str | None = None) -> str:  # noqa: D401
        raise NotImplementedError


class DeterministicProvider(Provider):
    def __init__(self) -> None:
        super().__init__(name="deterministic", deterministic=True)

    def generate(self, *, task: str, prompt: str, lang: str = "en", template: str | None = None) -> str:
        lang = "ar" if str(lang).lower().startswith("ar") else "en"
        gist = _summarise(prompt)
        banner = _REVIEW_BANNER[lang]

        if task == "outreach_draft":
            if lang == "ar":
                body = (
                    "مرحبًا، لاحظنا إشارة قد تستحق مراجعة workflow لديكم.\n"
                    "نقترح Diagnostic مجاني قصير لتحديد أكبر فرصة تحسين.\n"
                    f"السياق: {gist}"
                )
            else:
                body = (
                    "Hi — we noticed a signal that may be worth a quick workflow review.\n"
                    "We'd suggest a short, free Diagnostic to find the biggest improvement.\n"
                    f"Context: {gist}"
                )
            return f"{body}\n\n{banner}"

        header = {
            "proposal_section": ("مقترح (مسودة)", "Proposal section (draft)"),
            "lead_scoring_explanation": ("شرح تقييم العميل المحتمل", "Lead-scoring explanation"),
            "compliance_review": ("مراجعة الامتثال", "Compliance review"),
            "proof_report_summary": ("ملخص تقرير الإثبات", "Proof report summary"),
            "client_status_summary": ("ملخص حالة العميل", "Client status summary"),
        }.get(task, ("مسودة", "Draft"))
        title = header[0] if lang == "ar" else header[1]
        return f"{title}: {gist}\n\n{banner}"


class LiveProvider(Provider):
    def __init__(self) -> None:
        super().__init__(name="live", deterministic=False)
        self._fallback = DeterministicProvider()

    def generate(self, *, task: str, prompt: str, lang: str = "en", template: str | None = None) -> str:
        # No real model is wired here on purpose; live calls require explicit,
        # human-approved integration. Until then we degrade to deterministic.
        return self._fallback.generate(task=task, prompt=prompt, lang=lang, template=template)


def has_live_keys() -> bool:
    return bool(
        os.environ.get("ANTHROPIC_API_KEY")
        or os.environ.get("DEEPSEEK_API_KEY")
        or os.environ.get("GROQ_API_KEY")
    )


def get_provider(use_ai: bool = False) -> Provider:
    """Return the deterministic provider by default; live only when asked AND
    keys exist (and even then it degrades safely)."""
    if use_ai and has_live_keys():
        return LiveProvider()
    return DeterministicProvider()
