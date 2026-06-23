from pathlib import Path

required = [
 'founder-autopilot/FOUNDER_DAILY_AUTOPILOT_AR.md',
 'founder-autopilot/DAILY_COMMAND_BRIEF_SYSTEM_AR.md',
 'data/founder/founder_tasks.json',
 'data/founder/daily_decision_rules.json',
 'templates/founder/daily_command_brief_template.md',
 'scripts/dealix_founder_command_brief.py',
 'scripts/dealix_top10_task_ranker.py',
 'scripts/dealix_daily_artifact_generator.py',
 'scripts/dealix_founder_autopilot_dashboard.py',
 '.github/workflows/dealix-v15-founder-autopilot.yml'
]
missing=[p for p in required if not Path(p).exists()]
if missing:
    print('MISSING:')
    for p in missing: print('-', p)
    raise SystemExit(1)
print('OK: Dealix V15 founder daily execution autopilot files are present')
print(f'Checked: {len(required)} critical files')
