"""
Forecasting layer — EWMA + Holt linear trend + naive linear regression.
طبقة التنبؤ — متوسط أسي + اتجاه خطي + انحدار خطي بسيط.

Used by Dealix revenue dashboards, churn risk, sprint-burn forecasting.
Pure Python, deterministic, < 200 lines.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class ForecastResult:
    method: str
    next_value: float
    horizon: tuple[float, ...]
    lower_ci: tuple[float, ...]
    upper_ci: tuple[float, ...]
    smoothing_alpha: float
    trend_slope: float
    residual_std: float


def _mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _std(xs: Sequence[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


class Forecaster:
    """Compose multiple light forecasting methods."""

    def __init__(self, *, alpha: float = 0.4, beta: float = 0.2) -> None:
        if not 0.0 < alpha < 1.0:
            raise ValueError("alpha in (0,1)")
        if not 0.0 <= beta < 1.0:
            raise ValueError("beta in [0,1)")
        self.alpha = alpha
        self.beta = beta

    # ── Public ─────────────────────────────────────────────────────
    def forecast(
        self,
        series: Sequence[float],
        *,
        horizon: int = 4,
        method: str = "holt",  # "ewma" | "holt" | "linreg"
    ) -> ForecastResult:
        if not series:
            return ForecastResult(method, 0.0, tuple(), tuple(), tuple(), self.alpha, 0.0, 0.0)
        horizon = max(1, int(horizon))
        if method == "ewma":
            return self._ewma(series, horizon)
        if method == "linreg":
            return self._linreg(series, horizon)
        return self._holt(series, horizon)

    # ── EWMA ───────────────────────────────────────────────────────
    def _ewma(self, series: Sequence[float], horizon: int) -> ForecastResult:
        s = series[0]
        residuals: list[float] = []
        for x in series[1:]:
            pred = s
            residuals.append(x - pred)
            s = self.alpha * x + (1 - self.alpha) * s
        sigma = _std(residuals)
        h = tuple(s for _ in range(horizon))
        ci = tuple(1.96 * sigma * math.sqrt(i + 1) for i in range(horizon))
        return ForecastResult(
            method="ewma",
            next_value=s,
            horizon=h,
            lower_ci=tuple(s - c for c in ci),
            upper_ci=tuple(s + c for c in ci),
            smoothing_alpha=self.alpha,
            trend_slope=0.0,
            residual_std=round(sigma, 4),
        )

    # ── Holt linear ────────────────────────────────────────────────
    def _holt(self, series: Sequence[float], horizon: int) -> ForecastResult:
        if len(series) < 2:
            return self._ewma(series, horizon)
        L = series[0]
        T = series[1] - series[0]
        residuals: list[float] = []
        for x in series[1:]:
            pred = L + T
            residuals.append(x - pred)
            L_new = self.alpha * x + (1 - self.alpha) * (L + T)
            T = self.beta * (L_new - L) + (1 - self.beta) * T
            L = L_new
        sigma = _std(residuals)
        future = tuple(L + T * (i + 1) for i in range(horizon))
        ci = tuple(1.96 * sigma * math.sqrt(i + 1) for i in range(horizon))
        return ForecastResult(
            method="holt",
            next_value=future[0],
            horizon=future,
            lower_ci=tuple(f - c for f, c in zip(future, ci)),
            upper_ci=tuple(f + c for f, c in zip(future, ci)),
            smoothing_alpha=self.alpha,
            trend_slope=round(T, 4),
            residual_std=round(sigma, 4),
        )

    # ── Linear regression ──────────────────────────────────────────
    def _linreg(self, series: Sequence[float], horizon: int) -> ForecastResult:
        n = len(series)
        xs = list(range(n))
        x_mean = _mean(xs)
        y_mean = _mean(series)
        num = sum((xs[i] - x_mean) * (series[i] - y_mean) for i in range(n))
        den = sum((x - x_mean) ** 2 for x in xs) or 1.0
        slope = num / den
        intercept = y_mean - slope * x_mean
        preds = [intercept + slope * x for x in xs]
        residuals = [series[i] - preds[i] for i in range(n)]
        sigma = _std(residuals)
        future = tuple(intercept + slope * (n + i) for i in range(horizon))
        ci = tuple(1.96 * sigma * math.sqrt(i + 1) for i in range(horizon))
        return ForecastResult(
            method="linreg",
            next_value=future[0],
            horizon=future,
            lower_ci=tuple(f - c for f, c in zip(future, ci)),
            upper_ci=tuple(f + c for f, c in zip(future, ci)),
            smoothing_alpha=0.0,
            trend_slope=round(slope, 4),
            residual_std=round(sigma, 4),
        )
