# Sending Ramp Plan — خطة الإرسال التدريجي

250 drafts/day is allowed; sends ramp **slowly** from a healthy domain. Code:
[`../../dealix/market_production_os/sending_ramp.py`](../../dealix/market_production_os/sending_ramp.py) ·
Schema: [`../../schemas/sending_batch.schema.json`](../../schemas/sending_batch.schema.json).

## Phases — المراحل

| Phase | Window | Max sends/day | Conditions |
|---|---|---:|---|
| 0 | Week 1 | 20 | Generate 250 drafts/day; send 0–20 manually to test copy |
| 1 | Week 2 | 50 | 1 domain · ≥ 2 inboxes · personalized only |
| 2 | Week 3 | 150 | Only if bounce < 3% and complaints low |
| 3 | Week 4 | 250 | Only with excellent reputation + suppression + opt-out live |

`phase_cap(phase)` returns the ceiling; `allowed_sends(phase, account, ...)`
returns the actual permitted count (min of phase cap and the account's remaining
daily cap), or **0** if the domain is not ready or a ceiling is breached.

## Hard ceilings — حدود قصوى

- Bounce rate **≥ 3%** → 0 sends.
- Spam-complaint rate **≥ 0.3%** → 0 sends (Google guideline).
- `can_advance_phase(...)` refuses to advance while either ceiling is breached
  or at the final phase.

## Never — لا

- Never start at 250/day from a new domain.
- Never use the primary brand domain for heavy cold sending.
- Never send without a working opt-out.
- Never bypass the suppression list.

## Batching — التجميع

`plan_batch(...)` builds a `sending_batch` capped at `allowed_sends`. A batch
moves to `sending` only after **founder approval** (`approved_by` set) and only
within the ramp cap. Suppression is filtered first via
[`filter_suppressed`](UNSUBSCRIBE_POLICY_AR.md). Health is reviewed daily in
[`../../reports/outreach/DELIVERABILITY_REVIEW.md`](../../reports/outreach/DELIVERABILITY_REVIEW.md).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
