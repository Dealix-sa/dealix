# دليل المبيعات — Dealix Sales OS

الفهرس القانوني الوحيد لأصول المبيعات. عند التعارض بين ملفين، هذا الترتيب يحسم.

## المصدر الوحيد للأسعار

**`sales/PRICING_AND_OFFER_LADDER_AR.md`** — سلم العروض السداسي. أي ملف بيعي أو
صفحة موقع يجب أن يطابقه. نسخة الكود (تغذي الموقع كله):
`apps/web/lib/offers/canonical-offers.ts`.

| الدرجة | العرض | السعر |
|--------|-------|--------|
| 1 | التشخيص المجاني | مجاني (30 دقيقة) |
| 2 | Micro Sprint | 499 ريال |
| 3 | Data Intelligence Pack | 1,500 ريال |
| 4 | Managed AI Operations | 2,999–4,999 ريال/شهر (مسار موسع حتى 15,000) |
| 5 | Transformation Diagnostic Sprint — **نقطة الدخول** | 7,500–25,000 ريال (بيتا: 5,000–12,000) |
| 6 | Custom Enterprise System | 25,000–100,000+ ريال |

## رحلة البيع — أي ملف تستخدم متى

### 1. الفتح (أول تواصل)
- `CEO_INTRO_MESSAGE_AR.md` — رسالة التعريف الجاهزة للإرسال
- `ONE_PAGE_OFFER_AR.md` — الصفحة الواحدة تُرسل بعد الاهتمام
- `WHATSAPP_TEMPLATES_BY_SECTOR_AR.md` / `EMAIL_TEMPLATES_BY_SECTOR_AR.md` — قوالب حسب القطاع

### 2. مكالمة الاكتشاف
- `DISCOVERY_CALL_SCRIPT_AR.md` — سكربت المكالمة
- `playbook/QUALIFICATION_CHEATSHEET.md` — أسئلة التأهيل
- `playbook/FIVE_RUNG_RECOMMENDATION_GUIDE.md` — أي درجة من السلم تُقترح لمن

### 3. الاعتراضات
- `playbook/OBJECTION_BANK.md` — **النسخة الموسعة المعتمدة**
- `OBJECTION_HANDLING_AR.md` — النسخة المختصرة السريعة
- `NEGOTIATION_PLAYBOOK_AR.md` — التفاوض على السعر

### 4. العرض والإغلاق
- `PROPOSAL_TEMPLATE_AR.md` — قالب العرض الرسمي
- `PILOT_PROPOSAL_TEMPLATE_AR.md` — عرض السبرينت
- `custom_ai/CUSTOM_AI_PROPOSAL_TEMPLATE.md` — عروض المؤسسات (الدرجة 6)

### 5. المتابعة
- `FOLLOW_UP_SEQUENCE_AR.md` — تسلسل المتابعة الثلاثي (مسودات فقط)
- `playbook/WARM_LIST_CALL_SCRIPTS.md` — سكربتات القائمة الدافئة

### 6. الإيقاع اليومي والخطة
- `DAILY_FOUNDER_SELLING_ROUTINE_AR.md` — روتين البيع اليومي
- `FIRST_10_CLIENTS_PLAYBOOK_AR.md` — خطة أول 10 عملاء (90 يوم)

## صفحات الخدمات والحزم

- `service_pages/` — 5 ملفات خدمة كاملة (إيراد، تسويق، عمليات، ثقة، بوابة عميل)
  كلها مربوطة بسلم العروض
- `packages/DEALIX_COMMERCIAL_PACKAGES_AR.md` — الحزم الخمس بأسعار السلم

## الأدوات الحية (يولّدها النظام)

| الأداة | الأمر |
|--------|-------|
| عرض سعر عبر API | `POST /api/v1/proposals/render` |
| تشخيص مولّد | `POST /api/v1/commercial/diagnostic/generate` |
| رابط دفع (sandbox حتى قرار التفعيل) | `POST /api/v1/commercial/payment/link` |
| عروض تجريبية لكل السلم | `python3 scripts/launch/proposal_pack_dry_run.py` |
| الأمر اليومي للمؤسس | `python3 scripts/launch/founder_daily_command_dry_run.py` |

## القواعد غير القابلة للتفاوض

- لا إرسال خارجي بدون موافقتك — كل شيء مسودة أولاً.
- لا ضمانات نتائج ولا عملاء وهميين — لغة الفرضيات فقط (نتوقع، الهدف هو، سنقيس).
- كل عرض وفاتورة يمران بموافقتك الصريحة قبل الإرسال.
- القواعد الكاملة: `.claude/rules/dealix-commercial-os.md`.
