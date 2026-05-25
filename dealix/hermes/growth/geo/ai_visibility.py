"""
AiVisibility — score how visible a Dealix topic is inside AI search
answers. Real-world signals: cited URLs, paraphrased quotes, and direct
mentions across measured prompts.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AiVisibilityScore:
    topic: str
    citations: int
    paraphrases: int
    direct_mentions: int
    competitor_mentions: int
    measured_prompts: int
    share_of_voice: float
    score: float
    grade: str
    findings: tuple[str, ...] = field(default_factory=tuple)


def score_visibility(
    *,
    topic: str,
    citations: int,
    paraphrases: int,
    direct_mentions: int,
    competitor_mentions: int,
    measured_prompts: int,
) -> AiVisibilityScore:
    measured = max(measured_prompts, 1)
    own = citations + paraphrases + direct_mentions
    total = own + competitor_mentions
    sov = round(own / max(total, 1), 4)
    score = round(min(1.0, (citations * 3 + direct_mentions * 2 + paraphrases) / (5.0 * measured)), 4)
    if score >= 0.5:
        grade = "A"
    elif score >= 0.3:
        grade = "B"
    elif score >= 0.15:
        grade = "C"
    else:
        grade = "D"
    findings: list[str] = []
    if competitor_mentions > own * 2:
        findings.append("competitors dominate this topic; ship comparison and FAQ pages")
    if citations < direct_mentions:
        findings.append("answers mention the brand but don't link out; add citation-friendly pages")
    return AiVisibilityScore(
        topic=topic,
        citations=citations,
        paraphrases=paraphrases,
        direct_mentions=direct_mentions,
        competitor_mentions=competitor_mentions,
        measured_prompts=measured,
        share_of_voice=sov,
        score=score,
        grade=grade,
        findings=tuple(findings),
    )
