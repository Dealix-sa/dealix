from pathlib import Path

required = [
    "docs/control_plane/DEALIX_CONTROL_TOWER.md",
    "control_plane/control_tower.py",
    "scripts/generate_control_tower_brief.py",
    "docs/founder/MASTER_DAILY_CEO_LOOP.md",
    "docs/founder/MASTER_WEEKLY_CEO_LOOP.md",
    "docs/strategy/STRATEGIC_THEMES.md",
    "docs/strategy/OKR_SYSTEM.md",
    "docs/content/CUSTOMER_PROOF_SYSTEM.md",
    "docs/client_success/RETENTION_SYSTEM.md",
    "docs/strategy/COMPETITIVE_MOAT_SYSTEM.md",
    "docs/revenue/PRICING_POWER_SYSTEM.md",
    "docs/ops/CAPACITY_PLANNING_SYSTEM.md",
]

failures = []
for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 200:
        failures.append(f"Too short: {file}")

if failures:
    print("CEO Operating Intelligence v4 verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: CEO Operating Intelligence v4 is ready.")
