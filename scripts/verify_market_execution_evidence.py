"""Gate: market execution evidence must exist before claiming progress.

Inspects the private ops ledgers and ensures the CEO has at least:
- 25 leads in the pipeline tracker
- 25 outbound actions in the revenue action log
- 3 samples (rows or files in delivery/samples)
- 1 proposal in the proposal tracker
- 1 payment / PO follow-up in the revenue action log

Exits non-zero with the list of failures if any check fails.
"""

from pathlib import Path
import csv
import argparse


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
    pipeline = read_csv(root / "pipeline/pipeline_tracker.csv")
    actions = read_csv(root / "revenue/revenue_action_log.csv")
    proposals = read_csv(root / "sales/proposal_tracker.csv")
    outbound = [
        r for r in actions
        if (r.get("type") or "").strip().lower() == "outbound"
    ]
    samples = [
        r for r in actions
        if (r.get("type") or "").strip().lower() == "sample"
    ]
    payment_followups = [
        r for r in actions
        if "payment" in (r.get("type") or "").strip().lower()
        or "po" in (r.get("type") or "").strip().lower()
    ]
    failures = []
    if len(pipeline) < 25:
        failures.append(f"Need 25 leads, found {len(pipeline)}")
    if len(outbound) < 25:
        failures.append(f"Need 25 outbound actions, found {len(outbound)}")
    if len(samples) < 3 and not any((root / "delivery/samples").glob("*")):
        failures.append("Need 3 samples or files in delivery/samples")
    if len(proposals) < 1:
        failures.append("Need 1 proposal in sales/proposal_tracker.csv")
    if len(payment_followups) < 1:
        failures.append("Need 1 payment/PO follow-up in revenue_action_log.csv")
    if failures:
        print("Market execution evidence failed:")
        for failure in failures:
            print("-", failure)
        raise SystemExit(1)
    print("PASS: market execution evidence is complete.")


if __name__ == "__main__":
    main()
