# CI WORKFLOW MATRIX

## Required Workflows (Block PR if failing)

| Workflow | File | Purpose | Frequency |
|----------|------|---------|-----------|
| **CI** | `ci.yml` | Python tests, typecheck, lint | Every PR |
| **Security** | `security.yml` | Secret scan, dependency check | Every PR |
| **CodeQL** | `codeql.yml` | Static analysis | Every PR |
| **Agentic Security Gate** | `agentic-security-gate.yml` | AI-specific security checks | Every PR |

## Deploy Workflows (Required for release)

| Workflow | File | Purpose | Trigger |
|----------|------|---------|---------|
| **Deploy** | `deploy.yml` | Main deployment | Manual / push to main |
| **Railway Deploy** | `railway_deploy.yml` | Railway backend | Push to main |
| **Railway Frontend** | `railway_deploy_frontend.yml` | Railway frontend | Push to main |
| **Release Please** | `release-please.yml` | Automated releases | Push to main |

## Verification Workflows (Required for go-live)

| Workflow | File | Purpose | Trigger |
|----------|------|---------|---------|
| **Official Launch Verify** | `official-launch-verify.yml` | Launch gate verification | Manual |
| **Production Smoke** | `production-smoke.yml` | Live API smoke | Scheduled + manual |
| **Staging Smoke** | `staging-smoke.yml` | Staging verification | Manual |
| **Local Stack Verify** | `local_stack_verify.yml` | Full local verification | Manual |
| **Playwright Smoke** | `playwright_smoke.yml` | E2E browser tests | PR + manual |
| **Lighthouse CI** | `lighthouse_ci.yml` | Performance audit | PR |

## Optional Workflows (Do NOT block PR)

| Workflow | File | Purpose | Recommendation |
|----------|------|---------|---------------|
| `autonomous_executive_day.yml` | Founder automation | Daily exec routine | Keep but optional |
| `brain-control-command.yml` | Founder automation | Brain control | Mark optional |
| `business_now_snapshot.yml` | Founder automation | Business snapshot | Mark optional |
| `commercial-expand-weekly.yml` | Founder automation | Weekly expansion | Mark optional |
| `company-brain-daily.yml` | Founder automation | Daily brain ops | Mark optional |
| `company_daily_operating_pack.yml` | Founder automation | Daily ops | Mark optional |
| `cto_weekly_anchor.yml` | Founder automation | CTO weekly | Mark optional |
| `daily-revenue-machine.yml` | Founder automation | Revenue machine | Mark optional |
| `daily_digest.yml` | Founder automation | Daily digest | Mark optional |
| `daily_snapshot.yml` | Founder automation | Daily snapshot | Mark optional |
| `founder_*` (12 workflows) | Founder automation | Various founder ops | All optional |
| `governed-full-ops-daily.yml` | Founder automation | Full ops daily | Mark optional |
| `hermes-revenue-growth-os.yml` | Founder automation | Hermes revenue | Mark optional |
| `master_stable_day.yml` | Founder automation | Stable day check | Mark optional |
| `micro_day.yml` | Founder automation | Micro daily | Mark optional |
| `scorecard.yml` | Founder automation | Scorecard | Mark optional |
| `weekly_*` (3 workflows) | Founder automation | Weekly routines | All optional |
| `dlq_check.yml` | Ops | Dead letter check | Keep optional |
| `reliability_drills_scorecard.yml` | Ops | Reliability drills | Keep optional |
| `repository-hardening.yml` | Ops | Repo hardening | Consider merging into security.yml |
| `docker-build.yml` | Ops | Docker build test | Keep optional |
| `deploy-pages.yml` | Ops | GitHub Pages | Keep optional |
| `enterprise-control-plane.yml` | Ops | Enterprise | Keep optional |
| `enterprise-readiness.yml` | Ops | Enterprise readiness | Keep optional |
| `global-ai-transformation.yml` | Ops | AI transformation | Keep optional |
| `intake_day.yml` | Ops | Intake day | Keep optional |
| `labeler.yml` | Ops | PR labeling | Keep optional |
| `release.yml` | Ops | Release | Consider merging with release-please |
| `verify-full-autonomous-ops.yml` | Ops | Autonomous ops verify | Keep optional |
| `watchdog_drift.yml` | Ops | Watchdog | Keep optional |
| `production_api_trust_smoke.yml` | Ops | Trust smoke | Consider merging into production-smoke |
| `production-watchdog.yml` | Ops | Production watchdog | Consider merging into production-smoke |
| `design-system.yml` | Ops | Design system | Keep optional |
| `generate-web-lockfile.yml` | Ops | Lockfile gen | Keep optional |
| `dealix-ultimate-os-check.yml` | Ops | OS check | Keep optional |
| `client-acquisition-delivery-check.yml` | Ops | Client check | Keep optional |
| `scheduled_healthcheck.yml` | Ops | Health check | Consider merging into production-smoke |

## Recommendations

1. **Reduce from 60 to ~25 workflows** by:
   - Merging founder automation into 3-4 unified workflows
   - Merging trust/watchdog/smoke into production-smoke.yml
   - Removing or disabling obsolete workflows

2. **Mark 35 workflows as `optional: true`** in CI config so they don't block PRs

3. **Keep only 10 as required** for merge:
   - ci.yml, security.yml, codeql.yml, agentic-security-gate.yml
   - lighthouse_ci.yml, playwright_smoke.yml
   - deploy.yml (for main only), railway_deploy.yml (for main only)
   - official-launch-verify.yml (manual only)
