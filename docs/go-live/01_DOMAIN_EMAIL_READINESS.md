# Domain & Email Readiness — جاهزية النطاق والبريد

Email authentication and reputation setup that must pass before any external send. Authenticated mail protects the domain, the recipient, and the Dealix sender reputation.

إعداد مصادقة البريد والسمعة الذي يجب أن يجتاز قبل أي إرسال خارجي. البريد المُصادَق يحمي النطاق والمستلم وسمعة المُرسِل.

## DNS records — سجلات DNS

| Record | Purpose | Pass condition |
|---|---|---|
| MX | Mail routing | Resolves to the chosen provider |
| SPF | Authorizes sending hosts | One TXT record, no overlap, ends in `-all` or `~all` |
| DKIM | Signs outgoing mail | Public key published; mail signs and verifies |
| DMARC | Policy + reporting | `p=quarantine` or `p=reject` with `rua` reporting address |

## SPF — إطار سياسة المُرسِل

- Publish a single SPF TXT record listing only the provider(s) actually used.
- Avoid more than 10 DNS lookups.
- Verify with a checker before go-live.

## DKIM — مفاتيح بريد المجال

- Generate the key in the email provider, publish the public key in DNS.
- Confirm outgoing mail carries a valid DKIM signature that passes verification.

## DMARC — مصادقة الرسائل

- Start at `p=none` with `rua` reporting to observe alignment.
- Move to `p=quarantine`, then `p=reject` once SPF and DKIM align cleanly.
- Keep a monitored mailbox for `rua` aggregate reports.

## Google Postmaster Tools — أدوات مشرفي البريد من Google

- Verify the sending domain in Postmaster Tools.
- Monitor: spam rate, domain reputation, IP reputation, authentication pass rate.
- **Keep the spam rate under 0.3%.** Approaching 0.3% pauses the ramp and triggers review.

## Bounce tracking — تتبّع الارتداد

- Capture hard and soft bounces from the provider.
- Hard bounces are added to the suppression list immediately. See [03_SUPPRESSION_PROCESS.md](03_SUPPRESSION_PROCESS.md).
- Track bounce rate alongside spam rate; a rising bounce rate signals list-quality problems.

## Go-live checklist — قائمة الإطلاق

- [ ] MX resolves correctly.
- [ ] SPF passes, single record, sane lookups.
- [ ] DKIM signs and verifies.
- [ ] DMARC published with reporting; policy at least `quarantine`.
- [ ] Google Postmaster verified and monitored.
- [ ] Bounce capture wired to suppression.
- [ ] Spam rate baseline confirmed under 0.3%.

A failed item blocks the ramp in [02_MANUAL_OUTREACH_RAMP.md](02_MANUAL_OUTREACH_RAMP.md).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
