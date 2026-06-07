# Daily Operating Cadence — الإيقاع التشغيلي اليومي

إيقاع يومي بالأرقام لحزم اكتساب العملاء. كل يوم له هدف رقمي واحد، وكل رقم يُسجَّل في [../09_dashboards/daily_numbers_template.csv](../09_dashboards/daily_numbers_template.csv). قاعدة فوقية تحكم اليوم كله: `NO_LIVE_SEND` — لا شيء يُرسَل خارجياً دون مراجعة وموافقة بشرية. الإيقاع ثلاث كتل ثابتة (صباح، منتصف، مساء) حتى يكون اليوم قابلاً للتكرار والقياس لا مزاجياً.

روابط: [../02_daily_engine/DAILY_COMPANY_NUMBERS_ENGINE.md](../02_daily_engine/DAILY_COMPANY_NUMBERS_ENGINE.md) · [../05_outreach/OUTREACH_SCRIPTS.md](../05_outreach/OUTREACH_SCRIPTS.md) · [../03_offers/OFFER_PACKAGES.md](../03_offers/OFFER_PACKAGES.md) · [../10_compliance/COMPLIANCE_PACK.md](../10_compliance/COMPLIANCE_PACK.md) · [../../commercial/DEALIX_REVOPS_PACKAGES_AR.md](../../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · [../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md)

---

## كتلة الصباح

اختيار قطاع اليوم ومنطقته وتثبيتهما في صف اليوم (`sector`). بحث الشركات من المصادر العامة المسموح بها فقط: لا كشط، لا قوائم مشتراة، لا مصدر خارج السجل المسموح. تقييم كل شركة وتسجيلها في ملف التقييم. الهدف الرقمي للكتلة: ~50 شركة تُحلَّل (`companies_analyzed`)، و~15 تُؤهَّل (`companies_qualified`). الصباح هو كتلة المدخلات: كلما كان البحث أنظف ارتفعت جودة بقية اليوم.

## كتلة منتصف اليوم

إعداد ~10 مسودات مخصَّصة للمؤهَّلين (`drafts_prepared`) ودفعها إلى صندوق الموافقات. كل مسودة تربط الفجوة (`gap_identified`) بالعرض المناسب من حزمة العروض. يراجع المؤسس المسودات. ما تتم الموافقة عليه فقط يُرسَل يدوياً — لا إرسال تلقائي، لا إرسال جماعي، لا أتمتة واتساب أو لينكدإن. كل إرسال معتمَد يُسجَّل في `messages_sent_approved`. أي مسودة غير معتمَدة تبقى مسودة ولا تُرسَل.

## كتلة المساء

تسجيل النتائج: الردود (`replies`)، الاجتماعات المحجوزة (`meetings_booked`)، العروض المرسَلة (`proposals_sent`)، والإغلاقات (`closes`). ملء صف اليوم في `daily_numbers_template.csv` بالكامل وتسجيل `founder_minutes` — الوقت الفعلي الذي استثمره المؤسس في اليوم. تحديث حالات الشركات في خط الأنابيب وتحريك ما تقدّم. كل قيمة سعرية تقديرية لا متحقَّقة، وأي رقم نتيجة هو نمط آمن للحالة لا وعد.

## مجموعة الهدف اليومي

تُطابق أعمدة `daily_numbers_template.csv` بالضبط: `date, sector, companies_analyzed, companies_qualified, drafts_prepared, messages_sent_approved, replies, meetings_booked, proposals_sent, closes, founder_minutes, notes`.

- `date`: تاريخ اليوم التشغيلي.
- `sector`: القطاع الواحد المُشغَّل اليوم.
- `companies_analyzed`: ~50 (هدف لا ضمان).
- `companies_qualified`: ~15 (هدف لا ضمان).
- `drafts_prepared`: ~10 مسودات مخصَّصة.
- `messages_sent_approved`: ما وافق عليه المؤسس وأرسله يدوياً فقط.
- `replies` / `meetings_booked` / `proposals_sent` / `closes`: أنماط آمنة للحالة، لا أرقام مضمونة.
- `founder_minutes`: لقياس الكفاءة (مخرَج لكل دقيقة) لا حجم العمل.
- `notes`: ملاحظات اليوم والدروس وأي انحراف عن الهدف.

## ملاحظة المراجعة الأسبوعية

نهاية الأسبوع: جمع الصفوف اليومية السبعة، مقارنة الهدف بالفعلي عمود بعمود، وتحديد القطاعات الأعلى تأهيلاً مقابل `founder_minutes` المستثمَرة. القطاع الذي يعطي أعلى تأهيل لكل دقيقة يُعطى أولوية في الأسبوع التالي. لا أرقام تحويل أو إغلاق تُعرض كحقيقة — كلها تقديرية وأنماط آمنة للحالة. تُوثَّق الدروس في `notes` لتغذية اختيار القطاع التالي. تظل قاعدة `NO_LIVE_SEND` سارية في المراجعة كما في التشغيل: المراجعة تقيس ما حدث، ولا تأذن بإرسال جماعي مؤجَّل.

---

# Daily Operating Cadence

A daily rhythm by the numbers for the Client Acquisition Packs. Each day has one numeric target, and every number is logged in [../09_dashboards/daily_numbers_template.csv](../09_dashboards/daily_numbers_template.csv). One rule governs the whole day: `NO_LIVE_SEND` — nothing is sent externally without human review and approval. The rhythm is three fixed blocks (morning, midday, evening) so the day stays repeatable and measurable, not mood-driven.

Links: [../02_daily_engine/DAILY_COMPANY_NUMBERS_ENGINE.md](../02_daily_engine/DAILY_COMPANY_NUMBERS_ENGINE.md) · [../05_outreach/OUTREACH_SCRIPTS.md](../05_outreach/OUTREACH_SCRIPTS.md) · [../03_offers/OFFER_PACKAGES.md](../03_offers/OFFER_PACKAGES.md) · [../10_compliance/COMPLIANCE_PACK.md](../10_compliance/COMPLIANCE_PACK.md) · [../../commercial/DEALIX_REVOPS_PACKAGES_AR.md](../../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · [../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md)

---

## Morning block

Select the day's sector and region and fix them in the day's row (`sector`). Source companies from allowed public sources only: no scraping, no purchased lists, no source outside the allowed registry. Score and record each company in the scoring file. The block's numeric target: ~50 companies analyzed (`companies_analyzed`) and ~15 qualified (`companies_qualified`). Morning is the input block: the cleaner the research, the higher the quality of the rest of the day.

## Midday block

Prepare ~10 tailored drafts for the qualified set (`drafts_prepared`) and push them to the approval inbox. Each draft links the gap (`gap_identified`) to the right offer from the offer set. The founder reviews the drafts. Only approved drafts are sent manually — no automated send, no bulk send, no WhatsApp or LinkedIn automation. Every approved send is recorded in `messages_sent_approved`. Any unapproved draft stays a draft and is not sent.

## Evening block

Record results: replies (`replies`), meetings booked (`meetings_booked`), proposals sent (`proposals_sent`), and closes (`closes`). Fill the day's row in `daily_numbers_template.csv` completely and log `founder_minutes` — the actual time the founder invested in the day. Update company statuses in the pipeline and advance what progressed. Every price value is estimated, not verified, and any result number is a case-safe pattern, not a promise.

## The daily target set

Maps exactly to the `daily_numbers_template.csv` columns: `date, sector, companies_analyzed, companies_qualified, drafts_prepared, messages_sent_approved, replies, meetings_booked, proposals_sent, closes, founder_minutes, notes`.

- `date`: the operating day's date.
- `sector`: the single sector run that day.
- `companies_analyzed`: ~50 (target, not guarantee).
- `companies_qualified`: ~15 (target, not guarantee).
- `drafts_prepared`: ~10 tailored drafts.
- `messages_sent_approved`: only what the founder approved and sent manually.
- `replies` / `meetings_booked` / `proposals_sent` / `closes`: case-safe patterns, not guaranteed numbers.
- `founder_minutes`: to measure efficiency (output per minute), not workload.
- `notes`: the day's notes, lessons, and any deviation from target.

## Weekly review note

End of week: aggregate the seven daily rows, compare target vs. actual column by column, and identify the highest-qualifying sectors against the `founder_minutes` invested. The sector that yields the highest qualification per minute gets priority next week. No conversion or close numbers are presented as fact — all are estimated and case-safe patterns. Lessons are documented in `notes` to feed the next sector choice. The `NO_LIVE_SEND` rule stays in force during review as in operation: review measures what happened and never authorizes a deferred bulk send.

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
