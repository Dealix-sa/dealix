# CEO Cockpit OS — قمرة قيادة الرئيس التنفيذي

## الغرض

لوحة واحدة تجمع revenue وpipeline وdelivery وsite وmedia وsafety وfinance assumptions والمخاطر والقرارات والإجراءات وتحذيرات no-go.

## القاعدة غير القابلة للكسر

> AI يجهّز ويحلّل ويصيغ ويُقيّم ويرتّب ويوصي. المؤسس يراجع ويعتمد ويوقّع ويبيع ويرسل يدويًا ويقرر. النظام لا يرسل خارجيًا أبدًا.

## الواجهات

- daily view
- weekly view
- monthly view
- decision queue
- risk queue
- opportunity queue

## التوليد

- يولّدها `scripts/ceo_cockpit_generate.py` إلى `outputs/ceo_cockpit/latest/CEO_COCKPIT.md`.

## حدود الأمان (Safety Boundaries)

- لا إرسال خارجي (Email / WhatsApp / LinkedIn) من النظام أو من GitHub Actions.
- لا secrets ولا API keys ولا SMTP.
- لا scraping ولا auto-submit ولا أتمتة LinkedIn.
- لا إعلانات مدفوعة حيّة، ولا traction مزيّفة، ولا ROI مضمون.
- لا ادعاءات أمنية/امتثال غير مثبتة. كل المخرجات draft للمراجعة والاعتماد من المؤسس.

## التحقق (Verification)

- يُفحص هذا المستند ضمن سكربتات V10 verify ويُرفع تقريره في `outputs/v10_verification/`.
- المرجع الأعلى: `docs/master-command-center/` و`outputs/v10_verification/V10_MASTER_VERIFICATION.md`.
