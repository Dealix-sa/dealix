from pathlib import Path

required = [
    "docs/acquisition/DONE_FOR_YOU_ACQUISITION_OS.md",
    "docs/acquisition/LEAD_OUTREACH_AUTOPILOT_OS.md",
    "docs/acquisition/AUTOPILOT_EXECUTION_RULES.md",
    "docs/acquisition/GMAIL_DRAFT_WORKFLOW.md",
    "scripts/bootstrap_lead_sources.py",
    "scripts/create_research_queue.py",
    "scripts/build_lead_batch_from_research.py",
    "scripts/build_outreach_send_queue.py",
    "scripts/schedule_followups_from_sent.py",
    "scripts/route_replies.py",
    "scripts/generate_sample_tasks_from_replies.py",
    "scripts/generate_acquisition_daily_report.py",
]

failures = []
for file in required:
    p = Path(file)
    if not p.exists():
        failures.append(f"Missing: {file}")
    elif p.stat().st_size < 50:
        failures.append(f"Too short: {file}")

if failures:
    print("Acquisition autopilot verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: acquisition autopilot is ready.")
