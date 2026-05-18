<!-- Owner: Founder | Date: 2026-05-18 | Launch Master Plan -->
# هرم التشغيل الذاتي — Autonomous Org Pyramid

فريق Dealix من الوكلاء: كيف يُدار المشروع كآلة تشغيل ذاتية محكومة — كل عمل
داخلي مؤتمت، وكل فعل خارجي أو مالي محكوم ببوابة موافقة بشرية.

## النطاق / Scope

هذه الوثيقة تعرّف **الهرم التنظيمي للوكلاء** الذي يشغّل Dealix: من يفعل ماذا،
من يرفع لمن، وكيف تعمل حلقة Full-Ops. هي وثيقة تشغيل — مرجع الاستراتيجية
[`LAUNCH_MASTER_PLAN.md`](LAUNCH_MASTER_PLAN.md)، ومرجع الوكلاء التفصيلي
[`AGENT_OPERATING_MODEL.md`](AGENT_OPERATING_MODEL.md). ليست كوداً ولا منتجاً.

> **القاعدة الحاكمة:** الأتمتة تُجهّز القرار حتى بوابة الموافقة — لا تتجاوزها.
> «المبيعات أوتوماتيكية بالكامل» تعني أن كل خطوة قبل الإرسال مؤتمتة؛ الإرسال
> نفسه يبقى قرار المؤسس. هذا ليس قيداً — هو منتج Dealix نفسه.

## 1. الهرم — The Pyramid (13 وكيلاً)

```
                    ┌─────────────────────┐
                    │   dealix-pm (T0)    │  المنسّق / Orchestrator — COO
                    └──────────┬──────────┘
        ┌──────────┬───────────┼───────────┬──────────┬──────────┐
   ┌────┴────┐┌────┴────┐ ┌────┴────┐ ┌────┴────┐┌────┴────┐┌────┴─────┐┌────────┐
   │ sales   ││delivery │ │ content │ │engineer ││ growth  ││ finance  ││partner-│
   │  (CRO)  ││         │ │ (CMO)   │ │ (CTO)   ││(Demand) ││  (CFO)   ││ ships  │
   └─────────┘└─────────┘ └─────────┘ └────┬────┘└─────────┘└──────────┘└────────┘
        قادة المجالات — Tier-1 Domain Leads (7)   │
                                       ┌─────────┴─────────┐
                                  ┌────┴────┐         ┌────┴────┐
                                  │frontend │         │ backend │
                                  └─────────┘         └─────────┘
   المتخصصون — Tier-2 Specialists (5): analyst · qa · frontend · backend · research
```

| الطبقة | الوكيل | الدور | الحالة |
|--------|--------|------|--------|
| T0 | `dealix-pm` | المنسّق — الخطة، البوابات، الإيقاع، friction log | قائم |
| T1 | `dealix-sales` | المبيعات — تأهيل، عروض، مسودات تواصل | قائم |
| T1 | `dealix-delivery` | التسليم — Sprint، Proof Pack، نجاح العميل | قائم |
| T1 | `dealix-content` | المحتوى — وثائق ثنائية اللغة، AEO، case studies | قائم |
| T1 | `dealix-engineer` | الهندسة — كود، راوترات، migrations، cron | قائم |
| T1 | `dealix-growth` | النمو — محرك الطلب، AEO، مزيج القنوات | جديد |
| T1 | `dealix-finance` | المال — Moyasar، فوترة، MRR، وحدات اقتصادية | جديد |
| T1 | `dealix-partnerships` | الشركاء — برنامج الوكالات، affiliate | جديد |
| T2 | `dealix-analyst` | البيانات — مقاييس، لوحات، benchmark | جديد |
| T2 | `dealix-qa` | الجودة والحوكمة — Sales/Delivery QA، تدقيق العقيدة | جديد |
| T2 | `dealix-frontend` | الواجهة — landing/Next.js (محكوم بالتجميد) | جديد |
| T2 | `dealix-backend` | الخادم — API/تكامل/cron (محكوم بالتجميد) | جديد |
| T2 | `dealix-research` | البحث — سوق، منافسون، ICP، مواضيع AEO | جديد |

## 2. خطوط الرفع والتصعيد — Reporting & Escalation

- كل قادة T1 يرفعون إلى `dealix-pm`. `dealix-frontend` و`dealix-backend`
  يرفعان إلى `dealix-engineer`.
- المتخصصون (T2) يخدمون عدة قادة: `analyst` يخدم pm؛ `research` يخدم
  growth/content/sales؛ `qa` يدقّق الجميع (cross-cutting).
- **التصعيد:** أي بوابة موافقة بشرية، أي مخاطرة على العقيدة، أي قرار يتجاوز
  نطاق وكيل → يُرفع إلى `dealix-pm` ثم إلى المؤسس.

## 3. ملكية المحركات — Engine Ownership Map

| المحرك | الوكيل المالك | بوابة الفتح |
|--------|---------------|-------------|
| E1 تفعيل الإيراد | dealix-finance (+ المؤسس لـMoyasar live) | G0 |
| E2 البيع بقيادة المؤسس | dealix-sales | الآن |
| E3 التشخيص والاستقبال | dealix-delivery + dealix-backend | الآن |
| E4 الإثبات | dealix-delivery | G1 |
| E5 التسليم | dealix-delivery | G1 |
| E6 الفوترة والمال | dealix-finance + dealix-backend | G2 |
| E7 المحتوى والظهور | dealix-content + dealix-growth | الآن |
| E8 الطلب | dealix-growth + dealix-sales | G2 |
| E9 الشركاء والقنوات | dealix-partnerships | G3 |
| E10 نجاح العميل والتوسع | dealix-delivery | G2 |
| E11 برج التحكم التجاري | dealix-pm + dealix-analyst | الآن |
| E12 حلقة التشغيل الذاتي | dealix-pm + dealix-engineer | G3→G4 |

`dealix-qa` و`dealix-research` و`dealix-frontend/backend` يخدمون كل المحركات
ضمن نطاقهم — راجع [`ENGINE_SPECS.md`](ENGINE_SPECS.md).

## 4. حلقة التشغيل الذاتي — The Autonomous Full-Ops Loop

**يومياً:**
1. `dealix-pm` يشغّل حلقة برج التحكم ويوزّع العمل المُجدوَل.
2. كل قائد T1 ينفّذ عمل محركه — يُنتج **مسودات** (لا إرسال).
3. `dealix-analyst` يسجّل **Commercial Evidence Event** واحداً على الأقل.
4. أي مخرج موجّه للعميل يمرّ على بوابة QA قبل الموافقة.

**أسبوعياً:**
- `dealix-qa`: Sales QA (5 محادثات) + Delivery QA (بطاقة 10 نقاط).
- `dealix-analyst`: لوحة المقاييس + تقدّم البوابات.
- `dealix-pm`: مراجعة friction log + قرار الإيقاع.

**عند البوابات G0–G4:**
- `dealix-pm` + `dealix-analyst` يقيسان معايير [`GATE_CRITERIA.md`](GATE_CRITERIA.md)
  بالدليل؛ **المؤسس يوقّع** قبل أي انتقال مرحلة.

## 5. المبيعات الأوتوماتيكية المحكومة — Governed Sales Automation

أقوى نظام مبيعات = كل خطوة مؤتمتة حتى بوابة الموافقة، ثم إرسال بشري واحد:

| الخطوة | الوكيل | مؤتمت؟ |
|--------|--------|--------|
| إثراء سياق الـlead (ضمن الموافقة) | dealix-research | ✅ آلي |
| التأهيل (8 أسئلة) + توجيه العرض | dealix-sales | ✅ آلي |
| تجهيز أصول الدعم (case/AEO) | dealix-content / dealix-growth | ✅ آلي |
| رسم العرض bilingual | dealix-sales | ✅ آلي |
| تجهيز رابط الدفع والفاتورة | dealix-finance | ✅ آلي |
| **مراجعة وموافقة المؤسس** | المؤسس | 🔒 بشري |
| **الإرسال الخارجي** | المؤسس | 🔒 بشري |
| تسجيل الحدث في الـledger | dealix-analyst | ✅ آلي |

هذا يحقّق «المبيعات أوتوماتيكية بالكامل» دون خرق `no_live_send` أو
`no_cold_whatsapp` — ودون أن يفقد Dealix هوّيته كنظام محكوم.

## 6. بوابات الموافقة البشرية — Human-Approval Gates

لا يتجاوزها أي وكيل أبداً: (1) كل إرسال خارجي · (2) كل شحن مالي · (3) تحويل
Moyasar إلى live · (4) أي انتقال مرحلة/بوابة · (5) تفعيل شريك · (6) أي إنفاق
تسويقي مدفوع. مفروضة باختبارات `no_live_send` / `no_live_charge` / الحوكمة.

## 7. كيف تُستدعى الفِرَق — Invoking the Team

- المؤسس أو `dealix-pm` يستدعي الوكلاء؛ القادة يفوّضون لأسفل الهرم.
- العمل المتوازي المستقل يُطلق دفعةً واحدة.
- كل مخرج يُسجَّل في الـledger المناسب؛ لا تغييرات غير مُدقّقة.
- ملفات تعريف الوكلاء في `.claude/agents/` — 13 ملفاً.

## 8. العقيدة — الـ11 لا-تفاوض

لا scraping · لا cold WhatsApp/LinkedIn automation · لا fake proof · لا
ادعاءات نتائج مضمونة · لا PII في السجلات · لا إجابات بلا مصدر · لا مخرج AI
للعميل بلا QA · لا live send · لا live charge · موافقة بشرية لكل فعل خارجي ·
لا تقدّم مرحلة بلا دليل موثّق. كل وكيل في الهرم يحترمها أو يرفض المهمة.

---
*القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.*
