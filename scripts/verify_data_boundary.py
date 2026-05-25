from pathlib import Path

BLOCKED_PUBLIC_PATHS = [
    "dashboard_data/company_metrics.json",
    "dashboard_data/company_snapshot.json",
    "dashboard_data/revenue_metrics.json",
    "dashboard_data/trust_metrics.json",
]
BLOCKED_PATTERNS = [
    "api_key=",
    "secret_key=",
    "private_key",
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN RSA PRIVATE KEY",
]
SCAN_DIRS = [
    "docs/data",
    "schemas",
    "dealix_cli",
    "ops_runtime",
    "control_plane",
    "execution_engine",
]
SCRIPT_PATH = Path(__file__).resolve()

failures = []
for path_str in BLOCKED_PUBLIC_PATHS:
    path = Path(path_str)
    if path.exists():
        failures.append(f"Blocked public data file exists: {path_str}")

for folder in SCAN_DIRS:
    base = Path(folder)
    if not base.exists():
        continue
    for file in base.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix.lower() not in {".py", ".md", ".json", ".txt", ".yml", ".yaml"}:
            continue
        text = file.read_text(encoding="utf-8", errors="ignore").lower()
        for pattern in BLOCKED_PATTERNS:
            if pattern.lower() in text:
                failures.append(f"{file} contains blocked pattern: {pattern}")

# Also scan this verifier's directory (scripts) for our own boundary scripts
for file in Path("scripts").glob("verify_data_boundary*.py"):
    if file.resolve() == SCRIPT_PATH:
        continue
    text = file.read_text(encoding="utf-8", errors="ignore").lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern.lower() in text:
            failures.append(f"{file} contains blocked pattern: {pattern}")

if failures:
    print("Data boundary verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)
print("PASS: data boundary is clean.")
