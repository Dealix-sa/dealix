"""
AiSearchMonitor — capture snapshots of Dealix's visibility in AI answers
across a known prompt set.

The monitor itself is engine-agnostic: it records what a prompt was
asked, what the engine answered, and whether Dealix was cited /
paraphrased / direct-mentioned. The collector wiring lives in
``dealix/hermes/observability``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class AiSearchSnapshot:
    snapshot_id: str
    engine: str
    prompt: str
    topic: str
    cited: bool
    paraphrased: bool
    direct_mention: bool
    competitor_mentions: tuple[str, ...]
    captured_at: datetime = field(default_factory=lambda: datetime.now(UTC))


def snapshot_visibility(
    *,
    snapshot_id: str,
    engine: str,
    prompt: str,
    topic: str,
    response_text: str,
    brand_phrases: tuple[str, ...] = ("dealix",),
    competitors: tuple[str, ...] = (),
) -> AiSearchSnapshot:
    body = response_text.lower()
    cited = "dealix.sa" in body or "https://dealix" in body
    direct_mention = any(p in body for p in brand_phrases)
    paraphrased = direct_mention is False and any(p[:4] in body for p in brand_phrases)
    competitor_hits = tuple(c for c in competitors if c.lower() in body)
    return AiSearchSnapshot(
        snapshot_id=snapshot_id,
        engine=engine,
        prompt=prompt,
        topic=topic,
        cited=cited,
        paraphrased=paraphrased,
        direct_mention=direct_mention,
        competitor_mentions=competitor_hits,
    )
