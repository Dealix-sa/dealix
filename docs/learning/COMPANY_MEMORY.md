---
title: Company Memory
owner: Founder
status: active
last_review: 2026-05-23
---

# Company Memory — الذاكرة المؤسسية

## Purpose

Define what Dealix remembers, where it is written, and how it is found six months later. The company memory is the union of decisions, kills, doubles, and shipped capital. It is not the chat log. It is not the inbox.

## What gets captured

| Artifact | Location | Retention |
|---|---|---|
| Decisions | `dealix-ops-private/decisions/YYYY-MM-DD.md` | permanent |
| Kills (what we stopped doing) | `dealix-ops-private/decisions/kills.md` | permanent |
| Doubles (what we doubled down on) | `dealix-ops-private/decisions/doubles.md` | permanent |
| Weekly review notes | `dealix-ops-private/learning/weekly/` | 24 months |
| Monthly strategy notes | `dealix-ops-private/learning/monthly/` | permanent |
| Capital assets | [docs/09_capital_os/CAPITAL_LEDGER.md](../09_capital_os/CAPITAL_LEDGER.md) | permanent |
| Productization candidates | [docs/09_capital_os/PRODUCTIZATION_LEDGER.md](../09_capital_os/PRODUCTIZATION_LEDGER.md) | permanent |
| Proof packs | [docs/07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) | permanent |
| Incidents | `dealix-ops-private/incidents/` | permanent |

## Definitions

- **Decision** — a written commitment with: context, options considered, choice, reversibility, owner, date.
- **Kill** — a line of work intentionally stopped. Must cite the law or signal that triggered it.
- **Double** — a line of work intentionally amplified. Must cite the evidence base.
- **Asset** — a reusable artifact: template, playbook, prompt, schema, dataset, dashboard.

## Operations

1. Every Sunday review emits at least one entry to decisions, kills, or doubles — or an explicit "none this week".
2. Every promotion in the [LEARNING_ROUTER.md](./LEARNING_ROUTER.md) writes an asset row.
3. Every quarter, the founder reads the kills file end to end. If a killed item is silently back in scope, it is logged.
4. Memory is queryable by tag and date. If a question takes more than five minutes to answer, the indexing is broken — fix it.

## Evidence

- Memory files live in the private ops repo with commit history.
- Cross-link from any doc that references "we decided" or "we stopped" back to the dated decision file.

## Owner & cadence

- Founder owns this page.
- Reviewed monthly. Quarterly read-through of the kills file.

## AR — ملخّص

الذاكرة المؤسسية لديليكس هي اتحاد القرارات والإيقافات والمضاعفات والأصول الموثّقة. تُكتب في ملفات مؤرّخة في المستودع الخاص، ولها مالك وإيقاع. لا نعتمد على المحادثات؛ نعتمد على ملفات قابلة للبحث. القيمة التقديرية ليست قيمة مُتحقَّقة.
