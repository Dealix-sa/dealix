# Pilot Governance Model — حوكمة التجربة

## الغرض

كيف نحوكم pilot بمعايير نجاح واضحة وبوابة قبول.

## القاعدة غير القابلة للكسر

> AI يجهّز ويحلّل ويصيغ ويُقيّم ويرتّب ويوصي. المؤسس يراجع ويعتمد ويوقّع ويبيع ويرسل يدويًا ويقرر. النظام لا يرسل خارجيًا أبدًا.

## العناصر

- نطاق محدود
- معايير نجاح مقاسة
- بوابة قبول
- مسار التحول إلى retainer

## حدود الأمان (Safety Boundaries)

- لا إرسال خارجي (Email / WhatsApp / LinkedIn) من النظام أو من GitHub Actions.
- لا secrets ولا API keys ولا SMTP.
- لا scraping ولا auto-submit ولا أتمتة LinkedIn.
- لا إعلانات مدفوعة حيّة، ولا traction مزيّفة، ولا ROI مضمون.
- لا ادعاءات أمنية/امتثال غير مثبتة. كل المخرجات draft للمراجعة والاعتماد من المؤسس.

## التحقق (Verification)

- يُفحص هذا المستند ضمن سكربتات V10 verify ويُرفع تقريره في `outputs/v10_verification/`.
- المرجع الأعلى: `docs/master-command-center/` و`outputs/v10_verification/V10_MASTER_VERIFICATION.md`.
