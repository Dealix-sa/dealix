"""Verify the entire Dealix Founder Operating Layer is wired up.

Checks:

1. Founder doctrine, API contract, and runtime bindings docs exist.
2. The founder frontend exists and builds
   (delegates to ``scripts/verify_founder_frontend.py``).

Exits non-zero on the first failed check with a punch-list of what is
missing.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

DOCS = [
    "docs/founder/FOUNDER_COMMAND_LAYER.md",
    "docs/api/FOUNDER_INTERFACE_API_CONTRACT.md",
    "docs/runtime/FOUNDER_FRONTEND_RUNTIME_BINDINGS.md",
]

CHECKS = [
    ["python", "scripts/verify_founder_frontend.py"],
]


def main() -> None:
    failures: list[str] = []

    for doc in DOCS:
        path = Path(doc)
        if not path.exists():
            failures.append(f"Missing: {doc}")
        elif path.stat().st_size < 100:
            failures.append(f"Too small: {doc}")

    for cmd in CHECKS:
        print("+", " ".join(cmd))
        result = subprocess.run(cmd)
        if result.returncode != 0:
            failures.append("Failed: " + " ".join(cmd))

    if failures:
        print("Founder operating layer verification failed:")
        for f in failures:
            print("-", f)
        raise SystemExit(1)

    print("PASS: founder operating layer is ready.")


if __name__ == "__main__":
    main()
