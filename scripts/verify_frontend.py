"""Verify the Dealix Founder Next.js app (apps/web) builds cleanly.

Runs `npm ci` (or `npm install`) + `npm run build` in apps/web and exits non-zero
on any failure. This is the F1 gate of the Frontend Certification System
(see docs/frontend/FRONTEND_CERTIFICATION_SYSTEM.md).

Usage:
    python3 scripts/verify_frontend.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FRONTENDS = [REPO_ROOT / "apps" / "web"]


def _run(cmd: list[str], cwd: Path) -> bool:
    print(f"+ ({cwd.relative_to(REPO_ROOT)}) {' '.join(cmd)}", flush=True)
    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode == 0


def main() -> int:
    if not shutil.which("npm"):
        print("FAIL: npm not found on PATH. Install Node.js 20+ first.")
        return 1

    failures: list[str] = []
    for app in FRONTENDS:
        if not app.exists():
            failures.append(f"missing frontend app: {app.relative_to(REPO_ROOT)}")
            continue
        if not (app / "package.json").exists():
            failures.append(f"missing package.json in {app.relative_to(REPO_ROOT)}")
            continue

        install_cmd = ["npm", "ci"] if (app / "package-lock.json").exists() else ["npm", "install"]
        if not _run(install_cmd, app):
            failures.append(f"install failed in {app.relative_to(REPO_ROOT)}")
            continue
        if not _run(["npm", "run", "build"], app):
            failures.append(f"build failed in {app.relative_to(REPO_ROOT)}")

    if failures:
        print("FAIL: Frontend verification failed:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("PASS: Frontend builds successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
