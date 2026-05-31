"""
Source metadata — the immutable provenance tag for any data flowing
into the agentic plane.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from dealix.hermes.provenance.trust_level import TrustLevel, score_trust_level


@dataclass(frozen=True)
class SourceMetadata:
    source: str
    trust_level: TrustLevel
    captured_at: float
    captured_by: str
    notes: tuple[str, ...] = field(default_factory=tuple)


def build_source_metadata(
    source: str,
    captured_by: str,
    *,
    notes: list[str] | tuple[str, ...] = (),
) -> SourceMetadata:
    if not source:
        raise ValueError("source required")
    if not captured_by:
        raise ValueError("captured_by required")
    return SourceMetadata(
        source=source,
        trust_level=score_trust_level(source),
        captured_at=time.time(),
        captured_by=captured_by,
        notes=tuple(notes),
    )
