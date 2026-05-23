from pathlib import Path

required = [
    "docs/frontend/FOUNDER_INTERFACE_DATA_CONTRACT.md",
    "docs/api/FOUNDER_INTERNAL_API.md",
    "apps/web/lib/dealix-api.ts",
    "api/routers/internal_ceo.py",
]

required_endpoints = [
    "/api/v1/internal/ceo/summary",
    "/api/v1/internal/sales/funnel",
    "/api/v1/internal/approvals",
    "/api/v1/internal/workers/health",
    "/api/v1/internal/trust/flags",
    "/api/v1/internal/finance/summary",
]

failures = []
for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 50:
        failures.append(f"Too short: {file}")

api_doc = Path("docs/api/FOUNDER_INTERNAL_API.md")
if api_doc.exists():
    text = api_doc.read_text(encoding="utf-8")
    for endpoint in required_endpoints:
        if endpoint not in text:
            failures.append(f"Endpoint missing from contract: {endpoint}")

if failures:
    print("Frontend/API contract verification failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: frontend/API contract is consistent.")
