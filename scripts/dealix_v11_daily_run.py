import subprocess

cmds=[
 ['python','scripts/dealix_v11_readiness_check.py'],
 ['python','scripts/dealix_first_revenue_sprint.py'],
 ['python','scripts/dealix_revenue_dashboard.py'],
]
for c in cmds:
    print('RUN',' '.join(c))
    subprocess.check_call(c)
