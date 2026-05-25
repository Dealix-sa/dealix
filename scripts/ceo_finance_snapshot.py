#!/usr/bin/env python3
"""Render a finance snapshot for the Dealix founder.

Computes: 30-day cash, total cash, weighted pipeline, MRR, monthly burn,
runway. Missing data is reported gracefully ("N/A — fill <path>"), never
crashes. Stdlib only. Bilingual. Supports --json.
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
EXPENSES_CSV = PRIVATE / "finance" / "expenses.csv"


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open(encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    except (OSError, csv.Error):
        return []


def _float(val: str) -> float:
    try:
        return float(str(val).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def _parse_date(val: str) -> datetime | None:
    if not val:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(val.strip(), fmt)
        except ValueError:
            continue
    return None


def na(path: Path) -> str:
    return f"N/A — fill {path.relative_to(REPO_ROOT)}"


def compute() -> dict:
    cash_rows = _read_csv(CASH_CSV)
    pipeline_rows = _read_csv(PIPELINE_CSV)
    mrr_rows = _read_csv(MRR_CSV)
    expense_rows = _read_csv(EXPENSES_CSV)

    cutoff = datetime.utcnow() - timedelta(days=30)

    if cash_rows:
        cash_total = sum(_float(r.get("amount_sar", "")) for r in cash_rows)
        cash_30d = sum(
            _float(r.get("amount_sar", ""))
            for r in cash_rows
            if (d := _parse_date(r.get("date", ""))) and d >= cutoff
        )
        cash_total_v: float | str = round(cash_total, 2)
        cash_30d_v: float | str = round(cash_30d, 2)
    else:
        cash_total_v = na(CASH_CSV)
        cash_30d_v = na(CASH_CSV)

    if pipeline_rows:
        pipeline_v: float | str = round(
            sum(_float(r.get("weighted_value", "")) for r in pipeline_rows), 2
        )
    else:
        pipeline_v = na(PIPELINE_CSV)

    if mrr_rows:
        active = [r for r in mrr_rows if (r.get("status") or "").lower() == "active"]
        mrr_v: float | str = round(sum(_float(r.get("mrr_sar", "")) for r in active), 2)
    else:
        mrr_v = na(MRR_CSV)

    if expense_rows:
        # Treat every row as a monthly line item; flag recurring=yes only.
        monthly_burn = sum(
            _float(r.get("amount_sar", ""))
            for r in expense_rows
            if (r.get("recurring") or "").strip().lower() in {"yes", "y", "true", "1"}
        )
        # If no recurring flags filled, fall back to total / months span.
        if monthly_burn == 0.0:
            monthly_burn = sum(_float(r.get("amount_sar", "")) for r in expense_rows)
        monthly_burn_v: float | str = round(monthly_burn, 2)
    else:
        monthly_burn_v = na(EXPENSES_CSV)

    # Runway requires numeric cash + numeric burn > 0.
    runway_v: float | str
    if isinstance(cash_total_v, (int, float)) and isinstance(monthly_burn_v, (int, float)):
        if monthly_burn_v > 0:
            runway_v = round(cash_total_v / monthly_burn_v, 1)
        else:
            runway_v = "infinite (no burn) / لا يوجد حرق"
    else:
        runway_v = "N/A"

    return {
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "cash_collected_30d": cash_30d_v,
        "cash_collected_total": cash_total_v,
        "pipeline_weighted": pipeline_v,
        "mrr": mrr_v,
        "monthly_burn": monthly_burn_v,
        "runway_months": runway_v,
    }


def _fmt(val: object) -> str:
    if isinstance(val, (int, float)):
        return f"SAR {val:,.2f}"
    return str(val)


def print_human(snap: dict) -> None:
    print("Dealix Finance Snapshot / لقطة مالية")
    print("=" * 64)
    rows = [
        ("Cash collected (30d)", "النقد المُحصَّل (30 يومًا)", snap["cash_collected_30d"]),
        ("Cash collected (total)", "النقد المُحصَّل (إجمالي)", snap["cash_collected_total"]),
        ("Pipeline (weighted)", "الأنبوب (مرجَّح)", snap["pipeline_weighted"]),
        ("MRR (active)", "إيراد متكرر شهري (فعلي)", snap["mrr"]),
        ("Monthly burn", "الحرق الشهري", snap["monthly_burn"]),
    ]
    for en, ar, v in rows:
        label = f"{en} / {ar}"
        print(f"{label:<48}{_fmt(v)}")
    runway = snap["runway_months"]
    runway_label = f"{runway} months" if isinstance(runway, (int, float)) else str(runway)
    print(f"{'Runway / المهلة':<48}{runway_label}")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    snap = compute()
    if "--json" in argv:
        print(json.dumps(snap, ensure_ascii=False, indent=2))
    else:
        print_human(snap)
    return 0


if __name__ == "__main__":
    sys.exit(main())
