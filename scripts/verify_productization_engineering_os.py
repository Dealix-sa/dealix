from pathlib import Path

required = [
    "docs/product/PRODUCTIZATION_ENGINEERING_OS.md",
    "docs/product/PRODUCTIZATION_DECISION_SYSTEM.md",
    "docs/engineering/ENGINEERING_ARCHITECTURE.md",
    "docs/engineering/ENGINEERING_QUALITY_SYSTEM.md",
    "docs/automation/AUTOMATION_PERMISSION_MATRIX.md",
    "docs/agents/AGENT_READINESS_SYSTEM.md",
    "docs/agents/AGENT_REGISTRY.md",
    "ops_runtime/productization_scorer.py",
    "scripts/generate_productization_review.py",
    "docs/product/SAAS_ARCHITECTURE_GATE.md",
    "docs/product/FUTURE_SAAS_REPO_STRUCTURE.md",
    "docs/engineering/RELEASE_MANAGEMENT_SYSTEM.md",
    "docs/engineering/OBSERVABILITY_SYSTEM.md",
]

failures = []
for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 100:
        failures.append(f"Too short: {file}")

if failures:
    print("Productization & Engineering OS verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: Productization & Engineering OS is ready.")
