"""Proposal artifact builder — turns proposal markdown into a single
self-contained, shareable HTML file.

The artifact is the deliverable the founder hands to a prospect. It is
a DRAFT only — delivery to the customer routes through the Approval
Command Center; this module never sends anything.

Design constraints:
  - No new dependency: a minimal hand-rolled markdown converter.
  - Self-contained: inline CSS, no external assets, no remote ``src``.
  - Bilingual-safe: ``dir="auto"`` per block so AR and EN sections
    each render in the correct direction within one document.
"""
from __future__ import annotations

import html
import re
from datetime import UTC, datetime

_NON_GUARANTEE = (
    "Estimated outcomes are not guaranteed outcomes "
    "/ النتائج التقديرية ليست نتائج مضمونة."
)


def _inline(text: str) -> str:
    """Escape, then apply inline markdown (**bold**, _italic_)."""
    out = html.escape(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<em>\1</em>", out)
    return out


def markdown_to_html(md: str) -> str:
    """Minimal markdown → HTML. Handles headings, lists, hr, paragraphs.

    Deliberately small — proposal markdown is simple. Every block carries
    ``dir="auto"`` so mixed AR/EN content renders correctly.
    """
    lines = md.replace("\r\n", "\n").split("\n")
    blocks: list[str] = []
    para: list[str] = []
    list_items: list[str] = []

    def flush_para() -> None:
        if para:
            blocks.append(f'<p dir="auto">{"<br>".join(_inline(x) for x in para)}</p>')
            para.clear()

    def flush_list() -> None:
        if list_items:
            items = "".join(f'<li dir="auto">{_inline(x)}</li>' for x in list_items)
            blocks.append(f"<ul>{items}</ul>")
            list_items.clear()

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            flush_para()
            flush_list()
            continue
        if stripped in ("---", "***", "___"):
            flush_para()
            flush_list()
            blocks.append("<hr>")
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            flush_para()
            flush_list()
            level = len(heading.group(1))
            blocks.append(
                f'<h{level} dir="auto">{_inline(heading.group(2))}</h{level}>'
            )
            continue
        if stripped.startswith(("- ", "* ")):
            flush_para()
            list_items.append(stripped[2:])
            continue
        flush_list()
        para.append(stripped)

    flush_para()
    flush_list()
    return "\n".join(blocks)


_STYLE = """
:root { color-scheme: light; }
body { font-family: 'Segoe UI', Tahoma, Arial, sans-serif; line-height: 1.7;
  max-width: 820px; margin: 0 auto; padding: 48px 28px; color: #0f172a;
  background: #ffffff; }
h1 { font-size: 1.9rem; border-bottom: 3px solid #10b981; padding-bottom: 8px; }
h2 { font-size: 1.3rem; margin-top: 1.8em; color: #0f172a; }
h3 { font-size: 1.05rem; color: #334155; }
ul { padding-inline-start: 1.4em; }
li { margin: 4px 0; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 2.4em 0; }
strong { color: #0f172a; }
.dealix-meta { color: #64748b; font-size: 0.85rem; margin-bottom: 2em; }
.dealix-footer { margin-top: 3em; padding-top: 1em; border-top: 1px solid #e2e8f0;
  color: #64748b; font-size: 0.8rem; }
"""


def build_html_document(
    *,
    body_markdown: str,
    title: str,
    meta_line: str = "",
) -> str:
    """Return a single self-contained bilingual HTML document.

    Shared HTML engine: inline CSS, ``dir="auto"`` per block, HTML-escaped,
    no remote assets. Reused by every customer-facing rendered deliverable
    (proposal artifact, diagnostic report, Proof Pack) so the wrapper is
    defined once.
    """
    inner = markdown_to_html(body_markdown)
    meta = (
        f'<div class="dealix-meta" dir="auto">{html.escape(meta_line)}</div>\n'
        if meta_line
        else ""
    )
    footer = (
        f'<div class="dealix-footer" dir="auto">{html.escape(_NON_GUARANTEE)}<br>'
        "Dealix &mdash; Governed Revenue &amp; AI Operations. "
        "This document is a draft for review.</div>"
    )
    return (
        '<!DOCTYPE html>\n<html lang="ar" dir="auto">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(title)}</title>\n"
        f"<style>{_STYLE}</style>\n</head>\n<body>\n"
        f"{meta}{inner}\n{footer}\n</body>\n</html>\n"
    )


def build_proposal_artifact(
    *,
    body_markdown: str,
    engagement_id: str,
    customer_name: str = "",
    proposal_date: str = "",
) -> str:
    """Return a single self-contained bilingual HTML proposal artifact."""
    date = proposal_date or datetime.now(UTC).strftime("%Y-%m-%d")
    title = f"Dealix Proposal — {customer_name}".strip(" —")
    meta_line = f"Engagement: {engagement_id} · {date}"
    return build_html_document(
        body_markdown=body_markdown, title=title, meta_line=meta_line
    )


def proposal_artifact_filename(engagement_id: str) -> str:
    """Filesystem-safe artifact filename for an engagement — deterministic
    so the serve endpoint can locate it by engagement id alone."""
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", engagement_id)
    return f"proposal_{safe}.html"


__all__ = [
    "build_html_document",
    "build_proposal_artifact",
    "markdown_to_html",
    "proposal_artifact_filename",
]
