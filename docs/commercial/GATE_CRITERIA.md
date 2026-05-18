<!-- Owner: Founder | Date: 2026-05-18 | Launch Master Plan -->

# معايير البوابات G0–G4 — Decision Gate Criteria

> **قاعدة ذهبية:** لا مرحلة تتقدّم حتى يُستوفى **كل** معيار خروج بدليل موثّق. البوابة قرار — لا تُفتح بالنية، تُفتح بالدليل.
> **Golden rule:** No phase advances until every exit criterion is met with documented evidence. A gate is a decision — it opens on evidence, not intent.

## النطاق / Scope

- **هذا الملف:** **وثيقة التحكّم التشغيلية** للبوابات الخمس (G0–G4): لكل بوابة قائمة تحقّق قابلة للفحص موضوعياً، ما تفتحه البوابة (محركات / درجات سلم / رفع تجميد)، ومَن يعتمدها.
- **ليس هذا الملف:** الاستراتيجية الحاكمة ([`LAUNCH_MASTER_PLAN.md`](LAUNCH_MASTER_PLAN.md))، ولا مواصفات المحركات ([`ENGINE_SPECS.md`](ENGINE_SPECS.md))، ولا قائمة الأسعار (المصدر القانوني: [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)).
- **الجمهور:** المؤسس والوكلاء التشغيليون. يُراجَع هذا الملف عند كل قرار انتقال مرحلة.

## كيف تُقرأ البوابة — How to read a gate

- كل معيار **قابل للفحص موضوعياً**: له دليل موثّق في سجل (`docs/ledgers/`) أو نظام (billing، delivery ledger، capital ledger).
- البوابة لا تُفتح جزئياً. **كل** صفوف القائمة يجب أن تكون `مُتحقَّق` قبل الانتقال.
- لا ادعاء أرقام كحقيقة — كل رقم مستقبلي **تقدير تخطيطي** حتى يؤكّده النظام.

---

## G0 — يُغلق المرحلة P0 (Revenue Unlock، أيام 1–14)

**الهدف:** فتح قناة قبض المال وإتاحة أول عرض مدفوع للبيع.

| # | معيار الخروج | الدليل المطلوب | الحالة |
|---|--------------|-----------------|--------|
| G0.1 | Moyasar حيّ — رابط دفع اختباري ينجح | لقطة معاملة ناجحة + إدخال في capital ledger | ☐ |
| G0.2 | أول عرض مدفوع مُقفَل للبيع | 7-Day Revenue Proof Sprint بسعر 499 SAR موثّق في [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md) | ☐ |
| G0.3 | مسار الفاتورة جاهز ومرتبط بالـ SOW | قالب فاتورة مرتبط بـ payment link، مُراجَع من المؤسس | ☐ |
| G0.4 | بوابة الموافقة على الإرسال فعّالة | لا live charge — كل إرسال رابط دفع يتطلّب موافقة المؤسس موثّقة | ☐ |
| G0.5 | محرك E3 (Diagnostic & Intake) نشط | تشخيص مجاني يُنتج تقريراً + توصية ترقية | ☐ |

**ما تفتحه G0:** بناء محرك **E1 (Revenue Activation)** يكتمل · درجة سلم: تفعيل **7-Day Revenue Proof Sprint (499 SAR)** للبيع الفعلي · رفع التجميد: لا رفع — التجميد يبقى نافذاً على درجات 2–5.
**مَن يعتمد:** المؤسس (sign-off نهائي) بعد تأكيد dealix-engineer لـ G0.1/G0.3/G0.4 وdealix-sales لـ G0.2/G0.5.

---

## G1 — يُغلق المرحلة P1 (Proof & Repeatability، أيام 15–45)

**الهدف:** إثبات أن الحركة تتكرّر وتُنتج Proof معتمداً من العميل.

> **G1 هو شرط الخروج من Commercial Freeze:** أول pilot مدفوع مُسلَّم + Proof Pack مُعتمَد من العميل بمستوى دليل **L3 أو أعلى** ([`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md)).

| # | معيار الخروج | الدليل المطلوب | الحالة |
|---|--------------|-----------------|--------|
| G1.1 | 3 pilots مدفوعة مُسلَّمة | 3 أحداث `payment_received` + 3 أحداث `proof_pack_delivered` في delivery ledger | ☐ |
| G1.2 | 3 Proof Packs مُقيَّمة ≥ 8/10 | بطاقة QA من 10 نقاط لكل حزمة ([`DELIVERY_QA.md`](DELIVERY_QA.md)) | ☐ |
| G1.3 | أول Proof Pack مُعتمَد من العميل بمستوى L3+ | موافقة عميل مكتوبة موثّقة — **شرط خروج التجميد** | ☐ |
| G1.4 | 1 case study موثّقة | حالة مُجهَّلة منشورة بلا PII ([`SAMPLE_PROOF_PACK.md`](SAMPLE_PROOF_PACK.md)) | ☐ |
| G1.5 | سير عمل Sprint موثّق وقابل للتكرار | تسلسل خطوات Source→Owner→Approval→Evidence→Next مكتوب في السجل | ☐ |

**ما تفتحه G1:** بناء محركَي **E4 (Proof)** و**E5 (Delivery)** يكتمل · درجة سلم: **Data-to-Revenue Pack (1,500 SAR)** يُتاح بعد تأهيل · رفع التجميد: **الخروج الكامل من Commercial Freeze** — الانتقال من البناء المُجمَّد إلى تشغيل P2 يحكمه [`../90_DAY_BUSINESS_EXECUTION_PLAN.md`](../90_DAY_BUSINESS_EXECUTION_PLAN.md).
**مَن يعتمد:** المؤسس (sign-off نهائي + إعلان رفع التجميد) بعد تأكيد dealix-delivery لـ G1.1/G1.2/G1.5 وdealix-content لـ G1.4 وموافقة العميل لـ G1.3.

---

## G2 — يُغلق المرحلة P2 (Full-Ops Automation، أيام 46–90)

**الهدف:** إثبات أن سير العمل يتكرّر بثبات ويُنتج إيراداً متكرراً يبرّر أتمتة Full-Ops.

| # | معيار الخروج | الدليل المطلوب | الحالة |
|---|--------------|-----------------|--------|
| G2.1 | سير عمل التسليم تكرّر ≥ 3 مرات بنفس الخطوات | 3 إدخالات سير عمل متطابقة في delivery ledger | ☐ |
| G2.2 | أول retainer مُفعَّل | اشتراك Managed Revenue Ops نشط في billing بقبول عميل صريح | ☐ |
| G2.3 | MRR متكرر مؤكَّد ~15,000–25,000 SAR | تقرير billing — إيراد متكرر مؤكَّد من Moyasar لا عروض موقّعة | ☐ |
| G2.4 | جدول unit economics مُحدَّث | CAC وLTV مقيسان أولاً من capital ledger ([`FINANCIAL_MODEL.md`](FINANCIAL_MODEL.md)) | ☐ |
| G2.5 | رضا العميل ≥ 4/5 عبر الـ pilots | تقييمات موثّقة لكل عميل مدفوع | ☐ |

**ما تفتحه G2:** بناء محركات **E6 (Billing & Finance)** و**E8 (Demand)** و**E10 (CS & Expansion)** يكتمل · بناء **معمارية Full-Ops** ([`FULL_OPS_AUTOMATION_ARCHITECTURE.md`](FULL_OPS_AUTOMATION_ARCHITECTURE.md)) · درجة سلم: **Managed Revenue Ops (2,999–4,999 SAR/شهر)** كعرض تشغيلي · البناء عند الطلب يحكمه [`../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`](../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md).
**مَن يعتمد:** المؤسس (sign-off نهائي) بعد تأكيد dealix-engineer لـ G2.3/G2.4 وdealix-delivery لـ G2.1/G2.5 وdealix-pm لـ G2.2.

---

## G3 — يُغلق المرحلة P3 (Scale & Channels، أيام 91–180)

**الهدف:** إثبات أن النمو يأتي من قنوات متعددة لا من المؤسس وحده.

| # | معيار الخروج | الدليل المطلوب | الحالة |
|---|--------------|-----------------|--------|
| G3.1 | MRR متكرر مؤكَّد ≥ 50,000 SAR | تقرير billing — إيراد متكرر مؤكَّد | ☐ |
| G3.2 | 10 شركاء نشطون | 10 اتفاقيات شراكة موقّعة + leads مُقاسة الجودة لكل شريك | ☐ |
| G3.3 | inbound مُثبَت كقناة | leads inbound مؤهّلة موثّقة في DEMAND ledger ([`DEMAND_MODEL.md`](DEMAND_MODEL.md)) | ☐ |
| G3.4 | أول توظيف مبيعات مكتمل | عقد موظف مبيعات موقّع — بعد إغلاق المؤسس 10–20 عميلاً | ☐ |
| G3.5 | حلقة CS تخفض churn بدليل | churn rate موثّق ومستقر عبر الشهور | ☐ |

**ما تفتحه G3:** بناء محرك **E9 (Partner & Channel)** يكتمل · بدء بناء **E12 (Autonomous Ops Loop)** تدريجياً · درجة سلم: **Executive Command Center (7,500–15,000 SAR/شهر)** بعد 3 pilots مكتملة، و**Agency Partner OS (rev-share 15–30%)** بعد 3 proof packs.
**مَن يعتمد:** المؤسس (sign-off نهائي) بعد تأكيد dealix-engineer لـ G3.1 وdealix-pm لـ G3.2/G3.5 وdealix-content/dealix-sales لـ G3.3 وG3.4.

---

## G4 — يُغلق المرحلة P4 (Category & Platform، أيام 181–365)

**الهدف:** إثبات اقتصاد وحدة موجب يبرّر التحوّل إلى منصة وفئة.

| # | معيار الخروج | الدليل المطلوب | الحالة |
|---|--------------|-----------------|--------|
| G4.1 | MRR متكرر مؤكَّد ≥ 150,000 SAR | تقرير billing — إيراد متكرر مؤكَّد | ☐ |
| G4.2 | اقتصاد وحدة موجب | LTV > CAC بهامش موثّق في جدول unit economics | ☐ |
| G4.3 | CAC payback ≤ 8 أشهر | محسوب من capital ledger ومُتحقَّق ([`FINANCIAL_MODEL.md`](FINANCIAL_MODEL.md)) | ☐ |
| G4.4 | سير عمل Full-Ops موثّق ومستقر | E12 يعمل من طرف إلى طرف حتى بوابات الموافقة فقط | ☐ |
| G4.5 | كل البوابات الخارجية والمالية محفوظة | تدقيق: لا live send / لا live charge / موافقة بشرية لكل إجراء خارجي | ☐ |

**ما تفتحه G4:** اكتمال **E12 (Autonomous Ops Loop)** · الانتقال إلى وضع المنصة والفئة · لا رفع لأي بوابة موافقة بشرية — البنود الإحدى عشر تبقى نافذة دائماً.
**مَن يعتمد:** المؤسس (sign-off نهائي) بعد تدقيق dealix-engineer لـ G4.2/G4.3/G4.5 وdealix-pm لـ G4.1/G4.4.

---

## ملخص البوابات — Gates Summary

| البوابة | تُغلق المرحلة | المعيار الجوهري | يفتح |
|---------|---------------|------------------|------|
| **G0** | P0 Revenue Unlock | Moyasar حيّ + أول عرض مدفوع | E1 + درجة Sprint 499 SAR |
| **G1** | P1 Proof & Repeatability | 3 pilots + Proof Pack L3+ مُعتمَد | E4/E5 + **خروج من Commercial Freeze** |
| **G2** | P2 Full-Ops Automation | سير عمل ≥3× + retainer + MRR ~15–25K | E6/E8/E10 + معمارية Full-Ops |
| **G3** | P3 Scale & Channels | MRR ≥50K + 10 شركاء + inbound + توظيف مبيعات | E9 + E12 (تدريجي) + درجات 4–5 |
| **G4** | P4 Category & Platform | MRR ≥150K + اقتصاد وحدة موجب + payback ≤8 أشهر | E12 يكتمل + وضع المنصة |

## روابط داخلية / Cross-links

- [`LAUNCH_MASTER_PLAN.md`](LAUNCH_MASTER_PLAN.md) — الفهرس الرئيسي والمراحل الخمس.
- [`ENGINE_SPECS.md`](ENGINE_SPECS.md) — مواصفات المحركات التي تفتحها البوابات.
- [`FINANCIAL_MODEL.md`](FINANCIAL_MODEL.md) — أهداف الإيراد وunit economics.
- [`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md) — التجميد التجاري؛ G1 شرط خروجه.
- [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md) — سلم الخدمات والأسعار (canonical).
- [`../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`](../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md) — محفّزات البناء عند الطلب.

---

*القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.*
