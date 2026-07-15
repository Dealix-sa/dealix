# نظام التصريف — Dealix Distribution OS

> النسخة الإنجليزية القانونية: [`DEALIX_DISTRIBUTION_OS.md`](./DEALIX_DISTRIBUTION_OS.md).

## مرجع الدوكترين
- الالتزامات: #1، #2، #5.
- القرارات المثبّتة: الموافقة-أولًا للفعل الخارجي.

## الغرض

امتلاك كل المسارات من اكتشاف السوق إلى تحويل النقد، كمحفظة قنوات. كل قناة تُقاس، وأسبوعيًا تُضاعَف أو تُصلَح أو تُغلَق أو تُؤجَّل.

## المبدأ التشغيلي

التصريف محفظة، مو قناة واحدة. لا قناة تشتغل بدون فحص أسبوعي. لا قناة تتوسع بدون دليل تجربة.

## قنوات التصريف

1. تواصل المؤسس المباشر
2. استمارات التواصل (Inbound)
3. LinkedIn يدوي
4. drafts الإيميل
5. شركاء الإحالة
6. محتوى Inbound
7. تقارير قطاعية كـ Lead magnets
8. حسابات استراتيجية (ABM)
9. توسّع العملاء الحاليين
10. طلب مبني على الإثبات

## دورة القرار الأسبوعية

لكل قناة: ضاعف / أصلِح / أغلِق / أجِّل. قرار الأسبوع يُسجّل في `docs/founder/REVENUE_WAR_ROOM_OS_AR.md` ويُحدّث سجل التجارب.

## مؤشرات التشغيل (لكل قناة أسبوعيًا)

عملاء مكتشفون، مثرَون، معتمدون للتواصل، رسائل draft، رسائل مرسلة (بعد الموافقة)، ردود، ردود إيجابية، طلبات عينة، عروض، متابعات دفع، نقد مُحصَّل، طلبات احتفاظ، إحالات مستلمة.

أهداف كل قناة تُضبط بكل تجربة في `docs/distribution/EXPERIMENT_ENGINE_AR.md`، مو هاردكود.

## القواعد الجوهرية

- لا قناة تشتغل بدون مالك مسمى.
- لا قناة تتوسع بدون سجل تجربة.
- لا إرسال خارجي بدون سجل موافقة.
- لا لغة "ضمان" أو وعد نتائج في أي رسالة draft.
- قائمة الإيقاف تُفحص عند حدود القناة، مو وقت الإرسال فقط.

## الربط بالتشغيل

- `auto_client_acquisition/whatsapp_safe_send.py`.
- `auto_client_acquisition/outreach_window.py`.
- `api/routers/automation.py`.
- `autonomous_growth/orchestrator.py`، `autonomous_growth/agents/distribution`.
- `.github/workflows/founder_commercial_daily.yml`، `daily-revenue-machine.yml`.
- `scripts/dealix_founder_daily_brief.py`، `scripts/founder_cadence.sh`.

## روابط ذات صلة

- [`./EMAIL_DELIVERABILITY_SYSTEM_AR.md`](./EMAIL_DELIVERABILITY_SYSTEM_AR.md)
- [`./EXPERIMENT_ENGINE_AR.md`](./EXPERIMENT_ENGINE_AR.md)
- [`./ABM_STRATEGIC_ACCOUNT_MACHINE_AR.md`](./ABM_STRATEGIC_ACCOUNT_MACHINE_AR.md)
- [`../partners/PARTNER_REVENUE_MACHINE_AR.md`](../partners/PARTNER_REVENUE_MACHINE_AR.md)
- [`../founder/REVENUE_WAR_ROOM_OS_AR.md`](../founder/REVENUE_WAR_ROOM_OS_AR.md)
- [`../control_plane/APPROVAL_CENTER_V2_AR.md`](../control_plane/APPROVAL_CENTER_V2_AR.md)

## بنود مفتوحة

- بطاقة تصريف موحدة لكل القنوات في مكان واحد: غير موجودة.
- قنوات Content / Proof-based تعتمد على عامل الإثبات الجزئي.
- الجانب التنفيذي لسجل التجارب (استعلامات على قاعدة البيانات) ما زال مفتوحًا.
