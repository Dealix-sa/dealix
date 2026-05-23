# Inbound Content Machine

> Drafts inbound content per persona × pillar × week. Never publishes.

## 1. Purpose

Produce a steady stream of inbound content (LinkedIn posts, blog drafts, sector report sections, email newsletters) so the founder spends time **reviewing**, not writing from scratch.

## 2. Input

- Active personas (`BUYER_PERSONA_SYSTEM.md`).
- Active brand pillars (`DEALIX_BRAND_SYSTEM.md` §2).
- Weekly content calendar in `data/marketing/content_calendar.csv`.
- Recent observations from the Market Intelligence Machine.
- The week's KPI metrics (so content can lead with a metric).

## 3. Output

Rows in `data/marketing/content_ideas.csv` and `data/marketing/content_calendar.csv`:

```
content_id, theme, pillar, persona,
language, channel, format,
title, body, evidence_cited,
approval_state, scheduled_for, created_at
```

`approval_state` starts at `draft` or `queued`. Never `published`.

## 4. Channels supported

- LinkedIn post (founder-led, AR/EN).
- Blog post (long form, AR + EN side-by-side).
- Sector report section (monthly).
- Email newsletter (warm list).
- Landing page copy block (one-off).

## 5. Approval class

**A1.** Founder approves every piece individually.

## 6. Owner

Content Strategist agent + founder.

## 7. Worker name

`inbound_content_worker`.

## 8. KPI

- Drafts queued per week: ≥ 5 across all channels.
- Pillar coverage: every active pillar gets at least 1 draft per week.
- Persona coverage: every active persona gets at least 1 draft per fortnight.
- Evidence rate: 100% of drafts cite at least one observation, metric, or source.

## 9. Failure modes

| Failure                                  | Recovery                                          |
|------------------------------------------|---------------------------------------------------|
| Draft has no pillar tag                  | Refuse to emit                                    |
| Draft uses banned phrase                 | Refuse to emit; flag                              |
| Draft repeats a published piece          | Suppress; require founder override                |
| Draft is monolingual when bilingual req  | Refuse to emit                                    |

## 10. Quality gates

The Brand Guardian agent reviews each draft for:

- Tagline correctness.
- Pillar attribution.
- No guaranteed-results language.
- No hype superlatives.
- No emoji.
- Length appropriate for the channel.

## 11. Audit

Every draft, approval, edit, and reject is logged. Once approved and **published by a human**, the draft is moved to `data/marketing/content_calendar.csv` with `approval_state = published` and `published_at`.

## 12. Doctrine

This machine does **not** publish externally. Publishing is a human operation (the founder or a designated operator) that occurs after explicit approval.
