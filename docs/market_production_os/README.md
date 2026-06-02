# Dealix Market Production OS — نظام إنتاج السوق

**Status:** Operating system of record for Dealix go-to-market production
**Owner:** Founder (Sami)
**Scope:** Brand → Product Catalog → Sector Intelligence → Prospect Research → Cold Email Draft Factory → Compliance & Deliverability → Founder Approval → Sending Ramp → Reply Handling → Job Signals → Content → Press → Partnerships → WhatsApp Post-Reply → Founder GTM Control Room → Metrics.

> **Purpose / الغرض:** تحويل Dealix إلى ماكينة إنتاج سوق سعودية كاملة: تبني هوية، تبحث الشركات، تطابق العرض بالقطاع، تنتج مسودات شخصية بكثافة، تفحصها ضد الامتثال، ترتّبها للمؤسس، ترسل بتدرّج آمن، تصنّف الردود، وتنتج تقرير GTM يومي — **دون الإضرار بسمعة الدومين ودون مخالفة أي بند من البنود غير القابلة للتفاوض**.

This OS sits **on top of** the existing Dealix doctrine (Revenue OS, Trust gates, commercial chain, Brand Press Kit, founder-approval). It does not replace them. It adds the production layer that turns doctrine into daily commercial output.

---

## The decisive rule — القاعدة الحاسمة

```
كثافة إنتاج عالية في drafts   (High density in drafts)
حذر شديد في sends            (Extreme caution in sends)
تعلّم يومي من replies         (Daily learning from replies)
لا إرسال بلا موافقة          (No send without approval)
لا كولد واتساب               (No cold WhatsApp)
لا وعود بلا proof            (No promises without proof)
```

**250 drafts/day is allowed. 250 sends/day is NOT** — sends are gated by domain health (SPF/DKIM/DMARC), a working opt-out, a live suppression list, and the staged sending ramp. See [`../outreach/SENDING_RAMP_PLAN_AR.md`](../outreach/SENDING_RAMP_PLAN_AR.md).

---

## The 11 non-negotiables — البنود غير القابلة للتفاوض

Enforced in code by passing tests. If any request or in-progress work violates one, **refuse and propose a safe alternative** — never improvise around them.

1. No scraping systems. / لا أنظمة scraping.
2. No cold WhatsApp automation. / لا أتمتة واتساب باردة.
3. No LinkedIn automation. / لا أتمتة LinkedIn.
4. No fake / un-sourced claims. / لا ادعاءات بلا مصدر.
5. No guaranteed sales outcomes. / لا ضمان نتائج مبيعات.
6. No PII in logs. / لا بيانات شخصية في السجلّات.
7. No source-less knowledge answers. / لا إجابات بلا مصدر.
8. No external action without approval. / لا إجراء خارجي بلا موافقة.
9. No agent without identity. / لا وكيل بلا هوية.
10. No project without Proof Pack. / لا مشروع بلا Proof Pack.
11. No project without Capital Asset. / لا مشروع بلا أصل رأسمالي.

**Channel doctrine:** Cold **email** is the primary acquisition channel (PDPL + CAN-SPAM aware). **WhatsApp** is post-reply / opt-in only — never a cold channel. **LinkedIn** is manual only. See [`../outreach/COLD_EMAIL_COMPLIANCE_AR.md`](../outreach/COLD_EMAIL_COMPLIANCE_AR.md).

---

## The 12 machines — الماكينات الاثنتا عشرة

| # | Machine | Goal | Daily output | Spec |
|---|---|---|---|---|
| 1 | Brand Identity OS | Stable, credible identity | brand kit + messaging | [brand/](../brand/) |
| 2 | Product Catalog OS | Clear offers the agent never invents | product/offers | [commercial/PRODUCT_CATALOG_AR.md](../commercial/PRODUCT_CATALOG_AR.md) |
| 3 | Sector Intelligence OS | Knows what fits each company | sector/persona briefs | [sectors/](../sectors/) |
| 4 | Prospect Research OS | Researches + scores companies | prospect records | [outreach/PROSPECT_RESEARCH_OS_AR.md](../outreach/PROSPECT_RESEARCH_OS_AR.md) |
| 5 | Cold Email Draft Factory | 250 drafts/day | drafts queue | [outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md](../outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md) |
| 6 | Personalization Engine | Personalizes per company | pain + offer angle | [outreach/PERSONALIZATION_RULES_AR.md](../outreach/PERSONALIZATION_RULES_AR.md) |
| 7 | Compliance & Deliverability Gate | Prevents bans + spam | pass/fail | [outreach/EMAIL_DELIVERABILITY_POLICY_AR.md](../outreach/EMAIL_DELIVERABILITY_POLICY_AR.md) |
| 8 | Founder Approval Queue | Founder approves fast | approve/edit/reject | [outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md](../outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md) |
| 9 | Sending Ramp OS | Safe staged sending | batches | [outreach/SENDING_RAMP_PLAN_AR.md](../outreach/SENDING_RAMP_PLAN_AR.md) |
| 10 | Reply Handling OS | Classifies + routes replies | reply queue | [outreach/REPLY_HANDLING_OS_AR.md](../outreach/REPLY_HANDLING_OS_AR.md) |
| 11 | WhatsApp Client OS | Post-reply customer experience | assessment + action cards | [outreach/WHATSAPP_POST_REPLY_FLOW_AR.md](../outreach/WHATSAPP_POST_REPLY_FLOW_AR.md) |
| 12 | Metrics & Learning OS | Learns from results | daily/weekly reports | [reports/](../../reports/outreach/) |

Supporting machines: **Job Signal OS** ([signals/](../signals/)), **Content OS** ([content/](../content/)), **Press OS** ([press/](../press/)), **Partnerships OS** ([partnerships/](../partnerships/)), **Founder GTM Control Room** ([reports/outreach/FOUNDER_GTM_CONTROL_ROOM.md](../../reports/outreach/FOUNDER_GTM_CONTROL_ROOM.md)).

---

## Every cold message passes six gates — كل رسالة خارجية تمرّ على ست بوّابات

```
Brand Voice Gate    → tone, banned words, no hype
Offer Match Gate    → offer fits sector + persona
Personalization Gate→ ≥ P1 personalization (unless warm/press)
Compliance Gate     → opt-out present, accurate sender, no misleading subject, no fake Re:/Fwd:, no guaranteed claims, not suppressed
Deliverability Gate → domain health OK, within ramp cap
Founder Approval Gate→ explicit approve before any send
```

If any gate fails, the draft is **not sent**. The gates are implemented in [`dealix/market_production_os/compliance_gate.py`](../../dealix/market_production_os/compliance_gate.py).

---

## Canonical file map — خريطة الملفات

### Docs
- Brand OS: [`docs/brand/`](../brand/) — identity system, messaging house, voice, claims policy, content rules, visual direction, social system, outbound system, asset checklist.
- Product Catalog OS: [`docs/commercial/PRODUCT_CATALOG_AR.md`](../commercial/PRODUCT_CATALOG_AR.md) + offer ladder, pricing guardrails, ICP matrix, buyer personas, objection bank, proof library.
- Sector Intelligence OS: [`docs/sectors/`](../sectors/) — 10 sector briefs.
- Prospect / Outreach OS: [`docs/outreach/`](../outreach/) — prospect research, draft factory, compliance, deliverability, sending ramp, personalization, unsubscribe, reply handling, sequences (AR+EN), LinkedIn manual, WhatsApp post-reply.
- Job Signal OS: [`docs/signals/`](../signals/).
- Content OS: [`docs/content/`](../content/).
- Press OS: [`docs/press/`](../press/).
- Partnerships OS: [`docs/partnerships/`](../partnerships/).

### Schemas — `schemas/`
| File | Record |
|---|---|
| [`schemas/prospect.schema.json`](../../schemas/prospect.schema.json) | Researched + scored company |
| [`schemas/outreach_draft.schema.json`](../../schemas/outreach_draft.schema.json) | A single cold-email draft |
| [`schemas/email_account.schema.json`](../../schemas/email_account.schema.json) | A sending inbox + its domain health |
| [`schemas/sending_batch.schema.json`](../../schemas/sending_batch.schema.json) | An approved batch staged for sending |
| [`schemas/suppression.schema.json`](../../schemas/suppression.schema.json) | A suppressed (opt-out / bounce) address |
| [`schemas/reply.schema.json`](../../schemas/reply.schema.json) | A classified inbound reply |
| [`schemas/job_signal.schema.json`](../../schemas/job_signal.schema.json) | A hiring signal that implies a Dealix need |
| [`schemas/partner.schema.json`](../../schemas/partner.schema.json) | A channel/referral partner |

### Code — `dealix/market_production_os/`
| Module | Responsibility |
|---|---|
| `prospect_scoring.py` | Score + qualify a prospect (weighted rubric) |
| `personalization.py` | P0–P4 personalization-level detection + floor enforcement |
| `draft_factory.py` | Deterministic daily draft production (no external sends) |
| `compliance_gate.py` | The six-gate check over a draft |
| `deliverability.py` | Domain-health (SPF/DKIM/DMARC/...) evaluation |
| `sending_ramp.py` | Allowed sends/day per ramp phase + suppression filter |
| `reply_classifier.py` | Reply taxonomy + routed action |
| `control_room.py` | Assemble the daily GTM report |

Seeds (synthetic, no PII): [`dealix/market_production_os/seeds/`](../../dealix/market_production_os/seeds/).

### Runtime data — `data/` (gitignored; auto-created)
`data/prospects/prospects.jsonl` · `data/outreach/drafts.jsonl` · `data/outreach/sending_batches.jsonl` · `data/outreach/suppression_list.jsonl` · `data/outreach/replies.jsonl` · `data/signals/job_signals.jsonl` · `data/content/post_ideas.jsonl` · `data/partners/partners.jsonl`. Override any path with the matching `DEALIX_*_PATH` env var.

### Reports — `reports/`
`reports/outreach/` (daily draft production, deliverability review, approval queue, reply queue, GTM control room) · `reports/signals/` · `reports/content/` · `reports/press/` · `reports/partnerships/`.

---

## Daily operating rhythm — إيقاع اليوم

| Time | Action |
|---|---|
| 08:00 | Generate up to 250 drafts → run six gates → rank top 50. |
| 10:00 | Founder approves 30–50 → send a limited batch within today's ramp cap. |
| 12:00 | Review + classify replies → generate next drafts. |
| 15:00 | Job signals · partner prospects · press opportunities. |
| 18:00 | Content production · founder post · proof/case draft. |
| EOD | Daily GTM report: drafts generated/approved/sent, replies, meetings, unsubscribes, bounces, best sectors, tomorrow's plan. |

Run the daily production + control room:
```bash
python -m dealix.market_production_os.control_room --date today
```

---

## Metrics — أهم المقاييس

- **Draft:** generated · passed gates · rejected · approved · avg personalization level.
- **Sending:** sent · delivered · bounced · deferred · spam complaints · unsubscribes · reply rate · positive-reply rate.
- **Revenue:** meetings booked · proposals requested · proof packs sent · payment handoffs · won · pipeline value.
- **Brand:** LinkedIn posts · profile visits · press replies · partner replies · inbound requests.
- **Risk (hard ceilings):** spam rate (< 0.3%) · bounce rate (< 3%) · unsub rate · risky claims blocked · do-not-contact count.

Sources: Google Email sender guidelines (SPF/DKIM/DMARC, one-click unsubscribe, spam-rate < 0.3%) and the US CAN-SPAM Act (accurate sender, working opt-out, honored within the legal SLA). See [`../outreach/EMAIL_DELIVERABILITY_POLICY_AR.md`](../outreach/EMAIL_DELIVERABILITY_POLICY_AR.md).

---

## Roadmap mapping — خريطة التنفيذ

This OS was delivered as one branch implementing the full 15-part roadmap (Brand → Product Catalog → Sector Intelligence → Prospect Research → Draft Factory → Compliance/Deliverability → Approval Queue → Sending Ramp → Reply Handling → Job Signals → Content → Press → Partnerships → WhatsApp Post-Reply → Founder GTM Control Room → Metrics & tests).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
