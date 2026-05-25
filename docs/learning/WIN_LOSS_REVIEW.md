---
title: Win/Loss Review
owner: Sales Lead
status: active
last_review: 2026-05-23
---

# Win/Loss Review — مراجعة الفوز والخسارة

## Purpose

Every closed deal — won or lost — is categorized within seven days of closure. The output is a single row in the win/loss ledger and one promoted signal where the pattern repeats.

## Definitions

- **Won** — signed proposal or paid invoice.
- **Lost** — explicit no, ghosted past 21 days, or budget pulled.
- **Root cause** — the one factor that most influenced the outcome. One per deal.

## Root-cause categories

| Code | Name | Examples |
|---|---|---|
| FIT | Sector fit | wrong size, wrong stage, wrong sector |
| PRICE | Price | budget mismatch, anchor too high or low |
| PROOF | Proof gap | no relevant case-safe summary in sector |
| TIMING | Timing | quarter close, fiscal freeze, leadership change |
| SCOPE | Scope clarity | scope unclear, deliverables not concrete |
| TRUST | Trust signal | references missing, evidence chain weak |
| CHANNEL | Channel | warm intro vs cold path, sponsor seniority |
| COMPETE | Competition | named alternative chose us / chose them |
| INTERNAL | Internal capacity | we declined or paused due to capacity |

## Process (per closed deal)

1. Sales Lead opens the deal record within seven days of closure.
2. Fill the win/loss row: deal id, sector, ACV band, sponsor role, days from first contact to close, root cause code, one paragraph of evidence.
3. If lost, attempt a 10-minute closing call with the buyer to confirm the root cause. Record consent.
4. File the row in `dealix-ops-private/learning/win_loss.csv`.
5. Send the signal to the [LEARNING_ROUTER.md](./LEARNING_ROUTER.md) with tag `win_loss`.

## Promotion thresholds

- Three deals lost on the same root cause in a quarter → playbook update.
- Five deals lost on the same root cause in a quarter → template change or scope rule.
- Three deals won on the same pattern → case-safe summary candidate per [docs/07_proof_os/CASE_SAFE_SUMMARY.md](../07_proof_os/CASE_SAFE_SUMMARY.md).

## Evidence

- Win/loss CSV in private ops repo.
- Closing-call notes stored with consent record.
- Aggregated quarterly view feeds [SECTOR_PERFORMANCE.md](./SECTOR_PERFORMANCE.md) and [PRICING_LEARNING.md](./PRICING_LEARNING.md).

## Owner & cadence

- Sales Lead owns the row within seven days of closure.
- Founder reviews aggregated patterns at the monthly strategy update.

## AR — ملخّص

كل صفقة مغلقة (فوز أو خسارة) تُصنّف خلال سبعة أيام بسبب جذر واحد من قائمة محدّدة. ثلاث خسائر بنفس السبب تُحرّك playbook، وخمس تُحرّك قالباً أو قاعدة نطاق. ثلاث فوزات بنفس النمط تفتح ملخّصاً آمن الحالة. القيمة التقديرية ليست قيمة مُتحقَّقة.
