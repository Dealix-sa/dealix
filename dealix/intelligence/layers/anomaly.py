"""
Anomaly detection layer — z-score, IQR, EWMA-based.
طبقة كشف الشذوذ — درجة z، IQR، انحراف عن المتوسط الأسي.

Used by ops dashboards (latency spikes, cost anomalies, churn signals).
Returns indices + severity so callers can attach an action.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal, Sequence

Method = Literal["zscore", "iqr", "ewma"]


@dataclass(frozen=True)
class Anomaly:
    index: int
    value: float
    score: float
    severity: Literal["low", "medium", "high"]
    reason: str


@dataclass(frozen=True)
class AnomalyResult:
    method: Method
    anomalies: tuple[Anomaly, ...]
    threshold: float
    series_mean: float
    series_std: float


def _mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _std(xs: Sequence[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def _percentile(xs: list[float], p: float) -> float:
    if not xs:
        return 0.0
    s = sorted(xs)
    k = (len(s) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return s[int(k)]
    return s[f] * (c - k) + s[c] * (k - f)


def _severity(score: float, threshold: float) -> Literal["low", "medium", "high"]:
    ratio = abs(score) / threshold if threshold > 0 else abs(score)
    if ratio >= 2.0:
        return "high"
    if ratio >= 1.3:
        return "medium"
    return "low"


class AnomalyDetector:
    """Multi-method anomaly detector with consistent output shape."""

    def __init__(self, *, method: Method = "zscore", threshold: float | None = None) -> None:
        self.method = method
        self.threshold = threshold

    def detect(self, series: Sequence[float]) -> AnomalyResult:
        if not series:
            return AnomalyResult(self.method, tuple(), self.threshold or 0.0, 0.0, 0.0)
        m = _mean(series)
        sd = _std(series)
        if self.method == "iqr":
            return self._iqr(series, m, sd)
        if self.method == "ewma":
            return self._ewma(series, m, sd)
        return self._zscore(series, m, sd)

    # ── Methods ────────────────────────────────────────────────────
    def _zscore(self, series: Sequence[float], m: float, sd: float) -> AnomalyResult:
        threshold = self.threshold or 2.5
        anomalies: list[Anomaly] = []
        if sd == 0:
            return AnomalyResult("zscore", tuple(), threshold, m, sd)
        for i, x in enumerate(series):
            z = (x - m) / sd
            if abs(z) >= threshold:
                anomalies.append(
                    Anomaly(
                        index=i,
                        value=x,
                        score=round(z, 4),
                        severity=_severity(z, threshold),
                        reason=f"z={z:.2f} exceeds ±{threshold}",
                    )
                )
        return AnomalyResult("zscore", tuple(anomalies), threshold, round(m, 4), round(sd, 4))

    def _iqr(self, series: Sequence[float], m: float, sd: float) -> AnomalyResult:
        threshold = self.threshold or 1.5
        xs = list(series)
        q1 = _percentile(xs, 0.25)
        q3 = _percentile(xs, 0.75)
        iqr = q3 - q1
        lo = q1 - threshold * iqr
        hi = q3 + threshold * iqr
        anomalies: list[Anomaly] = []
        for i, x in enumerate(series):
            if x < lo or x > hi:
                span = max(iqr, 1e-9)
                score = (x - hi) / span if x > hi else (lo - x) / span
                anomalies.append(
                    Anomaly(
                        index=i,
                        value=x,
                        score=round(score, 4),
                        severity=_severity(score, 1.0),
                        reason=f"outside IQR fence [{lo:.2f},{hi:.2f}]",
                    )
                )
        return AnomalyResult("iqr", tuple(anomalies), threshold, round(m, 4), round(sd, 4))

    def _ewma(self, series: Sequence[float], m: float, sd: float) -> AnomalyResult:
        threshold = self.threshold or 3.0
        if not series:
            return AnomalyResult("ewma", tuple(), threshold, m, sd)
        alpha = 0.3
        ewma_val = series[0]
        ewmstd = 0.0
        anomalies: list[Anomaly] = []
        for i, x in enumerate(series):
            dev = x - ewma_val
            std_est = math.sqrt((1 - alpha) * (ewmstd ** 2 + alpha * dev ** 2))
            std_est = max(std_est, 1e-9)
            z = dev / std_est
            if abs(z) >= threshold:
                anomalies.append(
                    Anomaly(
                        index=i,
                        value=x,
                        score=round(z, 4),
                        severity=_severity(z, threshold),
                        reason=f"EWMA deviation z={z:.2f}",
                    )
                )
            ewma_val = alpha * x + (1 - alpha) * ewma_val
            ewmstd = std_est
        return AnomalyResult("ewma", tuple(anomalies), threshold, round(m, 4), round(sd, 4))
