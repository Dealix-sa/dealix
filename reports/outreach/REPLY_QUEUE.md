# Reply Queue — قائمة الردود

Classified inbound replies and their routed actions. **Source:**
[`../../docs/outreach/REPLY_HANDLING_OS_AR.md`](../../docs/outreach/REPLY_HANDLING_OS_AR.md) ·
code `dealix/market_production_os/reply_classifier.py`.

## Today — اليوم

| reply_id | prospect | classification | action | founder? | suppress? |
|---|---|---|---|---|---|
| … | … | positive | discovery_invite | yes | no |

## Safety first — السلامة أولاً

`unsubscribe`, `angry`, and `bounce` trigger **immediate suppression** — the
recipient is never re-contacted (see
[`UNSUBSCRIBE_POLICY_AR.md`](../../docs/outreach/UNSUBSCRIBE_POLICY_AR.md)).
A `positive` reply unlocks the opt-in
[WhatsApp / booking flow](../../docs/outreach/WHATSAPP_POST_REPLY_FLOW_AR.md).
No price or commitment is sent without founder approval.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
