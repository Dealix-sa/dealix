"""Charter pinning: HERMES_CHARTER.md cannot drift silently.

If you intentionally amend the Hermes Charter, update the expected lines
below in the same PR (see HERMES_CHARTER.md §8 'Charter amendment').
"""

from __future__ import annotations

from pathlib import Path

CHARTER = (
    Path(__file__).resolve().parent.parent.parent
    / "docs"
    / "institutional"
    / "HERMES_CHARTER.md"
)


def test_charter_file_exists() -> None:
    assert CHARTER.is_file(), f"Hermes Charter missing at {CHARTER}"


def test_charter_anchors_constitution() -> None:
    text = CHARTER.read_text(encoding="utf-8")
    assert "Dealix Constitution" in text
    assert "Non-Negotiables" in text or "non-negotiable" in text


def test_charter_lists_provider_routing() -> None:
    text = CHARTER.read_text(encoding="utf-8")
    assert "OpenRouter" in text
    assert "direct_deepseek" in text or "DeepSeek-direct" in text
    assert "HERMES_PROVIDER" in text


def test_charter_kill_switch_documented() -> None:
    text = CHARTER.read_text(encoding="utf-8")
    assert "HERMES_KILL_SWITCH" in text


def test_charter_lists_blocked_actions() -> None:
    text = CHARTER.read_text(encoding="utf-8")
    assert "Scrape" in text or "scrape" in text
    assert "cold outreach" in text or "Cold outreach" in text or "Initiate cold" in text
    assert "approval_center" in text or "approval center" in text.lower()
