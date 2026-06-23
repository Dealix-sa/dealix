from pathlib import Path

required = [
 'controlled-preview/CONTROLLED_PREVIEW_MASTER_PLAN_AR.md',
 'controlled-preview/LAUNCH_WEEK_EXECUTION_AR.md',
 'controlled-preview/PREVIEW_EXIT_CRITERIA_AR.md',
 'merge-control/PR_MERGE_GATE_AR.md',
 'quality-gates/SERVICE_QUALITY_GATE_AR.md',
 'quality-gates/CLIENT_DELIVERY_ACCEPTANCE_GATE_AR.md',
 'data/preview/preview_clients.json',
 'scripts/dealix_controlled_preview_plan.py',
 'scripts/dealix_launch_week_command_center.py',
 'scripts/dealix_preview_quality_gate.py',
 '.github/workflows/dealix-v14-controlled-preview.yml'
]
missing=[p for p in required if not Path(p).exists()]
if missing:
    print('MISSING:')
    print('\n'.join(missing))
    raise SystemExit(1)
print('OK: Dealix V14 controlled preview execution files are present')
print(f'Checked: {len(required)} critical files')
