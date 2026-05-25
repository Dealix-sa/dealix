"""
Generative Engine Optimization (GEO).

Surfaces optimized for AI-search citation rather than classical SEO.
"""

from __future__ import annotations

from dealix.hermes.growth.geo.ai_search_monitor import (
    AISearchMonitor,
    AISearchObservation,
)
from dealix.hermes.growth.geo.ai_visibility import (
    AIVisibilityScore,
    score_ai_visibility,
)
from dealix.hermes.growth.geo.answer_engine_pages import (
    AnswerEnginePage,
    score_answer_engine_page,
)
from dealix.hermes.growth.geo.citation_assets import (
    CitationAsset,
    is_citation_ready,
)
from dealix.hermes.growth.geo.comparison_builder import build_comparison_table
from dealix.hermes.growth.geo.entity_consistency import (
    GEOEntityCheck,
    check_geo_entity_alignment,
)
from dealix.hermes.growth.geo.faq_builder import FAQEntry, build_faq

__all__ = [
    "AIVisibilityScore",
    "score_ai_visibility",
    "AnswerEnginePage",
    "score_answer_engine_page",
    "CitationAsset",
    "is_citation_ready",
    "FAQEntry",
    "build_faq",
    "build_comparison_table",
    "GEOEntityCheck",
    "check_geo_entity_alignment",
    "AISearchMonitor",
    "AISearchObservation",
]
