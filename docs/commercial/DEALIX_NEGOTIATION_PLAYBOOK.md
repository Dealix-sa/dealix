# Dealix Negotiation Playbook

How the engine negotiates, handles objections, and proves value — without
promising results or dropping price first.

## Core principle

> We do not guarantee revenue. We prove where opportunities leak and measure the
> improvement during a pilot.

Arabic: **لا نقول "نضمن زيادة الإيرادات". نقول "نثبت أين تضيع الفرص ونقيس التحسن خلال pilot".**

## Concession rules (in order)

1. لا تخفض السعر مباشرة. — Never drop price first.
2. قلل النطاق بدل السعر. — Reduce scope instead of price.
3. ابدأ بـ pilot صغير. — Start with a small pilot.
4. اطلب إذن proof بدل خصم. — Ask for proof permission instead of a discount.
5. اربط الدفع بمخرج واضح. — Tie payment to a clear deliverable.
6. لا تعد بنتيجة غير مضمونة. — Never promise an uncertain result.
7. لا تقبل نطاقًا مفتوحًا بدون سعر. — No open scope without a price.

## Offer ladder used for matching

| Offer | Price | Best fit |
|---|---|---|
| Revenue Proof Sprint | 499 SAR | Lost follow-up, needs fast proof |
| Saudi Opportunity Snapshot | 499–1,500 SAR | Foreign / market-entry |
| Revenue Leak Diagnostic | 4,999 SAR | Has sales team, leaking leads |
| Saudi Market Access Sprint | 8,000–20,000 SAR | Foreign entrant, needs partners |
| B2G Readiness Sprint | 10,000–50,000 SAR | Enterprise readiness (no gov-access claims) |
| Revenue Command Room Retainer | monthly | Needs daily ops |

## Objection bank (excerpt)

Each objection returns: understanding → short reply → detailed reply →
follow-up question → negotiation move → proof needed. Full bank in
`data/dealix_conversation_negotiation/objections.json`.

| Trigger (AR) | Move | Proof needed |
|---|---|---|
| السعر غالي | reduce_scope_not_price | sample_proof_pack |
| وش تسوون بالضبط؟ | show_sample | one_page_snapshot |
| هل أنتم CRM؟ | position_as_layer | integration_note |
| ما نحتاج AI | focus_outcome_not_tech | one_page_snapshot |
| عندنا فريق مبيعات | augment_not_replace | followup_gap_estimate |
| ما عندنا ميزانية | smallest_paid_entry | sample_proof_pack |
| كيف تثبتون القيمة؟ | measure_dont_promise | proof_pack |
| هل تضمنون نتائج؟ | measure_dont_promise | proof_pack |
| هل تحتاجون صلاحيات على بياناتنا؟ | minimal_scoped_access | data_handling_note |
| هل ترسلون للعملاء نيابة عنا؟ | approval_first_reassurance | approval_policy_note |

## Negotiation plan shape

```json
{
  "target": "…",
  "offer": "…",
  "starting_position": "…",
  "minimum_commitment": "pilot صغير (7 أيام)…",
  "value_proof": "…",
  "likely_objections": [],
  "response_strategy": [],
  "concession_rules": [],
  "close_question": "…",
  "next_best_action": "إرسال ملخص صفحة واحدة للاعتماد (draft-only).",
  "approval_required": true
}
```

## Proof-of-value

Allowed measures: reply rate, qualified opportunities, follow-ups created,
missed leads detected, time saved, pipeline clarity, meetings booked after
approval, proof pack delivered.

Forbidden: guaranteed revenue/ROI, fabricated numbers, fake testimonials,
government access, guaranteed contracts. `proof_builder.validate_proof_pack`
enforces this on every pack.

## Trust reassurance

- **"هل ترسلون نيابة عنا؟"** → No auto-send. We prepare drafts; you approve in
  the approval queue before anything goes out.
- **"هل تحتاجون صلاحيات؟"** → Start with a small sample you share yourself
  (PDPL-aware); any access is explicit and scoped.
