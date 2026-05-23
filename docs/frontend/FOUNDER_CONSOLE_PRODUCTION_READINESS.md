# Founder Console Production Readiness

## F1 Build Ready
- `apps/web` builds successfully with `npm run build`.
- all P0 routes exist: /ceo /sales-cockpit /approvals /workers /trust /finance /distribution /delivery /retention /proof.

## F2 API Ready
- internal endpoints return JSON.
- fallback clearly marked with `source: "fallback"`.
- no fake production status.

## F3 Data Ready
- sales funnel reads source of truth.
- approvals read approval queue.
- finance reads payment/cash data.
- workers read runtime logs.

## F4 Action Ready
- approve/reject/request-edit endpoints exist.
- each action writes audit.
- each action passes policy evaluator.

## F5 Trust Ready
- no external action bypasses trust.
- A2/A3 behavior enforced.
- suppression checked before outreach.

## F6 Founder Ready
- /ceo gives one top action.
- /approvals shows pending decisions.
- /sales-cockpit shows funnel bottleneck.
- /workers shows failures.
- /finance shows payment follow-ups.

## Rule
Do not call Founder Console production-ready until F1–F5 pass.
