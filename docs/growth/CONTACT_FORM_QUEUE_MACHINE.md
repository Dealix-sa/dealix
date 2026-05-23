# Contact Form Queue Machine | آلة طابور نماذج التواصل

## Purpose | الغرض
For accounts that publish a contact form on their website (and no other channel
opens cleanly), draft and queue a form-friendly message. Founder submits manually
via the target site.

This machine exists because many KSA enterprises route inbound only through their
form — and submitting manually is the polite, legitimate path.

## Inputs | المدخلات
- B-bucket accounts with no LinkedIn/email channel signal
- Verified contact form URL
- Outbound Draft Machine content (compressed for form constraints)

## Outputs | المخرجات
- `form.queue`: queue_id, draft_id, form_url, name, company, email_used,
  message_text, state, submitted_at, screenshot_path
- Daily founder-friendly submission list

## Format constraints | قيود التنسيق
- Message ≤ 800 chars (most forms)
- Plain text only
- Phone number optional, only if founder consents
- One clear CTA: "Are you the right person, or who is?"
- AR/EN matched

## Submission protocol | بروتوكول الإرسال
1. Founder opens daily form list
2. Reviews and approves each draft
3. Founder manually opens form URL and submits
4. Founder uploads a confirmation screenshot
5. Worker records submitted_at and screenshot_path

## Anti-abuse rules | قواعد منع الإساءة
- Max 1 form submission per account per 60 days
- Never use fake names or fake company
- Always use a real reply-able email
- Do not bypass CAPTCHA programmatically

## Data source | مصدر البيانات
`form.queue`, `outbound.drafts`, `intelligence.accounts`.

## Approval class | فئة الموافقة
- A1: drafting, queueing
- A2: per-submission approval
- A3: forms on regulated/government sites

## Trust gate | بوابة الثقة
- No fake identity
- No CAPTCHA bypass
- No price/contract commitments
- Confirmation screenshot stored as audit evidence
- Policy snapshot + audit row per submission

## Owner | المالك
Founder owns the daily submission pass.

## Worker name
`growth.form_queue`

## KPI | المؤشرات
- Daily queue / approved / submitted
- Form-submission → response rate
- Response → meeting-booked rate

## Failure mode | حالات الفشل
- Form URL changes or breaks
- Form requires fields we can't honestly fill (e.g., RFP number)
- Multiple submissions to same account due to dedup miss

## Recovery path | مسار الاسترداد
- URL re-verified at queue time
- Drafts where required fields are unfillable are auto-quarantined for founder
- Strict dedup by (account_id, 60-day window)
