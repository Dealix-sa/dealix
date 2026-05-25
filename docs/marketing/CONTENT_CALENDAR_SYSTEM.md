# Content Calendar System

How we plan, approve, and publish Dealix content. The calendar lives in `data/marketing/content_calendar.csv`.

## 1. Schema

```
calendar_id, week, day, channel, format, pillar, persona, language,
title, hook, body_link, evidence_cited, approval_state,
scheduled_for, published_at, created_at
```

## 2. Planning cadence

- **Sunday evening:** founder reviews the upcoming week's calendar.
- **Each weekday morning:** founder reviews ≤ 2 LinkedIn drafts (10–15 minutes).
- **First Sunday of each month:** monthly content review — what worked, what to drop.

## 3. Per-week balance

A healthy week covers:

- **3 LinkedIn posts** — at least one per active brand pillar.
- **1 long-form** (blog or sector report section).
- **1 founder-voice piece** (longer, personal, observational).

We tolerate weeks below this in busy delivery phases — never weeks above.

## 4. Approval gates

| Stage             | Approver                  |
|-------------------|---------------------------|
| Idea              | Content strategist        |
| Draft             | Brand Guardian (verifier) |
| Final approval    | Founder                   |
| Publication       | Human operator            |

## 5. Format rules

| Format                  | Length              | Notes                                  |
|-------------------------|---------------------|----------------------------------------|
| LinkedIn (short)        | ≤ 220 words         | Lead with metric or observation        |
| LinkedIn (long)         | 600–900 words       | One pillar, one persona, one CTA       |
| Blog                    | 800–1,500 words      | AR + EN, side-by-side                  |
| Sector report section   | 1,500–3,000 words    | Footnotes, anonymisation, methodology  |
| Newsletter              | 250–400 words       | One signal + one CTA                   |

## 6. Hold criteria

A piece is **held** (not rejected) if:

- It needs better evidence.
- It would publish during a delivery escalation.
- It conflicts with a pending customer disclosure.

A held piece stays in the queue with a `hold_reason` and reappears in the next review.

## 7. Refusal criteria

A piece is **rejected** (not held) if:

- It uses banned language.
- It auto-translates without human review.
- It identifies a customer without approval.
- It pitches a refused offer to a persona.

## 8. Schema enforcement

The brand verifier requires every row in `content_calendar.csv` to have:

- A pillar tag.
- A persona tag.
- A language tag.
- An evidence cell.

Rows missing any of these fail the verifier.
