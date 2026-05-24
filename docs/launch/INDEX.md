# Launch / Marketing — Surface Index

Read-only index for the launch + marketing surface. This file exists so
`scripts/verify_marketing_system.py` can confirm the surface is wired.

## Canonical artifacts

- `scripts/generate_launch_report.py` — produces a launch readiness report.
- `scripts/generate_weekly_content_drafts.py` — weekly_content drafts
  routed through the existing approval flow.
- `.github/workflows/weekly-founder-content.yml` — weekly content cadence.
- `.github/workflows/founder_content_weekly.yml` — weekly founder content
  scoreboard.

## Governance

Marketing/launch artifacts are subject to:

- **NO_FAKE_PROOF / NO_UNAPPROVED_TESTIMONIAL** — no customer
  name/logo/case study public mention without signed permission.
- **NO_ROI_OR_GUARANTEE** — guarantee/ROI claims are unconditionally
  banned.
- **case_study_publish** requires approval + evidence.

See `dealix/config/claim_policy.yaml` and `dealix/config/approval_policy.yaml`.
