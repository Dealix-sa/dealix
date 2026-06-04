# Revenue Pipeline Rules — قواعد خط أنابيب الإيرادات

## الغرض (AR)
يعرّف هذا المستند مراحل خط الأنابيب وقواعد الانتقال بينها. كل انتقال يجب أن يكون مبررًا بحدث مُسجّل يدويًا، وكل تواصل خارجي يبقى يدويًا ومعتمدًا من المؤسس.

## Purpose (EN)
This document defines the pipeline stages and the rules for transitioning between them. Every transition must be justified by a manually recorded event, and all external contact remains manual and founder-approved.

## المراحل / Stages

| المرحلة / Stage | الوصف / Description |
|---|---|
| raw_lead | عميل خام / Raw, unworked lead |
| researched | تم البحث / Context gathered |
| draft_generated | مسودة مُولّدة / Draft produced |
| founder_review | مراجعة المؤسس / Founder reviewing |
| manual_action_selected | إجراء يدوي معتمد / Approved manual action |
| manually_contacted | تم التواصل يدويًا / Manually contacted |
| reply_positive | رد إيجابي / Positive reply |
| reply_neutral | رد محايد / Neutral reply |
| reply_negative | رد سلبي / Negative reply |
| discovery_booked | حجز اكتشاف / Discovery booked |
| diagnostic_proposed | عُرض التشخيص / Diagnostic proposed |
| diagnostic_sold | بيع التشخيص / Diagnostic sold |
| diagnostic_delivered | تسليم التشخيص / Diagnostic delivered |
| pilot_proposed | عُرضت التجربة / Pilot proposed |
| pilot_sold | بيع التجربة / Pilot sold |
| pilot_delivered | تسليم التجربة / Pilot delivered |
| retainer_proposed | عُرض العقد / Retainer proposed |
| retainer_started | بدء العقد / Retainer started |
| expansion_identified | فرصة توسّع / Expansion identified |
| lost | مفقود / Lost |
| suppressed | مُستبعد / Suppressed |

## قواعد الانتقال / Transition Rules
- **التقدّم للأمام فقط بحدث** / Forward movement requires a recorded event: لا تنتقل الصفقة إلى `manually_contacted` إلا بحدث `manual_send_recorded`.
- **لا قفز للمراحل** / No skipping: يجب المرور بـ`founder_review` و`manual_action_selected` قبل أي تواصل.
- **الردود حصرية** / Reply states are exclusive: واحدة فقط من `reply_positive/neutral/negative`.
- **التشخيص قبل التجربة** / Diagnostic precedes pilot: لا `pilot_proposed` قبل `diagnostic_delivered` (إلا باستثناء موثّق).
- **التجربة قبل العقد** / Pilot precedes retainer: لا `retainer_proposed` قبل `pilot_delivered`.
- **lost و suppressed نهائيتان** / Terminal states: يمكن إعادة التنشيط فقط بقرار مؤسس موثّق.
- **suppressed تعني عدم التواصل** / Suppressed = do-not-contact: تُحترم دائمًا ولا تُتجاوز آليًا.

## السلامة / Safety
- لا انتقال تلقائي يُحرّك تواصلًا خارجيًا.
- لا كشط، لا إرسال آلي، لا تعبئة نماذج.

No transition triggers external contact automatically. No scraping, no auto-sending, no form auto-submit.
