"""Customer-facing rendering for rung 0-1 deliverables.

Pure functions that turn a deliverable's content into a single
self-contained bilingual HTML document (and, for the Proof Pack, an
optional PDF). Two deliverable types are covered — the rung-0
``diagnostic_report`` and the rung-1 ``proof_pack``.

Reuse, not rebuild:
  - The HTML wrapper + markdown converter come from
    ``sales_os.proposal_artifact`` (``build_html_document``,
    ``markdown_to_html``) — one HTML engine, defined once.
  - The Proof Pack markdown comes from
    ``proof_architecture_os.proof_pack_render.proof_pack_to_markdown``
    (the 14 canonical sections of ``docs/empire/PROOF_PACK_STANDARD.md``).
  - PDF rendering degrades gracefully via
    ``proof_to_market.pdf_renderer`` — None when no engine is installed.

Doctrine:
  - Rendering produces a DRAFT artifact; nothing is auto-sent.
  - Bilingual AR+EN, HTML-escaped, no remote assets.
  - No fabricated proof — an empty Proof Pack renders an honest notice.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
    proof_pack_to_markdown,
)
from auto_client_acquisition.sales_os.proposal_artifact import (
    build_html_document,
)

_DISCLAIMER = (
    "Estimated outcomes are not guaranteed outcomes / "
    "النتائج التقديرية ليست نتائج مضمونة."
)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _coerce_sections(content: Any) -> dict[str, str]:
    """Coerce arbitrary section content to a ``{str: str}`` map.

    The render path accepts caller-supplied JSON, so a section value may
    be a non-string; coercing here keeps downstream ``.strip()`` safe.
    """
    if not isinstance(content, dict):
        return {}
    return {str(k): ("" if v is None else str(v)) for k, v in content.items()}


# ── Rung 0 — Free Diagnostic report ───────────────────────────────────

# Ordered (key, English title, Arabic title) for the diagnostic report.
_DIAGNOSTIC_SECTIONS: tuple[tuple[str, str, str], ...] = (
    ("context", "Context", "السياق"),
    ("inputs_reviewed", "Inputs Reviewed", "المدخلات المراجَعة"),
    ("observations", "Observations", "الملاحظات"),
    ("gaps", "Gaps Identified", "الفجوات المكتشفة"),
    ("recommended_next_step", "Recommended Next Step", "الخطوة التالية الموصى بها"),
)


def diagnostic_report_to_markdown(
    content: dict[str, Any] | None, *, customer_handle: str
) -> str:
    """Render a ``diagnostic_report`` deliverable to bilingual markdown.

    An empty/missing report renders an honest "not yet prepared" notice
    rather than fabricated findings.
    """
    customer_handle = customer_handle or "(customer)"
    sections = _coerce_sections(content)
    has_content = any(
        (sections.get(k) or "").strip() for k, _, _ in _DIAGNOSTIC_SECTIONS
    )
    generated_at = _now_iso()
    if not has_content:
        return "\n".join(
            [
                f"# Dealix Free Diagnostic — {customer_handle}",
                "",
                f"_Generated: {generated_at}_",
                "",
                "> **Diagnostic not yet prepared / لم يُعدّ التشخيص بعد.**",
                ">",
                "> This diagnostic has no recorded findings. Review the "
                "customer's inputs first. No findings are fabricated.",
                "",
                "---",
                f"_{_DISCLAIMER}_",
            ]
        )
    lines = [
        f"# Dealix Free Diagnostic — {customer_handle}",
        "",
        f"_Generated: {generated_at}_",
        "",
    ]
    for key, title_en, title_ar in _DIAGNOSTIC_SECTIONS:
        lines.append(f"## {title_en} / {title_ar}")
        lines.append("")
        lines.append((sections.get(key) or "").strip() or "_—_")
        lines.append("")
    lines.append("---")
    lines.append(f"_{_DISCLAIMER}_")
    return "\n".join(lines)


def render_diagnostic_report_html(
    content: dict[str, Any] | None, *, customer_handle: str
) -> str:
    """Render a ``diagnostic_report`` to a self-contained bilingual HTML file.

    Reuses the shared ``build_html_document`` engine — no duplicated wrapper.
    """
    md = diagnostic_report_to_markdown(content, customer_handle=customer_handle)
    return build_html_document(
        body_markdown=md,
        title=f"Dealix Free Diagnostic — {customer_handle or '(customer)'}",
        meta_line=f"Diagnostic · {datetime.now(UTC).strftime('%Y-%m-%d')}",
    )


# ── Rung 1 — 14-section Proof Pack ─────────────────────────────────────


def render_proof_pack_html(
    pack: dict[str, Any] | None, *, customer_handle: str
) -> str:
    """Render a 14-section ``proof_pack`` to a self-contained bilingual HTML file.

    The 14 sections follow ``docs/empire/PROOF_PACK_STANDARD.md``; the
    section markdown is produced by the canonical ``proof_pack_to_markdown``
    so the structure is not re-implemented here.
    """
    md = proof_pack_to_markdown(pack, customer_handle=customer_handle)
    return build_html_document(
        body_markdown=md,
        title=f"Dealix Proof Pack — {customer_handle or '(customer)'}",
        meta_line=f"Proof Pack · {datetime.now(UTC).strftime('%Y-%m-%d')}",
    )


def render_proof_pack_pdf(
    pack: dict[str, Any] | None, *, customer_handle: str
) -> bytes | None:
    """Render a ``proof_pack`` to PDF bytes, or None when no PDF engine exists.

    Graceful degradation: callers fall back to ``render_proof_pack_html``
    when this returns None (weasyprint / pandoc absent).
    """
    from auto_client_acquisition.proof_to_market.pdf_renderer import (
        render_markdown_to_pdf,
    )

    md = proof_pack_to_markdown(pack, customer_handle=customer_handle)
    return render_markdown_to_pdf(
        md, title=f"Dealix Proof Pack — {customer_handle or '(customer)'}"
    )


def render_deliverable_html(
    *,
    deliverable_type: str,
    content: dict[str, Any] | None,
    customer_handle: str,
) -> str:
    """Dispatch a deliverable type to its customer-facing HTML renderer.

    Supported (rung 0-1 only): ``diagnostic_report`` and ``proof_pack``.
    Any other type raises ``ValueError`` — this module deliberately does
    not render rung 2-5 deliverables (commercial freeze).
    """
    if deliverable_type == "diagnostic_report":
        return render_diagnostic_report_html(
            content, customer_handle=customer_handle
        )
    if deliverable_type == "proof_pack":
        return render_proof_pack_html(content, customer_handle=customer_handle)
    raise ValueError(
        f"unsupported_deliverable_type_for_render: {deliverable_type} "
        "(rung 0-1 delivery finish renders diagnostic_report + proof_pack only)"
    )


__all__ = [
    "diagnostic_report_to_markdown",
    "render_deliverable_html",
    "render_diagnostic_report_html",
    "render_proof_pack_html",
    "render_proof_pack_pdf",
]
