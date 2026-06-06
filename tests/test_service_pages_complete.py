"""Contract: every sales service page is complete, bilingual, and claim-safe.

Scans sales/service_pages/*.md and asserts each known page:
  - exists and is substantial (> 800 bytes)
  - contains an Arabic section header (e.g. ## الوعد or ## المخرجات)
  - contains an English mirror for that section
  - contains a /services CTA link
  - contains no guaranteed-claim trigger phrases (governance pre-check)

NOTE: page content is authored separately; this test may fail until the
content lands. That is expected — the test is the source of truth for the bar.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_client_acquisition.governance_os import policy_check_draft

PAGES_DIR = Path(__file__).resolve().parent.parent / "sales" / "service_pages"

# The five known service pages that must exist and be complete.
KNOWN_PAGES = [
    "client_portal_os.md",
    "marketing_os.md",
    "operations_os.md",
    "revenue_os.md",
    "trust_os.md",
]

# Arabic section headers we expect at least one of, paired with an English mirror.
ARABIC_HEADERS = ["## الوعد", "## المخرجات"]
ENGLISH_MIRRORS = ["The Promise", "Deliverables"]

# Section headers whose body is a NEGATED compliance disclaimer (states what the
# offer does NOT do). These lines name forbidden practices on purpose, so they
# must be excluded before running the guaranteed-claim guard — otherwise an
# honest "No cold WhatsApp" line would trip the forbidden-term detector.
_DISCLAIMER_HEADERS = (
    "ما لا يشمله",  # Out of Scope (ar)
    "out of scope",
    "شرط الإغلاق",  # Closing Terms (ar)
    "closing terms",
)


def _marketing_prose(text: str) -> str:
    """Return page text with negated-disclaimer sections removed.

    Drops any markdown section (## ...) whose header is a known disclaimer
    section. The promise/marketing prose that remains is what the guaranteed-
    claim guard must stay clean.
    """
    kept: list[str] = []
    in_disclaimer = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            header = stripped[3:].lower()
            in_disclaimer = any(h in header for h in _DISCLAIMER_HEADERS)
        if not in_disclaimer:
            kept.append(line)
    return "\n".join(kept)


def _page_path(name: str) -> Path:
    return PAGES_DIR / name


@pytest.mark.parametrize("name", KNOWN_PAGES)
def test_page_exists(name: str) -> None:
    assert _page_path(name).is_file(), f"missing service page: {name}"


@pytest.mark.parametrize("name", KNOWN_PAGES)
def test_page_is_substantial(name: str) -> None:
    path = _page_path(name)
    assert path.is_file(), f"missing service page: {name}"
    assert (
        path.stat().st_size > 800
    ), f"{name} is too short ({path.stat().st_size} bytes) — needs full content"


@pytest.mark.parametrize("name", KNOWN_PAGES)
def test_page_has_arabic_header_and_english_mirror(name: str) -> None:
    text = _page_path(name).read_text(encoding="utf-8")
    assert any(
        h in text for h in ARABIC_HEADERS
    ), f"{name} missing an Arabic section header (one of {ARABIC_HEADERS})"
    assert any(
        m in text for m in ENGLISH_MIRRORS
    ), f"{name} missing an English mirror section (one of {ENGLISH_MIRRORS})"


@pytest.mark.parametrize("name", KNOWN_PAGES)
def test_page_has_services_cta(name: str) -> None:
    text = _page_path(name).read_text(encoding="utf-8")
    assert "/services" in text, f"{name} missing a /services CTA link"


@pytest.mark.parametrize("name", KNOWN_PAGES)
def test_page_has_no_guaranteed_claims(name: str) -> None:
    text = _page_path(name).read_text(encoding="utf-8")
    # Run the same governance guard used by tests/test_no_guaranteed_claims.py,
    # but only over marketing prose — negated "Out of Scope" / "Closing Terms"
    # disclaimers legitimately name forbidden practices to rule them out.
    result = policy_check_draft(_marketing_prose(text))
    assert result.allowed is True, f"{name} contains a guaranteed-claim trigger: {result.issues}"
