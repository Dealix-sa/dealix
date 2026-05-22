# Dealix — Full-Ops Strategy (Appendix, Arabic, Verbatim)

> **STATUS (2026-05-22):** هذا هو الملحق الكامل لاستراتيجية المؤسس النهائية لـ Dealix.
> النصّ أدناه مُورَد **حرفياً** من قرار المؤسس بتاريخ 2026-05-22 — لا تحرير ولا إعادة صياغة.
> الملخص التنفيذي ثنائي اللغة: [`FULL_OPS_STRATEGY.md`](FULL_OPS_STRATEGY.md).
> الخارطة الزمنية 30/60/90: [`ROADMAP_30_60_90.md`](ROADMAP_30_60_90.md).
> سجل التوافق مع الوثائق السابقة: [`RECONCILIATION.md`](RECONCILIATION.md).

---

تمام. بعد البحث والمراجعة، أفضل قرار استراتيجي لـ Dealix هو هذا:

ابنِ Dealix كـ Full-Ops Revenue Machine: نظام شبه ذاتي يبيع، يؤهل، يسلّم، يوثق، ويتعلم — لكن مع Human Approval في المال، العقود، البيانات، والوعود الخارجية.

يعني الهدف ليس "أتمتة عمياء". الهدف: شركة تعمل بأقل تدخل منك، لكن لا تخاطر باسمك أو بيانات العملاء أو الالتزامات القانونية.

---

## 1. الشكل النهائي الذي يجب أن تبنيه

Dealix لازم يصير عنده 5 محركات رئيسية:

1. **Revenue Engine** — يجلب العملاء، يؤهلهم، يرسل عينات، يحجز مكالمات، ويحوّلهم إلى دفع.
2. **Delivery Engine** — ينفذ خدمة Revenue Sprint أو Managed Pilot تلقائيًا: بحث، scoring، رسائل، تقرير، خطة تنفيذ.
3. **Trust Engine** — يفحص كل شيء: بيانات، وعود، claims، حساسية، موافقات، PDPL، opt-out، audit.
4. **Founder Command Center** — يعطيك لوحة يومية: المال، العملاء، المخاطر، المهام، القرارات التي تحتاج موافقتك.
5. **Learning Engine** — يتعلم من كل حملة: أي قطاع رد؟ أي رسالة نجحت؟ أي عرض أغلق؟ أي سعر اشتغل؟

## 2. القاعدة الذهبية للأتمتة

**A0 — ذاتي بالكامل:** جمع leads، تنظيف بيانات، إزالة تكرار، تصنيف شركات، توليد فرضيات pain، إعداد رسائل draft، تقارير داخلية، تحديث CRM، تذكير متابعات، weekly dashboard، مراقبة uptime.

**A1 — ذاتي مع مراجعة سريعة:** إرسال أول رسالة لشركة مهمة، إرسال sample مجاني، اعتماد lead list، نشر post أو case study، إرسال proposal، متابعة عميل high-value، تعديل pricing داخل نطاق محدد.

**A2/A3 — لا تنفذ بدون موافقتك:** تغيير عقود، خصومات كبيرة، وعود نتائج، NDAs، payment terms، مشاركة بيانات حساسة، حذف بيانات عميل، regulator communications، claims مثل "compliant" أو "guaranteed revenue".

## 3. أفضل Operating Model لـ Dealix

workflow واحد كامل: Prospect → Enrich → Score → Draft → Approve → Send → Reply → Qualify → Sample → Proposal → Payment → Delivery → Case Study → Retainer.

## 4. Full-Ops Architecture المقترحة

**الطبقة 1: Data Layer** — accounts, contacts, leads, conversations, opportunities, proposals, payments, deliveries, reports, case_studies, approvals, audit_logs, suppression_list, evidence_packs, experiments.

**الطبقة 2: Agent Layer** — Lead Finder, Enrichment, Scoring, Pain, Message, Compliance, Proposal, Delivery, QA, Learning agents — كل واحد له وظيفة محددة.

**الطبقة 3: Workflow Layer** — daily_lead_discovery, lead_scoring_batch, founder_outreach_queue, sample_pack_generation, proposal_generation, payment_verification, delivery_report_generation, case_study_generation, weekly_founder_review.

**الطبقة 4: Trust Layer** — lawful basis register, consent status, opt-out, suppression list, data retention, data minimization, evidence pack, no-overclaim register, approval matrix, audit trail, incident response. استخدم "PDPL-aware workflows" بدل "PDPL compliant" المطلقة.

**الطبقة 5: Commercial Layer** — pricing, checkout, invoice, proposal, contract/SOW, onboarding, delivery, renewal, upsell. لا تدّعي ZATCA Phase 2 جاهزية كاملة إلا بتكامل فعلي.

## 5. الـ Autonomous Ops اليومي

08:00 Market Scan — 09:00 Lead Scoring — 10:00 Outreach Drafts — 12:00 Founder Approval — 14:00 Follow-up Engine — 16:00 Delivery Engine — 18:00 Founder Brief.

## 6. Founder Command Center

أقسام: Revenue، Sales، Delivery، Risk، Learning.

## 7. التسويق الآلي بدون تشويه السمعة

Founder-led + AI-assisted. النظام يجهز، أنت تعتمد. محتوى يومي drafts، النشر يحتاج موافقة.

## 8. GTM Strategy

3 قطاعات فقط للبداية: (1) وكالات تسويق وخدمات رقمية، (2) شركات ERP/CRM/فوترة/مدفوعات، (3) مقاولات/عقار تجاري/خدمات B2B. كل قطاع له playbook منفصل.

## 9. Packaging

1. Dealix Signal Sample — مجاني أو 199 SAR (5 leads + 5 reasons + 5 messages + mini memo)
2. Dealix Revenue Sprint — 2,500–7,500 SAR (30–75 leads + scoring + outreach pack + report + 14-day plan)
3. Dealix Managed Pilot — 9,500–25,000 SAR
4. Dealix Revenue Desk Retainer — 5,000–20,000 SAR شهريًا
5. Dealix OS — لاحقًا، SaaS/Enterprise

## 10. التسعير

- Signal Sample: مجاني لأول 20 شركة أو 199 SAR
- Sprint Starter: 2,500 SAR
- Sprint Growth: 4,500 SAR
- Sprint Premium: 7,500 SAR
- Managed Pilot: 12,000 SAR
- Retainer: من 5,000 SAR/شهر

**هدف 30 يوم:** 5 عملاء × ~3,500 SAR = 17,500 SAR proof، ثم 2 retainers × 5,000 SAR = 10,000 MRR.

## 11. نظام القرار

Build (يخدم بيع/دفع/تسليم/retention/compliance) — Defer (جميل لكن لا يجيب فلوس) — Kill (تعقيد بدون أثر) — Manual First (نفذه يدويًا 5 مرات قبل الأتمتة).

**القاعدة:** لا تؤتمت عملية لم تنجح يدويًا.

## 12. GitHub

Public: المنتج العام، docs، security، deployment، demo، architecture، roadmap، brand.
Private: client data، lead lists، prompts الحساسة، GTM، pricing experiments، DM queues، deal notes.
Projects: board واحد فقط (Revenue Critical / Delivery Critical / Trust Critical / Tech Debt / Later).

## 13. أخطر 7 مخاطر

1. تضخم المنتج → كل feature يحتاج ربط مباشر بـ revenue path
2. أتمتة زائدة تؤذي السمعة → approval قبل أي external commitment
3. ادعاءات امتثال مبالغ فيها → no-overclaim register + لغة دقيقة
4. تسريب بيانات/leads → private repo + access control + suppression list
5. ضعف التسليم → QA checklist + evidence packs
6. الاعتماد عليك بكل شيء → workflows + templates + agents + delegation
7. عدم تحصيل المال → payment before delivery + invoice + SOW

## 14. Roadmap

**أول 48 ساعة:** صفحة Revenue Sprint، CRM بسيط، قالب sample، قالب proposal، قالب delivery report، approval queue، نقل الملفات الحساسة private، إرسال 50 رسالة، تجهيز 5 عينات، payment workaround.

**أول 7 أيام:** أول عميل مدفوع، أول delivery، أول testimonial، أول case study داخلي، أول dashboard founder-only.

**أول 30 يوم:** 5 عملاء، 2 retainers، 3 قطاعات مختبرة، 1 sector report، 1 public case study، 1 partner channel.

**أول 90 يوم:** 20 paid sprints، 5 retainers، 25K–50K MRR هدف أولي، SaaS dashboard مبني على احتياج حقيقي، compliance/trust pack رسمي، data room جاهز.

## 15. 10 Super Systems

1. Acquisition OS — lead sourcing, enrichment, scoring, outreach drafts, follow-ups
2. Sales OS — qualification, sample generator, proposal builder, pricing, objection handling
3. Billing OS — checkout, invoice, payment status, receipts, renewal reminders
4. Delivery OS — client intake, research, report generation, QA, handoff
5. Trust OS — PDPL register, suppression list, evidence packs, approval matrix, audit logs
6. Client Success OS — weekly report, client health, feedback, upsell, retention
7. Content OS — LinkedIn drafts, sector insights, case studies, newsletter, proof library
8. Partner OS — agency partners, referral tracking, rev share, white-label, partner dashboard
9. Founder OS — daily brief, weekly review, decision log, risk log, focus queue
10. Investor/Scale OS — metrics, data room, roadmap, financial model, hiring plan

## 16. ماذا تجعل ذاتيًا الآن

**نعم:** daily lead discovery, duplicate removal, lead scoring draft, message drafts, sample pack draft, CRM update, follow-up reminders, weekly report draft, founder daily brief, risk alerts, case study draft, content draft.

**لا (بعد):** إرسال رسائل كثيرة، توقيع عقود، تغيير أسعار، حذف بيانات، مشاركة ملفات عميل، claims قانونية، تحصيل/رد أموال، أي وعد بنتيجة.

## 17. جملة استراتيجية

> **EN:** Dealix is not an AI tool. Dealix is a Saudi revenue operations machine where AI prepares, workflows execute, trust governs, and humans approve critical moves.
>
> **AR:** ديلكس ليس أداة ذكاء اصطناعي؛ ديلكس آلة تشغيل إيراد سعودية: الذكاء يجهز، الأنظمة تنفذ، الثقة تحكم، والإنسان يوافق على القرارات الحساسة.

## القرار النهائي

ابنِ Dealix كـ Full-Ops شبه ذاتي حول الإيراد، لا كـ SaaS عام. ابدأ بـ Revenue Sprint مدفوع، واجعل كل automation يخدم مسارًا واحدًا: Lead → Reply → Call → Payment → Delivery → Proof → Retainer. حافظ على أهم ميزة: Trust + Approval-first + Saudi-native.
