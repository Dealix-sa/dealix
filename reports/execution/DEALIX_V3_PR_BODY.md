# Dealix V3 Commercial OS

## Summary
This PR finalizes the Dealix V3 Commercial Operating System: a unified layer for daily execution, lead quality, proposal generation, website conversion, governance, and deployment readiness.

## What changed
- **Daily Operator**: `scripts/dealix_daily_operator.py` runs the full commercial sequence in one command.
- **Founder Dashboard**: JSON generator + TypeScript mirror + API endpoint.
- **Lead Quality**: Scoring model, persuasion libraries, 8 industry OS profiles.
- **Proposal & Closing**: 7 offer definitions, closing playbooks, discovery scripts, deal desk rules.
- **Website**: 10 components, 12+ pages, `/book` CTA page, updated homepage.
- **Governance**: Outreach review gate, retention policy, AI risk classes, approval matrix.
- **Deployment**: Vercel/Railway docs, post-deploy smoke test, production readiness check.
- **Tests**: 9 new tests + CI updates.

## Commercial impact
- Founder can run `python3 scripts/dealix_daily_operator.py --mode demo` and see full pipeline output.
- Website now has clear commercial pages: `/sales-machine`, `/offers`, `/pricing`, `/book`.
- Industry-specific playbooks enable targeted outreach.
- Proposal generator produces structured commercial docs with proof plans.

## Safety and governance
- No auto-send outreach. All drafts have `review_status = pending_review`.
- `tests/test_no_auto_send.py` scans repo for forbidden patterns.
- `scripts/check_no_secrets.py` runs before every daily operator.
- PDPL-aligned data retention policy documented.

## How to test
```bash
python3 scripts/check_no_secrets.py
python3 scripts/verify_dealix_ultimate_os.py
python3 scripts/dealix_daily_operator.py --mode demo
python3 scripts/production_readiness_check.py
cd apps/web && npm run typecheck && npm run build
pytest tests/v3/ -q --confcutdir=tests/v3
```

## Daily operator command
```bash
python3 scripts/dealix_daily_operator.py --mode demo
```

## Deployment notes
- Frontend: Vercel (`apps/web`)
- Backend: Railway (`api/`)
- See `docs/deploy/` for detailed guides.

## Known limitations
- Outreach drafts are template-based; deeper personalization requires CRM integration.
- Founder dashboard uses demo data until production CRM sync is configured.
- Some datetime deprecation warnings exist (non-breaking).

## Checklist
- [x] No auto-send outreach
- [x] Human review required
- [x] No secrets committed
- [x] Demo mode works
- [x] Web build passes
- [x] Master verification passes
- [x] Production readiness check passes
- [x] Branch pushed to GitHub
