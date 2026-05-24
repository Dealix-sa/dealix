# Email Outreach Guide | دليل التواصل عبر البريد

> Dealix never auto-sends. This guide is how the team drafts, queues, and approves email outreach that earns trust and books pipeline.

---

## 1. Operating Principle | المبدأ التشغيلي

Every Dealix-touched email is:
- **Drafted** (by operator + AI assist).
- **Queued** in the approval surface.
- **Approved** by the customer (when client-side) or by the founder/sales lead (when Dealix-side).
- **Sent** from the human's identity, not a brand inbox spoof.
- **Logged** in the evidence control plane.

No exceptions. No "batch sends." No "approve all without review."

---

## 2. Audience & Use Cases | الجمهور وحالات الاستخدام

| Use case | Audience | Channel | Cadence |
|---|---|---|---|
| Founder warm-intro | New buyer | Personal email | 1:1, drafted per recipient |
| Diagnostic follow-up | Form submitter | Personal email | within 24h, drafted by operator |
| Pilot outreach (client-side) | Client's prospects | Client team identity | drafted by Dealix, approved by client |
| Partner intro | Partner contact | Personal email | 1:1 |
| Newsletter | Consented list | Brand email | weekly |

---

## 3. Anatomy of a Dealix Email | تشريح البريد

| Part | Rule |
|---|---|
| From | Real human + real reply path. No no-reply for outreach. |
| Subject | ≤ 7 words, specific to the recipient or their company event. |
| Opener | Reference the recipient's context (role, hiring signal, news). No "hope you're well." |
| Body | 3–5 sentences max. Names one outcome, names the approval gate, names the next step. |
| CTA | One CTA. A specific time window or a one-click scheduler link. |
| Signature | Name, role, Dealix, mobile (optional), site. |
| Footer | If list-based, include physical address and one-click unsubscribe. PDPL-compliant. |

---

## 4. Template — Founder Warm Outreach (EN) | قالب — تواصل المؤسس

```
Subject: <Recipient-specific hook in ≤ 7 words>

Hi <First name>,

<1 sentence on the specific signal — hiring, news, growth, role change.>

<1 sentence on the pattern we have seen across similar KSA B2B teams (with range + N).>

<1 sentence on what we would explore in a 20-minute diagnostic.>

Worth a quick call <Tue/Wed> afternoon? Happy to send a link if useful.

— <Name>, Dealix
<Phone optional> | dealix.sa
```

---

## 5. Template — Founder Warm Outreach (AR) | قالب عربي

```
الموضوع: <عنوان قصير ومخصص للمستلم>

مرحباً <الاسم>،

<جملة تربط بسياق محدد عن الشركة أو الدور.>

<جملة عن نمط لاحظناه عبر فرق B2B سعودية مشابهة (مع نطاق وعدد مشاريع).>

<جملة عما سنستكشفه في تشخيص قصير لـ 20 دقيقة.>

هل يناسبك اتصال قصير يوم <الثلاثاء/الأربعاء>؟ يسعدني إرسال رابط الحجز إن أردت.

— <الاسم>، ديليكس
dealix.sa
```

---

## 6. Template — Diagnostic Follow-Up | متابعة التشخيص

```
Subject: Diagnostic prep — 3 quick inputs

Hi <First name>,

Thanks for booking the diagnostic for <date/time>. To make the 30 minutes useful, I'll send a written summary 24h after the call with:

— ICP density read on your current list
— Two sample bilingual drafts (you approve before any send)
— A 30-day Revenue Sprint shape, with ranges and conditions

Three quick inputs from you when convenient:
1) Current pipeline source mix
2) Two ICP examples you'd love more of
3) Any compliance constraints we should know

— <Name>, Dealix
```

---

## 7. Personalization Rules | قواعد التخصيص

- **One real signal** per email (hire, funding, product launch, public comment, sector event).
- Never use merge fields that the prospect can sniff out (`{{first_name}}` rendered or "I love your work").
- Never reference data the prospect did not put in public.
- Arabic personalization is written natively; do not transliterate names sloppily — verify spelling.

---

## 8. Approval Workflow | سير الموافقة

```
Operator drafts  →  Queue  →  Approver reviews
                →  Approve / Edit / Decline
                →  Send from human identity in approved window
                →  Log in evidence control plane
                →  Track reply  →  Apply lesson to template
```

- Approve rate, edit rate, decline rate are tracked per template and per ICP.
- Templates with > 30% decline rate are rebuilt, not retried.

---

## 9. Send Hygiene | نظافة الإرسال

- **Volume cap** per sender: align to mailbox provider best practice. We do not warm a brand new domain by blasting; we ramp gradually.
- **Reply path** is monitored daily. Bounces and complaints rebuild list quality before they impact deliverability.
- **Authentication:** SPF, DKIM, DMARC fully aligned on every sending domain.
- **List hygiene:** suppression list maintained; do not re-send to anyone who opted out, bounced hard, or said no.
- **No spoofing** of a customer's identity — Dealix sends from Dealix identities; client sends from client identities.

---

## 10. PDPL & Consent | الخصوصية والموافقة

- Saudi PDPL is the baseline. Process only the minimum personal data needed to send.
- Maintain a lawful basis (consent, legitimate interest with balance test) per list segment.
- Provide a clear, one-click unsubscribe. Honor within 24 hours.
- Reference: `docs/PRIVACY_PDPL_READINESS.md` and `docs/DPA_DEALIX_FULL.md`.

---

## 11. Reply Discipline | الردود

- Reply within 24 working hours.
- Replies stay in the same operator voice — no AI-only auto-reply.
- Pricing, contract, and payment questions: acknowledge, do not commit, escalate to the sales/founder owner.
- Negative or sensitive replies: thank, summarize what we will do, give a date for closure.

---

## 12. Don'ts | ما لا نفعله

- No bulk send under the founder's identity.
- No purchased lists. No scraped lists.
- No claim of customer logos, quotes, or specific revenue numbers in cold email.
- No "guaranteed" language.
- No spammy subject patterns ("Re:", "Fwd:" when there was none).

---

## 13. Non-Negotiables | الخطوط الحمراء

- No external sending without approval.
- No proof publishing without customer approval.
- No guaranteed-revenue claims.
- No pricing/contract commitments — escalate.
- Approval-gated automation only.

---

## 14. Owner & KPI | الملكية والمؤشرات

- **Owner:** Sales Lead, with Marketing Lead for templates and PDPL discipline.
- **KPI:** Reply rate per template per ICP (track baseline; iterate).
- **KPI:** Booked diagnostics per week from outreach.
- **KPI:** Spam complaint rate (target < 0.1%).
- **KPI:** Unsubscribe-honored-within-24h rate (target 100%).
- **KPI:** Non-negotiable violations (target 0).

---

## 15. Related Documents | مراجع

- `COPYWRITING_RULES.md`
- `BRAND_VOICE_EXAMPLES.md`
- `LINKEDIN_OUTREACH_GUIDE.md`
- `PARTNER_OUTREACH_GUIDE.md`
- `docs/PRIVACY_PDPL_READINESS.md`
- `docs/DPA_DEALIX_FULL.md`
