"""Outreach drafter — Sprint Day-4 deliverable.

Takes the ranked accounts from ``data_os.account_ranker`` and produces
bilingual AR + EN outreach drafts, one per account. **No LLM. No external
send. Approval-gated.**

Doctrine compliance:
- #2/#3 — no scraping, no auto-send. Drafts are written to disk with an
  explicit ``requires_approval`` flag and a sidecar approval_required.json.
- #4 — no fabricated context. Personalization only substitutes variables
  the caller actually supplied; missing fields become "" not invented.
- #5 — templates are validated against a small forbidden-language list
  (نضمن, guarantee, guaranteed, مضمون). Templates that promise outcomes
  are refused before any draft is rendered.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from auto_client_acquisition.data_os.account_ranker import RankedAccount

FORBIDDEN_LANGUAGE: tuple[str, ...] = (
    "نضمن",
    "مضمون",
    "guarantee",
    "guaranteed",
    "guaranteed outcome",
)
ALLOWED_DISCLAIMERS: tuple[str, ...] = (
    "ليست نتائج مضمونة",
    "ليست مضمونة",
    "estimated outcomes are not guaranteed outcomes",
    "estimated outcomes are not guaranteed",
    "are not guaranteed outcomes",
    "are not guaranteed",
    "not guaranteed outcomes",
    "not guaranteed",
    "it does not promise",
    "does not promise",
    "no guarantee",
)
TEMPLATE_VARS: tuple[str, ...] = (
    "company_name",
    "sector",
    "city",
    "offer_name",
    "founder_name",
)
DEFAULT_TEMPLATE_NAME = "revenue_intelligence_sprint_v1"


class OutreachDrafterError(ValueError):
    """Raised when a template or input violates doctrine (e.g. guarantee language)."""


@dataclass(frozen=True, slots=True)
class OutreachTemplate:
    """A bilingual template with AR + EN subject and body."""

    name: str
    subject_ar: str
    subject_en: str
    body_ar: str
    body_en: str

    def validate(self) -> None:
        """Refuse templates that contain forbidden guarantee language.

        The doctrine #5 disclaimer phrases (e.g. "ليست نتائج مضمونة",
        "not guaranteed") are explicitly allowed because they NEGATE the
        promise. We strip those phrases first, then scan the remainder.
        """
        haystack = " ".join(
            [self.subject_ar, self.subject_en, self.body_ar, self.body_en]
        ).lower()
        for allowed in ALLOWED_DISCLAIMERS:
            haystack = haystack.replace(allowed.lower(), " ")
        for term in FORBIDDEN_LANGUAGE:
            if term.lower() in haystack:
                raise OutreachDrafterError(
                    f"template {self.name!r} contains forbidden language: {term!r}"
                )


@dataclass(frozen=True, slots=True)
class OutreachDraft:
    """One generated draft for one ranked account."""

    company_name: str
    template_name: str
    subject_ar: str
    subject_en: str
    body_ar: str
    body_en: str
    requires_approval: bool = True
    rank_total: float = 0.0
    rank_reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_markdown(self) -> str:
        return (
            f"# {self.company_name} — DRAFT (requires founder approval before sending)\n\n"
            f"_Template: `{self.template_name}` · Rank total: {self.rank_total}_\n\n"
            "## القسم العربي\n\n"
            f"**الموضوع:** {self.subject_ar}\n\n"
            f"{self.body_ar}\n\n"
            "---\n\n"
            "## English Section\n\n"
            f"**Subject:** {self.subject_en}\n\n"
            f"{self.body_en}\n"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "company_name": self.company_name,
            "template_name": self.template_name,
            "subject_ar": self.subject_ar,
            "subject_en": self.subject_en,
            "body_ar": self.body_ar,
            "body_en": self.body_en,
            "requires_approval": self.requires_approval,
            "rank_total": self.rank_total,
            "rank_reasons": list(self.rank_reasons),
        }


DEFAULT_TEMPLATE = OutreachTemplate(
    name=DEFAULT_TEMPLATE_NAME,
    subject_ar="تشخيص إيرادات قصير لـ {company_name}",
    subject_en="A short revenue diagnostic for {company_name}",
    body_ar=(
        "السلام عليكم،\n\n"
        "اسمي {founder_name} من Dealix. لاحظنا أن قطاع {sector} في {city} "
        "يواجه نفس النمط: حسابات كثيرة، وقت متابعة محدود، وقرار يومي "
        "صعب حول من نتواصل معه اليوم.\n\n"
        "نقدّم سبرنت {offer_name} لمدة 7 أيام: نأخذ ملف الحسابات لديكم، "
        "نُصدر باسلاين جودة بيانات، ونرتّب أفضل 10 حسابات بمنطق "
        "قابل للتفسير، ونسلّم Proof Pack من 14 قسماً.\n\n"
        "النتائج التقديرية ليست نتائج مضمونة — السبرنت يُوثّق منهجية، لا يَعِد بصفقات.\n\n"
        "هل أرسل لكم خطّة السبرنت بصفحة واحدة؟\n\n"
        "— {founder_name} · Dealix"
    ),
    body_en=(
        "Hi,\n\n"
        "I'm {founder_name} from Dealix. We've noticed the same pattern in "
        "{sector} in {city}: too many accounts, limited follow-up time, and "
        "a hard daily call on who to contact today.\n\n"
        "We offer a 7-day {offer_name} Sprint: we take your accounts file, "
        "produce a data-quality baseline, rank the top 10 accounts with an "
        "explainable rubric, and deliver a 14-section Proof Pack.\n\n"
        "Estimated outcomes are not guaranteed outcomes — the Sprint documents "
        "a methodology, it does not promise deals.\n\n"
        "Want me to send the one-page Sprint plan?\n\n"
        "— {founder_name} · Dealix"
    ),
)

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slug(name: str) -> str:
    base = _SLUG_RE.sub("-", name.strip().lower()).strip("-")
    return (base or "unnamed")[:64]


def _render(template_str: str, ctx: dict[str, str]) -> str:
    """Replace {var} tokens with ctx values. Missing keys become empty."""
    out = template_str
    for key in TEMPLATE_VARS:
        out = out.replace("{" + key + "}", ctx.get(key, ""))
    return out


def generate_outreach_drafts(
    *,
    ranking: list[RankedAccount],
    offer_name: str,
    founder_name: str,
    template: OutreachTemplate | None = None,
    drafts_root: Path | str | None = None,
) -> list[OutreachDraft]:
    """One bilingual approval-gated draft per ranked account.

    If ``drafts_root`` is supplied, each draft is also written to
    ``<drafts_root>/<company-slug>.md`` and a sibling
    ``<company-slug>.approval_required.json`` is written to enforce the
    approval gate on disk. No network, no send.
    """
    if not offer_name.strip():
        raise OutreachDrafterError("offer_name is required")
    if not founder_name.strip():
        raise OutreachDrafterError("founder_name is required")
    tpl = template or DEFAULT_TEMPLATE
    tpl.validate()

    drafts: list[OutreachDraft] = []
    root = Path(drafts_root) if drafts_root else None
    if root is not None:
        root.mkdir(parents=True, exist_ok=True)

    for account in ranking:
        ctx = {
            "company_name": account.company_name,
            "sector": str(account.row.get("sector", "")).strip(),
            "city": str(account.row.get("city", "")).strip(),
            "offer_name": offer_name,
            "founder_name": founder_name,
        }
        draft = OutreachDraft(
            company_name=account.company_name,
            template_name=tpl.name,
            subject_ar=_render(tpl.subject_ar, ctx),
            subject_en=_render(tpl.subject_en, ctx),
            body_ar=_render(tpl.body_ar, ctx),
            body_en=_render(tpl.body_en, ctx),
            rank_total=account.total,
            rank_reasons=account.reasons,
        )
        drafts.append(draft)
        if root is not None:
            slug = _slug(account.company_name)
            (root / f"{slug}.md").write_text(draft.to_markdown(), encoding="utf-8")
            (root / f"{slug}.approval_required.json").write_text(
                json.dumps(
                    {
                        "company_name": account.company_name,
                        "template_name": tpl.name,
                        "state": "draft_only",
                        "requires_approval_before_send": True,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
    return drafts


__all__ = [
    "ALLOWED_DISCLAIMERS",
    "DEFAULT_TEMPLATE",
    "DEFAULT_TEMPLATE_NAME",
    "FORBIDDEN_LANGUAGE",
    "OutreachDraft",
    "OutreachDrafterError",
    "OutreachTemplate",
    "TEMPLATE_VARS",
    "generate_outreach_drafts",
]
