## دليل التواصل المباشر — Outreach Playbook (AR)

دليل التواصل المباشر في ديلكس يُدار يدوياً، بقيادة المؤسس، وبمراجعة بشرية على كل خطوة. لا scraping، لا cold WhatsApp، لا أتمتة LinkedIn، لا قواعد بيانات جاهزة من الإنترنت. كل اسم في القائمة وصلنا عبر مصدر معلن أو علاقة قائمة أو نموذج تسجيل صريح.

### الحلقة (7 خطوات)

1. **Segment** — تحديد القطاع والحجم والمسمّى الوظيفي.
2. **Lead list** — بناء قائمة دافئة (10–50 اسم/أسبوع) من LinkedIn، مؤتمرات، إحالات، نماذج تسجيل.
3. **Fit score** — تطبيق المعادلة الموزونة (راجع `dealix/revenue_marketing/scoring.py`) لترتيب القائمة.
4. **Pain hypothesis** — كتابة فرضية ألم في جملة لكل اسم، مرتبطة بإشارة معلنة.
5. **Manual send** — صياغة رسالة واحدة، إرسال يدوي، تسجيل في pipeline tracker.
6. **Follow-up cadence** — متابعة 3 محاولات بحد أقصى على مدى 14 يوماً، ثم إغلاق هادئ.
7. **Reply → Call** — أي ردّ، حتى السلبي، يُسجَّل ويُتابَع برأي بشري.

### معادلة الـ Fit Score (إشارة)

ديلكس يستخدم معادلة موزونة لترتيب الفرص (تفاصيل التطبيق في `dealix/revenue_marketing/scoring.py`). المكوّنات:

| المكوّن | الوزن المُقترَح | المصدر |
|---------|----------------|--------|
| ملاءمة الحجم (10–200 موظف) | 25% | LinkedIn، الموقع |
| ملاءمة القطاع (B2B، خدمات، تقنية، تجزئة B2B) | 20% | الملف العام |
| إشارة معلنة حديثة (تمويل، توسيع، توظيف، إعلان) | 25% | مصدر معلن (نُرفِق الرابط) |
| ملاءمة المسمّى الوظيفي (CEO، CRO، Head of Growth، CIO) | 15% | LinkedIn |
| اتصال موجود (إحالة، علاقة سابقة، حدث مشترك) | 15% | علاقات المؤسس |

الأوزان تُعدَّل عبر مراجعة شهرية. أي اسم بـ Fit Score < 60 يُحوَّل لقائمة "تنضيج" بدلاً من "إرسال".

### نموذج رسائل افتتاح (DRAFT — يحتاج اعتماد المؤسس قبل الإرسال)

#### Revenue Hunter Pilot — العميل المُحتمل: مؤسس B2B 30 موظف

**AR:**
> "السلام عليكم {{اسم}}. رأيت إعلانكم عن {{الإشارة}}. أنا سامي من ديلكس، نبني فرص مبيعات محكومة لشركات بحجم {{حجمكم}}. الباي‌لوت 999 ريالاً، 10 فرص خلال 7 أيام، كل واحدة بسجل أدلة. لو يهمّكم، أرسل لكم عيّنة فرصة قبل أي التزام."

**EN:**
> "Hello {{name}}. I saw your announcement on {{signal}}. I'm Sami from Dealix; we build governed sales opportunities for companies your size. The pilot is 999 SAR — 10 opportunities in 7 days, each with an evidence ledger. If useful, I can share a sample opportunity before any commitment."

**Status:** DRAFT — founder approval required before send.

#### AI Trust Kit — العميل المُحتمل: CIO في مؤسسة سعودية كبيرة

**AR:**
> "السلام عليكم {{اسم}}. الكثير من المؤسسات السعودية بدأت GenAI ولم تبني سجل أدلة. عندنا AI Trust Kit — أصول حوكمة جاهزة خلال أسبوعين. لو تسمحون، أرسل لكم Permission Matrix كعيّنة بدون أي التزام."

**EN:**
> "Hello {{name}}. Many Saudi enterprises started GenAI without building an evidence ledger. We have an AI Trust Kit — governance assets ready in two weeks. If you allow, I'll send you a Permission Matrix as a sample with no commitment."

**Status:** DRAFT — founder approval required before send.

#### Agency White-label — العميل المُحتمل: مدير وكالة رقمية سعودية

**AR:**
> "السلام عليكم {{اسم}}. الوكالات اللي زارتنا تشكو من نفس المشكلة: العميل يسأل عن AI ومافي أداة باسمهم. عندنا كيت White-label — منصة + قوالب + تدريب. 15K تفعيل + مشاركة إيراد. لو يهمّكم نقاش 20 دقيقة."

**EN:**
> "Hello {{name}}. Agencies we meet have the same complaint: clients ask for AI and they have no tool under their brand. We have a White-label Kit — platform + templates + training. 15K activation + revenue share. Happy to do a 20-minute call if useful."

**Status:** DRAFT — founder approval required before send.

### كادنس المتابعة

| اليوم | الإجراء | الحد |
|------|--------|-----|
| 0 | رسالة افتتاح | يدوي، مراجعة بشرية |
| +3 | متابعة قصيرة | "هل وصلت رسالتي؟" |
| +7 | إرسال أصل قيمة (Checklist أو Sample Report) | بلا CTA بيع |
| +14 | إغلاق هادئ | "أتمنى لكم التوفيق، أنا متاح متى أحببتم" |

بعد المحاولة 3، الاسم يُنقل لـ "تنضيج" لمدة 90 يوماً قبل أي محاولة جديدة.

### الأنماط الممنوعة (Anti-patterns)

- ❌ شراء قوائم WhatsApp.
- ❌ scraping LinkedIn أو أي موقع علني/خاص.
- ❌ أدوات أتمتة LinkedIn DM (Phantom، Expandi، إلخ.).
- ❌ Bulk email لقوائم غير مشترِكة.
- ❌ إرسال نيابة عن عميل دون موافقته الخطّية.
- ❌ ادّعاء علاقة سابقة لا تخصّك.
- ❌ تخصيص مزيّف ("أُعجبت بمنشورك الأخير" بدون قراءته فعلاً).

أي مخالفة لهذه الأنماط = إنذار داخلي + مراجعة فورية مع المؤسس.

---

## Outreach Playbook (EN)

The Dealix outreach playbook is run manually, founder-led, with human review at every step. No scraping, no cold WhatsApp, no LinkedIn automation, no ready-made internet databases. Every name on the list reached us via a public source, an existing relationship, or an explicit opt-in form.

### The Loop (7 Steps)

1. **Segment** — define sector, size, and role.
2. **Lead list** — build a warm list (10–50 names/week) from LinkedIn, conferences, referrals, opt-in forms.
3. **Fit score** — apply the weighted formula (see `dealix/revenue_marketing/scoring.py`) to rank.
4. **Pain hypothesis** — write a one-sentence pain hypothesis per name, tied to a public signal.
5. **Manual send** — craft one message, send manually, log in the pipeline tracker.
6. **Follow-up cadence** — at most 3 attempts over 14 days, then a quiet close.
7. **Reply → Call** — any reply, including negative, is logged and followed up by a human.

### Fit Score Formula (Reference)

Dealix uses a weighted formula to rank opportunities (implementation in `dealix/revenue_marketing/scoring.py`). Components:

| Component | Proposed Weight | Source |
|-----------|-----------------|--------|
| Size fit (10–200 employees) | 25% | LinkedIn, website |
| Sector fit (B2B, services, tech, B2B retail) | 20% | Public profile |
| Recent public signal (funding, expansion, hiring, announcement) | 25% | Public source (URL logged) |
| Role fit (CEO, CRO, Head of Growth, CIO) | 15% | LinkedIn |
| Existing connection (referral, prior relationship, shared event) | 15% | Founder relationships |

Weights are tuned monthly. Any name with Fit Score < 60 is moved to a "nurture" list instead of "send".

### Sample Opening Messages (DRAFT — founder approval required before send)

#### Revenue Hunter Pilot — Prospect: a 30-person B2B founder

(See AR section above. Same wording, founder-approved per send.)

**Status:** DRAFT — founder approval required before send.

#### AI Trust Kit — Prospect: CIO at a large Saudi enterprise

(See AR section above. Same wording, founder-approved per send.)

**Status:** DRAFT — founder approval required before send.

#### Agency White-label — Prospect: Saudi digital agency lead

(See AR section above. Same wording, founder-approved per send.)

**Status:** DRAFT — founder approval required before send.

### Follow-up Cadence

| Day | Action | Bar |
|-----|--------|-----|
| 0 | Opening message | Manual, human-reviewed |
| +3 | Short follow-up | "Did my message reach you?" |
| +7 | Send a value asset (Checklist or Sample Report) | No sales CTA |
| +14 | Quiet close | "Best of luck, I'm available whenever" |

After attempt 3, the name moves to "nurture" for 90 days before any new attempt.

### Forbidden Anti-patterns

- ❌ Buying WhatsApp lists.
- ❌ Scraping LinkedIn or any public/private site.
- ❌ LinkedIn DM automation tools (Phantom, Expandi, etc.).
- ❌ Bulk email to non-opt-in lists.
- ❌ Sending on a customer's behalf without their written approval.
- ❌ Claiming a prior relationship that does not exist.
- ❌ Fake personalization ("loved your recent post" without reading it).

Any breach = internal warning + immediate review with the founder.

---

**Disclosure / إفصاح:** Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

Cross-links: `dealix/revenue_marketing/scoring.py`, `docs/revenue_marketing/message_variants.md`, `docs/revenue_marketing/partner_kit.md`, `docs/ops/pipeline_tracker.csv`.
