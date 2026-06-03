# Deliverability Review — مراجعة قابلية التسليم

Daily domain-health check before any send. **Source:**
[`../../docs/outreach/EMAIL_DELIVERABILITY_POLICY_AR.md`](../../docs/outreach/EMAIL_DELIVERABILITY_POLICY_AR.md) ·
code `dealix/market_production_os/deliverability.py`.

## Account health — صحة الحسابات

| account_id | domain | SPF | DKIM | DMARC | dedicated | warmup | health | ready |
|---|---|---|---|---|---|---|---:|---|
| ea_sample_ready | go.dealix-mail.sa | ✓ | ✓ | ✓ | ✓ | warm | 100 | yes |
| ea_sample_notready | dealix.sa | ✓ | ✗ | ✗ | ✗ | cold | 15 | no |

## Ceilings — حدود قصوى (today)

| Metric | Ceiling | Today | Status |
|---|---|---|---|
| Bounce rate | < 3% | … | … |
| Spam complaints | < 0.3% | … | … |
| Ramp phase | 0–3 | … | … |
| Allowed sends today | — | … | — |

If any ceiling is breached or `ready = no`, `allowed_sends` is **0**. See the
[Sending Ramp Plan](../../docs/outreach/SENDING_RAMP_PLAN_AR.md).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
