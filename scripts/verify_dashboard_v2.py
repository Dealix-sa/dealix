from pathlib import Path
import json

required = [
    "internal_dashboard/ceo_dashboard_v2.html",
    "dashboard_data/demo/company_metrics.v2.demo.json",
    "docs/dashboard/CEO_DASHBOARD_V2.md",
    "ops_runtime/alerts_generator.py",
    "ops_runtime/target_scoring.py",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size == 0:
        failures.append(f"Empty: {file}")

demo_json = Path("dashboard_data/demo/company_metrics.v2.demo.json")
if demo_json.exists():
    try:
        data = json.loads(demo_json.read_text(encoding="utf-8"))
        for key in ["summary", "metrics", "targets", "target_status", "alerts", "bottlenecks", "decisions"]:
            if key not in data:
                failures.append(f"Demo v2 JSON missing {key}")
    except Exception as exc:
        failures.append(f"Invalid dashboard v2 demo JSON: {exc}")

html = Path("internal_dashboard/ceo_dashboard_v2.html")
if html.exists():
    text = html.read_text(encoding="utf-8", errors="ignore")
    for term in ["Dealix CEO Command Center", "Founder Focus", "Target Completion", "Decision Queue", "Bottlenecks"]:
        if term not in text:
            failures.append(f"Dashboard v2 HTML missing: {term}")

if failures:
    print("Dashboard v2 verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: CEO dashboard v2 files are valid.")
