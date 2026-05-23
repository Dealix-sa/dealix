"""safe_language register exists and has the expected shape."""
from __future__ import annotations

from pathlib import Path

REGISTER = Path(__file__).resolve().parent.parent.parent / "dealix" / "registers" / "safe_language.yaml"


def test_safe_language_register_exists():
    assert REGISTER.exists(), "safe_language.yaml is missing"


def test_safe_language_register_has_replacements():
    text = REGISTER.read_text(encoding="utf-8")
    assert "replacements:" in text
    assert "avoid:" in text
    assert "prefer:" in text


def test_register_lists_guaranteed_as_avoid():
    text = REGISTER.read_text(encoding="utf-8").lower()
    assert "guaranteed" in text, "avoid list should include 'guaranteed'"
