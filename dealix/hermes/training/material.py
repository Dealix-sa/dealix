"""Training material outlines (slides, worksheet, policy, prompt pack)."""

from __future__ import annotations

from typing import Any


class TrainingMaterial:
    def outline(self, *, title: str, modules: list[str]) -> dict[str, Any]:
        return {
            "title": title,
            "slides": [f"Slide {i + 1}: {m}" for i, m in enumerate(modules)],
            "worksheet": [f"Exercise: apply {m} to your context" for m in modules],
            "policy_template": "AI use policy — fill in scope, owners, review cadence.",
            "prompt_pack": [f"Prompt: {m} — reusable starting prompt" for m in modules],
        }
