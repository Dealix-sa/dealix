from pathlib import Path

required = [
    "docs/company/DEALIX_ENTERPRISE_COMPANY_OS_V3.md",
    "docs/data/UNIFIED_OPERATING_DATABASE.md",
    "schemas/unified_operating_database.schema.json",
    "docs/runtime/CSV_TO_POSTGRES_MIGRATION_PLAN.md",
    "docs/runtime/WORKER_MESH_OS.md",
    "deploy/PRODUCTION_SERVER_LAYOUT.md",
    "docs/product/CEO_COMMAND_CENTER_V1.md",
    "docs/api/REVENUE_FACTORY_API_SURFACE.md",
    "docs/distribution/DISTRIBUTION_FLYWHEEL.md",
    "docs/distribution/SECTOR_DOMINATION_PLAYBOOK.md",
    "docs/revenue/OFFER_LADDER_V3.md",
    "docs/revenue/PROPOSAL_FACTORY_V3.md",
    "docs/finance/PAYMENT_CAPTURE_OS_V3.md",
    "docs/client_success/CLIENT_EXPANSION_OS.md",
    "docs/content/PROOF_TO_DEMAND_MACHINE.md",
    "docs/partners/PARTNER_ECOSYSTEM_OS_V3.md",
    "docs/agents/AGENT_GOVERNANCE_V3.md",
    "docs/evals/EVAL_CI_GATE.md",
    "docs/finance/COST_CONTROL_OS.md",
    "docs/finance/STRATEGIC_FINANCE_OS.md",
    "docs/founder/GOVERNANCE_BOARD_PACK_V3.md",
]

failures = []
for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 50:
        failures.append(f"Too short: {file}")

if failures:
    print("Company OS v3 verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: Company OS v3 is ready.")
