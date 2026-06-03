# نظام تنفيذ الإيراد — Dealix Revenue Execution OS

هذا الملف هو **الخريطة العليا** لنظام تنفيذ الإيراد في Dealix: المراحل من استخبارات السوق حتى التجديد والمقاييس، والقاعدة الأمنية والتجارية الحاكمة، والـ11 بنداً غير القابلة للتفاوض.

This file is the **top-level map** of Dealix's Revenue Execution OS: the stages from market intelligence to renewal and metrics, the governing security/commercial rule, and the 11 non-negotiables.

مصدر الحقيقة للأسعار والنطاق / Pricing & scope source of truth: [../commercial/DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · [../commercial/PRODUCT_CATALOG_AR.md](../commercial/PRODUCT_CATALOG_AR.md)

---

## القاعدة الحاكمة / The governing rule

> **الذكاء الاصطناعي يصوغ. المؤسس يوافق. النظام يتتبّع. الإرسال الخارجي يبقى محكوماً.**
>
> **AI drafts. Founder approves. System tracks. External send stays controlled.**

---

## الخريطة الكاملة / The full map

```text
Market Intelligence → Prospect Scoring → Draft Factory → Approval Queue
→ Follow-up → Proposal → Proof → Payment → Delivery → Renewal
→ Win/Loss → Metrics
```

| المرحلة / Stage | الوصف / Description | الوثيقة / Spec |
|---|---|---|
| استخبارات السوق / Market Intelligence | فهم القطاع والطلب من مصادر مسموحة فقط. / Sector and demand sensing from allowed sources only. | [../commercial/MARKET_INTELLIGENCE_MASTER_INDEX_AR.md](../commercial/MARKET_INTELLIGENCE_MASTER_INDEX_AR.md) |
| تسجيل العملاء المحتملين / Prospect Scoring | تأهيل وتسجيل العميل المحتمل عبر دورة حياة واضحة. / Qualify and score the prospect through a clear lifecycle. | [PROSPECT_OS_AR.md](PROSPECT_OS_AR.md) |
| مصنع المسودات / Draft Factory | صياغة رسائل وعروض كمسودات فقط. / Draft messages and proposals as drafts only. | [DRAFT_SYSTEM_SPEC_AR.md](DRAFT_SYSTEM_SPEC_AR.md) · [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md) |
| طابور الموافقة / Approval Queue | مراجعة المؤسس قبل أي خطوة خارجية. / Founder review before any external step. | [../commercial/APPROVAL_POLICY_AR.md](../commercial/APPROVAL_POLICY_AR.md) |
| المتابعة / Follow-up | جدولة متابعة منضبطة بلا إزعاج. / Disciplined, non-annoying follow-up cadence. | [FOLLOWUP_ENGINE_AR.md](FOLLOWUP_ENGINE_AR.md) |
| العرض / Proposal | عرض مكتمل مربوط بمنتج وسعر معتمد. / A complete proposal linked to a product and approved price. | [PROPOSAL_FACTORY_AR.md](PROPOSAL_FACTORY_AR.md) |
| الدليل / Proof | حزمة دليل بمستوى L0–L5. / A proof pack with an L0–L5 level. | [PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md) |
| الدفع / Payment | تسليم للدفع بعد كل الموافقات — بلا تحصيل آلي. / Handoff to payment after all approvals — no auto-charge. | [PAYMENT_HANDOFF_AR.md](PAYMENT_HANDOFF_AR.md) |
| التسليم / Delivery | تسليم منظّم يمنع الفوضى بعد البيع. / Organized delivery preventing post-sale chaos. | [../delivery/DELIVERY_HANDOFF_AR.md](../delivery/DELIVERY_HANDOFF_AR.md) |
| التجديد / Renewal | تجديد وتوسعة بعد دورة قيمة ودليل. / Renewal and expansion after a value cycle and proof. | [RENEWAL_ENGINE_AR.md](RENEWAL_ENGINE_AR.md) |
| الربح/الخسارة / Win/Loss | تعلُّم موثَّق من كل نتيجة. / Documented learning from every outcome. | [WIN_LOSS_LEARNING_AR.md](WIN_LOSS_LEARNING_AR.md) |
| المقاييس / Metrics | مؤشرات يومية وأسبوعية. / Daily and weekly KPIs. | [DISTRIBUTION_METRICS_AR.md](DISTRIBUTION_METRICS_AR.md) |

---

## الكيانات الآلية / Machine-readable entities

تُستخدم أسماء الحقول التالية **حرفياً** في كل الوثائق لتطابق المخططات (schemas):

The following field names are used **verbatim** across all docs to match the schemas:

- **prospect:** `id`, `company`, `sector`, `region`, `source`, `decision_maker`, `status`, `pain_hypothesis`, `offer_angle`, `estimated_value_sar`, `confidence`, `preferred_channel`, `last_contact_at`, `next_action`, `next_action_date`, `risk`, `evidence_level`
- **draft:** `id`, `prospect_id`, `draft_type`, `channel`, `locale`, `subject`, `body`, `status`, `governance_status`, `quality_issues`, `evidence_level`, `created_at`, `product_id`
- **followup:** `id`, `prospect_id`, `due_date`, `channel`, `message_ref`, `status`, `risk`
- **proposal:** `id`, `prospect_id`, `product_id`, `sector`, `problem`, `proposed_solution`, `scope`, `out_of_scope`, `timeline`, `price_min_sar`, `price_max_sar`, `assumptions`, `evidence_level`, `risks`, `payment_terms`, `next_step`, `approval_status`
- **proof_pack:** `id`, `customer_id`, `current_process`, `leakage_points`, `quick_win`, `before_after`, `measurement_method`, `evidence_level`, `risk`, `recommended_pilot`
- **payment_handoff:** `id`, `proposal_id`, `customer_id`, `product_id`, `amount_sar`, `status`, `approvals` (`proposal_approved` / `scope_confirmed` / `price_confirmed` / `decision_maker_confirmed` / `risk_reviewed` / `founder_approved`)
- **delivery_handoff:** `id`, `customer_id`, `product_sold`, `scope`, `timeline`, `success_metric`, `first_workflow`, `required_access`, `owner`, `risks`, `next_meeting`
- **renewal:** `schedule_id`, `customer_id`, `plan`, `amount_sar`, `next_attempt_at`, `status`
- **win_loss:** `id`, `company`, `sector`, `offer`, `channel`, `outcome`, `reason`, `objection`, `lesson`, `next_change`

---

## الـ11 بنداً غير القابلة للتفاوض / The 11 non-negotiables

1. **الذكاء الاصطناعي يصوغ، المؤسس يوافق، النظام يتتبّع.** / AI drafts, founder approves, system tracks.
2. **لا إرسال خارجي آلي في الإصدار الأول (v1).** / No automated external send in v1.
3. **لا واتساب بارد.** / No cold WhatsApp.
4. **لا أتمتة LinkedIn.** / No LinkedIn automation.
5. **لا scraping.** / No scraping.
6. **كل المسودات بحالة انتظار موافقة.** / All drafts pending approval.
7. **لا ادعاءات مضمونة** (لا أرقام مبيعات/تحويل/ROI كحقيقة). / No guaranteed claims.
8. **لا PII في السجلات** (بريد/هاتف/هوية/أسماء حقيقية). / No PII in logs.
9. **مدعوم بالأدلة (L0–L5)** لكل ادعاء. / Evidence-backed (L0–L5) for every claim.
10. **ربط كل عرض بمنتج من الكتالوج** عبر `product_id`. / Link every offer to a catalog product.
11. **لا نشر إنتاجي ولا أسرار** ضمن هذا النظام. / No production deploy, no secrets.

> هذه البنود تُحترَم في كل وثيقة لاحقة، ولا يجوز لأي مرحلة تجاوزها. / These are honored across every downstream doc; no stage may bypass them.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
