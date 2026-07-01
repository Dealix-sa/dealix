"""Markdown → PDF renderer — Wave 14D.4 (+ Wave 16 fpdf2 fallback).

Three-tier fallback, tried in order:
  1. `weasyprint` — best fidelity (full CSS, proper Arabic/RTL shaping via
     Pango), but needs native system libraries (Pango, Cairo, GDK-Pixbuf)
     that are NOT currently installed in the production Docker image
     (see Dockerfile runtime stage) — so this tier is normally unavailable
     in production today.
  2. `pandoc` subprocess (+ xelatex) — good fidelity, but needs the pandoc
     binary and a LaTeX engine on PATH, also not currently installed in
     the production image.
  3. `fpdf2` — pure-Python (a `py3-none-any` wheel, zero native/system
     dependencies), works out of the box in the existing minimal Docker
     image with no Dockerfile changes. Basic layout only: headings and
     body text render cleanly for ASCII/Latin-script content. fpdf2's
     core fonts are latin-1 only, so this tier does NOT render Arabic
     script at all — Arabic runs are collapsed to a short "[ar]"
     placeholder (see `_latin1_safe`) rather than emitting a fabricated
     or broken glyph. It is a "the founder gets a real, valid PDF file
     today for the English content" safety net, not a substitute for
     tier 1's bilingual typographic quality. When a customer-facing
     Arabic PDF is required, the markdown export remains the correct
     deliverable until weasyprint (or a proper Arabic-shaping tier) is
     installed.

The PDF endpoints in api/routers/*.py call this; if it returns None they
fall back to returning the markdown directly with a Content-Type warning.
"""
from __future__ import annotations

import logging
import re
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


def _strip_markdown_lite(line: str) -> str:
    """Strip the handful of markdown markers fpdf2's plain-text renderer
    doesn't understand (#, **, `) so headings/bold/code don't show their
    literal punctuation in the final PDF. Deliberately minimal — this is
    a readability pass for the pure-Python fallback tier, not a full
    markdown parser."""
    text = line
    while text.startswith("#"):
        text = text[1:]
    text = text.strip()
    text = text.replace("**", "").replace("`", "")
    return text


def _latin1_safe(text: str) -> str:
    """Make ``text`` safe for fpdf2's core (latin-1-only) fonts.

    A naive ``encode("latin-1", errors="replace")`` turns every non-Latin
    character (e.g. Arabic) into a lone ``?``, but a long unbroken run of
    Arabic script (no ASCII spaces inside it) becomes a long unbroken run
    of ``?`` with no break point — which can exceed the printable line
    width and raise ``FPDFException: Not enough horizontal space``. Collapse
    any run of 2+ consecutive replacement characters into a short, clearly
    non-fabricated placeholder token instead, so word-wrap always has a
    break point. This is a legibility/robustness measure only — it does
    not attempt to render Arabic; see the module docstring for why this
    fallback tier does not shape Arabic script.
    """
    replaced = text.encode("latin-1", errors="replace").decode("latin-1")
    return re.sub(r"\?{2,}", "[ar]", replaced)


def _try_fpdf2(md: str, title: str) -> bytes | None:
    """Pure-Python fallback — no native/system dependencies. Renders plain
    text with light heading emphasis; does not attempt full markdown
    parsing or Arabic RTL shaping (see module docstring). Returns PDF
    bytes or None if fpdf2 is not installed or rendering fails."""
    try:
        from fpdf import FPDF  # type: ignore
    except ImportError:
        log.debug("pdf_renderer: fpdf2 not installed")
        return None
    try:
        pdf = FPDF()
        pdf.set_title(title)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", size=11)
        for raw_line in md.splitlines():
            line = raw_line.rstrip()
            if not line:
                pdf.ln(4)
                continue
            is_heading = line.lstrip().startswith("#")
            clean = _strip_markdown_lite(line)
            if not clean:
                continue
            pdf.set_font("Helvetica", style="B" if is_heading else "", size=13 if is_heading else 11)
            safe = _latin1_safe(clean)
            # A short prior line (e.g. a "---" rule) can leave fpdf2's x
            # cursor near the right margin instead of resetting it, which
            # then starves the next multi_cell of horizontal space and
            # raises FPDFException. Always start each line's cell at the
            # left margin explicitly rather than relying on multi_cell to
            # reset it.
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 7, safe)
        output = pdf.output()
        return bytes(output)
    except Exception:
        log.exception("pdf_renderer_fpdf2_failed")
        return None


def render_markdown_to_pdf(md: str, title: str = "Dealix Document") -> bytes | None:
    """Render markdown to PDF bytes. Returns None if no renderer available.

    Caller is responsible for falling back to text/markdown response when
    None is returned.
    """
    if not md:
        return None
    pdf = _try_weasyprint(md, title)
    if pdf is not None:
        return pdf
    pdf = _try_pandoc(md, title)
    if pdf is not None:
        return pdf
    return _try_fpdf2(md, title)


def is_pdf_available() -> dict[str, bool]:
    """Diagnostic helper used by /api/v1/health and tests."""
    weasy = False
    try:
        import weasyprint
        weasy = True
    except ImportError:
        pass
    pandoc = bool(shutil.which("pandoc"))
    fpdf2 = False
    try:
        import fpdf  # noqa: F401
        fpdf2 = True
    except ImportError:
        pass
    return {
        "weasyprint": weasy,
        "pandoc": pandoc,
        "fpdf2": fpdf2,
        "any": weasy or pandoc or fpdf2,
    }


__all__ = ["is_pdf_available", "render_markdown_to_pdf"]
