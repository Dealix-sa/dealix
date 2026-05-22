"""Financial Autonomy Layer — weekly metrics cycle + monthly board memo.

A weekly autonomous loop that aggregates MRR/ARR/NRR/churn/CAC/LTV/runway,
detects financial anomalies, evaluates threshold rules, and routes every
high-stakes financial decision to the founder approval queue. The monthly
board-memo cycle auto-populates a 12-section memo with real data and
queues it for founder approval.

Doctrine: AI explores, analyzes, recommends. Deterministic workflows
execute. Humans approve critical moves. Refunds, price changes,
write-offs and any other irreversible financial moves require an
explicit founder approval — nothing is ever sent or charged.
"""
from __future__ import annotations

from auto_client_acquisition.financial_autonomy.anomaly_detector import (
    Anomaly,
    detect_anomalies,
)
from auto_client_acquisition.financial_autonomy.board_memo_cycle import (
    BoardMemoReport,
    latest_board_memo,
    run_board_memo_cycle,
)
from auto_client_acquisition.financial_autonomy.financial_cycle import (
    FinancialCycleReport,
    latest_financial_report,
    run_financial_cycle,
)
from auto_client_acquisition.financial_autonomy.metrics_aggregator import (
    FinancialMetricsSnapshot,
    aggregate_financial_metrics,
)
from auto_client_acquisition.financial_autonomy.threshold_rules import (
    FINANCIAL_THRESHOLDS,
    ThresholdRule,
    ThresholdViolation,
    evaluate_thresholds,
)

__all__ = [
    "Anomaly",
    "BoardMemoReport",
    "FINANCIAL_THRESHOLDS",
    "FinancialCycleReport",
    "FinancialMetricsSnapshot",
    "ThresholdRule",
    "ThresholdViolation",
    "aggregate_financial_metrics",
    "detect_anomalies",
    "evaluate_thresholds",
    "latest_board_memo",
    "latest_financial_report",
    "run_board_memo_cycle",
    "run_financial_cycle",
]
