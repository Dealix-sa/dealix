# Email Draft Machine | آلة مسودات البريد الإلكتروني

## Purpose | الغرض
Convert outbound drafts into deliverability-safe email format, queue them for
founder approval, and never send externally without explicit approval.

## Inputs | المدخلات
- Outbound Draft Machine output
- Verified email address (via public sources or partner-provided)
- Email channel availability flag
- Founder daily email send budget

## Outputs | المخرجات
- `email.queue`: queue_id, draft_id, to_email, subject (≤ 80 chars),
  body_plain, body_html_optional, state, sent_at, response_id
- Daily approval list
- Deliverability check report (SPF, DKIM, blacklist, spam-score lint)

## Format constraints | قيود التنسيق
- Subject ≤ 80 chars, no ALL CAPS, no excessive punctuation
- Body plain-text preferred; HTML optional, minimal
- 1 link maximum, to a Dealix public page only
- No tracking pixels, no third-party tracking links
- AR or EN matched to persona

## Deliverability gate | بوابة التوصيل
- Domain auth in place (SPF/DKIM/DMARC checked at queue time)
- Subject + body run through spam-score lint (target < 3.0)
- Recipient domain not on internal block list
- Recipient email re-verified (MX check) at queue time

## Send protocol | بروتوكول الإرسال
1. Founder reviews and approves
2. Send via Dealix transactional provider (founder mailbox or controlled domain)
3. Per-mailbox daily cap enforced
4. Send result captured into `email.queue.sent_at` and response thread tracked

## Data source | مصدر البيانات
`email.queue`, `outbound.drafts`, `email.deliverability_log`.

## Approval class | فئة الموافقة
- A1: drafting, formatting, lint, queueing
- A2: per-email approval before send
- A3: emails to regulated/government recipients

## Trust gate | بوابة الثقة
- No tracking pixels or unauthorized tracking
- No price/contract/payment commitments
- No guaranteed revenue language
- Unsubscribe handled per PDPL norms
- Policy snapshot + audit row per send

## Owner | المالك
Founder approves every send.

## Worker name
`growth.email_drafter`

## KPI | المؤشرات
- Daily drafts produced / approved / sent
- Bounce rate (target < 3%)
- Spam-complaint rate (target < 0.1%)
- Reply rate, meeting-booked rate

## Failure mode | حالات الفشل
- Domain auth misconfigured → mass bounces
- Recipient email outdated → bounce
- Spam-score linter outdated → emails land in spam

## Recovery path | مسار الاسترداد
- Pre-send domain auth check; if failing, pause channel and alert founder
- MX re-check at queue time
- Weekly spam-score linter ruleset refresh
