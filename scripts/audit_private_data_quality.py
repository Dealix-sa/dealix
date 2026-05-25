import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops_runtime.data_validator import validate_csv_against_schema  # noqa: E402

CHECKS = [
    ("pipeline/pipeline_tracker.csv", "schemas/pipeline_tracker.schema.json"),
    ("revenue/revenue_action_log.csv", "schemas/revenue_action_log.schema.json"),
    ("revenue/cash_collected.csv", "schemas/cash_collected.schema.json"),
    ("revenue/pipeline_value.csv", "schemas/pipeline_value.schema.json"),
    ("revenue/mrr_tracker.csv", "schemas/mrr_tracker.schema.json"),
    ("trust/approval_log.csv", "schemas/approval_log.schema.json"),
    ("evidence/execution_evidence_ledger.csv", "schemas/execution_evidence_ledger.schema.json"),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    private_root = Path(args.private_ops).resolve()
    failures = []
    for relative_csv, schema in CHECKS:
        csv_path = private_root / relative_csv
        schema_path = REPO_ROOT / schema
        if not csv_path.exists():
            failures.append(f"Missing private CSV: {relative_csv}")
            continue
        if not schema_path.exists():
            failures.append(f"Missing schema: {schema}")
            continue
        failures.extend(validate_csv_against_schema(str(csv_path), str(schema_path)))
    if failures:
        print("Private data quality audit failed:")
        for failure in failures:
            print("-", failure)
        raise SystemExit(1)
    print("PASS: private data quality audit passed.")


if __name__ == "__main__":
    main()
