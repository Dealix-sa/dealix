"""
geo — Generative Engine Optimization. Make Dealix discoverable inside
answers from ChatGPT, Gemini, Perplexity, and Google AI Mode — not just
classical SERPs.
"""

from dealix.hermes.growth.geo.ai_search_monitor import AiSearchSnapshot, snapshot_visibility
from dealix.hermes.growth.geo.ai_visibility import AiVisibilityScore, score_visibility
from dealix.hermes.growth.geo.answer_engine_pages import (
    AnswerEnginePage,
    DEFAULT_PAGES,
    render_page_stub,
)
from dealix.hermes.growth.geo.citation_assets import CitationAsset
from dealix.hermes.growth.geo.comparison_builder import ComparisonTable, build_comparison
from dealix.hermes.growth.geo.faq_builder import FaqEntry, build_faq
from dealix.hermes.growth.geo.trust_signal_builder import build_trust_signal_block

__all__ = [
    "AiSearchSnapshot",
    "AiVisibilityScore",
    "AnswerEnginePage",
    "CitationAsset",
    "ComparisonTable",
    "DEFAULT_PAGES",
    "FaqEntry",
    "build_comparison",
    "build_faq",
    "build_trust_signal_block",
    "render_page_stub",
    "score_visibility",
    "snapshot_visibility",
]
