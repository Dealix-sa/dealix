"""Canonical, pure deal-intelligence primitives for Dealix."""

from .models import DealEvent, DealRecord, DealSnapshot, DealStage, NextAction, PortfolioMetrics
from .pipeline import analyze_deal, compute_portfolio, next_action
from .store import DealBook, DealBookError, load_book, save_book_atomic

__all__ = [
    "DealBook",
    "DealBookError",
    "DealEvent",
    "DealRecord",
    "DealSnapshot",
    "DealStage",
    "NextAction",
    "PortfolioMetrics",
    "analyze_deal",
    "compute_portfolio",
    "load_book",
    "next_action",
    "save_book_atomic",
]
