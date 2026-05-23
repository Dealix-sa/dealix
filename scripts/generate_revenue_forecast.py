"""Generate the Dealix Revenue Forecast — conservative, evidence-only.

Reads <private_ops>/ and writes:
  <private_ops>/finance/revenue_forecast.md

Implements Pipeline Weighting Model docs/finance/PIPELINE_WEIGHTING_MODEL.md.
No guaranteed revenue claims; outputs labelled as estimates.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


STAGE_WEIGHTS = {
    "discovery": 0.10,
    "sample_sent": 0.25,
    "proposal_sent": 0.40,
    "verbal_yes": 0.60,
    "invoice_issued": 0.80,
    "paid": 1.00,
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))
    except (OSError, csv.Error):
        return []


def _parse_date(s: str) -> date | None:
    if not s:
        return None
    try:
        return datetime.strptime(s.split("T")[0][:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def _days_since(s: str) -> int:
    d = _parse_date(s)
    if not d:
        return 0
    return max(0, (date.today() - d).days)


def _weighted(stage: str, amount: float, days_open: int) -> float:
    base = STAGE_WEIGHTS.get((stage or "").lower(), 0.0)
    if base >= 1.0:
        return amount
    if days_open >= 30:
        base = 0.05
    elif days_open >= 14:
        base *= 0.5
    return amount * base


def compute(private_ops: Path) -> dict:
    cash_rows = _read_csv(private_ops / "finance" / "cash_collected.csv")
    proposals = _read_csv(private_ops / "sales" / "proposal_log.csv")
    payments_q = _read_csv(private_ops / "finance" / "payment_capture_queue.csv")

    cash_collected = sum(float(r.get("amount_sar", 0) or 0) for r in cash_rows)
    open_proposal_value = sum(
        float(p.get("amount_sar", 0) or 0)
        for p in proposals
        if p.get("status", "").lower() not in {"paid", "lost", "killed"}
    )
    weighted = 0.0
    payment_risk_count = 0
    open_payments = []
    for p in proposals:
        status = (p.get("status") or "").lower()
        if status in {"paid", "lost", "killed"}:
            continue
        amt = float(p.get("amount_sar", 0) or 0)
        days = _days_since(p.get("date", ""))
        weighted += _weighted(status, amt, days)
        if status in {"proposal_sent", "verbal_yes", "invoice_issued"} and days >= 14:
            payment_risk_count += 1
            open_payments.append(p)

    if cash_collected > 0 and payment_risk_count <= 1:
        confidence = "high"
    elif cash_collected > 0:
        confidence = "medium"
    else:
        confidence = "low"

    next_action = "—"
    if open_payments:
        first = open_payments[0]
        next_action = (
            f"Follow-up payment على proposal {first.get('proposal_id', '?')} "
            f"للعميل {first.get('customer', '?')}"
        )
    elif open_proposal_value > 0:
        next_action = "حدد أعلى-قيمة proposal مفتوح وحرك خطوة واحدة (call/sample)."
    else:
        next_action = "افتح discovery call واحدة من القطاع المستهدف هذا الأسبوع."

    return {
        "cash_collected_sar": cash_collected,
        "open_proposal_value_sar": open_proposal_value,
        "weighted_pipeline_sar": round(weighted, 2),
        "payment_risk_count": payment_risk_count,
        "next_cash_action": next_action,
        "forecast_confidence": confidence,
        "open_payments_top": open_payments[:5],
        "queue_size": len(payments_q),
    }


def render(private_ops: Path, data: dict) -> str:
    lines = [
        f"# Revenue Forecast — {date.today().isoformat()}",
        "",
        f"_Generated: {_now_iso()}_",
        f"_Source: {private_ops}_",
        "",
        "## Cash collected — كاش مُحصَّل",
        f"- **{data['cash_collected_sar']:.0f} SAR** (مجموع `cash_collected.csv`)",
        "",
        "## Open proposal value — قيمة العروض المفتوحة",
        f"- **{data['open_proposal_value_sar']:.0f} SAR** (مجموع `proposal_log.csv` non-paid)",
        "",
        "## Weighted pipeline — pipeline موزون",
        f"- **{data['weighted_pipeline_sar']:.0f} SAR** (according to PIPELINE_WEIGHTING_MODEL.md)",
        "",
        "## Payment risk — مخاطر الدفع",
        f"- {data['payment_risk_count']} proposals بانتظار دفع ≥14 يوم",
    ]
    for p in data["open_payments_top"]:
        lines.append(
            f"  - {p.get('proposal_id','?')} → {p.get('customer','?')} "
            f"({p.get('status','?')}, D+{_days_since(p.get('date',''))})"
        )
    lines += [
        "",
        "## Next cash action — الـ action #1",
        f"- {data['next_cash_action']}",
        "",
        f"## Forecast confidence — ثقة التوقع: **{data['forecast_confidence']}**",
        "",
        "---",
        "",
        "_Estimate only. No guaranteed revenue. Numbers update with each run._",
    ]
    return "\n".join(lines)


def write(private_ops: Path) -> Path:
    data = compute(private_ops)
    target = private_ops / "finance" / "revenue_forecast.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(private_ops, data), encoding="utf-8")
    return target


def _empty_template(reason: str) -> str:
    return (
        f"# Revenue Forecast — {date.today().isoformat()}\n\n"
        f"_PRIVATE_OPS unavailable: {reason}_\n\n"
        "See docs/finance/REVENUE_FORECASTING_SYSTEM.md\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Dealix Revenue Forecast.")
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("PRIVATE_OPS") or os.environ.get("DEALIX_PRIVATE_OPS"),
    )
    parser.add_argument("--print", action="store_true")
    args = parser.parse_args(argv)

    if not args.private_ops:
        sys.stderr.write("[warn] PRIVATE_OPS not set — emitting template.\n")
        sys.stdout.write(_empty_template("not set"))
        return 0

    private_ops = Path(args.private_ops).expanduser().resolve()
    if not private_ops.exists():
        sys.stderr.write(f"[warn] PRIVATE_OPS missing: {private_ops}\n")
        sys.stdout.write(_empty_template(str(private_ops)))
        return 0

    out = write(private_ops)
    sys.stdout.write(f"[ok] wrote {out}\n")
    if args.print:
        sys.stdout.write(out.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
