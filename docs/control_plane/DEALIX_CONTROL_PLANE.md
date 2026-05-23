# Dealix Control Plane

The Control Plane is the operator's single pane of glass. Page:
`apps/web/app/control-plane/page.tsx`. API: `/api/v1/internal/control/*`.

## What it shows

- Policy version, approval classes, rule count.
- Agent registry version, count, kill-switch state, eval-required state.
- Open trust risks.
- Eval gate suite count + blocking failures.
- Operating scorecard summary (revenue, trust, runtime, leverage, product).
- Production token state (`DEALIX_INTERNAL_TOKEN` set or not).

## What it can do

- Disable or enable any agent in the registry.
- Read the open risk list (`/api/v1/internal/control/risks`).
- Pull the latest operating scorecard payload.

## What it must never do

- Send anything to a third party.
- Bypass policy.
- Hide an open trust flag.
