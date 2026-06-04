#!/usr/bin/env python3
"""Static checks for the read-only Commercial Launch API surface.

Without importing the FastAPI app, verify:
- a /health (or /healthz) endpoint exists in the API,
- the commercial-launch read-only router exists and uses GET only,
- that router has no send endpoints and no outbound-send imports,
- the router exposes the expected read-only endpoints.

Writes outputs/api/<date>/api_commercial_qa.json.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import OUTPUTS_DIR, ROOT, today_str, write_json

API = ROOT / "api"
READONLY_ROUTER = API / "routers" / "commercial_launch_readonly.py"

EXPECTED_ENDPOINTS = [
    "/verticals",
    "/offers",
    "/readiness",
    "/channel-policy",
    "/metrics-schema",
    "/calendar-schema",
]

OUTBOUND_IMPORTS = [
    r"import\s+smtplib",
    r"from\s+smtplib",
    r"\bsendgrid\b",
    r"\bmailgun\b",
    r"\bpostmark\b",
    r"twilio",
    r"\.send_email\(",
    r"\.send_mail\(",
]

SEND_ROUTE = re.compile(r"@\w+\.(post|put|patch|delete)\(", re.IGNORECASE)
# Only a *route decorator* whose path implies sending/submitting is a violation.
SEND_PATH = re.compile(
    r'@\w+\.(get|post)\(\s*["\'][^"\']*(send|outreach|whatsapp|/submit|push[-_]?send)',
    re.IGNORECASE,
)


def run(day: str) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if not API.exists():
        return {
            "date": day,
            "passed": True,
            "skipped": True,
            "note": "no api/ directory",
            "errors": [],
            "warnings": [],
        }

    # 1. /health endpoint exists somewhere.
    health_found = False
    for path in list(API.glob("main.py")) + list((API / "routers").glob("*.py")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "/health" in text or "/healthz" in text:
            health_found = True
            break
    if not health_found:
        errors.append("no /health or /healthz endpoint found in api/")

    # 2. Read-only router exists.
    if not READONLY_ROUTER.exists():
        errors.append("missing api/routers/commercial_launch_readonly.py")
        return {
            "date": day,
            "passed": False,
            "skipped": False,
            "errors": errors,
            "warnings": warnings,
        }

    rtext = READONLY_ROUTER.read_text(encoding="utf-8", errors="ignore")

    # 3. GET-only (no write verbs).
    write_routes = SEND_ROUTE.findall(rtext)
    if write_routes:
        errors.append(f"read-only router has write routes: {write_routes}")

    # 4. No send-style paths.
    if SEND_PATH.search(rtext):
        errors.append("read-only router has a send/submit-style path")

    # 5. No outbound imports.
    for pat in OUTBOUND_IMPORTS:
        if re.search(pat, rtext, re.IGNORECASE):
            errors.append(f"read-only router has outbound import: {pat}")

    # 6. Expected endpoints present.
    for ep in EXPECTED_ENDPOINTS:
        if ep not in rtext:
            errors.append(f"missing read-only endpoint: {ep}")

    passed = not errors
    return {
        "date": day,
        "passed": passed,
        "skipped": False,
        "health_endpoint": health_found,
        "endpoints_expected": EXPECTED_ENDPOINTS,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Static commercial API checks.")
    parser.add_argument("--date", default=today_str())
    args = parser.parse_args()

    report = run(args.date)
    out = OUTPUTS_DIR / "api" / args.date / "api_commercial_qa.json"
    write_json(out, report)

    if report.get("skipped"):
        print("API COMMERCIAL CHECK: SKIPPED (no api/).")
        return 0
    if report["passed"]:
        print("API COMMERCIAL CHECK: PASS — /health present, read-only, no send endpoints.")
        return 0
    print("API COMMERCIAL CHECK: FAIL", file=sys.stderr)
    for e in report["errors"]:
        print(f"  - {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
