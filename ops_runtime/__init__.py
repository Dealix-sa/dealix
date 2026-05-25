from __future__ import annotations

"""Operational runtime for Dealix Company Architecture v1.0 (Stage 9).

Reads private ops state, computes KPI metrics, and writes founder-facing
briefs, weekly reviews, decision queues, and scorecards.
"""

from .metrics_calculator import (
    compute_delivery_metrics,
    compute_pipeline_metrics,
    compute_revenue_metrics,
)
from .private_ops_reader import (
    read_clients,
    read_mrr,
    read_pipeline,
    read_revenue_actions,
)

__all__ = [
    "read_pipeline",
    "read_revenue_actions",
    "read_mrr",
    "read_clients",
    "compute_pipeline_metrics",
    "compute_revenue_metrics",
    "compute_delivery_metrics",
]
