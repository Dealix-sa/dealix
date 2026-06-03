# Cold Email Draft Factory — مصنع مسودات البريد البارد

Produce up to **250 drafts/day** — never 250 sends/day. The factory is
deterministic and performs **no external sends**: it queues drafts for the
founder. Code: [`../../dealix/market_production_os/draft_factory.py`](../../dealix/market_production_os/draft_factory.py) ·
Schema: [`../../schemas/outreach_draft.schema.json`](../../schemas/outreach_draft.schema.json).

## The rule — القاعدة

```
250 drafts/day ≠ 250 sends/day
```

Drafts are high-density production. Sends are gated by domain health, the
[sending ramp](SENDING_RAMP_PLAN_AR.md), opt-out, suppression, and founder
approval. See [`COLD_EMAIL_COMPLIANCE_AR.md`](COLD_EMAIL_COMPLIANCE_AR.md).

## Daily mix — التوزيع اليومي (250)

| Touch type | Count |
|---|---:|
| first_touch | 100 |
| follow_up_1 | 75 |
| follow_up_2 | 50 |
| proposal_intro | 15 |
| breakup | 10 |

`produce_daily(prospects, sender_identity=..., target=250)` cycles qualified
prospects through this mix. Each draft is built by `build_draft(...)`.

## Every draft carries — كل مسودة تحمل

A complete draft (per the schema) includes: `prospect_id`, `company`, `sector`,
`recipient_role` (title only), `pain_hypothesis`, `personalization_note`,
`personalization_level` (P0–P4), `offer`, `touch_type`, `subject` (honest — no
fake `Re:`/`Fwd:`), `body`, `cta`, `language`, `evidence_level`, `risk_level`,
`sender_identity` (accurate name + email + physical address), and
`unsubscribe_included = true` with `unsubscribe_method = reply_keyword`.

The body always ends with an accurate sender block and the opt-out line
(`«إيقاف»` for Arabic, `STOP` for English) so the draft can pass the compliance
gate. Offers are drawn only from the canonical catalog
([`../commercial/DEALIX_REVOPS_PACKAGES_AR.md`](../commercial/DEALIX_REVOPS_PACKAGES_AR.md)) —
the factory never invents an offer or a price.

## Workflow — سير العمل

1. Qualified prospects (score ≥ 60) enter the factory.
2. `build_draft` renders subject/body/cta per sector + offer + touch type.
3. The [compliance gate](COLD_EMAIL_COMPLIANCE_AR.md) runs over every draft;
   `compliance_status` becomes `pass` or `fail` with reasons.
4. Passing drafts go to the [Approval Queue](../../reports/outreach/APPROVAL_QUEUE.md);
   the founder approves/edits/rejects.
5. Approved drafts are staged into a [sending batch](SENDING_RAMP_PLAN_AR.md)
   within today's ramp cap.

Ready copy to adapt: [`COLD_EMAIL_SEQUENCES_AR.md`](COLD_EMAIL_SEQUENCES_AR.md) ·
[`COLD_EMAIL_SEQUENCES_EN.md`](COLD_EMAIL_SEQUENCES_EN.md).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
