"""Tests for the rung 0-1 delivery HTML renderer (scripts/dealix_render_html.py)."""
from __future__ import annotations

import importlib.util
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location(
    "dealix_render_html", _REPO / "scripts" / "dealix_render_html.py"
)
render_html_mod = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(render_html_mod)

_SAMPLE = """# Proof Pack — ACME

## النتائج

نص فقرة عربي **مهم**.

- بند أول
- بند ثانٍ

| العنصر | القيمة |
|--------|--------|
| فرص | 10 |
| سعر | 499 |

> ملاحظة حوكمة: لا إرسال بدون موافقة.

---

رابط: [Dealix](https://dealix.me)
"""


def test_body_renders_each_construct():
    body = render_html_mod.md_to_html_body(_SAMPLE)
    assert "<h1>Proof Pack — ACME</h1>" in body
    assert "<h2>" in body
    assert "<strong>مهم</strong>" in body
    assert "<ul>" in body and "<li>بند أول</li>" in body
    assert "<table>" in body and "<th>العنصر</th>" in body
    assert "<td>499</td>" in body
    assert "<blockquote>" in body
    assert "<hr/>" in body
    assert '<a href="https://dealix.me">Dealix</a>' in body


def test_full_document_is_self_contained_rtl():
    doc = render_html_mod.render_html(_SAMPLE, "Dealix — Proof Pack")
    assert doc.startswith("<!doctype html>")
    assert 'dir="rtl"' in doc and 'lang="ar"' in doc
    assert "<style>" in doc  # CSS embedded — no external assets
    assert "<title>Dealix — Proof Pack</title>" in doc


def test_inline_escapes_html():
    body = render_html_mod.md_to_html_body("نص فيه <script>alert(1)</script> خطر")
    assert "<script>" not in body
    assert "&lt;script&gt;" in body
