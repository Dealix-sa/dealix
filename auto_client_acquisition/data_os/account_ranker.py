"""Account ranking — Sprint Day-3 deliverable.

Takes the validated accounts from ``csv_intake.score_csv`` and produces the
top-N ranked accounts with an **explainable** rubric: fit, signal strength,
governance risk. Deterministic. No LLM. Reuses the row shape the rest of
data_os already uses (dicts with ``company_name``, ``sector``, ``city``,
optional ``source``, ``email``, ``phone``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

DEFAULT_TOP_N = 10
GOVERNANCE_RISK_SOURCES: frozenset[str] = frozenset(
    {
        "scrape",
        "scraped",
        "harvested",
        "purchased_list",
        "purchased",
        "list_buy",
        "unknown",
        "",
    }
)
FREEMAIL_DOMAINS: frozenset[str] = frozenset(
    {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com"}
)


@dataclass(frozen=True, slots=True)
class ICPProfile:
    """Ideal Customer Profile signal weights — every input is a tuple of strings."""

    preferred_sectors: tuple[str, ...] = ()
    preferred_cities: tuple[str, ...] = ()

    def normalized_sectors(self) -> frozenset[str]:
        return frozenset(s.strip().lower() for s in self.preferred_sectors if s.strip())

    def normalized_cities(self) -> frozenset[str]:
        return frozenset(c.strip().lower() for c in self.preferred_cities if c.strip())


@dataclass(frozen=True, slots=True)
class RankedAccount:
    """One ranked account with the three explainable sub-scores."""

    company_name: str
    fit: float
    signal_strength: float
    governance_risk: float
    total: float
    reasons: tuple[str, ...] = field(default_factory=tuple)
    row: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "company_name": self.company_name,
            "fit": self.fit,
            "signal_strength": self.signal_strength,
            "governance_risk": self.governance_risk,
            "total": self.total,
            "reasons": list(self.reasons),
        }


def _fit_score(row: dict[str, Any], icp: ICPProfile) -> tuple[float, list[str]]:
    """0-100 fit score from sector + city match against the ICP."""
    reasons: list[str] = []
    score = 0.0
    sector = str(row.get("sector", "")).strip().lower()
    city = str(row.get("city", "")).strip().lower()
    sectors = icp.normalized_sectors()
    cities = icp.normalized_cities()
    if not sectors and not cities:
        score = 60.0
        reasons.append("no_icp_supplied_default_60")
        return score, reasons
    if sectors:
        if sector and sector in sectors:
            score += 55.0
            reasons.append(f"sector_match:{sector}")
        elif sector:
            reasons.append(f"sector_off_icp:{sector}")
    if cities:
        if city and city in cities:
            score += 45.0
            reasons.append(f"city_match:{city}")
        elif city:
            reasons.append(f"city_off_icp:{city}")
    return round(min(score, 100.0), 1), reasons


def _signal_strength(row: dict[str, Any]) -> tuple[float, list[str]]:
    """0-100 — how much usable signal the row carries (more contact info = stronger)."""
    reasons: list[str] = []
    signals = 0
    total = 5
    if str(row.get("company_name", "")).strip():
        signals += 1
        reasons.append("has_company_name")
    if str(row.get("sector", "")).strip():
        signals += 1
        reasons.append("has_sector")
    if str(row.get("city", "")).strip():
        signals += 1
        reasons.append("has_city")
    if str(row.get("email", "")).strip():
        signals += 1
        reasons.append("has_email")
    if str(row.get("phone", "")).strip():
        signals += 1
        reasons.append("has_phone")
    return round(100.0 * signals / total, 1), reasons


def _governance_risk(row: dict[str, Any]) -> tuple[float, list[str]]:
    """0-100 risk — higher is worse. Flags un-sourced / freemail / scraping signals."""
    reasons: list[str] = []
    risk = 0.0
    source = str(row.get("source", "")).strip().lower()
    if source in GOVERNANCE_RISK_SOURCES:
        risk += 60.0
        reasons.append(f"risky_or_missing_source:{source or 'empty'}")
    email = str(row.get("email", "")).strip().lower()
    if email and "@" in email:
        domain = email.rsplit("@", 1)[1]
        if domain in FREEMAIL_DOMAINS:
            risk += 30.0
            reasons.append(f"freemail_domain:{domain}")
    if not str(row.get("company_name", "")).strip():
        risk += 30.0
        reasons.append("missing_company_name")
    return round(min(risk, 100.0), 1), reasons


def _total(fit: float, signal: float, risk: float) -> float:
    """Blend the three sub-scores. Governance risk subtracts. Clamped to [0,100]."""
    raw = 0.45 * fit + 0.35 * signal - 0.30 * risk
    return round(max(0.0, min(100.0, raw)), 1)


def rank_accounts(
    rows: list[dict[str, Any]],
    *,
    icp: ICPProfile | None = None,
    top_n: int = DEFAULT_TOP_N,
) -> list[RankedAccount]:
    """Sort accounts by the blended explainable score and return the top N.

    Stable ordering: ties broken by company_name (case-insensitive) so the
    same input always yields the same ranking — required for Proof Pack
    reproducibility.
    """
    if top_n <= 0:
        raise ValueError("top_n must be >= 1")
    profile = icp or ICPProfile()
    ranked: list[RankedAccount] = []
    for row in rows:
        company = str(row.get("company_name", "")).strip() or "(unnamed)"
        fit, fit_r = _fit_score(row, profile)
        signal, sig_r = _signal_strength(row)
        risk, risk_r = _governance_risk(row)
        ranked.append(
            RankedAccount(
                company_name=company,
                fit=fit,
                signal_strength=signal,
                governance_risk=risk,
                total=_total(fit, signal, risk),
                reasons=tuple(fit_r + sig_r + risk_r),
                row=dict(row),
            )
        )
    ranked.sort(key=lambda a: (-a.total, a.company_name.lower()))
    return ranked[:top_n]


__all__ = [
    "DEFAULT_TOP_N",
    "FREEMAIL_DOMAINS",
    "GOVERNANCE_RISK_SOURCES",
    "ICPProfile",
    "RankedAccount",
    "rank_accounts",
]
