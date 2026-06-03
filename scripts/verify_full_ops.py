import subprocess
import sys
from pathlib import Path

CHECKS = [
    ["python", "scripts/verify_master_tree.py"],
    ["python", "scripts/verify_document_quality.py"],
    ["python", "scripts/verify_company_os_deep.py"],
]

OPTIONAL_CHECKS = [
    ["python", "scripts/verify_public_safety.py"],
    ["python", "scripts/verify_private_boundary.py"],
]

failed = []

for cmd in CHECKS:
    print(f"\n== Running: {' '.join(cmd)} ==")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        failed.append(" ".join(cmd))

for cmd in OPTIONAL_CHECKS:
    if Path(cmd[1]).exists():
        print(f"\n== Running: {' '.join(cmd)} ==")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            failed.append(" ".join(cmd))

if failed:
    print("\nFAILED CHECKS:")
    for item in failed:
        print("-", item)
    sys.exit(1)

print("\nPASS: Dealix full ops verification passed.")
