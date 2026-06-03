# Brand Outbound System — نظام الـ Outbound

**Status:** كيف تحكم العلامة كل رسالة خارجية — البوابات الستّ، البريد البارد أولاً، واتساب بعد الردّ فقط، LinkedIn يدوي فقط.
**يمتد من:** [BRAND_IDENTITY_SYSTEM_AR.md](./BRAND_IDENTITY_SYSTEM_AR.md) · [BRAND_VOICE_AR.md](./BRAND_VOICE_AR.md)
**يطابق:** [نظام إنتاج السوق](../market_production_os/README.md) · [COMMERCIAL_GOVERNANCE_GATES_AR.md](../commercial/operations/COMMERCIAL_GOVERNANCE_GATES_AR.md)

---

## 1. المبدأ — The Principle

العلامة لا تُصان في المنشورات فقط؛ تُصان في **كل رسالة تخرج باسم Dealix**. القاعدة الحاسمة: كثافة عالية في المسودات، حذر شديد في الإرسال، ولا إرسال خارجي بلا موافقة. كل رسالة تمرّ على ستّ بوّابات قبل أن تُرسَل.

The brand is protected in every message that leaves as Dealix. High density in drafts, extreme caution in sends, no external send without approval.

## 2. البوابات الستّ — The Six Gates

كل رسالة خارجية تمرّ، بالترتيب، على ستّ بوّابات مطابقة لما تفرضه [نظام إنتاج السوق](../market_production_os/README.md). إن سقطت أيّ بوابة، الرسالة **لا تُرسَل**.

| # | البوابة | تفحص | الفشل يعني |
|---|---------|------|-----------|
| 1 | **Brand Voice — صوت العلامة** | النبرة، الكلمات الممنوعة، لا hype ([BRAND_VOICE_AR.md](./BRAND_VOICE_AR.md)) | كلمة ممنوعة أو نبرة خاطئة → رفض |
| 2 | **Offer Match — مطابقة العرض** | العرض يناسب القطاع والشخصية ([DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md)) | عرض غير مناسب → رفض |
| 3 | **Personalization — التخصيص** | تخصيص حقيقي لكل شركة (ألم + زاوية) | نصّ عام → رفض |
| 4 | **Compliance — الامتثال** | آلية إلغاء حاضرة، مُرسِل دقيق، عنوان غير مضلّل، لا Re:/Fwd: مزيف، لا ادعاء مضمون، غير مُدرَج في قائمة الكبح، PDPL | أيّ خرق → رفض |
| 5 | **Deliverability — قابلية التسليم** | صحّة الدومين (SPF/DKIM/DMARC)، ضمن سقف التدرّج | دومين غير سليم أو فوق السقف → تأجيل |
| 6 | **Founder Approval — موافقة المؤسس** | موافقة صريحة قبل أيّ إرسال | لا موافقة → لا إرسال |

البوابات تُنفَّذ في الكود وتحرسها اختبارات؛ هذا الملف هو **المرجع السردي للعلامة** خلفها. تُسجَّل كل رسالة مُرسَلة يدوياً كحدث دليل ([COMMERCIAL_GOVERNANCE_GATES_AR.md](../commercial/operations/COMMERCIAL_GOVERNANCE_GATES_AR.md)).

## 3. عقيدة القنوات — Channel Doctrine

| القناة | الدور | القاعدة |
|--------|-------|---------|
| **البريد البارد / Cold email** | القناة الأساسية للاكتساب | متوافق مع PDPL ومبادئ مكافحة الـ spam؛ يمرّ على البوابات الستّ كاملةً |
| **واتساب / WhatsApp** | تجربة ما بعد الردّ | **بعد الردّ / opt-in فقط** — ليس قناة بدء باردة أبداً |
| **LinkedIn** | قيادة فكرية وعلاقات | **يدوي فقط**؛ DM بعد قبول اتصال؛ لا أتمتة ([BRAND_SOCIAL_SYSTEM_AR.md](./BRAND_SOCIAL_SYSTEM_AR.md)) |
| **الشركاء / Partners** | إحالات دافئة | رسائل معتمدة وإفصاح؛ لا ادعاءات مضللة باسم Dealix |

البريد البارد **أولاً**؛ واتساب **بعد الردّ فقط**؛ LinkedIn **يدوي فقط**.

## 4. البريد البارد أولاً — Cold-Email-First

- البحث عن الشركات بمصادر مشروعة فقط — **لا scraping إنتاجي، لا قوائم مشتراة** (وفق سجلّ المصادر والمصادر الممنوعة).
- كثافة المسودات مسموحة؛ الإرسال مُقيَّد بصحّة الدومين وآلية إلغاء حيّة وقائمة كبح وتدرّج آمن.
- كل بريد: CTA واحد، إفصاح وآلية إلغاء، عنوان صادق، لا إلحاح مزيف، لا وعد مضمون.
- «أيّ Outreach في العروض = Draft Pack فقط حتى موافقة صريحة» ([DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md)).

## 5. واتساب بعد الردّ فقط — WhatsApp Post-Reply-Only

- لا بدء بارد على واتساب إطلاقاً (لا أتمتة واتساب باردة).
- يُستخدَم فقط مع: ردّ وارد، علاقة قائمة، أو إحالة دافئة موثّقة.
- بعد الردّ: تجربة عميل (تقييم + بطاقات إجراء)، شخصية وضمن البوابات.

## 6. LinkedIn يدوي فقط — LinkedIn Manual-Only

- لا أتمتة إرسال، لا scraping، لا رسائل جماعية، لا جمع جهات اتصال آلي.
- النشر والتفاعل وDM (بعد قبول اتصال) كلّها بيد المؤسس ([BRAND_SOCIAL_SYSTEM_AR.md](./BRAND_SOCIAL_SYSTEM_AR.md)).

## 7. صياغة العلامة في الرسالة — Brand Framing in the Message

- لا تدّعِ الرسالة أن Dealix **ترسل نيابةً عن العميل** بلا موافقته الصريحة.
- استخدم لغة الالتزام لا الضمان: «فرص مُثبتة بأدلة» لا «مبيعات مضمونة».
- اذكر المرحلة بصدق حين يلزم: مرحلة الشريك المؤسِّس ([BRAND_CLAIMS_POLICY_AR.md](./BRAND_CLAIMS_POLICY_AR.md)).
- إن خالف طلبٌ أيّ بوابة أو بند: **ارفض واقترح بديلاً آمناً** — لا التفاف.

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
