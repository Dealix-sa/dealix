import subprocess, sys
cmds=[
 ['scripts/dealix_v15_readiness_check.py'],
 ['scripts/dealix_top10_task_ranker.py'],
 ['scripts/dealix_founder_command_brief.py'],
 ['scripts/dealix_daily_artifact_generator.py'],
 ['scripts/dealix_founder_autopilot_dashboard.py'],
]
for c in cmds:
    subprocess.run([sys.executable]+c, check=True)
