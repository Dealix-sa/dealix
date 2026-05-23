# Referral Terms — شروط الإحالة المعيارية

## Purpose
Standard, public referral terms that apply to all referral partners by default. Negotiating outside these terms requires founder sign-off. Transparent, fair, simple.

## Owner
Founder. Terms reviewed annually.

## Inputs
- Margin profile from `docs/finance/`.
- Sales cycle data.
- Market norms in Saudi B2B services.

## Outputs
- This document.
- Standard referral clause embedded in `templates/PROPOSAL_*.md.j2` partner addendum.

## Standard Terms
### Qualification
A referral is qualified when:
1. The referred party has an active business need within Dealix's stated sectors.
2. The party has decision-maker authority or direct access.
3. A first meeting or written reply is achieved within 30 days of introduction.
4. The party was not already in Dealix's pipeline within 90 days prior (no overlap).

### Compensation
| Stage | Compensation |
|---|---|
| Qualified introduction (meeting held) | None — counted toward Partner Scorecard activity |
| Signed SOW (first deal) | 10% of first 90 days of revenue, paid 30 days after Dealix receives payment |
| Signed second engagement within 12 months | 5% of that engagement, same terms |
| Beyond 12 months | None — relationship is direct |

### Payment
- Paid by bank transfer within 30 days of Dealix collecting from the client.
- Partner issues invoice referencing client code (no client name in PO).
- No payment without active partner agreement and tax compliance.

## Rules
1. No referral payment without a signed referral agreement (master) and a per-deal acknowledgment.
2. No referral payment on deals where partner outreach used banned practices.
3. No double-counting; one partner per deal (the first to introduce).
4. Disputes resolved by founder; founder's decision final, written.
5. PII handling: the referred party's contact info is shared only after written consent from the partner that the introduction is authorized.
6. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to projected partner earnings.

## Non-Standard Terms
- Any deviation (higher %, exclusivity, equity, longer tail) requires written founder approval and a recorded rationale.
- Equity and exclusivity are not granted; this is a hard line.

## Metrics
- Referral payments paid on time (target 100%).
- Disputes (target 0).
- Average partner earning per qualified intro.
- % of deals sourced through standard vs non-standard terms (standard preferred).

## Cadence
- Annual review.
- Per-deal application.

## Evidence
- Signed master agreement.
- Per-deal acknowledgment.
- Payment records.

## Verifier
Founder.

## Runtime Command
`make referral-record DEAL=<id>` — applies the standard terms, prints expected partner payment.

## Arabic Summary — ملخص عربي
شروط إحالة معيارية: 10% من إيراد أول 90 يومًا للصفقة الأولى، 5% للصفقة الثانية خلال 12 شهرًا، صفر بعد ذلك. لا حصرية، لا أسهم. أي تعديل يتطلب توقيع المؤسس. القيم التقديرية ليست مُتحقَّقة.
