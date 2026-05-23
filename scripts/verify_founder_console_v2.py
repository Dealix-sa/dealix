"""Verify Founder Console v2 is wired end-to-end.

This script enforces production gate **F1 + F2 + F3 + F4** from
``docs/frontend/FOUNDER_CONSOLE_PRODUCTION_GATE.md``:

- All required files exist and are non-trivial.
- The 10 founder pages exist under ``apps/web/app``.
- The internal router, runtime client, and action client exist.
- ``apps/web`` ``npm run build`` succeeds.

Run from anywhere — the script anchors paths to the repository root.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


REQUIRED_FILES = [
    "docs/frontend/FOUNDER_CONSOLE_V1.md",
    "docs/frontend/APPROVAL_ACTION_FLOW.md",
    "docs/frontend/FOUNDER_CONSOLE_PRODUCTION_GATE.md",
    "docs/runtime/FOUNDER_CONSOLE_SOURCE_OF_TRUTH.md",
    "docs/api/INTERNAL_API_LAYER_V1.md",
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


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        path = repo / rel
        if not path.exists():
            failures.append(f"Missing: {rel}")
        elif path.stat().st_size < 50:
            failures.append(f"Too small: {rel}")

    if failures:
        print("Founder Console v2 verification failed:")
        for failure in failures:
            print("-", failure)
        return 1

    app = repo / "apps" / "web"
    install_cmd = (
        ["npm", "ci"] if (app / "package-lock.json").exists() else ["npm", "install"]
    )
    cmds = [install_cmd, ["npm", "run", "build"]]
    for cmd in cmds:
        print("+", " ".join(cmd))
        result = subprocess.run(cmd, cwd=app)
        if result.returncode != 0:
            print(f"FAIL: {' '.join(cmd)}")
            return result.returncode

    print("PASS: Founder Console v2 is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
