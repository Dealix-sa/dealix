"""
Answer-engine pages — high-density Q&A pages purpose-built for AI search.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AnswerEnginePage:
    slug: str
    title: str
    intent: str
    h1_present: bool
    has_summary_above_fold: bool
    qa_blocks: int
    comparison_tables: int
    citation_sources: int
    last_updated_iso: str


@dataclass
class AnswerEnginePageScore:
    slug: str
    score: float
    issues: list[str]


def score_answer_engine_page(page: AnswerEnginePage) -> AnswerEnginePageScore:
    issues: list[str] = []
    score = 100.0
    if not page.h1_present:
        issues.append("missing_h1")
        score -= 15
    if not page.has_summary_above_fold:
        issues.append("missing_above_fold_summary")
        score -= 15
    if page.qa_blocks < 5:
        issues.append(f"low_qa_blocks:{page.qa_blocks}<5")
        score -= 15
    if page.comparison_tables < 1:
        issues.append("missing_comparison_table")
        score -= 10
    if page.citation_sources < 2:
        issues.append(f"low_citations:{page.citation_sources}<2")
        score -= 10
    if not page.last_updated_iso:
        issues.append("missing_last_updated")
        score -= 10
    if not page.intent:
        issues.append("missing_intent")
        score -= 10
    return AnswerEnginePageScore(
        slug=page.slug,
        score=max(0.0, round(score, 2)),
        issues=issues,
    )
