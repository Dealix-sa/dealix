#!/usr/bin/env python3
"""Compute the Dealix weekly business score (0-100, 6 dimensions).

Reads optional CSV / markdown templates under dealix-ops-private/. If a
data source is missing or empty, the dimension is reported as "N/A" with
a hint pointing to the template that should be filled.

Stdlib only. Bilingual output. Supports --json.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PRIVATE = REPO_ROOT / "dealix-ops-private"

CASH_CSV = PRIVATE / "revenue" / "cash_collected.csv"
PIPELINE_CSV = PRIVATE / "revenue" / "pipeline_value.csv"
MRR_CSV = PRIVATE / "revenue" / "mrr_tracker.csv"
FOUNDER_TIME = PRIVATE / "founder" / "founder_time_log.md"
RISK_LOG = PRIVATE / "founder" / "risk_log.md"
EXPERIMENT_LOG = PRIVATE / "learning" / "experiment_log.md"


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            return [row for row in reader]
    except (OSError, csv.Error):
        return []


def _md_has_content(path: Path) -> bool:
    """Return True if a markdown template has been filled beyond placeholders.

    Treats files with ``status: template`` front-matter as empty, and
    requires at least one bullet line that does not contain a ``<…>``
    placeholder token.
    """
    if not path.exists():
        return False
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    # Untouched scaffold templates carry a `status: template` flag.
    if "status: template" in text:
        return False
    real_bullets = [
        ln for ln in text.splitlines()
        if ln.strip().startswith("- ")
        and "<" not in ln
        and "placeholder" not in ln.lower()
    ]
    return len(real_bullets) >= 1


def _float(val: str) -> float:
    try:
        return float(str(val).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def score_cash() -> tuple[float | None, str]:
    rows = _read_csv(CASH_CSV)
    if not rows:
        return None, f"N/A — fill template at {CASH_CSV.relative_to(REPO_ROOT)}"
    total = sum(_float(r.get("amount_sar", "")) for r in rows)
    # Target for the 90-day plan is SAR 90k (three sprints).
    target = 90_000.0
    pct = min(100.0, (total / target) * 100.0) if target else 0.0
    return round(pct, 1), f"cash collected total: SAR {total:,.0f}"


def score_proof() -> tuple[float | None, str]:
    pipeline = _read_csv(PIPELINE_CSV)
    cash = _read_csv(CASH_CSV)
    if not pipeline and not cash:
        return None, f"N/A — fill template at {PIPELINE_CSV.relative_to(REPO_ROOT)}"
    paid = sum(1 for r in cash if (r.get("status") or "").lower() in {"paid", "collected"})
    proposals = len(pipeline)
    # Conversion proxy: paid / proposals, scaled.
    if proposals == 0:
        return 0.0, "no proposals in pipeline yet"
    pct = min(100.0, (paid / max(proposals, 1)) * 200.0)
    return round(pct, 1), f"paid: {paid} / proposals: {proposals}"


def score_retention() -> tuple[float | None, str]:
    mrr = _read_csv(MRR_CSV)
    if not mrr:
        return None, f"N/A — fill template at {MRR_CSV.relative_to(REPO_ROOT)}"
    active = [r for r in mrr if (r.get("status") or "").lower() == "active"]
    total_mrr = sum(_float(r.get("mrr_sar", "")) for r in active)
    # 5k MRR = 100 score.
    pct = min(100.0, (total_mrr / 5_000.0) * 100.0)
    return round(pct, 1), f"active retainers: {len(active)} / MRR SAR {total_mrr:,.0f}"


def score_trust() -> tuple[float | None, str]:
    if not _md_has_content(RISK_LOG):
        return None, f"N/A — fill template at {RISK_LOG.relative_to(REPO_ROOT)}"
    try:
        text = RISK_LOG.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, "risk_log.md unreadable"
    open_risks = sum(
        1
        for ln in text.splitlines()
        if ln.strip().startswith("- ")
        and "open" in ln.lower()
        and "<" not in ln
    )
    pct = max(0.0, 100.0 - open_risks * 10.0)
    return round(pct, 1), f"open risks: {open_risks}"


def score_learning() -> tuple[float | None, str]:
    if not _md_has_content(EXPERIMENT_LOG):
        return None, f"N/A — fill template at {EXPERIMENT_LOG.relative_to(REPO_ROOT)}"
    try:
        text = EXPERIMENT_LOG.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, "experiment_log.md unreadable"
    experiments = sum(
        1
        for ln in text.splitlines()
        if ln.strip().startswith("- ") and "<" not in ln
    )
    pct = min(100.0, experiments * 20.0)
    return round(pct, 1), f"experiments logged: {experiments}"


def score_founder_leverage() -> tuple[float | None, str]:
    if not _md_has_content(FOUNDER_TIME):
        return None, f"N/A — fill template at {FOUNDER_TIME.relative_to(REPO_ROOT)}"
    try:
        text = FOUNDER_TIME.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, "founder_time_log.md unreadable"
    revenue_hours = sum(
        1
        for ln in text.splitlines()
        if "revenue" in ln.lower() and ln.strip().startswith("- ")
    )
    total_hours = sum(1 for ln in text.splitlines() if ln.strip().startswith("- "))
    if total_hours == 0:
        return 0.0, "no time entries yet"
    pct = min(100.0, (revenue_hours / total_hours) * 100.0)
    return round(pct, 1), f"revenue hours / total: {revenue_hours}/{total_hours}"


DIMENSIONS = [
    ("Cash", "النقد", score_cash),
    ("Proof", "الإثبات", score_proof),
    ("Retention", "الاحتفاظ", score_retention),
    ("Trust", "الثقة", score_trust),
    ("Learning", "التعلم", score_learning),
    ("Founder Leverage", "رافعة المؤسس", score_founder_leverage),
]


def compute() -> dict:
    results: list[dict] = []
    numeric_scores: list[float] = []
    for en, ar, fn in DIMENSIONS:
        try:
            score, note = fn()
        except Exception as exc:  # defensive: never crash the CEO dashboard
            score, note = None, f"error: {exc}"
        results.append(
            {
                "dimension_en": en,
                "dimension_ar": ar,
                "score": score,
                "note": note,
            }
        )
        if score is not None:
            numeric_scores.append(score)
    overall = round(sum(numeric_scores) / len(numeric_scores), 1) if numeric_scores else None
    return {
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "overall": overall,
        "dimensions": results,
    }


def print_human(report: dict) -> None:
    print("Dealix Weekly Business Score / درجة الأعمال الأسبوعية")
    print("=" * 64)
    overall = report["overall"]
    overall_label = f"{overall}/100" if overall is not None else "N/A"
    print(f"Overall / الإجمالي : {overall_label}")
    print("-" * 64)
    print(f"{'Dimension / البُعد':<32}{'Score / النتيجة':<18}Note")
    print("-" * 64)
    for d in report["dimensions"]:
        label = f"{d['dimension_en']} / {d['dimension_ar']}"
        score = "N/A" if d["score"] is None else f"{d['score']}/100"
        print(f"{label:<32}{score:<18}{d['note']}")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    report = compute()
    if "--json" in argv:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
