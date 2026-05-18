"""Rung 0-1 deliverable rendering tests — Workstream B (B1 + B2).

Covers the customer-facing HTML rendering for the rung-0 ``diagnostic_report``
and the rung-1 14-section ``proof_pack``. The renderers reuse the shared
``proposal_artifact`` HTML engine — these tests assert the doctrine holds:
self-contained HTML, bilingual AR+EN, escaped, honest empty notices, no
fabricated proof.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.deliverables.render import (
    diagnostic_report_to_markdown,
    render_deliverable_html,
    render_diagnostic_report_html,
    render_proof_pack_html,
    render_proof_pack_pdf,
)
from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
)
from auto_client_acquisition.proof_to_market.pdf_renderer import is_pdf_available

_DIAG_CONTENT = {
    "context": "Reviewed the lead intake sheet and the WhatsApp inbox.",
    "inputs_reviewed": "120 leads, 3 screens.",
    "observations": "No owner on 40% of leads.",
    "gaps": "Follow-up gap on stale leads.",
    "recommended_next_step": "Run the 7-Day Revenue Proof Sprint.",
}


def _full_pack() -> dict:
    return {
        "engagement_id": "e1",
        "customer_id": "c1",
        "sections": {k: f"Content for {k}." for k in PROOF_PACK_V2_SECTIONS},
        "score": 88,
        "tier": "case_candidate",
    }


# ── B1 — diagnostic report ─────────────────────────────────────────────


def test_diagnostic_markdown_renders_all_sections_bilingual() -> None:
    md = diagnostic_report_to_markdown(_DIAG_CONTENT, customer_handle="Acme")
    assert md.count("## ") == 5
    assert "Context / السياق" in md
    assert "Recommended Next Step / الخطوة التالية الموصى بها" in md
    assert "Acme" in md
    assert "ليست نتائج مضمونة" in md


def test_diagnostic_empty_renders_honest_notice() -> None:
    md = diagnostic_report_to_markdown({}, customer_handle="Acme")
    assert "not yet prepared" in md.lower()
    assert "لم يُعدّ التشخيص بعد" in md
    # No fabricated section content for an empty diagnostic.
    assert "## Context" not in md


def test_diagnostic_html_is_self_contained_and_bilingual() -> None:
    html_doc = render_diagnostic_report_html(_DIAG_CONTENT, customer_handle="Acme")
    assert html_doc.startswith("<!DOCTYPE html>")
    assert "http://" not in html_doc
    assert "https://" not in html_doc
    assert "<style>" in html_doc
    assert 'dir="auto"' in html_doc
    assert "السياق" in html_doc
    assert "Free Diagnostic" in html_doc


def test_diagnostic_html_escapes_injection() -> None:
    html_doc = render_diagnostic_report_html(
        {"context": "<script>alert(1)</script>"}, customer_handle="Acme"
    )
    assert "<script>alert(1)</script>" not in html_doc
    assert "&lt;script&gt;" in html_doc


# ── B2 — 14-section Proof Pack ─────────────────────────────────────────


def test_proof_pack_html_renders_14_sections_bilingual() -> None:
    html_doc = render_proof_pack_html(_full_pack(), customer_handle="Acme")
    assert html_doc.startswith("<!DOCTYPE html>")
    assert html_doc.count("<h2") == len(PROOF_PACK_V2_SECTIONS) == 14
    assert "الملخص التنفيذي" in html_doc
    assert "القيود والحدود" in html_doc
    assert "Acme" in html_doc


def test_proof_pack_html_is_self_contained() -> None:
    html_doc = render_proof_pack_html(_full_pack(), customer_handle="Acme")
    assert "http://" not in html_doc
    assert "https://" not in html_doc
    assert "ليست نتائج مضمونة" in html_doc


def test_proof_pack_empty_html_renders_not_generated_notice() -> None:
    html_doc = render_proof_pack_html({}, customer_handle="Acme")
    assert "not yet generated" in html_doc.lower()
    # No fabricated section content for an empty pack.
    assert html_doc.count("<h2") == 0


def test_proof_pack_pdf_degrades_gracefully() -> None:
    pdf = render_proof_pack_pdf(_full_pack(), customer_handle="Acme")
    if is_pdf_available()["any"]:
        assert pdf is not None
        assert pdf[:5] == b"%PDF-"
    else:
        # Graceful degradation: caller falls back to HTML.
        assert pdf is None


# ── dispatch ───────────────────────────────────────────────────────────


def test_dispatch_routes_known_types() -> None:
    diag = render_deliverable_html(
        deliverable_type="diagnostic_report",
        content=_DIAG_CONTENT,
        customer_handle="Acme",
    )
    pack = render_deliverable_html(
        deliverable_type="proof_pack",
        content=_full_pack(),
        customer_handle="Acme",
    )
    assert "Free Diagnostic" in diag
    assert "Proof Pack" in pack


def test_dispatch_rejects_rung_2_5_types() -> None:
    """Freeze: this renderer covers rung 0-1 only — other types are rejected."""
    with pytest.raises(ValueError, match="unsupported_deliverable_type"):
        render_deliverable_html(
            deliverable_type="executive_pack",
            content={},
            customer_handle="Acme",
        )
