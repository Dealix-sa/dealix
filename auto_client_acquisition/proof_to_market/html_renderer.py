"""HTML renderer for rung 0-1 customer-facing deliverables.

Turns the markdown produced by the existing renderers (the Free AI Ops
Diagnostic report and the 7-Day Revenue Proof Sprint Proof Pack) into a
self-contained, Arabic-first / bilingual HTML document.

Reuse, not reinvention: the markdown bodies are produced upstream by
``diagnostic_engine`` and ``proof_architecture_os.proof_pack_render``. This
module only adds the HTML wrapping layer that the PDF renderer already
builds internally but never exposed as a standalone deliverable. No new
markdown / PDF / templating dependency is introduced -- the markdown->HTML
conversion here is intentionally minimal and deterministic.

Doctrine: Arabic-first (``dir='rtl' lang='ar'``), draft-only (no send), and
the document carries the payment->delivery audit reference in its footer so
every rendered deliverable is traceable to a paid / committed pilot.
"""

from __future__ import annotations

import html as _html
import re
from datetime import datetime, timezone

from auto_client_acquisition.proof_to_market.delivery_audit import DeliveryAuditLink

_DISCLAIMER = (
    "Estimated outcomes are not guaranteed outcomes / "
    "النتائج التقديرية ليست نتائج مضمونة."
)

# Self-contained stylesheet. Arabic-first: RTL base direction, mixed LTR
# fragments (code, English lines) auto-render via the unicode-bidi default.
_STYLE = (
    "body{font-family:'Segoe UI','Noto Sans Arabic','Noto Sans',"
    "Tahoma,Arial,sans-serif;line-height:1.7;margin:0;padding:2rem;"
    "color:#1a1a2e;background:#f7f7fb}"
    ".doc{max-width:820px;margin:0 auto;background:#fff;padding:2.5rem;"
    "border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.08)}"
    "h1{font-size:1.5rem;color:#0b0b2b;margin-top:0}"
    "h2{font-size:1.15rem;color:#13134a;border-bottom:1px solid #e3e3ee;"
    "padding-bottom:.3rem;margin-top:1.8rem}"
    "h3{font-size:1rem;color:#2a2a5a}"
    "code{background:#f0f0f6;padding:.1rem .3rem;border-radius:4px;"
    "font-size:.9em;direction:ltr;unicode-bidi:embed}"
    "blockquote{border-inline-start:3px solid #c9c9e0;margin-inline:0;"
    "padding-inline-start:1rem;color:#444}"
    "table{border-collapse:collapse;width:100%;margin:1rem 0}"
    "th,td{border:1px solid #d8d8e4;padding:.5rem;text-align:start}"
    "hr{border:0;border-top:1px solid #e3e3ee;margin:1.6rem 0}"
    ".audit{font-size:.8rem;color:#666;margin-top:1.4rem;direction:ltr;"
    "unicode-bidi:embed}"
    ".disclaimer{font-size:.85rem;color:#8a8a8a;font-style:italic}"
    ".draft{display:inline-block;background:#fff4d6;color:#7a5b00;"
    "border:1px solid #e6c65a;border-radius:4px;padding:.15rem .5rem;"
    "font-size:.8rem}"
)

_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")


def _inline(text: str) -> str:
    """Escape, then apply the minimal inline markdown set (bold, code)."""
    out = _html.escape(text)
    out = _INLINE_CODE.sub(lambda m: f"<code>{m.group(1)}</code>", out)
    out = _BOLD.sub(lambda m: f"<strong>{m.group(1)}</strong>", out)
    return out


def markdown_to_html_fragment(md: str) -> str:
    """Deterministic minimal markdown -> HTML body fragment.

    Supports the subset the rung 0-1 renderers actually emit: ATX headings,
    unordered/ordered lists, blockquotes, horizontal rules, and paragraphs
    with inline bold + code. No new dependency, no network, no LLM.
    """
    lines = (md or "").replace("\r\n", "\n").split("\n")
    parts: list[str] = []
    list_open: str | None = None  # "ul" | "ol" | None
    para: list[str] = []

    def _flush_para() -> None:
        if para:
            parts.append("<p>" + "<br>".join(_inline(x) for x in para) + "</p>")
            para.clear()

    def _close_list() -> None:
        nonlocal list_open
        if list_open:
            parts.append(f"</{list_open}>")
            list_open = None

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            _flush_para()
            _close_list()
            continue
        if stripped in ("---", "***", "___"):
            _flush_para()
            _close_list()
            parts.append("<hr>")
            continue
        heading = re.match(r"(#{1,6})\s+(.*)$", stripped)
        if heading:
            _flush_para()
            _close_list()
            level = len(heading.group(1))
            parts.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
            continue
        if stripped.startswith(("> ", ">")):
            _flush_para()
            _close_list()
            parts.append(
                "<blockquote>" + _inline(stripped[1:].strip()) + "</blockquote>"
            )
            continue
        ol = re.match(r"\d+[.)]\s+(.*)$", stripped)
        ul = re.match(r"[-*+]\s+(.*)$", stripped)
        if ol:
            _flush_para()
            if list_open != "ol":
                _close_list()
                parts.append("<ol>")
                list_open = "ol"
            parts.append(f"<li>{_inline(ol.group(1))}</li>")
            continue
        if ul:
            _flush_para()
            if list_open != "ul":
                _close_list()
                parts.append("<ul>")
                list_open = "ul"
            parts.append(f"<li>{_inline(ul.group(1))}</li>")
            continue
        _close_list()
        para.append(stripped)

    _flush_para()
    _close_list()
    return "\n".join(parts)


def render_deliverable_html(
    md: str,
    *,
    title: str,
    audit_link: DeliveryAuditLink | None = None,
) -> str:
    """Wrap a markdown deliverable body in a self-contained bilingual HTML page.

    ``audit_link`` -- when supplied, the payment/written-commitment audit
    reference is embedded in the footer so the rendered deliverable is
    traceable to a paid or committed pilot. The document is always marked a
    draft: it is reviewed and sent by the founder, never auto-sent.
    """
    safe_title = _html.escape(title or "Dealix Document")
    body = markdown_to_html_fragment(md)
    generated_at = datetime.now(timezone.utc).isoformat()

    audit_html = ""
    if audit_link is not None:
        ref = _html.escape(
            f"{audit_link.audit_id} "
            f"({audit_link.reference_kind}:{audit_link.reference_id})"
        )
        audit_html = (
            f'<p class="audit">Audit / مرجع التدقيق: {ref}<br>'
            f"engagement: {_html.escape(audit_link.engagement_id)}</p>"
        )

    return (
        "<!doctype html>"
        "<html lang='ar' dir='rtl'>"
        "<head>"
        "<meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        f"<title>{safe_title}</title>"
        f"<style>{_STYLE}</style>"
        "</head>"
        "<body>"
        "<div class='doc'>"
        "<p><span class='draft'>Draft / مسودة — founder review required "
        "before sending</span></p>"
        f"{body}"
        "<hr>"
        f"{audit_html}"
        f"<p class='disclaimer'>{_html.escape(_DISCLAIMER)}</p>"
        f"<p class='audit'>Generated / صدر: {_html.escape(generated_at)}</p>"
        "</div>"
        "</body>"
        "</html>"
    )


__all__ = [
    "markdown_to_html_fragment",
    "render_deliverable_html",
]
