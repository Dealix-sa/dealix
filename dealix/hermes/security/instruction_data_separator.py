"""
Instruction/data separator.

LLMs do not natively distinguish instructions from data, so we do it
structurally: wrap user / tool content in tagged blocks and require
downstream consumers to refer to them by reference, not by inlining.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SeparatedPrompt:
    instructions: str
    data_blocks: dict[str, str]

    def render(self) -> str:
        parts = [self.instructions.strip(), ""]
        for name, content in self.data_blocks.items():
            parts.append(f"<{name}>")
            parts.append(content.strip())
            parts.append(f"</{name}>")
        return "\n".join(parts)


def separate_instructions_from_data(
    instructions: str, data_blocks: dict[str, str]
) -> SeparatedPrompt:
    cleaned: dict[str, str] = {}
    for name, content in data_blocks.items():
        if "<" in name or ">" in name or "/" in name:
            raise ValueError(f"invalid data block name: {name!r}")
        # never let data blocks carry tags that look like instructions
        cleaned[name] = (
            content.replace("</", "</")
            .replace("<system>", "[system]")
            .replace("<assistant>", "[assistant]")
        )
    return SeparatedPrompt(instructions=instructions, data_blocks=cleaned)
