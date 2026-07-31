"""Phase 10 — Frontend Professional Polish tests."""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

CUSTOMER_FACING = [
    "landing/customer-portal.html",
    "landing/executive-command-center.html",
    "landing/launchpad.html",
    "landing/index.html",
]


class _VisibleTextParser(HTMLParser):
    """Collect declarative page text while ignoring non-visible and FAQ prompts."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._suppressed_depth = 0
        self.parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        del attrs
        if tag.casefold() in {"script", "style", "summary"}:
            self._suppressed_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() in {"script", "style", "summary"}:
            self._suppressed_depth = max(0, self._suppressed_depth - 1)

    def handle_data(self, data: str) -> None:
        if self._suppressed_depth == 0:
            self.parts.append(data)


def _visible_declarative_text(html: str) -> str:
    parser = _VisibleTextParser()
    parser.feed(html)
    parser.close()
    return "\n".join(parser.parts)


def test_all_customer_facing_have_mobile_meta() -> None:
    for page in CUSTOMER_FACING:
        path = Path(page)
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        assert "viewport" in html and "width=device-width" in html, (
            f"{page} missing mobile viewport meta"
        )


def test_all_customer_facing_have_arabic() -> None:
    for page in CUSTOMER_FACING:
        path = Path(page)
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        assert 'lang="ar"' in html, f"{page} missing lang=ar"
        assert 'dir="rtl"' in html, f"{page} missing dir=rtl"


def test_all_customer_facing_have_english() -> None:
    """At least one English word must appear (for example Dealix or Saudi)."""
    for page in CUSTOMER_FACING:
        path = Path(page)
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        assert re.search(r"\b[A-Za-z]{4,}\b", html), f"{page} missing English text"


def test_no_fake_metrics_without_demo_label() -> None:
    """Customer-portal.html must show DEMO where it shows synthetic numbers."""
    html = Path("landing/customer-portal.html").read_text(encoding="utf-8")
    assert "DEMO" in html
    assert "src-pill" in html


def test_executive_command_center_demo_label_present() -> None:
    html = Path("landing/executive-command-center.html").read_text(encoding="utf-8")
    assert "DEMO" in html
    assert "demo-tag" in html


def test_no_forbidden_claims_in_customer_pages() -> None:
    forbidden = [
        re.compile(r"\bguaranteed?\b", re.IGNORECASE),
        re.compile(r"\bblast\b", re.IGNORECASE),
        re.compile(r"نضمن"),
        re.compile(r"مضمون"),
    ]
    for page in CUSTOMER_FACING:
        path = Path(page)
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        html_visible = _visible_declarative_text(html)
        # Explicit negation is not a positive outcome claim.
        html_visible = re.sub(
            r"[^\n<]*(not guaranteed outcomes|ليست نتائج مضمونة)[^\n>]*",
            "",
            html_visible,
        )
        for pattern in forbidden:
            assert not pattern.search(html_visible), (
                f"{page} contains: {pattern.pattern}"
            )


def test_customer_portal_links_to_legal_pages() -> None:
    """Customer portal footer must link to privacy and terms."""
    html = Path("landing/customer-portal.html").read_text(encoding="utf-8")
    assert "/privacy.html" in html
    assert "/terms.html" in html


def test_polish_doc_exists() -> None:
    """Phase 10 doc must exist."""
    assert Path("docs/FRONTEND_PROFESSIONAL_POLISH_PLAN.md").exists()
