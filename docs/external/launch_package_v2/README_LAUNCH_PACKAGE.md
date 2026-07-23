# Dealix Launch Package — 2026-06-07

This package adds a practical launch layer on top of Dealix:

- Website conversion blueprint
- Public offer packages
- Custom AI Systems page
- Daily prospecting OS
- Approval-first prospect draft generator
- Launch readiness checker
- Static Arabic landing page
- GitHub Actions workflow for daily growth queue

## Merge
Copy the folders into the repository root:

```bash
cp -R docs sales marketing data scripts landing frontend .github /path/to/dealix/
cd /path/to/dealix
python scripts/dealix_launch_readiness_check.py
python scripts/dealix_daily_prospect_drafts.py
```

## Git commands

```bash
git checkout -b feat/launch-website-growth-os-2026-06-07
git add docs/launch data/prospects scripts landing frontend/src/app .github/workflows
python scripts/dealix_launch_readiness_check.py
python scripts/dealix_daily_prospect_drafts.py
git commit -m "feat(launch): add website growth OS and daily prospecting workflow"
git push -u origin feat/launch-website-growth-os-2026-06-07
```

## Operating rule
The prospecting script creates drafts only. It never sends messages.
