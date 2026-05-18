"""W2 — rung 0-1 customer-facing HTML renderer + payment->delivery audit link.

Covers the public functions added for the Commercial Launch first-paid-pilot
track: the HTML wrapper, the proof-pack HTML helper, and the audit link being
embedded in rendered deliverables.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
    proof_pack_to_html,
)
from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
)
from auto_client_acquisition.proof_to_market.delivery_audit import (
    PAYMENT_REF,
    RUNG0_DIAGNOSTIC,
    RUNG1_PROOF_PACK,
    WRITTEN_COMMITMENT_REF,
    DeliveryAuditError,
    audit_reference_label,
    record_delivery_audit_link,
)
from auto_client_acquisition.proof_to_market.html_renderer import (
    markdown_to_html_fragment,
    render_deliverable_html,
)


@pytest.fixture(autouse=True)
def _isolated_ledger(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))
    yield


def _full_pack() -> dict:
    return {
        "engagement_id": "e1",
        "customer_id": "c1",
        "sections": {k: f"Content for {k}." for k in PROOF_PACK_V2_SECTIONS},
        "score": 88,
        "tier": "case_candidate",
    }


# ── markdown_to_html_fragment ────────────────────────────────────────


def test_fragment_renders_headings_lists_and_inline():
    md = "# Title\n\n- one\n- two\n\n1. first\n\n**bold** and `code`\n\n---\n\n> quote"
    html = markdown_to_html_fragment(md)
    assert "<h1>Title</h1>" in html
    assert "<ul>" in html and "<li>one</li>" in html
    assert "<ol>" in html and "<li>first</li>" in html
    assert "<strong>bold</strong>" in html
    assert "<code>code</code>" in html
    assert "<hr>" in html
    assert "<blockquote>" in html


def test_fragment_escapes_html_injection():
    html = markdown_to_html_fragment("a <script>alert(1)</script> b")
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_fragment_empty_input_is_safe():
    assert markdown_to_html_fragment("") == ""


# ── render_deliverable_html ──────────────────────────────────────────


def test_render_deliverable_html_is_arabic_first_and_draft():
    html = render_deliverable_html("# Hello", title="Doc")
    assert html.startswith("<!doctype html>")
    assert "lang='ar'" in html and "dir='rtl'" in html
    assert "Draft / مسودة" in html
    assert "founder review required" in html
    # Doctrine: no guarantee language, disclaimer present.
    assert "النتائج التقديرية ليست نتائج مضمونة" in html


def test_render_deliverable_html_embeds_audit_link():
    link = record_delivery_audit_link(
        customer_id="c1",
        engagement_id="e1",
        deliverable_kind=RUNG1_PROOF_PACK,
        reference_kind=PAYMENT_REF,
        reference_id="pay_abc123",
    )
    html = render_deliverable_html("# Pack", title="Doc", audit_link=link)
    assert "pay_abc123" in html
    assert link.audit_id in html
    assert "مرجع التدقيق" in html


def test_render_deliverable_html_without_audit_link_has_no_audit_ref():
    html = render_deliverable_html("# Pack", title="Doc")
    assert "مرجع التدقيق" not in html


# ── proof_pack_to_html ───────────────────────────────────────────────


def test_proof_pack_to_html_renders_full_pack():
    html = proof_pack_to_html(_full_pack(), customer_handle="Acme")
    assert "<!doctype html>" in html
    assert "Acme" in html
    assert "Executive Summary" in html
    assert "88/100" in html


def test_proof_pack_to_html_empty_pack_renders_not_generated():
    html = proof_pack_to_html({}, customer_handle="Acme")
    assert "not yet generated" in html.lower()
    # No fabricated proof for an empty pack.
    assert "Content for executive_summary" not in html


def test_proof_pack_to_html_with_audit_link():
    link = record_delivery_audit_link(
        customer_id="c1",
        engagement_id="e1",
        deliverable_kind=RUNG1_PROOF_PACK,
        reference_kind=PAYMENT_REF,
        reference_id="pay_xyz",
    )
    html = proof_pack_to_html(_full_pack(), customer_handle="Acme", audit_link=link)
    assert "pay_xyz" in html


# ── delivery_audit guards ────────────────────────────────────────────


def test_audit_rung1_requires_payment_reference():
    with pytest.raises(DeliveryAuditError):
        record_delivery_audit_link(
            customer_id="c1",
            engagement_id="e1",
            deliverable_kind=RUNG1_PROOF_PACK,
            reference_kind=WRITTEN_COMMITMENT_REF,
            reference_id="commit_1",
        )


def test_audit_rung0_accepts_written_commitment():
    link = record_delivery_audit_link(
        customer_id="c1",
        engagement_id="e1",
        deliverable_kind=RUNG0_DIAGNOSTIC,
        reference_kind=WRITTEN_COMMITMENT_REF,
        reference_id="commit_1",
    )
    assert link.deliverable_kind == RUNG0_DIAGNOSTIC
    assert link.reference_id == "commit_1"


def test_audit_requires_non_empty_reference():
    with pytest.raises(DeliveryAuditError):
        record_delivery_audit_link(
            customer_id="c1",
            engagement_id="e1",
            deliverable_kind=RUNG0_DIAGNOSTIC,
            reference_kind=WRITTEN_COMMITMENT_REF,
            reference_id="   ",
        )


def test_audit_reference_label_is_bilingual():
    link = record_delivery_audit_link(
        customer_id="c1",
        engagement_id="e1",
        deliverable_kind=RUNG0_DIAGNOSTIC,
        reference_kind=WRITTEN_COMMITMENT_REF,
        reference_id="commit_1",
    )
    label = audit_reference_label(link)
    assert "Audit" in label and "مرجع التدقيق" in label
    assert link.audit_id in label
