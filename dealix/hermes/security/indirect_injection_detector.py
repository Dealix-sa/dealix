"""
Indirect prompt injection detector — flags prompts that embed user-
sourced content carrying suspicious instruction markers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from dealix.hermes.agent_comms.message_sanitizer import sanitize_message

_USER_CONTENT_MARKERS = (
    re.compile(r"(?is)<\s*user_content\s*>(.*?)<\s*/\s*user_content\s*>"),
    re.compile(r"(?is)<\s*document\s*>(.*?)<\s*/\s*document\s*>"),
    re.compile(r"(?is)<\s*tool_output\s*>(.*?)<\s*/\s*tool_output\s*>"),
)


@dataclass
class IndirectInjectionVerdict:
    safe: bool
    findings: list[str]
    sanitized_segments: list[str]


def detect_indirect_injection(prompt: str) -> IndirectInjectionVerdict:
    if not prompt:
        return IndirectInjectionVerdict(True, [], [])
    findings: list[str] = []
    sanitized_segments: list[str] = []
    for marker in _USER_CONTENT_MARKERS:
        for match in marker.finditer(prompt):
            inner = match.group(1)
            result = sanitize_message(inner)
            if not result.safe:
                findings.extend([f"indirect:{f}" for f in result.findings])
            sanitized_segments.append(result.sanitized_text)
    return IndirectInjectionVerdict(
        safe=not findings,
        findings=findings,
        sanitized_segments=sanitized_segments,
    )
