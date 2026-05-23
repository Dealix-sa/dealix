# Feature Intake Template — نموذج استقبال طلبات الميزات

## Purpose
Standard intake for every feature request, internal or client-driven. No feature enters the backlog without this form filled and counter-signed. Eliminates "wouldn't it be cool" features.

## Owner
Founder. Intake filled by whoever surfaces the request (founder, analyst, client AE).

## Inputs
- Source of the request (client name, internal observation, partner).
- Problem statement (1-2 sentences, no solution language).
- Evidence (link to signed SOW, ticket, recorded call, written client request).
- Frequency observed (how many distinct clients or runs in last 90 days).
- Estimated value (hours saved × frequency, or revenue at stake).

## Outputs
- Filed intake under `docs/product/intake/FT-YYYY-NNN.md`.
- Entry added to `docs/product/FEATURE_BACKLOG.md` with status `intake`.
- Decision routed to `docs/product/BUILD_DEFER_KILL.md` within 7 days.

## Intake Schema
```json
{
  "id": "FT-2026-001",
  "title": "",
  "requester": "",
  "source": "client | internal | partner",
  "problem": "",
  "evidence_links": [],
  "frequency_90d": 0,
  "distinct_clients": 0,
  "estimated_value_sar": 0,
  "estimated_build_hours": 0,
  "risk_flags": [],
  "ai_workflow_touch": false,
  "data_sensitivity": "none | low | medium | high",
  "labelled_estimate": "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"
}
```

## Rules
1. No feature enters backlog without an intake.
2. No intake without at least one evidence link.
3. Frequency below 3 distinct clients goes straight to `Defer`.
4. Any feature touching AI workflows requires a risk-flag review.
5. Estimated value is labelled and never quoted as verified.
6. PII in evidence is redacted before filing.

## Metrics
- Intake count per month.
- Approval rate (intake → build).
- Defer rate, Kill rate.
- Median time from intake to decision.

## Cadence
- Continuous intake.
- Weekly triage during founder review.
- Monthly trend review.

## Evidence
- Stored intake file with evidence links.
- Decision log entry in `docs/product/BUILD_DEFER_KILL.md`.

## Verifier
Founder signs the decision. Delivery analyst verifies frequency counts.

## Runtime Command
`make feature-intake` — generates a new intake file from template, refuses to file without required fields.

## Arabic Summary — ملخص عربي
لا تدخل أي ميزة قائمة العمل قبل تعبئة هذا النموذج وتوقيع المؤسس. الأدلة شرط. التكرار أقل من ثلاثة عملاء = تأجيل. القيم التقديرية ليست مُتحقَّقة.
