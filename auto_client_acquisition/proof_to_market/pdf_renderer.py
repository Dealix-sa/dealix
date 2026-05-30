"""Markdown → PDF renderer — Wave 14D.4.

Thin wrapper. Prefers `weasyprint` if installed, falls back to `pandoc`
subprocess if available, otherwise returns None + logs reason. The PDF
endpoints in api/routers/*.py call this; if it returns None they fall
back to returning the markdown directly with a Content-Type warning.
"""
from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

log = logging.getLogger(__name__)


def _try_weasyprint(md: str, title: str) -> bytes | None:
    """Try weasyprint. Returns PDF bytes or None."""
    try:
        # Light HTML wrapper around the markdown — minimal but readable.
        # We avoid heavy markdown→HTML libs; weasyprint can render plain
        # text wrapped in <pre>.
        try:
            import markdown as _md  # type: ignore
            html_body = _md.markdown(md, extensions=["tables", "fenced_code"])
        except ImportError:
            # Fallback: wrap in <pre> for monospace readable output
            import html as _html
            html_body = f"<pre style='white-space:pre-wrap'>{_html.escape(md)}</pre>"

        full_html = (
            "<!doctype html><html lang='ar' dir='auto'><head>"
            "<meta charset='utf-8'>"
            f"<title>{title}</title>"
            "<style>"
            "body{font-family:'Noto Sans','Helvetica Neue',Arial,sans-serif;line-height:1.5;"
            "margin:2cm;color:#222}"
            "h1,h2,h3{color:#0a0a0a;border-bottom:1px solid #ddd;padding-bottom:6px}"
            "table{border-collapse:collapse;width:100%;margin:12px 0}"
            "th,td{border:1px solid #ccc;padding:6px}"
            "pre{background:#f6f8fa;padding:10px;border-radius:6px;overflow-x:auto}"
            "</style></head><body>"
            f"{html_body}"
            "</body></html>"
        )

        from weasyprint import HTML  # type: ignore
        return HTML(string=full_html).write_pdf()
    except ImportError:
        log.debug("pdf_renderer: weasyprint not installed")
        return None
    except Exception:
        log.exception("pdf_renderer_weasyprint_failed")
        return None


def _try_pandoc(md: str, title: str) -> bytes | None:
    """Try pandoc subprocess. Returns PDF bytes or None."""
    if not shutil.which("pandoc"):
        log.debug("pdf_renderer: pandoc binary not available on PATH")
        return None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as fp_in:
            fp_in.write(md)
            md_path = Path(fp_in.name)
        out_path = md_path.with_suffix(".pdf")
        proc = subprocess.run(  # noqa: S603 — pandoc args from controlled templates
            [  # noqa: S607 — PATH-resolved trusted tool
                "pandoc",
                str(md_path),
                "-o",
                str(out_path),
                "--metadata",
                f"title={title}",
                "--pdf-engine=xelatex",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if proc.returncode != 0 or not out_path.exists():
            log.warning("pdf_renderer_pandoc_failed: %s", proc.stderr[:200])
            return None
        data = out_path.read_bytes()
        try:
            md_path.unlink(missing_ok=True)
            out_path.unlink(missing_ok=True)
        except Exception:
            pass
        return data
    except Exception:
        log.exception("pdf_renderer_pandoc_exception")
        return None


def _try_reportlab(md: str, title: str) -> bytes | None:
    """Try reportlab — pure Python, no system deps. Returns PDF bytes or None."""
    try:
        import io
        import re

        from reportlab.lib import colors  # type: ignore
        from reportlab.lib.pagesizes import A4  # type: ignore
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # type: ignore
        from reportlab.lib.units import cm  # type: ignore
        from reportlab.platypus import (  # type: ignore
            HRFlowable,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
        )
        from reportlab.pdfbase import pdfmetrics  # type: ignore
        from reportlab.pdfbase.ttfonts import TTFont  # type: ignore

        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
            title=title,
        )

        # Register a Unicode-capable font if available, otherwise use Helvetica
        base_font = "Helvetica"
        bold_font = "Helvetica-Bold"

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "DTitle",
            parent=styles["Title"],
            fontName=bold_font,
            fontSize=18,
            textColor=colors.HexColor("#0a0a0a"),
            spaceAfter=12,
        )
        h2_style = ParagraphStyle(
            "DH2",
            parent=styles["Heading2"],
            fontName=bold_font,
            fontSize=12,
            textColor=colors.HexColor("#1a1a2e"),
            spaceBefore=14,
            spaceAfter=4,
        )
        body_style = ParagraphStyle(
            "DBody",
            parent=styles["Normal"],
            fontName=base_font,
            fontSize=10,
            leading=15,
            spaceAfter=6,
        )
        caption_style = ParagraphStyle(
            "DCaption",
            parent=styles["Normal"],
            fontName=base_font,
            fontSize=8,
            textColor=colors.HexColor("#666666"),
            spaceAfter=4,
        )

        story = [Paragraph(title, title_style), Spacer(1, 0.3 * cm)]

        # Parse markdown into reportlab flowables
        for line in md.splitlines():
            stripped = line.strip()
            if not stripped:
                story.append(Spacer(1, 0.15 * cm))
                continue
            # Escape HTML-special chars for reportlab's XML parser
            safe = (
                stripped
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            if stripped.startswith("# "):
                story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd"), spaceAfter=4))
                story.append(Paragraph(safe[2:].strip(), h2_style))
            elif stripped.startswith("## "):
                story.append(Paragraph(safe[3:].strip(), h2_style))
            elif stripped.startswith("### "):
                story.append(Paragraph(f"<b>{safe[4:].strip()}</b>", body_style))
            elif stripped.startswith(("- ", "* ", "• ")):
                story.append(Paragraph(f"• {safe[2:].strip()}", body_style))
            elif re.match(r"^\d+\.\s", stripped):
                story.append(Paragraph(safe, body_style))
            elif stripped.startswith("**") and stripped.endswith("**"):
                story.append(Paragraph(f"<b>{safe[2:-2]}</b>", body_style))
            elif stripped.startswith("_") and stripped.endswith("_"):
                story.append(Paragraph(f"<i>{safe[1:-1]}</i>", caption_style))
            else:
                story.append(Paragraph(safe, body_style))

        doc.build(story)
        return buf.getvalue()
    except ImportError:
        log.debug("pdf_renderer: reportlab not installed")
        return None
    except Exception:
        log.exception("pdf_renderer_reportlab_failed")
        return None


def render_markdown_to_pdf(md: str, title: str = "Dealix Document") -> bytes | None:
    """Render markdown to PDF bytes. Returns None if no renderer available.

    Tries weasyprint → reportlab → pandoc in order. Caller is responsible
    for falling back to text/markdown when None is returned.
    """
    if not md:
        return None
    pdf = _try_weasyprint(md, title)
    if pdf is not None:
        return pdf
    pdf = _try_reportlab(md, title)
    if pdf is not None:
        return pdf
    pdf = _try_pandoc(md, title)
    return pdf


def is_pdf_available() -> dict[str, bool]:
    """Diagnostic helper used by /api/v1/health and tests."""
    weasy = False
    try:
        import weasyprint
        weasy = True
    except ImportError:
        pass
    pandoc = bool(shutil.which("pandoc"))
    return {"weasyprint": weasy, "pandoc": pandoc, "any": weasy or pandoc}


__all__ = ["is_pdf_available", "render_markdown_to_pdf"]
