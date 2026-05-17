"""Proposal artifact — shareable, self-contained, bilingual HTML.

The artifact is the deliverable the founder hands a prospect. It must be
self-contained (no remote assets), bilingual-safe, and carry the
non-guarantee disclaimer. It is a draft — never auto-delivered.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.sales_os.proposal_artifact import (
    build_proposal_artifact,
    markdown_to_html,
    proposal_artifact_filename,
)

_SAMPLE_MD = """# Revenue Intelligence Sprint — Proposal

**Customer:** Acme Co
- 7-day sprint
- Proof Pack

---

# عرض مشروع

فقرة بالعربية لاختبار الاتجاه.
"""


def test_artifact_is_self_contained_html() -> None:
    html_doc = build_proposal_artifact(
        body_markdown=_SAMPLE_MD, engagement_id="prop_x", customer_name="Acme Co"
    )
    assert html_doc.startswith("<!DOCTYPE html>")
    # Self-contained: no remote assets that could leak or break offline.
    assert "http://" not in html_doc
    assert "https://" not in html_doc
    assert "<style>" in html_doc


def test_artifact_is_bilingual_safe() -> None:
    html_doc = build_proposal_artifact(
        body_markdown=_SAMPLE_MD, engagement_id="prop_x", customer_name="Acme Co"
    )
    # dir="auto" lets each block render AR/EN in the correct direction.
    assert 'dir="auto"' in html_doc
    assert "فقرة بالعربية" in html_doc
    assert "Revenue Intelligence Sprint" in html_doc


def test_artifact_carries_non_guarantee_disclaimer() -> None:
    html_doc = build_proposal_artifact(
        body_markdown="# x", engagement_id="prop_x"
    )
    assert "not guaranteed outcomes" in html_doc
    assert "ليست نتائج مضمونة" in html_doc


def test_markdown_converts_inline_and_blocks() -> None:
    out = markdown_to_html("## Heading\n\n**bold** and _it_.\n\n- a\n- b")
    assert "<h2" in out
    assert "<strong>bold</strong>" in out
    assert "<em>it</em>" in out
    assert out.count("<li") == 2


def test_markdown_escapes_html_injection() -> None:
    out = markdown_to_html("<script>alert(1)</script>")
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("prop_abc", "proposal_prop_abc.html"),
        ("prop/../etc", "proposal_prop____etc.html"),
        ("a b!c", "proposal_a_b_c.html"),
    ],
)
def test_artifact_filename_is_path_safe(raw: str, expected: str) -> None:
    assert proposal_artifact_filename(raw) == expected
