from pathlib import Path
required = [
    "docs/control_plane/ENTERPRISE_CONTROL_ARCHITECTURE.md",
    "docs/ops/ENTERPRISE_SYSTEM_REGISTRY.md",
    "docs/founder/CEO_AUDIT_TRAIL_SYSTEM.md",
    "docs/learning/COMPANY_MEMORY_SYSTEM.md",
    "docs/customer_intelligence/CUSTOMER_INTELLIGENCE_SYSTEM.md",
    "docs/strategy/MARKET_EXPERIMENT_SYSTEM.md",
    "docs/finance/REVENUE_FORECAST_SYSTEM.md",
    "control_plane/risk_alerts.py",
]
failures = []
for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 120:
        failures.append(f"Too short: {file}")
if failures:
    print("Enterprise operating expansion verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)
print("PASS: enterprise operating expansion is ready.")
