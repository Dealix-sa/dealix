# Ultimate Founder Console

Stack: Next.js 15 App Router (`apps/web/`). All pages are server
components and call the internal API via `apps/web/lib/dealix-runtime.ts`.

## Pages

| Route | What it does |
|---|---|
| `/` | Entry, links into the console. |
| `/ceo` | Top action + daily metrics. |
| `/sales-cockpit` | Funnel from lead intel to payment capture. |
| `/approvals` | Pending decisions. |
| `/workers` | Worker health. |
| `/trust` | Trust flags + suppression + A3 attempts. |
| `/finance` | Cash, pipeline, follow-ups. |
| `/distribution` | Sectors, channels, double-down candidate. |
| `/delivery` | In-flight delivery items. |
| `/retention` | Won customers. |
| `/proof` | Proof library (manual publish only). |
| `/control-plane` | Policies, agents, scorecard, kill switches. |
| `/audit` | Append-only decision log. |
| `/evals` | Eval gate state. |
| `/product` | Productization candidates. |
| `/security` | Security control posture. |

## Rendering rule

Every page declares `export const dynamic = "force-dynamic";` so server
components always re-fetch. Fallback responses are tagged
`source: "fallback"` and rendered with a warning badge so the founder
never confuses them with live data.

## Building

```
npm --prefix apps/web ci
npm --prefix apps/web run build
```
