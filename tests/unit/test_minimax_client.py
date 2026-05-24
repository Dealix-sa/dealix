"""MiniMax client helpers."""

from __future__ import annotations

from core.llm.openai_compat import _strip_minimax_thinking


def test_strip_minimax_thinking():
    raw = (
        "<think>\nreasoning here\n</think>\n\n"
        "Hello! How can I help?"
    )
    assert _strip_minimax_thinking(raw) == "Hello! How can I help?"


def test_strip_minimax_thinking_empty():
    assert _strip_minimax_thinking("") == ""
