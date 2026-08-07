# Broken or Weak Areas — Dealix V3

## Broken
- **apps/web typecheck/build** — `tsc` and `next` not found until `npm install` runs.
- **Missing scripts** — `check_no_secrets.py`, `verify_dealix_ultimate_os.py`, `production_readiness_check.py` do not exist.

## Weak
1. **Business layer depth**
   - No lead scoring model documented.
   - No persuasion libraries (objections, CTAs).
   - No industry-specific weakness taxonomy.
   - No offer definitions for core products.
   - No closing playbooks or discovery scripts.

2. **Frontend surface**
   - Pages like `/war-room`, `/pipeline`, `/operator`, `/book` do not exist.
   - No reusable component library (Nav, Footer, CTA, MetricCard, etc.).
   - Static pages do not read from generated data.

3. **Daily execution**
   - No single script runs the full daily commercial sequence.
   - Founder dashboard data is not generated automatically.

4. **Governance / Safety**
   - No programmatic check for auto-send patterns.
   - No outreach review gate document.
   - No client data retention policy.
   - No AI output risk classification.

5. **Deployment readiness**
   - No post-deploy smoke test script.
   - No unified deployment docs for Vercel + Railway.
   - No environment variable reference.

6. **Tests**
   - No tests for scoring, draft safety, proposal generation, or daily operator.

## Plan
Address all weak areas in Phases 1–9. Fix broken areas by installing dependencies and creating missing scripts.
