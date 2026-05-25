---
title: Message Performance
owner: Content Lead
status: active
last_review: 2026-05-23
---

# Message Performance — أداء الرسائل

## Purpose

Measure how Dealix written messages perform — proposals, sample summaries, intro DMs sent only with consent or via warm channels, and email follow-ups. The goal is to keep what evidences fit and kill what does not, without ever promising a result.

## What gets measured

| Surface | Metric | Source |
|---|---|---|
| Intro DM (warm/consented) | reply rate, qualified-reply rate | DM log |
| Sample summary | open rate, share rate, meeting booked | tracked link |
| Proposal | proposal-to-signed rate, days to decision | CRM |
| Follow-up email | reply rate, opt-out rate | email log |
| Case-safe summary | meeting-booked rate when attached | proposal log |

## Non-negotiables

- No bulk outreach. No scraping. No LinkedIn automation. No cold WA automation.
- Every measured surface is one where the recipient is either an existing contact, a warm intro, or has explicitly opted in.
- Variants compared are on identical recipients shape, not cherry-picked.
- No claim is added to a variant to lift performance if the claim is not verified.

## What gets logged per variant

```yaml
variant_id: MSG-YYYY-NNN
surface: dm | sample | proposal | follow_up | case_safe
hypothesis: "Variant changes X; expected lift on Y."
recipients_n: n
period: YYYY-WW range
metric_primary: name, value
metric_guardrail: opt-out rate, complaint rate
winner: yes | no | inconclusive
decision: keep | kill | iterate
linked_experiment: EXP-id (optional)
```

## Operations

1. Content Lead drafts variant and files the row before sending.
2. Minimum sample size set per surface (see internal table in `dealix-ops-private/learning/message_minimums.md`).
3. After the period closes, the row is filled and the signal sent to the [LEARNING_ROUTER.md](./LEARNING_ROUTER.md).
4. Winners are promoted to templates after the fifth replication per the Learning Rule.

## Evidence

- Variant log: `dealix-ops-private/learning/message_variants.csv`.
- Sample assets stored alongside.

## Owner & cadence

- Content Lead reviews weekly.
- Founder reviews monthly aggregate at the strategy update.

## AR — ملخّص

أداء الرسائل يُقاس على سطوح موافق عليها فقط: DM دافئ، ملخّص عيّنة، عرض، متابعة. كل نسخة لها بطاقة قبل الإرسال ومقياس أساسي وحارس (نسبة الانسحاب/الشكوى). الفائزون يترقّون قوالب بعد خمس تكرارات. لا ادّعاء غير متحقّق. القيمة التقديرية ليست قيمة مُتحقَّقة.
