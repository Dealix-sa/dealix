from pathlib import Path
import json

required = [
    "internal_dashboard/ceo_dashboard.html",
    "dashboard_data/demo/company_metrics.demo.json",
    "docs/dashboard/CEO_DASHBOARD_DATA_MODEL.md",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size == 0:
        failures.append(f"Empty: {file}")

demo_json = Path("dashboard_data/demo/company_metrics.demo.json")
if demo_json.exists():
    try:
        data = json.loads(demo_json.read_text(encoding="utf-8"))
        if "metrics" not in data:
            failures.append("Demo dashboard JSON missing metrics")
        if "bottlenecks" not in data:
            failures.append("Demo dashboard JSON missing bottlenecks")
    except Exception as exc:
        failures.append(f"Invalid dashboard demo JSON: {exc}")

html = Path("internal_dashboard/ceo_dashboard.html")
if html.exists():
    text = html.read_text(encoding="utf-8", errors="ignore")
    for term in ["Dealix CEO Dashboard", "Bottlenecks", "Operating Rule"]:
        if term not in text:
            failures.append(f"Dashboard HTML missing: {term}")

if failures:
    print("Dashboard verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: CEO dashboard files are valid.")
