# Email Deliverability Policy — سياسة قابلية التسليم

Protect the domain reputation before scaling sends. Code:
[`../../dealix/market_production_os/deliverability.py`](../../dealix/market_production_os/deliverability.py) ·
Schema: [`../../schemas/email_account.schema.json`](../../schemas/email_account.schema.json).

## DNS / domain requirements — متطلبات الدومين

| Requirement | Why |
|---|---|
| **SPF** | Authorizes sending hosts |
| **DKIM** | Signs messages for authenticity |
| **DMARC** (policy ≥ quarantine) | Aligns SPF/DKIM, instructs receivers |
| **Dedicated domain** | Cold outreach never uses the primary brand domain |
| **Custom tracking domain** | Avoids shared-domain reputation drag |
| **Postmaster Tools connected** | Visibility into spam rate + reputation |
| **Bounce handling** | Hard bounces feed suppression |
| **Unsubscribe endpoint** | One-click + reply opt-out both work |

`evaluate_account(account)` returns a `health_score` (0–100) and a `ready` flag.
`ready_to_send(account)` requires SPF + DKIM + DMARC + dedicated domain +
unsubscribe endpoint + bounce handling, and a domain that is **not cold**
(warming/warm).

## Google sender guidelines — إرشادات Google

- All senders to Gmail must set up **SPF or DKIM**.
- Bulk senders (≈ 5,000+/day) must set **SPF + DKIM + DMARC**, provide
  **one-click unsubscribe**, and keep the **spam-complaint rate under 0.3%**.
- Do not buy address lists or mail people who never opted in — it damages domain
  reputation.

## Sending behavior — سلوك الإرسال

Never: sudden volume spikes · burst sending · misleading subjects · fake
`Re:`/`Fwd:` · purchased lists · sending without opt-out · contacting anyone who
opted out. These are enforced by the
[compliance gate](COLD_EMAIL_COMPLIANCE_AR.md) and the
[sending ramp](SENDING_RAMP_PLAN_AR.md).

## Hard ceilings — حدود قصوى

`allowed_sends(...)` drops to **0** when the account is not ready, or when bounce
rate ≥ 3% or spam-complaint rate ≥ 0.3%. Suppression is applied first via
[`UNSUBSCRIBE_POLICY_AR.md`](UNSUBSCRIBE_POLICY_AR.md).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
