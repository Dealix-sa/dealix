# Nurture Machine

> Keeps B/C accounts warm without spamming them.

## 1. Purpose

Maintain a respectful, low-frequency nurture stream for **B** and **C** priority accounts so we are top-of-mind when their priority shifts to A.

## 2. Input

- Accounts with `final_priority` in {B, C} from `data/growth/account_scores.csv`.
- Content drafts approved by Inbound Content Machine.
- Sector reports.

## 3. Output

- Monthly bilingual nurture digest (1 piece of content + 1 sector signal).
- Quarterly sector report mailing.
- Re-scoring trigger after each nurture cycle.

## 4. Cadence

| Priority | Touches per quarter | Channels                              |
|----------|---------------------|---------------------------------------|
| B        | 3                   | Email + LinkedIn (founder-approved)   |
| C        | 1                   | Email only (founder-approved)         |

## 5. Approval class

**A1.** Founder approves each batch.

## 6. Worker name

`nurture_worker`.

## 7. KPI

- ≥ 95% of B accounts receive ≥ 3 touches per quarter (queue-side).
- ≥ 90% of C accounts receive 1 touch per quarter.
- Re-scoring rate: ≥ 30% of B accounts re-scored quarterly.
- Unsubscribe rate: < 0.5%.

## 8. Doctrine

- One unsubscribe link in every email. Honoured permanently.
- Never re-add an unsubscribed contact (verifier-enforced).
- Nurture content is **valuable on its own** — sector insight, not "checking in".

## 9. Failure modes

| Failure                                      | Recovery                                        |
|----------------------------------------------|-------------------------------------------------|
| Touch frequency exceeds cap                  | Suppress; founder reviews                       |
| Same content sent twice to same contact      | Refuse                                          |
| Unsubscribed contact re-appears              | Refuse; flag                                    |
