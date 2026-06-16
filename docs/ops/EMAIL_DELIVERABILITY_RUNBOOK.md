# Email Deliverability Runbook

## DNS Records (dealix.me)
- **SPF**: `v=spf1 include:_spf.google.com include:sendgrid.net ~all`
- **DKIM**: configured per provider.
- **DMARC**: `v=DMARC1; p=quarantine; rua=mailto:dmarc@dealix.me`

## Sending Limits
- 25 emails/day.
- 10 emails/batch.
- 90 seconds between sends.

## Content Rules
- Clear subject.
- Unsubscribe link in every email.
- No misleading claims.
- No attachments > 5MB.

## Monitoring
- Bounce rate < 5%.
- Spam complaint rate < 0.1%.
- Open rate tracked weekly.

## Troubleshooting
- High bounces → check list quality and verification.
- Low delivery → check DNS records.
- Spam folder → review content, reduce links, warm up IP.
