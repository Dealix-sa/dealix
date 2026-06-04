# The 400/day Draft Factory

The factory produces **at least 400 founder-review-only drafts every day**,
across 5 verticals and 4 channels, in Arabic and English. It never sends.

## Daily channel mix (minimum)

| Channel | Min drafts/day |
|---------|----------------|
| Cold email | 175 |
| Follow-up | 100 |
| LinkedIn (manual) | 75 |
| Website / contact form | 50 |
| **Total** | **400** |

Source of truth: `config/commercial_launch.json` → `daily_targets_by_channel`.

## How to run

```bash
python scripts/commercial_generate_400_drafts.py --target 400
# with a real lead file:
python scripts/commercial_generate_400_drafts.py --target 400 --leads data/commercial_seed_leads.jsonl
```

The script is **standard-library only** — no external dependencies, no secrets,
no network calls.

## Every draft carries these fields

```
draft_id, created_at, company_name, vertical, country, city, channel,
language, buyer_persona, buyer_title, offer, pain_angle, subject, body, cta,
opt_out, quality_score, compliance_score, risk_level, research_required,
founder_notes, send_allowed (false), external_send_blocked (true),
requires_founder_approval (true), source_lead_id, status (founder_review)
```

## A draft can NEVER contain

`send_allowed: true` · `auto_send: true` · `smtp_send` · `whatsapp_send` ·
`linkedin_send` · `api_send` · mass outreach · scraped personal emails ·
fake familiarity ("as discussed") · guaranteed ROI · deceptive urgency ·
claims about accessing the prospect's data · WhatsApp cold outreach ·
LinkedIn automation · any unproven promise.

These are enforced by the quality gate, the compliance gate, and the safety
audit. See [`06_COMPLIANCE_AND_SAFETY_GATES.md`](06_COMPLIANCE_AND_SAFETY_GATES.md).

## With and without real leads

- **No real leads:** the factory generates placeholder companies marked
  `research_required: true`, adds warnings, and still produces ≥ 400 drafts.
  Nothing is send-ready until the founder enriches them.
- **Real leads** (`data/commercial_seed_leads.jsonl`): each lead is used once
  before placeholders fill the rest, so drafts are tied to real accounts.

The run only **fails** if it produces fewer than the target or if the safety
audit fails.

## Determinism

Generation is seeded from the run date (overridable with `--seed`) so CI runs
and tests are reproducible.

## Outputs

See [`05_FOUNDER_DAILY_REVIEW_PLAYBOOK.md`](05_FOUNDER_DAILY_REVIEW_PLAYBOOK.md)
for the full output bundle and how to review it.
