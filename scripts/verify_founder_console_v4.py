"""Founder Console v4 verifier — static + frontend build gate."""

from __future__ import annotations

import subprocess
from pathlib import Path

required = [
    "docs/frontend/FOUNDER_CONSOLE_V4_LIVE_RUNTIME.md",
    "docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md",
    "docs/trust/FOUNDER_CONSOLE_POLICY_ENFORCEMENT_V4.md",
    "api/internal/runtime_reader.py",
    "api/routers/internal/founder_console.py",
    "apps/web/components/founder-shell.tsx",
    "apps/web/lib/dealix-runtime.ts",
    "apps/web/lib/dealix-actions.ts",
    "apps/web/app/ceo/page.tsx",
    "apps/web/app/sales-cockpit/page.tsx",
    "apps/web/app/approvals/page.tsx",
]

failures: list[str] = []

for item in required:
    p = Path(item)
    if not p.exists():
        failures.append(f"Missing: {item}")
    elif p.stat().st_size < 80:
        failures.append(f"Too small: {item}")

router = Path("api/routers/internal/founder_console.py")
if router.exists():
    text = router.read_text(encoding="utf-8", errors="ignore")
    for phrase in [
        "append_csv",
        "approval_decisions.csv",
        "ALLOW_AFTER_APPROVAL",
        "/ceo/summary",
        "/sales/funnel",
        "/approvals",
    ]:
        if phrase not in text:
            failures.append(f"Router missing live/audit phrase: {phrase}")

reader = Path("api/internal/runtime_reader.py")
if reader.exists():
    text = reader.read_text(encoding="utf-8", errors="ignore")
    for phrase in [
        "lead_intelligence_base.csv",
        "outreach_queue.csv",
        "conversation_log.csv",
        "payment_capture_queue.csv",
        "ceo_summary",
        "sales_funnel_summary",
    ]:
        if phrase not in text:
            failures.append(f"Runtime reader missing phrase: {phrase}")

if failures:
    print("Founder Console v4 verification failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

app = Path("apps/web")
cmds = [
    ["npm", "ci"] if (app / "package-lock.json").exists() else ["npm", "install"],
    ["npm", "run", "build"],
]
for cmd in cmds:
    print("+", " ".join(cmd))
    result = subprocess.run(cmd, cwd=app)
    if result.returncode != 0:
        raise SystemExit(f"Failed: {' '.join(cmd)}")

print("PASS: Founder Console v4 live runtime layer is ready.")
