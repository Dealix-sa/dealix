from pathlib import Path

required = [
    "docs/founder/BOARD_LEVEL_OPERATING_SYSTEM.md",
    "scripts/generate_board_pack.py",
    "docs/finance/DEFAULT_ALIVE_SYSTEM.md",
    "control_plane/strategic_decision_engine.py",
    "scripts/generate_strategic_decision_report.py",
    "docs/ops/CEO_MANAGEMENT_SYSTEM.md",
]

failures = []
for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 150:
        failures.append(f"Too short: {file}")

if failures:
    print("Board-level OS verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: Board-level OS is ready.")
