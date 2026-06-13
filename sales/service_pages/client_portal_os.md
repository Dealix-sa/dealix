# Dealix Client Portal OS

Make your value visible to clients through progress, proof, documents, and renewal signals.

Deliverables:
- client portal map
- proof room
- executive client report
- renewal tracker

> Client Portal OS طبقة الإثبات والتجديد التي تعرض مخرجات الباقات في كتالوج التسعير الداخلي (`finance_os/pricing_catalog.py`) — مصدر الحقيقة الوحيد. تستند إلى **Proof Pack موقَّع** من **باقة بداية النمو — Pilot (499 ريال)** و**Proof Pack شهري** من **نظام تشغيل القيادة التنفيذية (2,999 ريال/شهر)**. وعدها رؤية موثّقة، لا رقم تجديد.

## الوعد / The Promise

نجعل قيمتك مرئية للعميل عبر التقدّم والأدلة والمستندات وإشارات التجديد: غرفة إثبات (Proof Room) تعرض ما نُفّذ، تقرير تنفيذي للعميل، ومتتبّع تجديد يربط القرار بالأدلة المسجّلة. كل ما يُعرض في البوابة مربوط بالسجل (ledger-backed) ومأخوذ من Proof Pack موقَّع أو شهري — لا ادعاءات بلا مصدر، ولا أرقام تجديد موعودة. الإثبات الموثّق هو أساس قرار التجديد، لا الوعد.

We make your value visible to the client through progress, proof, documents, and renewal signals: a Proof Room showing what was executed, an executive client report, and a renewal tracker that links the decision to recorded evidence. Everything shown in the portal is ledger-backed and drawn from a signed or monthly Proof Pack — no claims without a source, and no promised renewal numbers. Documented proof is the basis for the renewal decision, not a promise.

## العميل المثالي / Ideal Customer

- مزوّد خدمة يحتاج إظهار قيمته للعميل قبل نقاش التجديد.
- وكالة أو شركة تشغيل تريد غرفة إثبات بدل رسائل WhatsApp متفرقة.
- صاحب قرار يطلب رؤية تنفيذية موثّقة قبل توقيع ريتينر.

- A service provider who needs to show value to the client before the renewal conversation.
- An agency or ops firm that wants a Proof Room instead of scattered WhatsApp threads.
- A decision-maker who wants documented executive visibility before signing a retainer.

## المخرجات / Deliverables

تعرض البوابة مخرجات الباقات من الكتالوج وتنظّمها كإثبات وتجديد:

**من باقة بداية النمو — Pilot (`includes`):**
- Proof Pack موقَّع يوثّق الـ 10 فرص والمتابعة (`signed_proof_pack`)

**من نظام تشغيل القيادة التنفيذية (`includes`):**
- موجز تنفيذي أسبوعي للعميل (`weekly_executive_brief`)
- Proof Pack شهري كأساس لقرار التجديد (`monthly_proof_pack`)
- ساعة مكتب أسبوعية مع المؤسس (`founder_office_hour_each_week`)
- كل مزايا الباقات الأدنى (`all_lower_tier_features`)

**طبقة البوابة:** خريطة بوابة العميل، غرفة إثبات، تقرير تنفيذي للعميل، ومتتبّع تجديد.

The portal surfaces catalog deliverables and organizes them as proof and renewal:

- A signed Proof Pack from the **Growth Starter Pilot** recording the 10 opportunities and follow-up (`signed_proof_pack`).
- A weekly executive brief, a monthly Proof Pack as the renewal basis, a weekly founder office hour, and all lower-tier features from **Executive Growth OS**.
- Portal layer: client portal map, Proof Room, executive client report, and renewal tracker.

## ما لا يشمله / Out of Scope

- لا وعود إيراد مضمونة (`guaranteed_revenue_promises`).
- لا خصم خارجي مباشر (`live_external_charge`) دون موافقة موثّقة.
- لا عرض أدلة غير مربوطة بالسجل، ولا أرقام تجديد أو ROI مضمونة.

- No guaranteed revenue promises (`guaranteed_revenue_promises`).
- No live external charge (`live_external_charge`) without documented approval.
- No display of proof that is not ledger-backed, and no guaranteed renewal or ROI figures.

## السعر ومسار الترقية / Price & Upgrade Path

| الباقة / Tier | السعر / Price | الأساس / Basis | مسار الترقية / Upgrade |
|---|---|---|---|
| باقة بداية النمو — Pilot / Growth Starter Pilot | 499 ريال / 499 SAR | دفعة واحدة / one-shot | ← نظام تشغيل القيادة التنفيذية / Executive Growth OS |
| نظام تشغيل القيادة التنفيذية / Executive Growth OS | 2,999 ريال/شهر / 2,999 SAR/mo | شهري متكرّر / recurring | ← برج التحكّم الكامل (مخصّص) / full control tower (custom) |

غرفة الإثبات تبدأ بـ Proof Pack موقَّع من الـ Pilot، ثم تتغذّى شهرياً تحت Executive Growth OS كأساس لقرار التجديد.

The Proof Room starts with a signed Proof Pack from the Pilot, then is fed monthly under Executive Growth OS as the basis for the renewal decision.

## شرط الإغلاق / Closing Terms

- لا إرسال آلي — كل رسالة أو مستند يبقى مسوّدة حتى موافقة العميل الصريحة.
- لا ضمان ROI بدون baseline موثّق.
- كل رسالة خارجية تحتاج موافقة قبل الإرسال.
- كل دليل في البوابة مربوط بالسجل (ledger-backed)، لا ادعاءات بلا مصدر.

- No auto-send — every message or document stays a draft until explicit client approval.
- No ROI guarantee without a documented baseline.
- Every external message requires approval before sending.
- All proof in the portal is ledger-backed; no claims without a source.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

روابط: [/ar/services](/ar/services) · [/en/services](/en/services)
