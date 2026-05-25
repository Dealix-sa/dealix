---
title: Autonomy Policy
owner: Trust Lead
status: active
last_review: 2026-05-23
---

# Autonomy Policy — سياسة الاستقلالية

## Purpose

State plainly what Dealix agents may do without a human, and what they may never do alone. The rule: **Agents prepare. Humans approve critical moves. A3 never executes automatically.**

## What agents may do (A0)

- Draft proposals, emails, reports into private staging.
- Enrich a lead from public sources (company website, official registries).
- Score leads against the rules in [docs/delivery/revenue_sprint/SCORING_RULES.md](../delivery/revenue_sprint/SCORING_RULES.md).
- Run schema validation, claim filtering, redaction.
- Write internal notes, summaries, retros.
- Query the AI Run Ledger.

## What agents may prepare but never send (A1+)

- Outbound messages to a buyer (WhatsApp, email, LinkedIn DM).
- Proposals or quotes leaving the staging area.
- Public posts.
- Invoices or payment links.

## What agents may never do (hard block)

- Scrape sites that prohibit it, or any closed platform.
- Send cold WhatsApp at scale or automate LinkedIn outreach.
- Sign contracts, accept POs, or commit Dealix to a counterparty.
- Make regulator or legal communications (A3).
- Issue refunds.
- Publish anything to a public repo or public channel.
- Fabricate evidence, customers, metrics, or outcomes.

## Operational rule

Every agent run carries a `governance_status` field. Values:

- `auto_ok` — A0, action completed.
- `pending_approval` — A1 or A2, parked in queue.
- `external_review_required` — A3, parked plus reviewer assigned.
- `blocked` — violated a hard rule; routed to [INCIDENT_RESPONSE.md](./INCIDENT_RESPONSE.md).

## Failure mode handling

If an agent tries to execute outside its autonomy:

1. The action is blocked.
2. An incident is auto-opened.
3. The agent is paused until a human resumes it.

## Evidence

- `ai_run_ledger.jsonl` carries `governance_status` and `autonomy_band` on every row.
- Blocked attempts produce an incident file.

## Cross-links

- [APPROVAL_MATRIX.md](./APPROVAL_MATRIX.md) — level definitions.
- [TRUST_CONTROL_SYSTEM.md](./TRUST_CONTROL_SYSTEM.md) — C-06 kill switch.
- [docs/02_saudi_positioning/WHATSAPP_BOUNDARY.md](../02_saudi_positioning/WHATSAPP_BOUNDARY.md) — channel limits.

## Owner & cadence

- Trust Lead owns this policy. Reviewed quarterly and after any incident.

## AR — ملخّص

الوكلاء يُجهّزون، والبشر يوافقون على الخطوات الحرجة، والمستوى A3 لا يُنفَّذ آليًا أبدًا. كل تشغيل يحمل حالة حوكمة، وأي محاولة لتجاوز الحدود تُغلق فورًا وتُفتح لها حادثة. القيمة التقديرية ليست قيمة مُتحقَّقة.
