# SOP: حلقة المسوّدات اليومية بالموافقة أولاً — Daily Approval-First Drafts Loop

> **العربية أولاً · English parallel below.**
> هذا الإجراء يصف كيف يُنتج المؤسس ٥–١٠ مسوّدات تواصل دافئ ومتابعة يوميًا،
> يراجعها، ثم يرسلها **يدويًا**. لا شيء يُرسَل تلقائيًا. لا واتساب بارد.
> لا scraping. لا أتمتة LinkedIn.

---

## ١. الهدف — Objective (AR)

إنتاج خط أنابيب حقيقي عبر تواصل **دافئ مُعتمَد يدويًا** فقط:
- ٥–١٠ مسوّدات/يوم (مزيج تعريف دافئ + متابعة).
- كل مسوّدة تمر بمراجعة المؤسس قبل الإرسال.
- الإرسال يدوي بالكامل من حساب المؤسس الشخصي (LinkedIn DM / واتساب لجهة تعرفك / بريد).
- كل مسوّدة مربوطة بدرجة في السلّم: تشخيص مجاني → Sprint ٤٩٩ → Command Sprint.

> **القاعدة الحاكمة:** الأداة تكتب المسوّدة؛ الإنسان يقرر ويرسل. لا استثناء.

## ٢. المخرجات اليومية — Daily Outputs (AR)

| المخرج | العدد | المصدر |
|--------|-------|--------|
| مسوّدات تعريف دافئ | ٣–٧ | `scripts/warm_list_outreach.py` من `data/warm_list.csv` |
| مسوّدات متابعة | ٢–٣ | `sales/daily_drafts/SAMPLE_PACK_AR.md` (قسم المتابعة) |
| تحديث المتابعة | كل جهة | `docs/ops/pipeline_tracker.csv` |

## ٣. الخطوات — The Loop (AR)

1. **عبّئ القائمة الدافئة.** انسخ القالب مرة واحدة:
   `cp data/warm_list.csv.template data/warm_list.csv`
   ثم أضِف جهات تعرفها فعليًا (شبكتك، إحالات، لقاءات). الأعمدة:
   `name,role,company,sector,relationship,city,linkedin_url,notes`.
   **لا تُدخل أسماء أو أرقامًا لا تملك أساسًا مشروعًا للتواصل معها.**
2. **ولّد المسوّدات.** شغّل:
   `python scripts/warm_list_outreach.py`
   يكتب الناتج إلى `data/outreach/warm_list_drafts.md` (ملف للقراءة فقط — لا يُرسِل شيئًا خارجيًا).
   تظهر بجانب كل جهة شارة تأهيل (accept / diagnostic_only / reframe / reject / refer_out).
3. **راجِع بشريًا.** اقرأ كل مسوّدة:
   - هل العلاقة دافئة فعلًا (تعرفك الجهة أو هناك إحالة)؟ إن لا → احذفها.
   - هل اللهجة سليمة والاسم/الشركة صحيحان؟
   - هل ظهرت "doctrine violations"؟ إن نعم → ارفض الجهة بنظافة، لا ترسل.
4. **اختر ٥–١٠ فقط.** لا تتجاوز ١٠ في اليوم. الجودة قبل الحجم.
5. **أرسِل يدويًا.** انسخ النص والصقه في القناة المناسبة من حسابك الشخصي.
   احترم "غير مهتم" فورًا — لا تكرار.
6. **سجّل.** حدّث `docs/ops/pipeline_tracker.csv`: `sent_at`, `channel`, `reply_status`, `next_followup`.
7. **جدوِل المتابعة.** ضع تذكير +٢ / +٥ / +١٠ يوم لكل جهة (انظر cadence أدناه).

## ٤. حدود صارمة — Hard Limits (AR)

- لا إرسال آلي ولا جدولة آلية — كل رسالة بيد المؤسس.
- لا واتساب بارد لأرقام لا تملك أساس تواصل معها.
- لا scraping ولا قوائم مشتراة ولا بيانات بلا مصدر.
- لا أتمتة LinkedIn ولا أدوات تخالف شروط المنصّة.
- لا أرقام مبيعات مضمونة — استخدم "فرص مُثبتة بأدلة".
- لا أكثر من ٥ رسائل/ساعة، موزّعة على اليوم.

## ٥. إيقاع المتابعة — Follow-up Cadence (AR)

| اليوم | النوع | الغرض |
|-------|-------|-------|
| +٢ | تذكير لطيف | "وصلتك رسالتي؟" |
| +٥ | قيمة مضافة | شارك زاوية/مثال case-safe |
| +١٠ | إغلاق مهذّب | "أتركها لك — أخبرني إن تغيّر التوقيت" |

---

## 1. Objective (EN)

Build a real pipeline using **manually-approved warm outreach only**:
- 5–10 drafts/day (warm intros + follow-ups).
- Every draft passes founder review before it is sent.
- Sending is fully manual from the founder's own account (LinkedIn DM / WhatsApp to someone who knows you / email).
- Each draft is tied to a ladder rung: free diagnostic → 499 Sprint → Command Sprint.

> **Governing rule:** the tool writes the draft; the human decides and sends. No exceptions.

## 2. Daily Outputs (EN)

| Output | Count | Source |
|--------|-------|--------|
| Warm-intro drafts | 3–7 | `scripts/warm_list_outreach.py` from `data/warm_list.csv` |
| Follow-up drafts | 2–3 | `sales/daily_drafts/SAMPLE_PACK_AR.md` (follow-up section) |
| Follow-up logging | per contact | `docs/ops/pipeline_tracker.csv` |

## 3. The Loop (EN)

1. **Fill the warm list.** Copy the template once:
   `cp data/warm_list.csv.template data/warm_list.csv`
   then add people you actually know (your network, referrals, meetings). Columns:
   `name,role,company,sector,relationship,city,linkedin_url,notes`.
   **Never enter names or numbers you have no lawful basis to contact.**
2. **Generate drafts.** Run:
   `python scripts/warm_list_outreach.py`
   Output is written to `data/outreach/warm_list_drafts.md` (read-only file — it sends nothing externally).
   Each contact shows a qualification badge (accept / diagnostic_only / reframe / reject / refer_out).
3. **Review by hand.** For each draft:
   - Is the relationship genuinely warm (they know you, or there's a referral)? If not → delete it.
   - Is the tone right and the name/company correct?
   - Any "doctrine violations" flagged? If yes → decline the contact cleanly, do not send.
4. **Pick only 5–10.** Never exceed 10/day. Quality over volume.
5. **Send manually.** Copy the text and paste it into the right channel from your own account.
   Respect "not interested" immediately — no repeat outreach.
6. **Log it.** Update `docs/ops/pipeline_tracker.csv`: `sent_at`, `channel`, `reply_status`, `next_followup`.
7. **Schedule follow-up.** Set +2 / +5 / +10 day reminders per contact (cadence below).

## 4. Hard Limits (EN)

- No auto-send and no auto-scheduling — every message goes out by the founder's hand.
- No cold WhatsApp to numbers you have no basis to contact.
- No scraping, no purchased lists, no source-less data.
- No LinkedIn automation, no tools that violate platform terms.
- No guaranteed sales numbers — use "evidenced opportunities".
- No more than 5 messages/hour, spread across the day.

## 5. Follow-up Cadence (EN)

| Day | Type | Purpose |
|-----|------|---------|
| +2 | Gentle bump | "Did my note reach you?" |
| +5 | Value-add | Share an angle / case-safe example |
| +10 | Polite close | "I'll leave it with you — ping me if timing changes" |

---

## روابط — Related (AR + EN)

- مسوّدات جاهزة: [`daily_drafts/SAMPLE_PACK_AR.md`](daily_drafts/SAMPLE_PACK_AR.md)
- بناء خط الأنابيب قانونيًا: [`LEAD_INTAKE_FRAMEWORK_AR.md`](LEAD_INTAKE_FRAMEWORK_AR.md)
- بذور القطاعات: [`target_segments.csv`](target_segments.csv)
- سكربت مكالمة الاكتشاف: [`CALL_KIT_AR.md`](CALL_KIT_AR.md)
- مولّد المسوّدات: [`../scripts/warm_list_outreach.py`](../scripts/warm_list_outreach.py)
- قالب القائمة الدافئة: [`../data/warm_list.csv.template`](../data/warm_list.csv.template)
- متتبّع خط الأنابيب: [`../docs/ops/pipeline_tracker.csv`](../docs/ops/pipeline_tracker.csv)
- اعتراض واتساب الآلي: [`../docs/29_sales_os/OBJECTION_NO_WHATSAPP_AUTOMATION.md`](../docs/29_sales_os/OBJECTION_NO_WHATSAPP_AUTOMATION.md)
- اعتراض scraping: [`../docs/29_sales_os/OBJECTION_NO_SCRAPING.md`](../docs/29_sales_os/OBJECTION_NO_SCRAPING.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
