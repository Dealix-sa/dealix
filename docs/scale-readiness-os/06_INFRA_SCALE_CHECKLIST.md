# قائمة جاهزية البنية التحتية | Infrastructure Scale Checklist

> **AR:** يوفّر هذا المستند قائمة تحقق للبنية التحتية قبل أي توسّع، لضمان أن الأنظمة تتحمّل الحمل المتزايد دون كسر الأمان أو الموثوقية. القائمة تُراجَع ويعتمدها المؤسس، ولا تُفعّل أي تغييرات إنتاجية تلقائيًا.
>
> **EN:** This document provides an infrastructure checklist before any scale, ensuring systems handle increased load without breaking security or reliability. The checklist is reviewed and founder-approved; no production changes activate automatically.

## محاور الجاهزية | Readiness Dimensions

| المحور Dimension | السؤال Question |
|---|---|
| الأداء / Performance | هل تتحمّل الأنظمة الحمل المتوقَّع؟ / Can systems handle expected load? |
| الموثوقية / Reliability | هل توجد نسخ احتياطية واسترجاع؟ / Backups and recovery in place? |
| الأمان / Security | هل الأسرار محمية وغير مكشوفة؟ / Secrets protected and not exposed? |
| المراقبة / Observability | هل التنبيهات والسجلات كافية؟ / Alerts and logging sufficient? |
| التكلفة / Cost | هل تكلفة البنية ضمن الاقتصاد؟ / Infra cost within unit economics? |

## قائمة التحقق | Checklist

- [ ] اختبار حمل يغطّي الطلب المتوقَّع. / Load test covering expected demand.
- [ ] نسخ احتياطي مُختبَر للاسترجاع. / Backups tested for restore.
- [ ] لا أسرار أو مفاتيح في الكود أو السجلات. / No secrets/keys in code or logs.
- [ ] مراقبة وتنبيهات على المسارات الحرجة. / Monitoring and alerts on critical paths.
- [ ] حدود معدّل وحماية من إساءة الاستخدام. / Rate limits and abuse protection.
- [ ] خطة تراجع (rollback) موثّقة. / Documented rollback plan.
- [ ] تقدير تكلفة البنية بعد التوسّع. / Post-scale infra cost estimate.

## عملية المراجعة | Review Process

1. تُملأ القائمة كمسودّة. / The checklist is filled as a draft.
2. تُراجَع البنود الحرجة (أمان، استرجاع). / Critical items reviewed (security, recovery).
3. يعتمد المؤسس الجاهزية قبل التوسّع. / Founder approves readiness before scaling.

## حدود الأمان | Safety Boundaries

- لا تطبيق تغييرات إنتاجية تلقائيًا من النظام. / No automatic production changes from the OS.
- لا أسرار أو مفاتيح API في أي مصنوع. / No secrets or API keys in any artifact.
- لا توسّع قبل اكتمال البنود الحرجة. / No scaling before critical items pass.

## قاعدة الأمان | Safety Rule

> الجاهزية التقنية شرط للتوسّع، والاعتماد بشري يدوي. / Technical readiness gates scaling; approval is human and manual.
