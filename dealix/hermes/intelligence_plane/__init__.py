"""
Hermes Intelligence Plane — graphs و learning engine.

كل graph منفصل في ملف لأن لكل منها cardinality وقوة بحث مختلفة:

    Signal Graph     — يربط الإشارات بالفرص.
    Outcome Graph    — يربط التنفيذ بالنتائج.
    Revenue Graph    — يربط الصفقات بالدخل الحقيقي.
    Attribution      — يربط الدخل بالحملات/الرسائل/الشركاء/الأصول/الوكلاء.
    Asset Graph      — يربط النتائج بالقوالب والـ playbooks.
    Learning Engine  — يستخرج ما يجب توسيعه أو قتله.
    Recommendations  — أفضل فعل تالي.
"""

from .asset_graph import Asset, AssetGraph
from .attribution_graph import AttributionGraph, AttributionLink
from .learning_engine import LearningEngine, LearningInsight
from .outcome_graph import Outcome, OutcomeGraph
from .recommendations import RecommendationEngine
from .revenue_graph import RevenueGraph
from .signal_graph import Signal, SignalGraph

__all__ = [
    "Asset",
    "AssetGraph",
    "AttributionGraph",
    "AttributionLink",
    "LearningEngine",
    "LearningInsight",
    "Outcome",
    "OutcomeGraph",
    "RecommendationEngine",
    "RevenueGraph",
    "Signal",
    "SignalGraph",
]
