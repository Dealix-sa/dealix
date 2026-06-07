import subprocess, sys
cmds=[
 ['python','scripts/dealix_v14_readiness_check.py'],
 ['python','scripts/dealix_controlled_preview_plan.py'],
 ['python','scripts/dealix_launch_week_command_center.py'],
 ['python','scripts/dealix_preview_quality_gate.py'],
 ['python','scripts/dealix_post_launch_review.py'],
]
for cmd in cmds:
    print('\n$',' '.join(cmd))
    r=subprocess.run(cmd)
    if r.returncode!=0: sys.exit(r.returncode)
