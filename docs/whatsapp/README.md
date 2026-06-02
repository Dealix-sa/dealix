# Dealix WhatsApp Client OS — فهرس التوثيق · Documentation Index

مساعد سير عمل أعمال محكوم عبر واتساب لشركات B2B السعودية — **وليس** شات بوت عام.
هذه الحزمة توثيقية فقط؛ الكود مبني بالفعل.

- **الموديول (الكود):** `auto_client_acquisition/whatsapp_client_os/`
- **مسار الـ API:** `/api/v1/whatsapp-client-os`
- **الراوتر:** `api/routers/whatsapp_client_os.py`
- **بيانات الفحص والقوالب:** `data/whatsapp/assessment_questions.yaml` · `data/whatsapp/templates.yaml`

## المستندات · Documents

| # | الملف | الوصف بسطر واحد |
|---|---|---|
| 1 | [WHATSAPP_CLIENT_OS_AR.md](WHATSAPP_CLIENT_OS_AR.md) | النظرة الشاملة: ما هو وما ليس، المعمارية (webhook → guard → state machine → cards → audit)، خريطة الموديول، نقاط الـ API. |
| 2 | [WHATSAPP_CONVERSATION_POLICY_AR.md](WHATSAPP_CONVERSATION_POLICY_AR.md) | قواعد تجربة المحادثة: رسائل قصيرة، خيار واحد واضح، «ما أعرف — اقترح علي»، «الخطوة X من Y»، توجيه حتمي. |
| 3 | [WHATSAPP_FLOW_MAP_AR.md](WHATSAPP_FLOW_MAP_AR.md) | رحلات العميل الخمس + جدول المراحل والانتقالات. |
| 4 | [WHATSAPP_CLIENT_EXPERIENCE_AR.md](WHATSAPP_CLIENT_EXPERIENCE_AR.md) | تجربة العميل قبل/أثناء/بعد الشراء، وكيف ينافس Dealix الكبار. |
| 5 | [WHATSAPP_SECURITY_PRIVACY_AR.md](WHATSAPP_SECURITY_PRIVACY_AR.md) | قاعدة عدم إرسال الأسرار في الشات، مسار البوابة الآمنة، وعي PDPL، لا PII في السجلات، القائمة الممنوعة. |
| 6 | [CLIENT_ONBOARDING_ASSESSMENT_AR.md](CLIENT_ONBOARDING_ASSESSMENT_AR.md) | «فحص جاهزية الشركة»: المحاور العشرة، الركائز الثلاث، التقييم، نطاقات المخاطرة، نموذج التقرير. |
| 7 | [WHATSAPP_PERMISSION_ONBOARDING_AR.md](WHATSAPP_PERMISSION_ONBOARDING_AR.md) | سلّم الصلاحيات L0–L5، القواعد، مسار «نحتاج مفتاح/رابط» الآمن، كرت الصلاحية. |
| 8 | [WHATSAPP_HANDOFF_POLICY_AR.md](WHATSAPP_HANDOFF_POLICY_AR.md) | متى نصعّد لشخص (الأسباب التسعة)، حزمة التحويل، حفظ السياق بلا PII. |
| 9 | [WHATSAPP_TEMPLATE_LIBRARY_AR.md](WHATSAPP_TEMPLATE_LIBRARY_AR.md) | القوالب الأربعة عشر، غرضها، قواعد النبرة، والنص العربي الفعلي لكل قالب. |
| 10 | [WHATSAPP_APPROVAL_CARDS_AR.md](WHATSAPP_APPROVAL_CARDS_AR.md) | أنواع الكروت، أمثلة كرت الإجراء/الموافقة/الصلاحية، وقاعدة الموافقة الصريحة قبل أي إرسال خارجي. |
| 11 | [WHATSAPP_SUPPORT_ESCALATION_AR.md](WHATSAPP_SUPPORT_ESCALATION_AR.md) | قائمة الدعم، تصنيف الإلحاح، خدمة ذاتية/تذكرة/شخص، ومسار «أحتاج شخص». |

## المرجع · Source of truth

كل ادعاء في هذه المستندات مشتق من الكود المبني. عند أي اختلاف، الكود هو المرجع:

- النماذج: `auto_client_acquisition/whatsapp_client_os/schemas.py`
- التقييم والتوصية: `auto_client_acquisition/whatsapp_client_os/assessment.py`
- آلة الحالة: `auto_client_acquisition/whatsapp_client_os/conversation_state.py`
- حارس السياسة: `auto_client_acquisition/whatsapp_client_os/whatsapp_policy_guard.py`
- التحويل البشري: `auto_client_acquisition/whatsapp_client_os/handoff_router.py`
- الصلاحيات: `auto_client_acquisition/whatsapp_client_os/permission_levels.py`

الدستور: [../00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md)
