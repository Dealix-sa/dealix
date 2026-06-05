#!/usr/bin/env python3
"""
targeting_scorecard.py — the 100-point targeting scorecard.

Turns an enriched company record into a deterministic score + grade so the
founder reviews the *right* 5 companies, not 400. Weights and penalties live in
data/targeting/scoring_weights.yml (single source of truth). Pure functions, no
network, no side effects — safe to unit test.

Axes (sum to 100): ICP fit 25 · business pain 20 · timing/intent 15 ·
access 10 · Dealix fit 10 · evidence confidence 10 · strategic value 10.

Usage:
    python scripts/targeting_scorecard.py --in data/targeting/company_master.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import yaml  # noqa: E402

DEFAULT_WEIGHTS = _ROOT / "data" / "targeting" / "scoring_weights.yml"
DEFAULT_SIGNALS = _ROOT / "data" / "targeting" / "signals.yml"


def load_weights(path: Path | None = None) -> dict[str, Any]:
    path = path or DEFAULT_WEIGHTS
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data


def _load_signal_weights(path: Path | None = None) -> dict[str, float]:
    """Map signal id -> weight (0..1) for both pain and intent libraries."""
    path = path or DEFAULT_SIGNALS
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out: dict[str, float] = {}
    for key in ("signals", "intent_signals"):
        for item in data.get(key, []) or []:
            sid = item.get("id")
            if sid:
                out[sid] = float(item.get("weight", 0.5))
    return out


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


# --------------------------------------------------------------------------- #
# Per-axis fractions (each returns 0..1)
# --------------------------------------------------------------------------- #
def _icp_fraction(company: dict[str, Any]) -> float:
    """ICP fit from sector match, in-plan city, and size signal."""
    frac = 0.0
    if company.get("sector"):
        frac += 0.5  # has a known sector at all
    if company.get("icp_in_phase", True):  # enricher marks whether sector∈active phase
        frac += 0.3
    size = str(company.get("company_size_signal", "")).lower()
    if any(k in size for k in ("smb", "mid", "midmarket", "mid-market")):
        frac += 0.2
    return _clamp01(frac)


def _pain_fraction(company: dict[str, Any], sig_w: dict[str, float]) -> float:
    """Strength of evidence-backed pain signals (diminishing returns)."""
    signals = company.get("pain_signals", []) or []
    if not signals:
        return 0.0
    total = sum(sig_w.get(s, 0.5) for s in signals)
    # 1 strong signal ~0.6, two ~0.85, three+ saturates toward 1.0
    return _clamp01(1.0 - (0.5**total))


def _timing_fraction(company: dict[str, Any], sig_w: dict[str, float]) -> float:
    signals = company.get("intent_signals", []) or []
    if not signals:
        return 0.0
    total = sum(sig_w.get(s, 0.5) for s in signals)
    return _clamp01(1.0 - (0.6**total))


def _access_fraction(company: dict[str, Any]) -> float:
    channel = str(company.get("contact_channel", "")).lower()
    official = {"website_form", "official_email", "contact_page", "official_phone"}
    if channel in official:
        return 1.0
    if channel and channel not in {"none", "personal_mobile", "personal_phone"}:
        return 0.5
    return 0.0


def _dealix_fit_fraction(company: dict[str, Any]) -> float:
    """Clean map to exactly one Dealix OS angle scores highest."""
    offer = company.get("recommended_offer")
    if not offer:
        return 0.0
    # A single, specific offer is better than a vague 'multiple'.
    return 1.0 if isinstance(offer, str) and offer.strip() else 0.5


def _evidence_fraction(company: dict[str, Any]) -> float:
    n = int(company.get("evidence_count", len(company.get("source_urls", []) or [])))
    if n >= 3:
        return 1.0
    if n == 2:
        return 0.7
    if n == 1:
        return 0.3
    return 0.0


def _strategic_fraction(company: dict[str, Any]) -> float:
    frac = 0.0
    if company.get("partnership_signal"):
        frac += 0.4  # agency/channel potential
    size = str(company.get("company_size_signal", "")).lower()
    if "mid" in size or "enterprise" in size:
        frac += 0.4
    if company.get("long_b2b_accounts") or "long_b2b_accounts" in (
        company.get("pain_signals", []) or []
    ):
        frac += 0.2
    return _clamp01(frac)


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #
def grade_for(score: float, weights: dict[str, Any]) -> dict[str, str]:
    for band in weights.get("grades", []):
        if score >= float(band["min"]):
            return {"grade": band["grade"], "decision": band["decision"]}
    return {"grade": "D", "decision": "do_not_target_now"}


def compute_penalties(
    company: dict[str, Any], weights: dict[str, Any]
) -> tuple[float, list[str], bool]:
    """Return (penalty_total, applied[], force_reject)."""
    pen = weights.get("penalties", {})
    applied: list[str] = []
    total = 0.0
    force_reject = False

    n_sources = len(company.get("source_urls", []) or [])
    evidence = int(company.get("evidence_count", n_sources))

    def _apply(key: str) -> None:
        nonlocal total, force_reject
        val = pen.get(key)
        if val is None:
            return
        if isinstance(val, str) and val.lower() == "reject":
            force_reject = True
            applied.append(f"{key}:reject")
        else:
            total += float(val)
            applied.append(f"{key}:{val}")

    if evidence <= 1:
        _apply("single_source_only")
    if not company.get("sector") or not company.get("city"):
        _apply("incomplete_data")
    if company.get("is_sensitive_sector") or "sensitive_sector" in (
        company.get("risk_flags", []) or []
    ):
        _apply("sensitive_sector")
    if _access_fraction(company) == 0.0:
        _apply("no_official_channel")
    if company.get("weakness_hypothesis") and not (company.get("pain_signals")):
        _apply("guess_without_evidence")
    flags = set(company.get("risk_flags", []) or [])
    if "blocked_source" in flags or "forbidden_source_type" in flags:
        _apply("disallowed_source")
    if company.get("is_duplicate"):
        _apply("duplicate")

    return total, applied, force_reject


def score_company(
    company: dict[str, Any],
    weights: dict[str, Any] | None = None,
    signal_weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Score one company. Returns score, grade, decision, axis breakdown,
    and the list of penalties applied. Deterministic and side-effect free."""
    weights = weights or load_weights()
    sig_w = signal_weights if signal_weights is not None else _load_signal_weights()
    axes = weights.get("axes", {})

    fractions = {
        "icp_fit": _icp_fraction(company),
        "business_pain": _pain_fraction(company, sig_w),
        "timing_intent": _timing_fraction(company, sig_w),
        "access_contactability": _access_fraction(company),
        "dealix_fit": _dealix_fit_fraction(company),
        "evidence_confidence": _evidence_fraction(company),
        "strategic_value": _strategic_fraction(company),
    }
    breakdown = {k: round(fractions[k] * float(axes.get(k, 0)), 2) for k in fractions}
    base = sum(breakdown.values())

    penalty_total, applied, force_reject = compute_penalties(company, weights)
    score = max(0.0, min(100.0, base + penalty_total))
    score = round(score, 1)

    if force_reject:
        grade_info = {"grade": "D", "decision": "do_not_target_now"}
        score = min(score, 59.0)
    else:
        grade_info = grade_for(score, weights)

    return {
        "targeting_score": score,
        "grade": grade_info["grade"],
        "decision": grade_info["decision"],
        "axis_breakdown": breakdown,
        "penalties": applied,
        "force_reject": force_reject,
    }


def score_and_merge(company: dict[str, Any], **kw: Any) -> dict[str, Any]:
    """Score, then write results back onto a copy of the company record."""
    result = score_company(company, **kw)
    merged = dict(company)
    merged["targeting_score"] = result["targeting_score"]
    merged["grade"] = result["grade"]
    merged["next_action"] = (
        "Manual founder review" if result["grade"] in {"A+", "A"} else "Nurture / re-evaluate"
    )
    merged["_score_detail"] = result
    return merged


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            rows.append(json.loads(line))
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix Targeting OS scorecard")
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--weights", default=str(DEFAULT_WEIGHTS))
    args = ap.parse_args(argv)

    weights = load_weights(Path(args.weights))
    sig_w = _load_signal_weights()
    rows = [
        score_and_merge(c, weights=weights, signal_weights=sig_w)
        for c in _read_jsonl(Path(args.infile))
    ]
    rows.sort(key=lambda r: r["targeting_score"], reverse=True)
    for r in rows:
        print(
            json.dumps(
                {
                    "company": r.get("company_name"),
                    "score": r["targeting_score"],
                    "grade": r["grade"],
                    "next_action": r["next_action"],
                },
                ensure_ascii=False,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
