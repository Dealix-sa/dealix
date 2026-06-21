import subprocess
for cmd in [
 ['python','scripts/dealix_v12_readiness_check.py'],
 ['python','scripts/dealix_weekly_operating_rhythm.py'],
 ['python','scripts/dealix_client_portfolio_review.py'],
 ['python','scripts/dealix_automation_backlog_ranker.py'],
 ['python','scripts/dealix_partner_quota_dashboard.py'],
 ['python','scripts/dealix_scale_dashboard.py'],
]:
    print('\n$',' '.join(cmd))
    subprocess.run(cmd, check=True)
