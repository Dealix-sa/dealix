<!-- Owner: Founder | Date: 2026-05-18 | Launch Master Plan -->

# النموذج المالي وآلة المال — Financial Model & Money Machine

> **قاعدة ذهبية:** لا إيراد قبل الدفع. لا بناء قبل تكرار سير العمل ≥3 مرات. لا ترقية درجة بدون دليل.
> **Golden rule:** No revenue before payment. No build before a workflow repeats ≥3×. No rung advance without evidence.

> **إفصاح:** كل الأرقام المستقبلية في هذا الملف **تقديرات تخطيطية (planning Estimates)** وليست وعوداً ولا ضمانات.
> All forward-looking numbers here are **planning Estimates**, not promises or guarantees.

---

## النطاق / Scope

يصف هذا الملف **آلة المال** لـ Dealix: كيف يتحرك المال من العميل إلى السجل المالي، ما هي أهداف الإيراد لكل مرحلة، وما هي وحدة الاقتصاد (unit economics) لكل درجة في سلم العروض. الملف **لا** يخترع أسعاراً — المصدر الوحيد للأسعار هو [OFFER_LADDER_AND_PRICING.md](../OFFER_LADDER_AND_PRICING.md). الملف يعمل ضمن **Commercial Freeze** النشط ([COMMERCIAL_FREEZE.md](../ops/COMMERCIAL_FREEZE.md)): التجميد هو آلية الحوكمة المالية وليس عائقاً — فهو يمنع صرف الجهد على بناء درجات لم تُثبت طلباً بعد.

This document defines Dealix's **money machine**: how cash moves from customer to capital ledger, the revenue targets per phase, and the unit economics per offer rung. It invents no prices. It operates inside the active Commercial Freeze, which it treats as the financial gating mechanism.

---

## 1) تدفّق المال — The Money Flow

كل خطوة في التدفّق محكومة، وكل **شحن (charge)** مرتبط بموافقة صريحة من العميل — **لا live charge**، لا خصم تلقائي بدون قبول مكتوب.

| الخطوة | الوصف | البوابة البشرية |
|--------|-------|-----------------|
| Moyasar | مزوّد الدفع المعتمد للسوق السعودي | — |
| Payment link | رابط دفع يُولَّد لكل عرض ويُرسَل بعد موافقة المؤسس | موافقة المؤسس على الإرسال |
| Invoice | فاتورة مرتبطة برابط الدفع وبالـ SOW | مراجعة المؤسس |
| Recurring subscription | اشتراك شهري (Managed Ops / Command Center) يبدأ فقط بقبول صريح متجدد | قبول العميل لكل تجديد |
| Dunning | تذكير دفع متأخر — **مسودة** تذكير، لا خصم تلقائي | موافقة المؤسس على كل تذكير |
| Revenue recognition | الإيراد يُعترف به فقط بعد تأكيد الدفع الفعلي من Moyasar | تأكيد آلي + مراجعة |
| Capital ledger | السجل المالي المركزي تحت `docs/ledgers/` — مصدر الحقيقة للنقد | تدقيق أسبوعي |

**الثابت المالي:** الأتمتة **تُجهّز** روابط الدفع والفواتير ومسودات الـ dunning؛ الإنسان **يوافق ويُرسِل ويُحصِّل**. لا يوجد مسار يخصم من بطاقة عميل بدون قبول صريح موثّق.

The flow is governed end-to-end. Automation **prepares** payment links, invoices, and dunning drafts; the human **approves, sends, and collects**. No path charges a customer card without explicit, logged consent.

---

## 2) أهداف الإيراد لكل مرحلة — MRR Targets per Phase

| المرحلة / Phase | البوابة | الإيراد لمرة واحدة (One-time) | MRR متكرر | عدد العملاء (تقدير) |
|-----------------|---------|-------------------------------|-----------|----------------------|
| P0 — Revenue Unlock (أيام 1–14) | G0 | أول 499 SAR (Sprint واحد) | 0 | 1 |
| P1 — Proof & Repeatability (أيام 15–45) | G1 | 5–8 pilots لمرة واحدة (Sprint/Pack) | أول retainer (Managed Ops) | 6–9 |
| P2 — Full-Ops Automation (أيام 46–90) | G2 | استمرار pilots | ~15,000–25,000 SAR | 10–18 |
| P3 — Scale & Channels (أيام 91–180) | G3 | عبر شركاء | ≥ 50,000 SAR | 20–35 |
| P4 — Category & Platform (أيام 181–365) | G4 | منصة + شراكات | ≥ 150,000 SAR | 40+ |

**ملاحظة GTM:** أول 10 عملاء من **بيع بقيادة المؤسس** لا من inbound. أول موظف مبيعات يُوظَّف بعد إغلاق المؤسس 10–20 عميلاً (~50–100K MRR) — يتزامن مع بوابة G3.

All figures above are planning Estimates. The first 10 customers come from founder-led selling, not inbound. The first salesperson is hired after the founder closes 10–20 customers, aligned with gate G3.

---

## 3) وحدة الاقتصاد — Unit Economics

تعريفات موحّدة تُستخدم في كل التقارير المالية:

- **CAC** — تكلفة اكتساب العميل: إجمالي مصروف البيع والتسويق ÷ عدد العملاء المدفوعين الجدد في الفترة.
- **LTV** — القيمة الدائمة للعميل: متوسط الإيراد الشهري × الهامش الإجمالي × متوسط عمر العميل (بالأشهر).
- **CAC-payback** — أشهر استرداد تكلفة الاكتساب: CAC ÷ (الإيراد الشهري × الهامش الإجمالي). **الهدف ≤ 8 أشهر** (متّسق مع تشغيل AI-native).
- **Gross margin** — الهامش الإجمالي لكل درجة، مرجعه [OFFER_LADDER_AND_PRICING.md](../OFFER_LADDER_AND_PRICING.md).

### الهامش الإجمالي لكل درجة — Gross Margin per Rung

| الدرجة / Rung | السعر (المصدر القانوني) | الهامش الإجمالي (تقدير) |
|---------------|--------------------------|--------------------------|
| Free Diagnostic | مجاني | تكلفة API < 2 SAR |
| 7-Day Revenue Proof Sprint | 499 SAR | ~85% |
| Data-to-Revenue Pack | 1,500 SAR | ~75% |
| Managed Revenue Ops | 2,999–4,999 SAR/شهر | ~70% |
| Executive Command Center | 7,500–15,000 SAR/شهر | ~65% |
| Agency Partner OS | rev-share 15–30% | ~55–60% بعد rev-share |

### جدول تتبّع وحدة الاقتصاد — Unit Economics Tracking Table

يُحدَّث هذا الجدول شهرياً من Capital ledger؛ القيم أدناه **أهداف تخطيطية**:

| المؤشر | P1 (هدف) | P2 (هدف) | P3 (هدف) | المصدر |
|--------|----------|----------|----------|--------|
| CAC | يُقاس أولاً | ينخفض مع الأتمتة | مستقر | Capital ledger |
| LTV | يُقاس أولاً | يرتفع مع retainers | يرتفع | سجل الاشتراكات |
| CAC-payback | يُقاس | ≤ 8 أشهر | ≤ 8 أشهر | محسوب |
| Gross margin مرجّح | ~80% | ~72% | ~70% | حسب مزيج الدرجات |

---

## 4) قواعد الانضباط المالي — Financial Discipline Rules

1. **لا إيراد قبل الدفع** — الإيراد يُعترف به فقط بعد تأكيد Moyasar؛ العرض الموقّع ليس إيراداً.
2. **لا بناء قبل تكرار سير العمل ≥3 مرات** — أي أتمتة جديدة تُبنى فقط بعد إثبات تكرار يدوي ثلاث مرات.
3. **لا ترقية درجة بدون دليل** — الانتقال لدرجة أعلى يتطلّب Proof Pack مُتحقَّق منه (L3+) من الدرجة السابقة.
4. **لا live charge / لا live send** — كل شحن وكل إرسال يمرّ ببوابة موافقة بشرية.
5. **التجميد التجاري نافذ** — لا صرف على درجات 2–5 حتى يفتح طلب حقيقي بوابة البناء.

No revenue before payment. No build before a workflow repeats three times. No rung advance without verified evidence. The Commercial Freeze stays in force until real demand unlocks the next build.

---

## روابط داخلية / Cross-links

- [Offer Ladder & Pricing — المصدر القانوني للأسعار](../OFFER_LADDER_AND_PRICING.md)
- [Commercial Freeze — آلية الحوكمة](../ops/COMMERCIAL_FREEZE.md)
- [Agent Operating Model — نموذج التشغيل والوكلاء](AGENT_OPERATING_MODEL.md)
- [Full-Ops Automation Architecture — معمارية الأتمتة الكاملة](FULL_OPS_AUTOMATION_ARCHITECTURE.md)
- [REVOPS Packages — حزم Dealix التجارية](DEALIX_REVOPS_PACKAGES_AR.md)
