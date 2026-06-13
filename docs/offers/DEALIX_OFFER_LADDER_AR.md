# Dealix Offer Ladder

> **Status:** 6 offers, all productized, none with a final price.
> **Default first offer:** `Revenue Leak Audit` (3–5 days).
> **Pricing policy:** all `pricing_status: draft_only` until founder approves a range.

The ladder is sequenced by **trust before upsell**. The first offer is the door. The next four are the room. The last is the floor you build on once the room is full.

## The ladder

| # | Offer | Length | Buyer | What it proves | Pricing status |
| -- | --- | --- | --- | --- | --- |
| 1 | Revenue Leak Audit | 3–5 days | Owner / GM | Dealix can read their mess and name 10 specific losses | `draft_only` |
| 2 | WhatsApp & Follow-up OS | 2–4 weeks | Sales lead | Dealix can be deployed with consent and produce daily digests | `approved_range_required` |
| 3 | Sales Command Center | 4–6 weeks | Founder / GM | Dealix can be the daily decision layer for the founder | `approved_range_required` |
| 4 | Proposal & Proof Pack OS | 4–8 weeks | Sales lead | Dealix can produce proof-bearing proposals on demand | `approved_range_required` |
| 5 | AI Operating System for SMB | 8–12 weeks | Founder | Dealix can be the OS layer above CRM + content + reporting | `founder_approval_required` |
| 6 | Custom Enterprise OS | 12+ weeks | COO / VP | Dealix can be customized to the enterprise's specific ops | `founder_approval_required` |

## One-line card per offer (the print version)

### 1. Revenue Leak Audit (3–5 days)

> نطلع لك 10 فرص ضايعة + 10 إصلاحات + خطة أسبوع. بدون ربط، بدون عقد، بدون سعر في العرض.

**Target:** agency owner, training center owner, founder of a 5–50 person company.
**Promise without overclaim:** "نحدد على الأقل 10 فرص ضايعة في 5 أيام."
**Proof needed:** case study of the first audit (after delivery).
**Card:** `docs/offers/REVENUE_LEAK_AUDIT_OFFER_AR.md`.

### 2. WhatsApp & Follow-up OS (2–4 weeks)

> نرتب الواتساب والـ inbox عندك. routing، تصنيف، قوالب، تقارير يومية، approval قبل أي رد.

**Target:** sales lead, customer success lead.
**Promise without overclaim:** "نخفض وقت فرز الواتساب من 40 دقيقة إلى 5 دقائق."
**Card:** `docs/offers/WHATSAPP_FOLLOWUP_OS_OFFER_AR.md`.

### 3. Sales Command Center (4–6 weeks)

> لوحة قيادة يومية للمدير العام: pipeline، follow-ups، approvals، stuck deals، next action.

**Target:** founder, GM.
**Promise without overclaim:** "تشوف كل يوم 5 أشياء محددة تحتاج قرار."
**Card:** `docs/offers/SALES_COMMAND_CENTER_OFFER_AR.md`.

### 4. Proposal & Proof Pack OS (4–8 weeks)

> نولّد عروض مدعومة بـ proof packs. كل claim له evidence_level. كل عرض له payment handoff يحتاج موافقة.

**Target:** sales lead, founder.
**Promise without overclaim:** "نخفض وقت إعداد العرض من 4 ساعات إلى 30 دقيقة."
**Card:** `docs/offers/PROPOSAL_PROOF_PACK_OS_OFFER_AR.md`.

### 5. AI Operating System for SMB (8–12 weeks)

> نظام تشغيل كامل للشركة: workflows + dashboards + reports + draft factory + approval gates.

**Target:** founder of a 30+ person company.
**Promise without overclaim:** "تشغّل الشركة على نظام واحد واضح."
**Card:** `docs/offers/AI_OPERATING_SYSTEM_FOR_SMB_OFFER_AR.md`.

### 6. Custom Enterprise OS (12+ weeks)

> حل مخصص للعمليات المعقدة: discovery, architecture, implementation, governance, training.

**Target:** COO, VP Operations.
**Promise without overclaim:** "نبني النظام على العمليات مالتك، مش على template."
**Card:** `docs/offers/CUSTOM_ENTERPRISE_OS_OFFER_AR.md`.

## Pricing policy

Read `docs/offers/PRICING_LOGIC_AND_APPROVAL_POLICY_AR.md` for the full policy. The summary:

| Status | Meaning | Allowed in |
| --- | --- | --- |
| `draft_only` | No number has been set. Founder can quote. | First 5 deals, founder-quoted |
| `approved_range_required` | A range (e.g. SAR 25k–40k) is approved. Founder finalizes per deal. | After first 5 deals, ranges are approved |
| `founder_approval_required` | Per-deal approval; no range yet. | Custom Enterprise OS, anything > SAR 100k |
| `final_approved` | (not used in week 1) | Never for custom work |

**Never** put a final price in a draft. **Never** generate a payment link. **Never** write a number in a public doc.

## Upsell motion

After the audit (offer 1), the natural sequence is:

- Audit → 1 paid pilot in offer 2 or 3.
- Offer 2 → 3 (WhatsApp OS is the natural door to Command Center).
- Offer 3 → 4 (Command Center surfaces the need for Proposal OS).
- Offer 4 → 5 (Proposal OS unblocks AI OS for SMB).
- Offer 5 → 6 (SMB AI OS at scale becomes Enterprise).

The motion is **one offer at a time**, never the whole ladder in one pitch.

## Cross-offer risks

| Risk | Mitigation |
| --- | --- |
| Founder pitches the whole ladder in the audit debrief | The audit deliverable is the report. The debrief is 30 min. No deck. |
| Client wants offer 5 without offers 1–4 | Push back. Offer 5 needs the trust and the data. Without offers 1–4, the engagement is brittle. |
| Client says "send me a proposal" before the audit | Don't. Send a discovery summary + audit offer. The audit is the door. |

## What's NOT an offer

- "Custom AI for our company" — too vague. Map to one of the 6.
- "Training" — content is in offer 3 or 5, not standalone.
- "Free consulting" — protect the founder's time. The audit is paid or free; the conversation is not free.
