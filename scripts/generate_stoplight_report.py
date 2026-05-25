"""Generate the Dealix strategic stoplight report.

Reads the market execution ledgers and writes a red/yellow/green status
table to <private-ops>/founder/strategic_stoplight.md so the CEO can see
the first bottleneck at a glance every morning.
"""

import argparse
from pathlib import Path
from datetime import date
import csv


def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    leads = read_csv(root / "pipeline/pipeline_tracker.csv")
    actions = read_csv(root / "revenue/revenue_action_log.csv")
    proposals = read_csv(root / "sales/proposal_tracker.csv")
    cash = read_csv(root / "revenue/cash_collected.csv")
    outbound = [r for r in actions if (r.get("type") or "").lower() == "outbound"]
    samples = [r for r in actions if (r.get("type") or "").lower() == "sample"]
    payments = [
        r for r in actions
        if "payment" in (r.get("type") or "").lower()
        or "po" in (r.get("type") or "").lower()
    ]
    cash_collected = sum(
        float(r.get("amount_sar") or 0)
        for r in cash
        if (r.get("status") or "").lower() in {"paid", "collected", "done"}
    )
    checks = {
        "Leads": (len(leads), 25),
        "Outbound": (len(outbound), 25),
        "Samples": (len(samples), 3),
        "Proposals": (len(proposals), 1),
        "Payment Followups": (len(payments), 1),
        "Cash Collected": (cash_collected, 1),
    }
    rows = []
    for name, (actual, target) in checks.items():
        if actual >= target:
            color = "GREEN"
        elif actual > 0:
            color = "YELLOW"
        else:
            color = "RED"
        rows.append(f"| {name} | {actual} | {target} | {color} |")
    content = f"""# Dealix Strategic Stoplight
## Date
{date.today().isoformat()}
| Area | Actual | Target | Status |
|---|---:|---:|---|
{chr(10).join(rows)}
## CEO Rule
Red means fix immediately.
Yellow means push.
Green means maintain and move to next bottleneck.
"""
    out = root / "founder/strategic_stoplight.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print("PASS: strategic stoplight generated.")
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
