# Retention Playbook — دليل الاحتفاظ بالعميل

## Purpose
A specific, sequenced playbook to save an at-risk client. Activated automatically when health score < 40 or a critical incident occurs. Eliminates panic improvisation.

## Owner
Founder. Personally led; not delegated.

## Inputs
- Health score from `docs/client_success/CLIENT_HEALTH_SCORE.md`.
- Recent feedback entries from `docs/client_success/FEEDBACK_LOOP.md`.
- Engagement history (work log, weekly reports).
- Payment status.

## Outputs
- A3 entry filed (5-Why, root cause, countermeasures).
- Recovery plan signed by founder and shared with client.
- Resolution decision within 14 days: recovered / managed-exit.

## The 48-Hour Activation
- [ ] Founder reads last 4 weekly reports.
- [ ] Founder reads last 5 feedback entries.
- [ ] Founder writes a 1-page situation brief (no client jargon).
- [ ] Founder requests a 30-min direct call within 48 hours.
- [ ] Analyst prepares a fact pack: SOW vs delivered, hours used, outcomes vs goals.

## The Call (30 min, founder leads)
1. Open: "We see signals that the engagement is not where it should be. I want to understand from you."
2. Listen for 15 minutes. No defending, no explaining.
3. Reflect back the 3 main points heard.
4. Ask: "What outcome in the next 30 days would change your view?"
5. Close: commit to a written recovery plan within 72 hours.

## The Recovery Plan (≤ 1 page)
- Acknowledged issues (in client's words).
- Three concrete actions with owners and dates.
- One success measure with kill criterion.
- Communication cadence for the next 30 days.
- Renewal conversation deferred until success measure met.

## Rules
1. Retention playbook is never delegated.
2. No discounts offered as the primary lever; outcomes first, pricing last.
3. The kill criterion is real: if not met, managed exit is the right outcome.
4. No new commitments without scope clarity.
5. PII and confidential numbers stay within the engagement; not used in marketing.
6. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to projected recovery outcomes.

## Metrics
- Activation count per quarter.
- Recovery rate (target ≥ 50% recovered).
- Managed-exit rate (target ≤ 50%; both are acceptable outcomes).
- Time from activation to resolution (target ≤ 14 days).

## Cadence
- Per-trigger.

## Evidence
- `evidence/retention/<client_id>/<YYYY-MM-DD>/` with brief, plan, A3.

## Verifier
Founder.

## Runtime Command
`make retention-activate CLIENT=<id>` — opens the 48-hour checklist; refuses to mark recovered without signed recovery plan.

## Arabic Summary — ملخص عربي
دليل احتفاظ مُسلسل يُفعَّل تلقائيًا عند مؤشر صحة تحت 40. مكالمة خلال 48 ساعة، خطة تعافٍ خلال 72 ساعة، قرار خلال 14 يومًا. لا تخفيضات كأداة أولى. القيم التقديرية ليست مُتحقَّقة.
