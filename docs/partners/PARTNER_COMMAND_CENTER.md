# Partner Command Center — مركز قيادة الشركاء

## Purpose
Single dashboard for partner relationships — agencies, sector specialists, referral partners. Tracks active partners, pipeline contribution, and health. Prevents partner sprawl and ensures every partner has a verified deal economic.

## Owner
Founder. Updated weekly.

## Inputs
- Signed partner agreements.
- Referral log (deals attributed).
- Joint client engagements.
- Partner scorecards from `docs/partners/PARTNER_SCORECARD.md`.

## Outputs
- Live table: partner, type, status, deals referred (last 90d), revenue contribution, health.
- Weekly attention list.
- Quarterly partner portfolio review.

## Dashboard Panels
1. **Active partners** — count, type (agency / specialist / referrer).
2. **Pipeline contribution** — deals introduced last 90 days.
3. **Closed deals** — count and revenue.
4. **Partner health** — score from `docs/partners/PARTNER_SCORECARD.md`.
5. **Dormant partners** — > 90 days no activity.
6. **Onboarding queue** — partners in onboarding stage.
7. **Disputes / friction** — open items.

## Rules
1. No partner is onboarded before proof gate Delivery is passed (see `docs/partners/PARTNER_STRATEGY.md`).
2. No partner promised exclusivity, equity, or guaranteed revenue.
3. Referral terms follow `docs/partners/REFERRAL_TERMS.md` strictly.
4. No outbound on Dealix's behalf without written approval per engagement.
5. Dormant > 180 days → amicable parted unless explicit revival reason.
6. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to projected partner economics.

## Metrics
- Active partner count (target: small and effective, not many and shallow).
- Pipeline contribution share (target: 20-40% of new deals long-term).
- Partner-sourced close rate vs direct close rate.
- Dispute count (target 0).

## Cadence
- Weekly review.
- Monthly partner 1:1 (for active partners).
- Quarterly portfolio review.

## Evidence
- `evidence/partners/<YYYY-Www>.md` snapshot.

## Verifier
Founder.

## Runtime Command
`make partner-status` — prints the table, flags dormant and at-risk partnerships.

## Arabic Summary — ملخص عربي
لوحة قيادة الشركاء: نشطون، مساهمة في الأنبوب، صحة الشراكة. لا حصرية، لا ضمانات. شركاء قلائل فعَّالون أفضل من كُثر سطحيين. القيم التقديرية ليست مُتحقَّقة.
