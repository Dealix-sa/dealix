# Follow-up Sequence · تسلسل المتابعة

> 3-touch sequence over 7 days. Bilingual. WhatsApp + Email variants.
> Doctrine: every send manually approved (never auto). No WhatsApp on
> cold contacts (must be warm intro).

**Merge fields:** `{{lead_name}}`, `{{company}}`, `{{sector}}`,
`{{founder_name}}`, `{{diagnostic_url}}`, `{{calendly_url}}`,
`{{whatsapp_warm_consent_yes_no}}`.

---

## Touch 1 — Day 0: Initial outreach (post first contact)

### Channel decision tree

| Source | Channel | Reason |
|--------|---------|--------|
| Warm intro from existing customer | WhatsApp (with consent) | High permission |
| Warm intro from agency partner | Email (CC partner) | Maintains transparency |
| LinkedIn DM reply | LinkedIn DM (no escalation) | Stay where they are |
| Form submission on dealix.sa | Email | Their stated channel |
| Diagnostic completion | Email + calendar invite | Strong signal |

**Never use:** cold WhatsApp, cold LinkedIn DM (without prior connection),
purchased lists.

### Day 0 Email — Arabic

**Subject:** خطوة قصيرة بعد محادثتنا · {{lead_name}}

أهلًا {{lead_name}}،

شكرًا على وقتك أمس. كما اتفقنا، أرفق:

1. **ملخص مكتوب** للنقاش (نصف صفحة، PDF)
2. **Free Diagnostic** خاص بقطاع {{sector}}: [{{diagnostic_url}}]({{diagnostic_url}}) — ٦ أسئلة، ٢٤ ساعة ردّ.
3. **رابط حجز** لجلسة ١٥ دقيقة لو أردت تعمق: [{{calendly_url}}]({{calendly_url}})

لا التزام بأي خطوة. متى ما كان لديك سؤال — وقت ما كان.

{{founder_name}}

### Day 0 Email — English

**Subject:** Quick step after our conversation · {{lead_name}}

Hello {{lead_name}},

Thanks for your time yesterday. As discussed, attached:

1. **Written summary** of our discussion (half page, PDF)
2. **Free Diagnostic** for {{sector}}: [{{diagnostic_url}}]({{diagnostic_url}}) — 6 questions, 24h reply.
3. **Booking link** for a 15-min deep dive if you want to go further: [{{calendly_url}}]({{calendly_url}})

No commitment on any step. Whenever you have a question — anytime.

{{founder_name}}

### Day 0 WhatsApp — Arabic (warm consent only)

> ⚠️ Only send if `whatsapp_warm_consent_yes_no = yes` (logged in
> source_passport). Doctrine #2 (no_cold_whatsapp).

السلام عليكم {{lead_name}}،
شكراً على وقتك قبل قليل. أرسلت لك تفاصيل النقاش عبر الإيميل. لو
حصلت أسئلة، أنا متاح.
{{founder_name}}

### Day 0 WhatsApp — English (warm consent only)

Hi {{lead_name}} — appreciated the conversation earlier. I sent the
discussion summary by email. Available anytime for questions.
{{founder_name}}

---

## Touch 2 — Day 3: Value-add nudge

### Trigger

If no response by end of Day 2 KSA time, queue Day 3 draft.

### Day 3 Email — Arabic

**Subject:** نقطة مهمة لم نتطرق لها · {{company}}

أهلًا {{lead_name}}،

لاحظت بعد جلستنا نقطة مهمة لشركتكم {{company}}: غالب شركات
{{sector}} السعودية لديها فرصة في تتبع ICP-fit للـ leads الحالية —
وأغلبها لا يستخدم ranking system. هذه نقطة قد تستحق نقاش لاحق.

أرفقت مثالًا واحدًا (مجهول الهوية، من Sprint سابق) — صفحة واحدة
يوضح كيف تظهر هذه الفرصة في data B2B سعودية فعلية.

[{{anonymized_case_url}}]({{anonymized_case_url}})

لا حاجة للرد. لو رأيت قيمة في النقاش — أنا متاح.

{{founder_name}}

### Day 3 Email — English

**Subject:** A point we didn't cover · {{company}}

Hello {{lead_name}},

After our session, noticed an important angle for {{company}}: most
Saudi {{sector}} firms have an unexplored opportunity in
ICP-fit tracking on existing leads — most don't use a ranking
system. Could be worth a future conversation.

Attached one anonymized example (from a prior Sprint) — single page
showing how this opportunity surfaces in real Saudi B2B data.

[{{anonymized_case_url}}]({{anonymized_case_url}})

No need to reply. If you see value in continuing — I'm here.

{{founder_name}}

---

## Touch 3 — Day 7: Decision moment

### Day 7 Email — Arabic

**Subject:** قرار قصير · {{company}}

أهلًا {{lead_name}}،

اليوم آخر متابعة من جانبي. ثلاث خيارات الآن:

1. **بدء Sprint ٤٩٩ ر.س** — أبدأ لكم خلال ٢٤ ساعة (احجز:
   [{{calendly_url}}]({{calendly_url}}))
2. **Free Diagnostic أولًا** — قرار صغير بدون التزام
   ([{{diagnostic_url}}]({{diagnostic_url}}))
3. **لاحقًا** — أضع رقمكم في الـ nurture list، أعود بعد ٣٠ يوم
   بدون رسائل في الأثناء.

لو لم أسمع منك خلال ٧٢ ساعة — أعتبره **خيار ٣** تلقائيًا. لا متابعة
مزعجة.

شكرًا على وقتك {{lead_name}}،
{{founder_name}}

### Day 7 Email — English

**Subject:** A short decision · {{company}}

Hello {{lead_name}},

Last follow-up from me on this. Three options now:

1. **Start the 499 SAR Sprint** — I begin within 24h (book:
   [{{calendly_url}}]({{calendly_url}}))
2. **Free Diagnostic first** — smaller commitment
   ([{{diagnostic_url}}]({{diagnostic_url}}))
3. **Later** — I add you to the nurture list and reach out in 30
   days. No noise in between.

If I don't hear back within 72h I'll default to **option 3**.
No persistent follow-up.

Thanks for your time {{lead_name}},
{{founder_name}}

---

## Pipeline state transitions

| Touch | If no reply → | If reply ≠ yes → | If reply = yes → |
|-------|---------------|-------------------|-------------------|
| Day 0 | queue Day 3   | log objection     | move to Sprint    |
| Day 3 | queue Day 7   | address + extend  | move to Sprint    |
| Day 7 | → nurture     | log "no" reason   | move to Sprint    |

Log every transition in `pipeline_leads.last_status_change` (PR #522
audit recommendation). The `nurture` tag triggers a 30-day pause —
no contact during the window.

## Doctrine reminders

- Every send manually approved via `approval_center` (Doctrine #1).
- No WhatsApp without warm-consent flag (Doctrine #2).
- No autonomous follow-up — the founder presses "approve" on each
  draft (Doctrine #4).
- Suppression list checked before each send (Doctrine #5).
- "No reply" is a valid signal — respect it (no escalation).

## Audit trail

Each touch produces:
- `proof_ledger` event: `outbound_draft_approved` with approval_id
- `pipeline_leads.touches` increment
- `friction_log` entry if doctrine gate fired
