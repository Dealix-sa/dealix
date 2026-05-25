# Contractor Onboarding — تهيئة المتعاقدين

## Purpose
A repeatable onboarding for every contractor (engineering, content, sector analyst, ops). Sets expectations, IP, compliance, communication, and the scorecard upfront. No contractor starts work without this completed.

## Owner
Founder. Ops manager runs post-hire.

## Inputs
- Signed contractor agreement (scope, IP assignment, NDA, PDPL clauses).
- Tax / commercial documents (CR for company contractors).
- Communication preferences.
- Tools list and access plan.

## Outputs
- Onboarding record under `evidence/contractors/<contractor_id>/onboarding.md`.
- Access provisioning record.
- First-deliverable defined.

## Day 0 (Signing)
- [ ] Contractor agreement signed.
- [ ] NDA signed.
- [ ] PDPL data-handling brief shared.
- [ ] Banned-practices acknowledgment signed (`docs/product/NO_OVERBUILD_POLICY.md`, no scraping, no automation Dealix doesn't offer).
- [ ] Code of conduct shared.
- [ ] Tax / invoicing details collected.

## Day 1 (Kickoff)
- [ ] 60-min kickoff call (bilingual).
- [ ] Scope walk-through with explicit kill criterion.
- [ ] Tool access provisioned (least-privilege).
- [ ] Communication channel agreed (no shadow channels).
- [ ] First deliverable defined with deadline.
- [ ] Scorecard introduced.

## Day 3
- [ ] First check-in (15 min).
- [ ] Blockers surfaced.
- [ ] Access fully verified.

## Day 7
- [ ] First deliverable reviewed.
- [ ] Scorecard partial fill (first reading).
- [ ] Adjust pace or scope if needed.

## Day 14 / 30 (Trial Review)
- [ ] Trial-period decision: continue / extend / part ways.
- [ ] If continue: cadence locked in.
- [ ] If part ways: amicable close, access revoked same day.

## Rules
1. No work before all Day 0 items completed.
2. IP assignment is mandatory for build contractors; content contractors assign in scope of paid work only.
3. PDPL brief is non-negotiable; signed acknowledgment.
4. Access is least-privilege; review every 30 days.
5. No contractor speaks for Dealix externally without written approval.
6. Banned practices (scraping, cold WhatsApp automation, LinkedIn bots, bulk outreach) explicitly rejected in writing.
7. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to any projected contractor ROI.

## Metrics
- Onboarding on-time completion (target 100%).
- Trial-period conversion (signal of selection quality).
- Time to first deliverable.
- Access-review on-time rate.

## Cadence
- Per-contractor, once at start.
- 30-day access review.
- Quarterly contractor portfolio review.

## Evidence
- Signed agreements, NDA, PDPL ack, banned-practices ack.

## Verifier
Founder.

## Runtime Command
`make contractor-onboard ID=<id>` — checklist, refuses access provisioning without all Day 0 signatures.

## Arabic Summary — ملخص عربي
تهيئة قياسية للمتعاقدين: توقيع، إقرار حماية البيانات، إقرار رفض الممارسات المحظورة، نطاق وصول بأدنى صلاحية. لا عمل قبل اكتمال اليوم الصفر. القيم التقديرية ليست مُتحقَّقة.
