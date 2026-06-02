# Reply Handling OS — نظام معالجة الردود

Classify every inbound reply and route it to the right action. Code:
[`../../dealix/market_production_os/reply_classifier.py`](../../dealix/market_production_os/reply_classifier.py) ·
Schema: [`../../schemas/reply.schema.json`](../../schemas/reply.schema.json).

## Classifications + actions — التصنيفات والإجراءات

| Reply | Action | Founder? | Suppress? |
|---|---|---|---|
| positive | discovery_invite | yes | no |
| interested_but_later | nurture_followup | yes | no |
| price_question | offer_card | yes | no |
| send_more_info | proof_pack | yes | no |
| not_interested | nurture | no | no |
| wrong_person | ask_referral | yes | no |
| unsubscribe | suppress_immediately | no | **yes** |
| angry | apologize_and_suppress | yes | **yes** |
| auto_reply | retry_later | no | no |
| bounce | suppress_email | no | **yes** |

`classify(text)` returns the classification, recommended action,
`requires_founder`, a `suppress` flag, and a confidence. AR + EN keywords are
matched; safety classes (unsubscribe / bounce / angry) are checked first.
Ambiguous replies route to the founder with low confidence.

## Suppression on opt-out — القمع عند الإيقاف

Any reply classified `unsubscribe`, `angry`, or `bounce` triggers **immediate**
suppression — the recipient is never re-contacted. Suppression is keyed on a
sha256 hash of the address (NO_PII); see
[`UNSUBSCRIBE_POLICY_AR.md`](UNSUBSCRIBE_POLICY_AR.md).

## After a positive reply — بعد ردّ إيجابي

A `positive` reply unlocks the opt-in WhatsApp / booking flow — never a cold
channel. See [`WHATSAPP_POST_REPLY_FLOW_AR.md`](WHATSAPP_POST_REPLY_FLOW_AR.md).
Offers and prices come only from
[`../commercial/DEALIX_REVOPS_PACKAGES_AR.md`](../commercial/DEALIX_REVOPS_PACKAGES_AR.md);
nothing is committed without founder approval.

The reply queue is reviewed in
[`../../reports/outreach/REPLY_QUEUE.md`](../../reports/outreach/REPLY_QUEUE.md).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
