"""PDF renderer — Wave 14D.4 (+ Wave 16 fpdf2 fallback tier)."""
from __future__ import annotations

import pytest

from auto_client_acquisition.proof_to_market.pdf_renderer import (
    _latin1_safe,
    _try_fpdf2,
    is_pdf_available,
    render_markdown_to_pdf,
)


def test_render_returns_none_on_empty_input():
    assert render_markdown_to_pdf("") is None


def test_is_pdf_available_returns_shape():
    info = is_pdf_available()
    assert "weasyprint" in info
    assert "pandoc" in info
    assert "fpdf2" in info
    assert "any" in info
    assert isinstance(info["any"], bool)


def test_render_gracefully_handles_missing_backend():
    # When neither weasyprint nor pandoc is available, returns None (NOT raise).
    info = is_pdf_available()
    pdf = render_markdown_to_pdf("# Hello\n\nWorld.", title="Test")
    if info["any"]:
        # If a backend exists, PDF bytes start with %PDF-.
        assert pdf is not None
        assert pdf[:5] == b"%PDF-"
    else:
        assert pdf is None


# ---------------------------------------------------------------------------
# fpdf2 fallback tier — pure-Python, zero native/system dependencies. These
# tests exercise the tier directly (bypassing weasyprint/pandoc) so they run
# deterministically regardless of what else is installed in the environment.
# ---------------------------------------------------------------------------


def test_fpdf2_available_in_this_environment():
    # fpdf2 is a declared, pinned requirement (requirements.txt) — if this
    # ever goes False, the dependency was accidentally dropped.
    assert is_pdf_available()["fpdf2"] is True


def test_fpdf2_renders_plain_ascii_markdown():
    pdf = _try_fpdf2("# Title\n\nSome body text.", title="Test")
    assert pdf is not None
    assert pdf[:5] == b"%PDF-"


def test_fpdf2_never_raises_on_bilingual_disclaimer_line():
    """Regression test: a line mixing English + a long unbroken Arabic run
    (e.g. the standard bilingual disclaimer) previously crashed fpdf2's
    line-breaking with 'Not enough horizontal space to render a single
    character' because encode(errors='replace') produced an unbroken run
    of '?' with no space to wrap on. Must render successfully (as bytes),
    never raise, and never silently fall through to None for this input."""
    md = (
        "## Section\n\n"
        "Body content.\n\n"
        "---\n"
        "_Estimated outcomes are not guaranteed outcomes / "
        "النتائج التقديرية ليست نتائج مضمونة._"
    )
    pdf = _try_fpdf2(md, title="Bilingual Test")
    assert pdf is not None
    assert pdf[:5] == b"%PDF-"


def test_fpdf2_cursor_reset_after_horizontal_rule():
    """Regression test: rendering a short line like '---' can leave fpdf2's
    internal x cursor near the right margin instead of resetting it, which
    then starves the next multi_cell() call of horizontal space. The
    renderer must explicitly reset the x cursor before every line."""
    md = "First line.\n\n---\nSecond line right after a horizontal rule."
    pdf = _try_fpdf2(md, title="Cursor Reset Test")
    assert pdf is not None
    assert pdf[:5] == b"%PDF-"


def test_latin1_safe_collapses_long_arabic_runs_to_placeholder():
    text = "English words النتائج التقديرية ليست نتائج مضمونة more English"
    safe = _latin1_safe(text)
    # No long unbroken run of literal '?' replacement characters remains.
    assert "?" * 2 not in safe
    assert "[ar]" in safe
    assert "English words" in safe
    assert "more English" in safe


def test_latin1_safe_leaves_pure_ascii_untouched():
    text = "Plain ASCII text, no special characters."
    assert _latin1_safe(text) == text


@pytest.mark.parametrize(
    "md",
    [
        "",
        "\n\n\n",
        "# Heading only",
        "**bold** and `code` and normal text",
        "A " * 500,  # a single very long line to exercise wrapping
    ],
)
def test_fpdf2_handles_edge_case_inputs_without_raising(md):
    # None is an acceptable outcome for empty input at the top-level
    # render_markdown_to_pdf() (guarded there), but _try_fpdf2 itself must
    # never raise for any of these shapes — either bytes or None, no
    # exception should propagate.
    result = _try_fpdf2(md, title="Edge Case")
    assert result is None or result[:5] == b"%PDF-"
