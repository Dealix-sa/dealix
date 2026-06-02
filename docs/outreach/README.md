# Outreach OS — Index — فهرس نظام التواصل

The cold-**email**-first acquisition engine for Dealix. Cold email is the
primary channel; WhatsApp is post-reply / opt-in only; LinkedIn is manual only.
Parent: [`../market_production_os/README.md`](../market_production_os/README.md).

## Policy + engine docs (this folder)

| Doc | Machine |
|---|---|
| [PROSPECT_RESEARCH_OS_AR.md](PROSPECT_RESEARCH_OS_AR.md) | Research + score companies (no scraping) |
| [COLD_EMAIL_DRAFT_FACTORY_AR.md](COLD_EMAIL_DRAFT_FACTORY_AR.md) | 250 drafts/day production |
| [PERSONALIZATION_RULES_AR.md](PERSONALIZATION_RULES_AR.md) | P0–P4 levels + the P1 cold floor |
| [COLD_EMAIL_COMPLIANCE_AR.md](COLD_EMAIL_COMPLIANCE_AR.md) | The six gates every message passes |
| [EMAIL_DELIVERABILITY_POLICY_AR.md](EMAIL_DELIVERABILITY_POLICY_AR.md) | SPF/DKIM/DMARC + domain health |
| [SENDING_RAMP_PLAN_AR.md](SENDING_RAMP_PLAN_AR.md) | Staged sending ramp + ceilings |
| [UNSUBSCRIBE_POLICY_AR.md](UNSUBSCRIBE_POLICY_AR.md) | Opt-out + suppression |
| [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md) | Reply classification + routing |

## Sequences + adjacent channels

| Doc | Use |
|---|---|
| [COLD_EMAIL_SEQUENCES_AR.md](COLD_EMAIL_SEQUENCES_AR.md) · [COLD_EMAIL_SEQUENCES_EN.md](COLD_EMAIL_SEQUENCES_EN.md) | Ready-to-adapt copy (5 touch types) |
| [LINKEDIN_MANUAL_OUTREACH_AR.md](LINKEDIN_MANUAL_OUTREACH_AR.md) | Manual-only LinkedIn workflow |
| [WHATSAPP_POST_REPLY_FLOW_AR.md](WHATSAPP_POST_REPLY_FLOW_AR.md) | Post-reply / opt-in WhatsApp flow |

## Schemas (`schemas/`)

[`prospect`](../../schemas/prospect.schema.json) ·
[`outreach_draft`](../../schemas/outreach_draft.schema.json) ·
[`email_account`](../../schemas/email_account.schema.json) ·
[`sending_batch`](../../schemas/sending_batch.schema.json) ·
[`suppression`](../../schemas/suppression.schema.json) ·
[`reply`](../../schemas/reply.schema.json)

## Code (`dealix/market_production_os/`)

`prospect_scoring.py` · `personalization.py` · `draft_factory.py` ·
`compliance_gate.py` · `deliverability.py` · `sending_ramp.py` ·
`reply_classifier.py` · `control_room.py`. Run:
`python -m dealix.market_production_os.control_room --produce --print`.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
