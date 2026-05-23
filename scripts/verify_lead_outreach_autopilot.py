from pathlib import Path

required = [
    "docs/acquisition/LEAD_OUTREACH_AUTOPILOT_OS.md",
    "docs/acquisition/AUTOPILOT_EXECUTION_RULES.md",
    "schemas/lead_batch.schema.json",
    "scripts/create_lead_batch_template.py",
    "scripts/score_lead_batch.py",
    "scripts/generate_outreach_for_batch.py",
    "scripts/generate_outreach_approval_queue.py",
    "scripts/export_approved_leads_to_pipeline.py",
]

failures = []
for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 50:
        failures.append(f"Too short: {file}")

if failures:
    print("Lead Outreach Autopilot verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: Lead Outreach Autopilot is ready.")
