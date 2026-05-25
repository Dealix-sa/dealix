# Partner Onboarding Flow — تهيئة الشريك

## Purpose
A repeatable onboarding for new partners (agency, sector specialist, referrer). Sets scope, IP, compliance, and the scorecard up front. Replaces ad-hoc onboarding with a verifiable sequence.

## Owner
Founder. Ops manager assists.

## Inputs
- Signed partner agreement (master + per-engagement).
- Referral terms acknowledgment (`docs/partners/REFERRAL_TERMS.md`).
- Banned-practices acknowledgment.
- Tax / commercial documents.
- Communication preferences.

## Outputs
- Onboarding record under `evidence/partners/<partner_id>/onboarding.md`.
- First deal or first deliverable identified.
- Scorecard initialized.

## Day 0 (Signing)
- [ ] Master partner agreement signed.
- [ ] NDA signed.
- [ ] Referral terms acknowledged (if applicable).
- [ ] Banned-practices acknowledgment signed (no scraping, no cold blast, no automation Dealix doesn't offer, PDPL compliance).
- [ ] Tax / invoicing details collected.
- [ ] Partner type classified (`docs/partners/PARTNER_STRATEGY.md`).

## Day 1 (Kickoff)
- [ ] 60-min kickoff call (bilingual).
- [ ] Profile alignment confirmed (`docs/partners/PARTNER_PROFILE.md`).
- [ ] Scope walk-through.
- [ ] Pipeline expectations set without guarantees.
- [ ] Tool access provisioned (least-privilege; partners do not access client data unless engagement-specific NDA signed).
- [ ] Scorecard introduced (`docs/partners/PARTNER_SCORECARD.md`).

## Day 7
- [ ] First check-in (30 min).
- [ ] First introduction or first joint engagement identified.
- [ ] Communication cadence locked.

## Day 30 (Trial Review)
- [ ] First introduction quality reviewed (referral partners).
- [ ] First joint engagement progress (agency / specialist).
- [ ] Scorecard partial reading.
- [ ] Decision: continue / extend trial / amicable close.

## Day 90 (Trial-to-Permanent)
- [ ] Scorecard at 90 days.
- [ ] Partner Yes/No for ongoing relationship.

## Rules
1. No partner activity before Day 0 completion.
2. Banned-practices acknowledgment is non-negotiable; refusal terminates onboarding.
3. Least-privilege access; access reviewed every 30 days.
4. Partner does not speak for Dealix externally without written approval.
5. Partner does not access client data unless an engagement-specific NDA is signed.
6. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to projected joint economics.

## Metrics
- Onboarding on-time rate (target 100%).
- Day-30 trial pass rate.
- Day-90 permanent conversion rate.
- Access-review on-time rate.

## Cadence
- Per-partner, once.

## Evidence
- Signed agreements, ack forms, access logs.

## Verifier
Founder.

## Runtime Command
`make partner-onboard ID=<partner>` — checklist; refuses access provisioning without all Day 0 signatures.

## Arabic Summary — ملخص عربي
تهيئة شريك بسبع مراحل: توقيع، إقلاع، فحص أول، مراجعة تجريبية في 30 يوم، قرار دائم في 90 يوم. إقرار الممارسات المحظورة شرط. القيم التقديرية ليست مُتحقَّقة.
