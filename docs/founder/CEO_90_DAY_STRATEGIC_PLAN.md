# CEO 90-Day Strategic Plan — Four Proof Gates — خطة 90 يومًا

## Purpose
A four-phase strategic plan covering the founder's next 90 days. Each phase ends with a named proof gate. No phase is skipped, no gate is implied — gates pass with written evidence. Replaces ambition with proof.

## Owner
Founder. Plan reviewed weekly; rewritten at each gate-pass.

## Inputs
- Current state from `docs/founder/CEO_MASTER_DASHBOARD.md`.
- Operating model from `docs/founder/CEO_OPERATING_MODEL.md`.
- Cash from `docs/finance/`.
- Pipeline.

## Outputs
- This plan (dated).
- Per-phase gate evidence filed under `evidence/founder/gates/`.
- Weekly progress note in the CEO weekly scorecard.

## The Four Phases

### Phase 1 — Days 1-7: Proof of Interest
**Goal**: Confirm that named Saudi B2B buyers want to talk and will engage substantively.

**Gate evidence required**:
- 10 substantive conversations held with ICP buyers (recorded notes, not blasts).
- 3 written "we want to explore this" responses.
- 1 in-person or video meeting scheduled.

**Banned**: cold blasts, scraped lists, automation.

**Owner**: Founder.

### Phase 2 — Days 8-30: Proof of Conversion
**Goal**: Convert at least one interested buyer into a signed, paid Statement of Work.

**Gate evidence required**:
- 1 signed SOW.
- 1 payment received (or invoice issued with confirmed payment commitment within 30 days).
- Sprint kick-off scheduled.

**Banned**: free pilots used as a substitute for paid conversion.

**Owner**: Founder.

### Phase 3 — Days 31-60: Proof of Delivery
**Goal**: Deliver the first paid sprint, on time, with a verified outcome.

**Gate evidence required**:
- Sprint closed on or before agreed date.
- Verified outcome (numbers, not estimates).
- Weekly client reports delivered every week of the sprint.
- Client written acceptance of delivery.
- A3 written on what worked and what did not.

**Banned**: silently extending scope to avoid acknowledging delays.

**Owner**: Founder (delivery lead).

### Phase 4 — Days 61-90: Proof of Retention
**Goal**: Earn the right to a renewal conversation, or a referral, or a written reference — by demonstrated value.

**Gate evidence required**:
- 1 of the following: a signed renewal SOW, a written client reference, a qualified referral introduced by the client.
- Health score ≥ 75 at end of engagement.
- Sprint close A3 reviewed by founder.

**Banned**: pressuring clients for testimonials without value delivered.

**Owner**: Founder.

## Rules
1. No phase skipped. Failing a gate triggers an A3 and a revised plan, not a workaround.
2. Each gate's evidence is filed before declaring the gate passed.
3. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to any projected outcomes.
4. Founder's calendar in each phase reflects that phase's priority (see weekly scorecard).
5. Failing Phase 1 within 7 days is acceptable; failing Phase 1 within 30 days requires an A3 on ICP definition.
6. No hire, no SaaS bet, no major content investment before Phase 3 is passed.

## Metrics
- Gate-pass rate (target: all four within 90 days).
- Time per phase (median).
- Gate evidence completeness.
- A3 quality on gate failures.

## Cadence
- Weekly review.
- Gate-pass rewrite.

## Evidence
- `evidence/founder/gates/phase_<n>_<YYYY-MM-DD>/`.

## Verifier
Founder.

## Runtime Command
`make gate-check PHASE=<n>` — verifies the gate evidence; refuses to mark gate passed if any item is missing.

## Arabic Summary — ملخص عربي
أربع مراحل في 90 يومًا: إثبات الاهتمام (7 أيام)، إثبات التحويل (30 يومًا)، إثبات التسليم (60 يومًا)، إثبات الاحتفاظ (90 يومًا). لا مرحلة تُتخطى، لا بوابة بدون أدلة. القيم التقديرية ليست مُتحقَّقة.
