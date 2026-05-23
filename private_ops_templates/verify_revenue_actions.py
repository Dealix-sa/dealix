from pathlib import Path
import csv

path = Path("revenue/revenue_action_log.csv")

if not path.exists():
    raise SystemExit("Missing revenue/revenue_action_log.csv")

required_headers = [
    "date",
    "lead_or_client",
    "action",
    "type",
    "status",
    "next_action",
    "evidence",
]

with path.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames or []
    rows = list(reader)

for header in required_headers:
    if header not in fieldnames:
        raise SystemExit(f"Missing revenue action header: {header}")

print(f"Revenue actions: {len(rows)}")
print("PASS: revenue action log is valid.")
