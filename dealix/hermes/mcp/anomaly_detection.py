"""
Anomaly detection — flags MCP servers whose behavior drifts from baseline.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AnomalyReport:
    server_id: str
    anomalies: list[str]
    severity: str  # "info" | "warn" | "critical"


def detect_anomalies(
    *,
    server_id: str,
    baseline_avg_latency_ms: float,
    observed_avg_latency_ms: float,
    baseline_error_rate: float,
    observed_error_rate: float,
    baseline_call_volume_per_hour: float,
    observed_call_volume_per_hour: float,
) -> AnomalyReport:
    anomalies: list[str] = []
    if observed_avg_latency_ms > baseline_avg_latency_ms * 3 and baseline_avg_latency_ms > 0:
        anomalies.append(
            f"latency_spike:{observed_avg_latency_ms:.0f}ms vs baseline "
            f"{baseline_avg_latency_ms:.0f}ms"
        )
    if observed_error_rate > max(0.05, baseline_error_rate * 5):
        anomalies.append(
            f"error_rate_spike:{observed_error_rate:.3f} vs baseline "
            f"{baseline_error_rate:.3f}"
        )
    if (
        baseline_call_volume_per_hour > 0
        and observed_call_volume_per_hour > baseline_call_volume_per_hour * 4
    ):
        anomalies.append(
            f"call_volume_spike:{observed_call_volume_per_hour:.0f}/h vs "
            f"{baseline_call_volume_per_hour:.0f}/h"
        )

    severity = "info"
    if any("error_rate" in a or "call_volume" in a for a in anomalies):
        severity = "critical"
    elif anomalies:
        severity = "warn"
    return AnomalyReport(server_id=server_id, anomalies=anomalies, severity=severity)
