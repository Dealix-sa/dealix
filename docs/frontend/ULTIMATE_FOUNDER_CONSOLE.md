# Ultimate Founder Console

Sixteen pages, one shell, one runtime client, one action client.

## Pages

| Path | Purpose |
|---|---|
| `/ceo` | top-of-funnel pulse |
| `/sales-cockpit` | funnel by stage |
| `/approvals` | queue + decisions |
| `/workers` | worker heartbeats |
| `/trust` | open trust flags |
| `/finance` | cash + capture |
| `/distribution` | by channel + sector |
| `/delivery` | active proposals + delivery |
| `/retention` | retention flags |
| `/proof` | staged proof artefacts |
| `/control-plane` | governance + scorecards |
| `/audit` | approval decision log |
| `/evals` | eval suites |
| `/product` | productization candidates |
| `/security` | internal API auth + security status |
| `/sovereign` | sovereign readiness scorecard |

## Files

* Shell: `apps/web/components/founder-shell.tsx`
* Runtime client: `apps/web/lib/dealix-runtime.ts`
* Action client: `apps/web/lib/dealix-actions.ts`

## Conventions

* Every page uses `export const dynamic = "force-dynamic"` so SSR
  reads the latest runtime state.
* Every reader returns `{ source, ... }`. `source === "fallback"` is
  surfaced as a banner.
* Every action posts to the internal API, never to a third-party.
