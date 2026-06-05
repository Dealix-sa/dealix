#!/usr/bin/env python3
"""Scoring engine — turns a company profile into an auditable score out of 100.

Score = sum of axis points (each capped at its axis max) − penalties, clamped to
[0, 100]. Every point has a reason, so a founder can see *why* a company scored
what it did. The decision band (A+/A/B/C/D) and human action come from
data/targeting/scoring_weights.yml.

Axes (max 100):
    icp_fit 25 · pain_signal 20 · timing_intent 15 · access 10 ·
    dealix_os_fit 10 · evidence_confidence 10 · strategic_value 10

Penalties: single source, no website, no pain, sensitive sector, weak channel,
compliance risk (→ reject), generic-message risk.

Usage:
    python scripts/targeting_scorecard.py \\
        --in data/targeting/company_master.jsonl \\
        --out data/targeting/out --top 80
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from scripts.targeting_common import (
    COMPANY_MASTER,
    OUT_DIR,
    load_cities,
    load_companies,
    load_sectors,
    load_signals,
    load_weights,
)

ALLOWED_CHANNELS = {
    "official_website_form",
    "official_business_email",
    "official_phone_switchboard",
    "official_linkedin_company_page",
    "in_person_event",
    "warm_introduction",
}
STRONG_CHANNELS = {"warm_introduction", "in_person_event", "official_business_email"}


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def score_company(
    company: dict[str, Any],
    *,
    weights: dict[str, Any] | None = None,
    sectors: dict[str, Any] | None = None,
    cities: dict[str, Any] | None = None,
    signals: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a full scoring breakdown for one company.

    The result has: ``score`` (int 0-100), ``grade``, ``decision``, ``axes``
    (per-axis points + reasons), ``penalties`` (applied), and a ``reject`` flag.
    """
    weights = weights or load_weights()
    sectors = sectors or load_sectors()
    cities = cities or load_cities()
    signals = signals or load_signals()

    axes_cfg = weights.get("axes", {})
    pen_cfg = weights.get("penalties", {})
    axes: dict[str, dict[str, Any]] = {}
    reasons: dict[str, list[str]] = {}

    def axis_max(name: str) -> float:
        return float(axes_cfg.get(name, {}).get("max", 0))

    sector_key = company.get("sector") or "other"
    sector = sectors.get(sector_key, {})

    # ── ICP fit ──
    icp_weight = float(sector.get("icp_weight", 0.5))
    icp_pts = axis_max("icp_fit") * icp_weight
    icp_reason = [f"sector {sector_key} icp_weight={icp_weight}"]
    if company.get("b2b"):
        icp_reason.append("b2b")
    axes["icp_fit"] = {"points": round(icp_pts, 1)}
    reasons["icp_fit"] = icp_reason

    # ── Pain signal ──
    pain_pts = 0.0
    pain_reason: list[str] = []
    for sig_name, sig in signals.get("pain_signals", {}).items():
        if company.get(sig_name):
            pain_pts += float(sig.get("points", 0))
            pain_reason.append(sig_name)
    pain_pts = _clamp(pain_pts, 0, axis_max("pain_signal"))
    axes["pain_signal"] = {"points": round(pain_pts, 1)}
    reasons["pain_signal"] = pain_reason or ["no pain signal observed"]

    # ── Timing / intent ──
    timing_pts = 0.0
    timing_reason: list[str] = []
    for sig_name, sig in signals.get("timing_signals", {}).items():
        if company.get(sig_name):
            timing_pts += float(sig.get("points", 0))
            timing_reason.append(sig_name)
    timing_pts = _clamp(timing_pts, 0, axis_max("timing_intent"))
    axes["timing_intent"] = {"points": round(timing_pts, 1)}
    reasons["timing_intent"] = timing_reason or ["no timing signal"]

    # ── Access ──
    channel = (company.get("contact_channel") or "").strip()
    if channel in STRONG_CHANNELS:
        access_pts = axis_max("access")
    elif channel in ALLOWED_CHANNELS:
        access_pts = axis_max("access") * 0.6
    else:
        access_pts = axis_max("access") * 0.2
    axes["access"] = {"points": round(access_pts, 1)}
    reasons["access"] = [f"channel={channel or 'none'}"]

    # ── Dealix OS fit ── (pain maps cleanly onto an OS angle)
    has_weakness = bool(pain_reason)
    os_pts = axis_max("dealix_os_fit") * (1.0 if has_weakness else 0.3)
    axes["dealix_os_fit"] = {"points": round(os_pts, 1)}
    reasons["dealix_os_fit"] = [
        sector.get("default_angle", "n/a") if has_weakness else "no clear OS angle yet"
    ]

    # ── Evidence confidence ──
    evidence = int(company.get("evidence_count") or 0)
    ev_pts = _clamp(evidence * 3.0, 0, axis_max("evidence_confidence"))
    axes["evidence_confidence"] = {"points": round(ev_pts, 1)}
    reasons["evidence_confidence"] = [f"evidence_count={evidence}"]

    # ── Strategic value ── (market density + partner potential)
    city = cities.get(company.get("city") or "other", {})
    market_w = float(city.get("market_weight", 0.5))
    strat_pts = axis_max("strategic_value") * market_w
    if company.get("serves_many_clients"):
        strat_pts = min(axis_max("strategic_value"), strat_pts + 3)
    axes["strategic_value"] = {"points": round(strat_pts, 1)}
    reasons["strategic_value"] = [
        f"city={company.get('city')} market_weight={market_w}"
        + (" +partner_potential" if company.get("serves_many_clients") else "")
    ]

    subtotal = sum(a["points"] for a in axes.values())

    # ── Penalties ──
    applied_penalties: list[dict[str, Any]] = []
    reject = False

    def apply(key: str, condition: bool) -> None:
        nonlocal reject
        if not condition or key not in pen_cfg:
            return
        val = pen_cfg[key]
        if val == "reject":
            reject = True
            applied_penalties.append({"penalty": key, "value": "reject"})
        else:
            applied_penalties.append({"penalty": key, "value": int(val)})

    apply("single_source_only", evidence <= 1)
    apply("no_official_website", not (company.get("website") or "").strip())
    apply("no_pain_signal", not has_weakness)
    apply("sensitive_sector", bool(sector.get("sensitive")))
    apply("weak_contact_channel", channel not in ALLOWED_CHANNELS or not channel)
    apply(
        "compliance_risk", bool(company.get("personal_phone") or company.get("no_robots_respect"))
    )
    # Generic-message risk: thin pain + thin evidence → message would be generic.
    apply("generic_message_risk", (not has_weakness) and evidence <= 1)

    penalty_total = sum(p["value"] for p in applied_penalties if isinstance(p["value"], int))
    raw = subtotal + penalty_total
    score = round(_clamp(raw, 0, 100))

    # ── Band / decision ──
    grade, decision = "D", "do_not_target"
    label_en, label_ar = "Do not target now", "لا يُستهدف الآن"
    for band in weights.get("bands", []):
        if score >= int(band.get("min", 0)):
            grade = band.get("grade", grade)
            decision = band.get("decision", decision)
            label_en = band.get("label_en", label_en)
            label_ar = band.get("label_ar", label_ar)
            break

    if reject:
        grade, decision = "REJECT", "reject_compliance"
        label_en, label_ar = "Reject (compliance)", "مرفوض (امتثال)"
        score = 0

    return {
        "company_name": company.get("company_name"),
        "sector": sector_key,
        "city": company.get("city"),
        "score": score,
        "grade": grade,
        "decision": decision,
        "label_en": label_en,
        "label_ar": label_ar,
        "reject": reject,
        "axes": axes,
        "axis_reasons": reasons,
        "penalties": applied_penalties,
        "evidence_count": evidence,
    }


def rank(companies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Score and sort companies high→low, dropping compliance rejects to the end."""
    weights, sectors, cities, signals = (
        load_weights(),
        load_sectors(),
        load_cities(),
        load_signals(),
    )
    scored = [
        score_company(c, weights=weights, sectors=sectors, cities=cities, signals=signals)
        for c in companies
    ]
    scored.sort(key=lambda s: (not s["reject"], s["score"]), reverse=True)
    return scored


def _write_ranked_csv(scored: list[dict[str, Any]], out_dir: Path, top: int | None) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "ranked_targets.csv"
    rows = scored[:top] if top else scored
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(
            [
                "rank",
                "company_name",
                "sector",
                "city",
                "score",
                "grade",
                "decision",
                "evidence_count",
                "top_reasons",
            ]
        )
        for i, s in enumerate(rows, 1):
            top_axes = sorted(s["axes"].items(), key=lambda kv: kv[1]["points"], reverse=True)[:3]
            reason = "; ".join(f"{k}={v['points']}" for k, v in top_axes)
            w.writerow(
                [
                    i,
                    s["company_name"],
                    s["sector"],
                    s["city"],
                    s["score"],
                    s["grade"],
                    s["decision"],
                    s["evidence_count"],
                    reason,
                ]
            )
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix targeting scorecard")
    ap.add_argument("--in", dest="infile", default=str(COMPANY_MASTER))
    ap.add_argument("--out", dest="outdir", default=str(OUT_DIR))
    ap.add_argument("--top", type=int, default=80)
    args = ap.parse_args(argv)

    companies = load_companies(Path(args.infile))
    scored = rank(companies)
    out_dir = Path(args.outdir)
    path = _write_ranked_csv(scored, out_dir, args.top)

    grades: dict[str, int] = {}
    for s in scored:
        grades[s["grade"]] = grades.get(s["grade"], 0) + 1
    print(
        json.dumps(
            {"scored": len(scored), "grades": grades, "out": str(path)},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
