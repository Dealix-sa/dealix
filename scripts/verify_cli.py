from pathlib import Path
import subprocess
import sys

required = [
    "dealix_cli/__init__.py",
    "dealix_cli/__main__.py",
    "dealix_cli/commands.py",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size == 0:
        failures.append(f"Empty: {file}")

if failures:
    print("CLI verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

result = subprocess.run(
    [sys.executable, "-m", "dealix_cli", "--help"],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    print(result.stdout)
    print(result.stderr)
    raise SystemExit("CLI help command failed")

for term in ["daily", "weekly", "dashboard", "verify"]:
    if term not in result.stdout:
        raise SystemExit(f"CLI help missing command: {term}")

print("PASS: Dealix CLI is valid.")
