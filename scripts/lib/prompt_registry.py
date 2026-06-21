"""Prompt registry for the AI router (V14).

Maps a logical task (+ language) to a versioned prompt template stored under
``business/ai/prompts/``. Templates are plain Markdown; the registry only
resolves and loads them — it does not call a model.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = REPO_ROOT / "business" / "ai" / "prompts"

# Logical task -> prompt template filename stem. Bilingual tasks resolve to a
# language-specific file; single-language tasks share one template.
_TASKS: dict[str, dict[str, str]] = {
    "outreach_draft": {"ar": "outreach_draft_ar", "en": "outreach_draft_en"},
    "proposal_section": {"ar": "proposal_section_ar", "en": "proposal_section_en"},
    "objection_response": {"ar": "objection_response_ar", "en": "objection_response_en"},
    "lead_scoring_explanation": {"*": "lead_scoring_explanation"},
    "compliance_review": {"*": "compliance_review"},
    "proof_report_summary": {"*": "proof_report_summary"},
    "client_status_summary": {"*": "client_status_summary"},
    "sales_call_summary": {"*": "sales_call_summary"},
    "weakness_hypothesis": {"*": "weakness_hypothesis"},
    "translation_ar_en": {"*": "translation_ar_en"},
}


def list_tasks() -> list[str]:
    return sorted(_TASKS)


def has_task(task: str) -> bool:
    return task in _TASKS


def resolve_path(task: str, lang: str = "en") -> Path | None:
    spec = _TASKS.get(task)
    if not spec:
        return None
    stem = spec.get(lang) or spec.get("*") or next(iter(spec.values()))
    path = PROMPTS_DIR / f"{stem}.md"
    return path if path.exists() else None


def get_prompt(task: str, lang: str = "en") -> str | None:
    """Return the template text for a task/language, or ``None`` if absent."""
    path = resolve_path(task, lang)
    if path is None:
        return None
    return path.read_text(encoding="utf-8")
