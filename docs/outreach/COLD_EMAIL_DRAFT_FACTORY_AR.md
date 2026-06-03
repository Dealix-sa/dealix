# مصنع مسودات البريد البارد — Cold Email Draft Factory

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المالك:** المؤسس + عمليات الـ Outreach
**المخطط:** schemas/outreach_draft.schema.json
**آخر تحديث:** 2026-06-02

---

## العقيدة الأساسية (لا تتجاوزها)

**250 مسودة/يوم هو هدف الإنتاج. 250 إرسالة/يوم ممنوع.**

المصنع يُنتج 250 مسودة عالية الجودة يومياً. الإرسال **منفصل تماماً** ويتدرّج ببطء بعد اجتياز صحة النطاق + الانسحاب بنقرة + قائمة الكبح + موافقة المؤسس (انظر docs/outreach/SENDING_RAMP_OS_AR.md و docs/outreach/SENDING_RAMP_PLAN_AR.md). لا قوائم مشتراة. لا مواضيع مضلِّلة. لا `Re:`/`Fwd:` زائفة. لا إرسال بدون انسحاب بنقرة واحدة.

## مدخلات المصنع

عملاء محتملون بحالة `draft_ready` من نظام البحث (docs/outreach/PROSPECT_RESEARCH_OS_AR.md)، كلٌّ بإشارة تخصيص حقيقية موثّقة.

## الخليط اليومي (250 مسودة)

| النوع | العدد | الغرض |
|-------|------|-------|
| first-touch (تواصل أول) | 100 | فتح حوار بفرضية ألم + إشارة محدّدة |
| follow-up-1 (متابعة 1) | 75 | تذكير خفيف + زاوية قيمة جديدة |
| follow-up-2 (متابعة 2) | 50 | دليل/حالة آمنة + دعوة واضحة |
| proposal-intro (تمهيد عرض) | 15 | لعملاء أبدوا اهتماماً — تقديم بطاقة عرض |
| close-loop / breakup (إغلاق الحلقة) | 10 | إنهاء مهذّب + باب مفتوح لاحقاً |

التوزيع إرشادي ويُعاد موازنته حسب صف الموافقة وإشارات الرد (docs/outreach/REPLY_HANDLING_OS_AR.md).

## حقول المسودة (مرجع المخطط)

```
company, sector, recipient_role, source, pain_hypothesis,
personalization_note, offer, subject, body, CTA, language,
evidence_level, risk_level, compliance_status, approval_status,
send_status, unsubscribe_included
```

- `language`: ar أو en (لا خلط داخل الرسالة الواحدة).
- `evidence_level`: high / medium / low — أي ادّعاء بلا دليل = `low` ويُحجب.
- `risk_level`: low / medium / high.
- `compliance_status`: pass / fail (يراجع docs/outreach/COLD_EMAIL_COMPLIANCE_AR.md).
- `approval_status`: pending / approved / rejected / rewrite.
- `send_status`: draft (افتراضي) — لا تُكتب `sent` هنا، بل عبر نظام الإرسال المرحلي.
- `unsubscribe_included`: true إلزامي قبل أي إرسال.

## سلّم العروض المرجعي في المسودات

كل مسودة تختار عرضاً واحداً من السلّم المعتمد ولا تَعِد بنتيجة:

| العرض | السعر (SAR) |
|-------|-------------|
| التشخيص المجاني (Free Diagnostic) | 0 |
| Revenue Intelligence Sprint | 499 (premium 3,500–15,000) |
| Data-to-Revenue Pack | 1,500 |
| Managed Revenue Ops | 2,999–4,999/شهر |
| Custom AI Setup | 5,000–25,000 |
| Enterprise Governance Review | 25,000–50,000 |

التواصل الأول غالباً نحو **التشخيص المجاني** أو **Sprint** — العروض الأعلى تُقترح بعد إشارة اهتمام.

## قاعدة الجودة — لا تُرسَل مسودة إذا

- درجة التخصيص دون **P1** (انظر docs/outreach/PERSONALIZATION_RULES_AR.md).
- `risk_level = high`.
- الانسحاب غير مضمَّن (`unsubscribe_included = false`).
- ادّعاء بلا دليل (`evidence_level = low` على جملة تتضمن رقماً أو نتيجة).
- الشركة في قائمة الكبح (schemas/suppression.schema.json).
- الموضوع مضلِّل، أو يحاكي رداً/تحويلاً لم يحدث.

أي مسودة تفشل في معيار واحد ترجع للكاتب، ولا تدخل صف الموافقة.

## ضمانات اللغة

- لا «نضمن» ولا وعد بمبيعات أو نِسَب تحويل كحقيقة. استخدم «فرص مُثبتة بأدلة» و«قيمة تقديرية».
- لا مبالغات («ثوري»، «أضعاف مضاعفة»). أسماء وأرقام ملموسة فقط.
- الموضوع يصف المحتوى بصدق وبطول معقول.
- جملة واحدة لدعوة الإجراء (CTA) — خطوة تالية واضحة منخفضة الالتزام.

## معايير الإنتاج اليومي (Definition of Done)

1. 250 مسودة مكتملة الحقول.
2. كل مسودة باجتياز `compliance_status = pass` و`unsubscribe_included = true`.
3. كل مسودة بإشارة تخصيص ≥ P1.
4. لا ادّعاء بلا دليل.
5. تقرير الإنتاج معبّأ: reports/outreach/DAILY_DRAFT_PRODUCTION.md.
6. أفضل 50 مسودة مرفوعة لصف الموافقة (docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md).

## الخطوة التالية بعد المصنع

المسودات المعتمدة فقط تمرّ إلى نظام الإرسال المرحلي. لا مسودة تُرسَل قبل موافقة المؤسس وفحص النطاق والكبح والانسحاب.

## روابط

- بحث العملاء: docs/outreach/PROSPECT_RESEARCH_OS_AR.md
- قواعد التخصيص: docs/outreach/PERSONALIZATION_RULES_AR.md
- القوالب (عربي): docs/outreach/COLD_EMAIL_SEQUENCES_AR.md · (إنجليزي): docs/outreach/COLD_EMAIL_SEQUENCES_EN.md
- صف الموافقة: docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md
- الامتثال والمواضيع: docs/outreach/COLD_EMAIL_COMPLIANCE_AR.md
- الانسحاب: docs/outreach/UNSUBSCRIBE_POLICY_AR.md
- التسليم: docs/outreach/EMAIL_DELIVERABILITY_POLICY_AR.md

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
