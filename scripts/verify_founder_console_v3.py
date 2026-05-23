"""
Founder Console v3 verifier.

Static checks:
- required files exist
- internal router exposes the expected endpoints

Optional build check (default on, disable with --skip-build):
- apps/web installs and builds with Next.js
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "docs/frontend/FOUNDER_CONSOLE_V3.md",
    "docs/frontend/FOUNDER_CONSOLE_ARCHITECTURE_V3.md",
    "docs/frontend/FOUNDER_CONSOLE_PRODUCTION_READINESS.md",
    "docs/trust/APPROVAL_AUDIT_LOG_CONTRACT.md",
    "docs/trust/FOUNDER_CONSOLE_TRUST_GATE.md",
    "api/routers/internal/__init__.py",
    "api/routers/internal/founder_console.py",
    "apps/web/components/founder-shell.tsx",
    "apps/web/lib/dealix-runtime.ts",
    "apps/web/lib/dealix-actions.ts",
    "apps/web/app/ceo/page.tsx",
    "apps/web/app/sales-cockpit/page.tsx",
    "apps/web/app/approvals/page.tsx",
    "apps/web/app/workers/page.tsx",
    "apps/web/app/trust/page.tsx",
    "apps/web/app/finance/page.tsx",
    "apps/web/app/distribution/page.tsx",
    "apps/web/app/delivery/page.tsx",
    "apps/web/app/retention/page.tsx",
    "apps/web/app/proof/page.tsx",
]

REQUIRED_ENDPOINTS = [
    "/ceo/summary",
    "/sales/funnel",
    "/approvals",
    "/workers/health",
    "/trust/flags",
    "/finance/summary",
    "/distribution/summary",
    "/delivery/queue",
    "/retention/queue",
    "/proof/library",
    "/approvals/{approval_id}/approve",
    "/approvals/{approval_id}/reject",
    "/approvals/{approval_id}/request-edit",
]


def check_static() -> list[str]:
    failures: list[str] = []
    for rel in REQUIRED_FILES:
        path = REPO_ROOT / rel
        if not path.exists():
            failures.append(f"Missing: {rel}")
            continue
        # __init__.py is allowed to be tiny; everything else must have content.
        if path.name == "__init__.py":
            continue
        if path.stat().st_size < 50:
            failures.append(f"Too small: {rel}")

    router = REPO_ROOT / "api/routers/internal/founder_console.py"
    if router.exists():
        text = router.read_text(encoding="utf-8", errors="ignore")
        for endpoint in REQUIRED_ENDPOINTS:
            if endpoint not in text:
                failures.append(f"Router missing endpoint: {endpoint}")

    main = REPO_ROOT / "api/main.py"
    if main.exists():
        text = main.read_text(encoding="utf-8", errors="ignore")
        if "founder_console_v3_router" not in text:
            failures.append("api/main.py does not register founder_console_v3_router")

    return failures


def run_build() -> list[str]:
    failures: list[str] = []
    app = REPO_ROOT / "apps/web"
    if not shutil.which("npm"):
        failures.append("npm not installed; skip --skip-build or install Node.js")
        return failures
    install_cmd = ["npm", "ci"] if (app / "package-lock.json").exists() else ["npm", "install"]
    for cmd in (install_cmd, ["npm", "run", "build"]):
        print("+", " ".join(cmd), flush=True)
        result = subprocess.run(cmd, cwd=app)
        if result.returncode != 0:
            failures.append(f"Failed: {' '.join(cmd)}")
            break
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip the apps/web install + build step (static check only).",
    )
    args = parser.parse_args()

    failures = check_static()
    if failures:
        print("Founder Console v3 static verification failed:")
        for f in failures:
            print("-", f)
        return 1
    print("PASS: Founder Console v3 static files and endpoints present.")

    if args.skip_build:
        print("Skipped apps/web build (--skip-build).")
        return 0

    build_failures = run_build()
    if build_failures:
        print("Founder Console v3 build failed:")
        for f in build_failures:
            print("-", f)
        return 1
    print("PASS: Founder Console v3 builds.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
