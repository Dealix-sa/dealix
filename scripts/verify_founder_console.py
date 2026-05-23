#!/usr/bin/env python3
"""Verify Dealix Founder Console v1 — files, backend wiring, frontend build.

Checks performed:
  1. Required files exist and have non-trivial size.
  2. The existing `/approvals` page still mounts `OversightQueue` and
     `ApprovalDecisionModal` (regression guard for the FounderShell wrap).
  3. `api.main` imports cleanly and registers the internal founder router
     so that all 7 endpoints appear under `/api/v1/internal/founder/*`.
  4. `npm ci` + `npm run build` succeed inside `apps/web/`.

Exits 0 on success, 1 with a bulleted FAILURES list otherwise.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

FAILURES: list[str] = []


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  FAIL: {msg}")


REQUIRED_FILES: tuple[str, ...] = (
    # docs
    "docs/frontend/FOUNDER_CONSOLE_V1.md",
    "docs/api/INTERNAL_FOUNDER_API_V1.md",
    "docs/runtime/FOUNDER_CONSOLE_RUNTIME_BINDING_PLAN.md",
    # frontend shell + adapter
    "apps/web/components/founder-shell.tsx",
    "apps/web/lib/dealix-runtime.ts",
    "apps/web/app/globals.css",
    "apps/web/package.json",
    # 10 founder console pages
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
    # backend router
    "api/routers/internal/__init__.py",
    "api/routers/internal/founder.py",
    # CI
    ".github/workflows/dealix-founder-console.yml",
)

EXPECTED_INTERNAL_ROUTES: tuple[str, ...] = (
    "/api/v1/internal/founder/ceo/summary",
    "/api/v1/internal/founder/sales/funnel",
    "/api/v1/internal/founder/approvals",
    "/api/v1/internal/founder/workers/health",
    "/api/v1/internal/founder/trust/flags",
    "/api/v1/internal/founder/finance/summary",
    "/api/v1/internal/founder/distribution/summary",
)


def check_files() -> None:
    print("\n[1] required files exist")
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            fail(f"missing file: {rel}")
            continue
        size = path.stat().st_size
        # __init__.py is allowed to be empty; everything else must be substantive
        if rel.endswith("__init__.py"):
            ok(f"{rel} ({size}B)")
            continue
        if size < 80:
            fail(f"file too small ({size}B): {rel}")
        else:
            ok(f"{rel} ({size}B)")


def check_approvals_regression_guard() -> None:
    print("\n[2] /approvals page regression guard")
    page = ROOT / "apps/web/app/approvals/page.tsx"
    if not page.exists():
        fail("apps/web/app/approvals/page.tsx missing")
        return
    body = page.read_text(encoding="utf-8")
    for needle in ("OversightQueue", "ApprovalDecisionModal", "FounderShell"):
        if needle not in body:
            fail(f"approvals page is missing reference to {needle}")
        else:
            ok(f"approvals page references {needle}")


def check_backend_router() -> None:
    print("\n[3] backend router registration")
    try:
        from api.main import create_app
    except Exception as exc:  # noqa: BLE001
        fail(f"api.main import failed: {exc!r}")
        return
    try:
        app = create_app()
    except Exception as exc:  # noqa: BLE001
        fail(f"create_app() failed: {exc!r}")
        return
    registered = {getattr(r, "path", "") for r in app.routes}
    for expected in EXPECTED_INTERNAL_ROUTES:
        if expected in registered:
            ok(f"route registered: {expected}")
        else:
            fail(f"route NOT registered: {expected}")


def check_frontend_build() -> None:
    print("\n[4] frontend npm ci + npm run build")
    if "--skip-build" in sys.argv:
        ok("skipped (--skip-build)")
        return
    npm = shutil.which("npm")
    if npm is None:
        fail("npm not found on PATH — install Node 20+ to run the frontend build check")
        return
    web = ROOT / "apps" / "web"
    lock = web / "package-lock.json"
    install_cmd = [npm, "ci"] if lock.exists() else [npm, "install"]
    for cmd in (install_cmd, [npm, "run", "build"]):
        printable = " ".join(cmd)
        print(f"  $ {printable}  (cwd={web})")
        result = subprocess.run(cmd, cwd=web)
        if result.returncode != 0:
            fail(f"command failed: {printable}")
            return
        ok(printable)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip the npm ci + npm run build step (use when Node is not installed).",
    )
    parser.parse_args()

    print("Dealix Founder Console v1 — verification")
    print(f"  repo: {ROOT}")

    check_files()
    check_approvals_regression_guard()
    check_backend_router()
    check_frontend_build()

    print()
    if FAILURES:
        print("Founder Console verification FAILED:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("PASS: Founder Console v1 ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
