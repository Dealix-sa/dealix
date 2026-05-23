from pathlib import Path
import json

path = Path("dashboard_data/demo/targets.demo.json")

if not path.exists():
    raise SystemExit("Missing dashboard_data/demo/targets.demo.json")

data = json.loads(path.read_text(encoding="utf-8"))

if "weekly" not in data:
    raise SystemExit("Targets missing weekly section")

if "monthly" not in data:
    raise SystemExit("Targets missing monthly section")

required_weekly = ["lead_count", "contacted", "replied", "call_booked", "proposal_sent", "sample_sent"]

for key in required_weekly:
    if key not in data["weekly"]:
        raise SystemExit(f"Weekly targets missing {key}")

print("PASS: dashboard targets are valid.")
