"""Verify the Dealix founder frontend layer exists and builds.

Fails the run if a required founder-facing route or library file is
missing, too small to be real, or if `npm ci` / `npm run build` fail in
``apps/web``.

This is the gate that the GitHub workflow
``dealix-founder-frontend.yml`` enforces.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

REQUIRED_ROUTES = [
    "apps/web/app/ceo/page.tsx",
    "apps/web/app/sales-cockpit/page.tsx",
    "apps/web/app/approvals/page.tsx",
    "apps/web/app/distribution/page.tsx",
    "apps/web/app/workers/page.tsx",
    "apps/web/app/trust/page.tsx",
    "apps/web/app/finance/page.tsx",
    "apps/web/lib/dealix-api.ts",
]


def main() -> None:
    failures: list[str] = []

    for route in REQUIRED_ROUTES:
        path = Path(route)
        if not path.exists():
            failures.append(f"Missing: {route}")
        elif path.stat().st_size < 80:
            failures.append(f"Too small: {route}")

    app = Path("apps/web")
    if not (app / "package.json").exists():
        failures.append("Missing apps/web/package.json")

    if failures:
        print("Founder frontend verification failed:")
        for f in failures:
            print("-", f)
        raise SystemExit(1)

    install_cmd = (
        ["npm", "ci"] if (app / "package-lock.json").exists() else ["npm", "install"]
    )
    for cmd in (install_cmd, ["npm", "run", "build"]):
        print("+", " ".join(cmd))
        result = subprocess.run(cmd, cwd=app)
        if result.returncode != 0:
            raise SystemExit(f"Failed: {' '.join(cmd)}")

    print("PASS: founder frontend exists and builds.")


if __name__ == "__main__":
    main()
