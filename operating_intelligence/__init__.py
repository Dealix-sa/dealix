"""
Operating intelligence layer.

Synthesizes raw company state and signals into prioritized work, weekly
reviews, and strategic deltas. Consumed by the control plane and the
founder dashboard.
"""

from .operating_signals import OperatingSignal, collect_signals
from .priority_engine import PriorityEngine, PrioritizedItem
from .bottleneck_detector import BottleneckDetector, Bottleneck
from .opportunity_detector import OpportunityDetector, Opportunity
from .risk_prioritizer import prioritize_risks
from .learning_synthesizer import LearningSynthesizer, LearningSummary
from .weekly_review_generator import WeeklyReview, generate_weekly_review
from .monthly_strategy_generator import MonthlyStrategy, generate_monthly_strategy
from .system_improvement_planner import (
    SystemImprovementPlanner,
    ImprovementProposal,
)

__all__ = [
    "OperatingSignal",
    "collect_signals",
    "PriorityEngine",
    "PrioritizedItem",
    "BottleneckDetector",
    "Bottleneck",
    "OpportunityDetector",
    "Opportunity",
    "prioritize_risks",
    "LearningSynthesizer",
    "LearningSummary",
    "WeeklyReview",
    "generate_weekly_review",
    "MonthlyStrategy",
    "generate_monthly_strategy",
    "SystemImprovementPlanner",
    "ImprovementProposal",
]
