import os
import subprocess
from pathlib import Path

required_routes = [
    "apps/web/app/ceo/page.tsx",
    "apps/web/app/sales-cockpit/page.tsx",
    "apps/web/app/approvals/page.tsx",
    "apps/web/app/distribution/page.tsx",
    "apps/web/app/workers/page.tsx",
    "apps/web/app/trust/page.tsx",
    "apps/web/app/finance/page.tsx",
]

failures = []
for route in required_routes:
    path = Path(route)
    if not path.exists():
        failures.append(f"Missing route: {route}")
    elif path.stat().st_size < 100:
        failures.append(f"Route too small: {route}")

app = Path("apps/web")
if not (app / "package.json").exists():
    failures.append("Missing apps/web/package.json")

if failures:
    print("Founder frontend route verification failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

if os.environ.get("SKIP_FOUNDER_FRONTEND_BUILD") == "1":
    print("PASS (routes only): founder frontend files present. Build skipped.")
    raise SystemExit(0)

cmds: list[list[str]] = []
if (app / "package-lock.json").exists():
    cmds.append(["npm", "ci"])
else:
    cmds.append(["npm", "install"])
cmds.append(["npm", "run", "build"])

for cmd in cmds:
    print("+", " ".join(cmd))
    result = subprocess.run(cmd, cwd=app)
    if result.returncode != 0:
        raise SystemExit(f"Failed: {' '.join(cmd)}")

print("PASS: founder frontend exists and builds.")
