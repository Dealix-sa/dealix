# Dealix WhatsApp Client OS — النظرة الشاملة

مساعد **سير عمل أعمال** محكوم يُقدَّم عبر واتساب لشركات B2B السعودية. يقود العميل عبر مسار واضح: فحص الجاهزية ← توصية بمنتج ← صلاحيات ← مسودات ← عرض ← إثبات ← دفع/إعداد ← دعم ← تحويل بشري عند الحاجة.

> الموديول: `auto_client_acquisition/whatsapp_client_os/` · مسار الـ API: `/api/v1/whatsapp-client-os`

## ما هو · وما ليس

| هو | ليس |
|---|---|
| مساعد سير عمل محكوم بقوائم وأزرار | شات بوت عام للأسئلة المفتوحة |
| توجيه حتمي (deterministic) للقرارات | نموذج لغوي يقرر المسار |
| كل توصية مربوطة بكتالوج المنتجات + مستوى دليل | وعود بأرقام مبيعات أو نسب تحويل |
| موافقة بشرية صريحة قبل أي إرسال خارجي | إرسال نيابة عن العميل بلا موافقة |
| إدخال الأسرار عبر بوابة آمنة فقط | طلب مفاتيح/كلمات سر داخل الشات |

> النموذج اللغوي قد يصيغ النص فقط؛ **القرارات حتمية في الكود** عبر آلة الحالة.

هذا النظام مختلف عن `whatsapp_decision_bot` الداخلي المخصص للمؤسس وحده.

## المعمارية · من الرسالة إلى السجل

```
الرسالة الواردة (نص/زر)
      ↓
تصنيف النية (intent_router) — حتمي: زر ثم كلمات مفتاحية ثم unknown
      ↓
حارس السياسة (whatsapp_policy_guard) — كشف الأسرار + الطلبات غير الآمنة
      ↓
فحص التحويل البشري (handoff_router) — غموض/حساس/سعر/عقد/شكوى
      ↓
آلة الحالة (conversation_state) — المرحلة القادمة من (المرحلة، النية)
      ↓
بناء الكروت (action_card_builder) — menu/action/approval/permission/recommendation/report
      ↓
الحفظ والتدوين (client_profile_store) — سجلات JSONL، بلا PII خام
      ↓
الرد المحكوم (ClientOSResponse)
```

قاعدة صارمة: الرسالة المحجوبة (أسرار/غير آمنة) **لا تُقدِّم الحالة ولا تُخزَّن قيمتها أبدًا**.

## خريطة الموديول

| الملف | المسؤولية |
|---|---|
| `schemas.py` | كل النماذج (session, card, assessment, permission, handoff). |
| `intent_router.py` | تصنيف النية الحتمي من الأزرار والنص. |
| `whatsapp_policy_guard.py` | كشف الأسرار والطلبات غير الآمنة + تفويض السياسة القنواتية. |
| `conversation_state.py` | آلة الحالة: المراحل والانتقالات. |
| `assessment.py` | المحاور العشرة، التقييم، التوصية المربوطة بالكتالوج. |
| `permission_levels.py` + `permission_guard.py` | سلّم L0–L5 وبناء طلبات الصلاحية. |
| `action_card_builder.py` | بناء الكروت وحمولات واتساب التفاعلية (توليد فقط). |
| `handoff_router.py` | اكتشاف سبب التحويل وبناء حزمة السياق. |
| `templates.py` | تحميل وعرض القوالب الأربعة عشر. |
| `engine.py` | المنسّق: يربط المراحل السابقة في رد واحد محكوم. |
| `metrics.py` | مقاييس القمع من السجلات (بلا أرقام مخترعة). |
| `client_profile_store.py` | تخزين الجلسات والتقييمات والكروت والتحويلات. |

## نقاط الـ API

البادئة: `/api/v1/whatsapp-client-os`

| الطريقة | المسار | الغرض |
|---|---|---|
| POST | `/message` | المدخل الرئيسي (نص أو زر) ← رد محكوم. |
| POST | `/assessment/start` | بدء فحص الجاهزية. |
| POST | `/assessment/answer` | الإجابة على محور واحد. |
| GET | `/assessment/{id}/report` | تقرير الجاهزية (markdown + json). |
| GET | `/sessions` | قائمة الجلسات (عمليات المؤسس). |
| GET | `/sessions/{id}` | جلسة واحدة. |
| GET | `/action-cards` | الكروت المنتظرة (إجراء/موافقة/صلاحية). |
| POST | `/handoff/human` | فرض تحويل بشري مع السياق. |
| GET | `/metrics` | مقاييس القمع والتحويل. |
| GET | `/permissions/levels` | سلّم الصلاحيات L0–L5. |
| GET | `/templates` | مفاتيح القوالب المتاحة. |

## غير قابل للتفاوض (مختصر)

- لا مفاتيح/أسرار في الشات — بوابة آمنة فقط.
- لا واتساب بارد، لا أتمتة LinkedIn، لا scraping، لا إرسال جماعي أو قوائم مشتراة.
- موافقة بشرية لأي التزام خارجي.
- تحويل بشري عند الغموض/الحساس/السعر/العقد/الشكوى.
- كل توصية مربوطة بالكتالوج + مستوى دليل.
- كل إجراء مُدوَّن.

التفاصيل: [WHATSAPP_SECURITY_PRIVACY_AR.md](WHATSAPP_SECURITY_PRIVACY_AR.md) · الدستور: [../00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md)

## روابط المستندات

- سياسة المحادثة: [WHATSAPP_CONVERSATION_POLICY_AR.md](WHATSAPP_CONVERSATION_POLICY_AR.md)
- خريطة التدفق: [WHATSAPP_FLOW_MAP_AR.md](WHATSAPP_FLOW_MAP_AR.md)
- تجربة العميل: [WHATSAPP_CLIENT_EXPERIENCE_AR.md](WHATSAPP_CLIENT_EXPERIENCE_AR.md)
- فحص الجاهزية: [CLIENT_ONBOARDING_ASSESSMENT_AR.md](CLIENT_ONBOARDING_ASSESSMENT_AR.md)
- الصلاحيات: [WHATSAPP_PERMISSION_ONBOARDING_AR.md](WHATSAPP_PERMISSION_ONBOARDING_AR.md)
- التحويل البشري: [WHATSAPP_HANDOFF_POLICY_AR.md](WHATSAPP_HANDOFF_POLICY_AR.md)
- مكتبة القوالب: [WHATSAPP_TEMPLATE_LIBRARY_AR.md](WHATSAPP_TEMPLATE_LIBRARY_AR.md)
- كروت الموافقة: [WHATSAPP_APPROVAL_CARDS_AR.md](WHATSAPP_APPROVAL_CARDS_AR.md)
- الدعم والتصعيد: [WHATSAPP_SUPPORT_ESCALATION_AR.md](WHATSAPP_SUPPORT_ESCALATION_AR.md)
