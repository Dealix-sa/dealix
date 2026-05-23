import subprocess
from pathlib import Path

checks = [
    ["python", "scripts/verify_founder_frontend.py"],
    ["python", "scripts/verify_frontend_api_contract.py"],
]

failures = []
for cmd in checks:
    print("+", " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        failures.append("Failed: " + " ".join(cmd))

required_docs = [
    "docs/frontend/FOUNDER_INTERFACE_ARCHITECTURE.md",
    "docs/frontend/FOUNDER_INTERFACE_DATA_CONTRACT.md",
    "docs/api/FOUNDER_INTERNAL_API.md",
]

for doc in required_docs:
    path = Path(doc)
    if not path.exists():
        failures.append(f"Missing: {doc}")

if failures:
    print("Founder operating interface verification failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: founder operating interface is ready.")
