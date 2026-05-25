from pathlib import Path

required = [
    "docs/data/COMPANY_DATA_ARCHITECTURE.md",
    "docs/data/DATA_FRESHNESS_POLICY.md",
    "docs/data/DATA_PRIVACY_BOUNDARY.md",
    "docs/data/REVENUE_DATA_MODEL.md",
    "docs/data/SAAS_METRICS_LATER.md",
    "ops_runtime/data_validator.py",
    "scripts/audit_private_data_quality.py",
    "scripts/export_company_snapshot.py",
    "scripts/verify_data_boundary.py",
    "schemas/pipeline_tracker.schema.json",
    "schemas/revenue_action_log.schema.json",
    "schemas/cash_collected.schema.json",
    "schemas/pipeline_value.schema.json",
    "schemas/mrr_tracker.schema.json",
    "schemas/approval_log.schema.json",
    "schemas/execution_evidence_ledger.schema.json",
]
failures = []
for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 50:
        failures.append(f"Too short: {file}")
if failures:
    print("Company data architecture verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)
print("PASS: company data architecture is ready.")
