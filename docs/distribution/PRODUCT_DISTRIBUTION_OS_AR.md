# Dealix Product Distribution OS — النظام الكامل لتصريف المنتجات

> الهدف: تشغيل يومي يصرّف منتجات Dealix فعليًا — قابل للقياس، آمن، ومبني على
> موافقات وأدلة. **بدون** أن يتحول إلى spam أو أتمتة خطيرة.

## 1. لماذا هذه الطبقة؟

الذكاء الاصطناعي في المبيعات يتدرّج: **augmentation** (يساعد البائع) →
**automation** (مهام محددة) → **controlled autonomy** (تنسيق workflows). كلما زادت
الصلاحيات زادت المخاطر — لذلك كل شيء هنا يبدأ كـ augmentation محكوم: النظام يجهّز،
والمؤسس يقرّر ويرسل.

## 2. المبدأ الأم

```
operating_mode = draft_only_no_auto_send
```

- كل draft / proposal / proof / payment / renewal يبدأ `*_pending_approval`.
- لا قناة ترسل تلقائيًا. لا رابط دفع يُنشأ أو يُرسل تلقائيًا.
- الأدلة موسومة بمستوى L0–L5؛ الاستخدام العام يتطلب L4 + موافقة.

## 3. التدفق اليومي

```
اكتشاف فرصة → اختيار قطاع → اختيار حسابات → توليد مسودات → فحص جودة
→ موافقة → إرسال يدوي → متابعة → تشخيص → عرض → proof pack
→ تسليم دفع → تسليم → تقرير → تجديد/upsell → تعلّم
```

## 4. المعمارية

| الطبقة | المكان |
| --- | --- |
| منطق مُختبَر | `dealix/distribution/` |
| أوامر CLI | `scripts/*.py` (عبر Makefile) |
| مخططات | `schemas/*.schema.json` |
| إعداد/أمثلة | `data/distribution/*` (مُتعقّبة) |
| سجلات زمنية | `data/<type>/*.jsonl` (متجاهَلة — لا PII في git) |
| تقارير | `reports/distribution/*` (متجاهَلة — قد تحوي أسماء عملاء) |

تعتمد الطبقة على ركائز موجودة بدل تكرارها:

- الحوكمة: `auto_client_acquisition/safe_send_gateway` (نفس non-negotiables المطبّقة بالاختبارات).
- مستويات الأدلة: `auto_client_acquisition/proof_engine/evidence` (L0–L5).
- كتالوج العروض: `os/03_OFFERS.yml` (التسعير في مكان واحد — لا أرقام مخترعة).
- تنقية PII/الأسرار: `auto_client_acquisition/security_privacy/log_redaction`.

## 5. الأوامر

```bash
make distribution-day        # السلسلة الكاملة (PASS/FAIL)
make distribution-drafts     # توليد مسودات حسب القطاع
make draft-quality           # بوابة الجودة (تفشل إن وُجدت مسودة غير آمنة)
make draft-queue             # قائمة الموافقة
make followup-queue          # المتابعات المستحقة (تذكير فقط)
make proposal-drafts         # عروض من الكتالوج الرسمي
make proof-packs             # أطقم إثبات (L1 افتراضيًا)
make payment-handoffs        # تسليم دفع (لا رابط تلقائي)
make renewal-queue           # تجديد/upsell (لا upsell قبل proof)
make distribution-metrics    # لوحة المؤشرات
make win-loss                # تعلّم الربح/الخسارة
make distribution-weekly     # المراجعة الأسبوعية
```

## 6. خرج التشغيل

- `DEALIX_DISTRIBUTION_DAY=PASS|FAIL` (متوافق مع بقية مُحقّقات Dealix).
- `reports/distribution/DISTRIBUTION_DAY.md` — ملخص المؤسس + الخطوة التالية.
- `FAIL` يحدث فقط إذا فشلت مدخلات الـ prospects أو بوابة جودة المسودات.

## 7. ماذا يفعل المؤسس غدًا؟

1. شغّل `make distribution-day`.
2. افتح قائمة الموافقة (`make draft-queue`) واعتمد الأنسب أولًا.
3. انسخ المسودة المعتمدة وأرسلها يدويًا عبر القناة المناسبة.
4. سجّل النتائج لاحقًا عبر `make win-loss --record` لتغذية التعلّم.

## 8. ما الذي لا تفعله هذه الطبقة (عمدًا)

- لا ترسل بريدًا/واتساب/LinkedIn تلقائيًا.
- لا تعمل scraping ولا جمع ويب غير مصرّح.
- لا تنشئ/ترسل روابط دفع ولا تسحب بطاقات.
- لا تطلق وعودًا مضمونة ولا أرقامًا غير مثبتة.

## 9. الخطوات التالية (PRs لاحقة)

- واجهة المؤسس `Founder Revenue Control Room` (`/[locale]/ops/revenue-control`).
- Distribution API (`api/routers/distribution.py`) بمفتاح admin + audit log.
- تدفقات n8n حتمية (intake/تذكير/مزامنة) — بصلاحيات مضبوطة، لا إرسال في CI.
- Playwright E2E لمسار «الموافقة أولًا» (نختبر حالة النسخ اليدوي، لا إرسالًا حقيقيًا).
