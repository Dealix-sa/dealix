"""
Board / investor surface — speak the language of capital allocators.
"""

from __future__ import annotations

from dealix.hermes.board.board_memo import BoardMemo, render_board_memo
from dealix.hermes.board.executive_metrics import (
    ExecutiveMetrics,
    compute_executive_metrics,
)
from dealix.hermes.board.investor_update import (
    InvestorUpdate,
    render_investor_update,
)
from dealix.hermes.board.traction_report import (
    TractionReport,
    build_traction_report,
)

__all__ = [
    "ExecutiveMetrics",
    "compute_executive_metrics",
    "BoardMemo",
    "render_board_memo",
    "InvestorUpdate",
    "render_investor_update",
    "TractionReport",
    "build_traction_report",
]
