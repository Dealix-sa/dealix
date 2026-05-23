# Partner Referral Machine

**Owner:** Operations + Founder
**Source of truth:** This doc + `docs/growth/PARTNER_STRATEGY.md` + `docs/growth/PARTNER_NETWORK.md`

## Purpose

The Partner Referral Machine handles inbound referrals from Dealix's partner network — Saudi B2B integrators, consultancies, event hosts, sector specialists, agencies — and runs the partner-side outbound rhythm that produces referrals in the first place.

It is the highest-trust intake path. Partner referrals carry weight no cold outreach can match.

## Inputs

- **Partner referral submissions** — partner-initiated introductions to a Saudi B2B account.
- **Partner network roster** — active partners, partner economics, partner sector coverage.
- **Partner check-in schedule** — quarterly partner reviews.
- **Active sprint catalog** — to map referrals to fit offers.

## Outputs

- **Referral intake record** — partner, referred account, persona, context, partner economics tag.
- **Tailored response draft** to the referred persona, copying the partner where appropriate.
- **Partner thank-you note** acknowledging the referral.
- **Partner update** — outcome notification when the referral converts, declines, or stalls.
- **Partner pipeline report** — quarterly summary of referrals per partner with outcomes.

## Partner-side outbound rhythm

The machine also drives partner-facing activity:

- **Monthly partner update** — what Dealix shipped, what sectors are active, what referrals are most welcome.
- **Quarterly partner review call** — joint pipeline review, economics review, what's working.
- **Annual partner summit** — in-person or virtual; aligns category language and shared playbooks.

Partner-facing activity follows the same brand voice and trust gates as customer-facing activity.

## Source of truth

This doc + `docs/growth/PARTNER_NETWORK.md` + the partner ledger.

## Approval class

- **A1** — Partner intake; auto-acknowledge.
- **A2** — Personal response to referred persona (Founder + Operator).
- **A2** — Partner-facing communication.

## Trust gate

- Referred persona is contacted only with explicit partner consent to make the intro (verify in intake).
- Partner economics terms are documented before any cash-share scenario.
- No partner can be promised "guaranteed referrals back" — Dealix's referral flow to partners is goodwill-driven.
- Partner-facing communications follow `docs/brand/DEALIX_BRAND_VOICE.md`.
- PDPL-compliant data handling on referred personas.

## Owner

- **Code owner:** Operations Engineering.
- **Operational owner:** Founder (per response) + Partner Lead (per partner relationship).

## Worker script (placeholder)

`workers/partner_referral_worker.py` (planned). Webhook intake + partner-side scheduler.

## KPI

| Metric | Target |
|---|---|
| Referral-intake response latency | <= 1 business day |
| Referral-to-Diagnostic-call rate | >= 50 percent (referrals carry pre-built trust) |
| Referral-to-sprint conversion | observed; published in partner review |
| Partner satisfaction (quarterly survey) | >= 4 / 5 |
| Active partners with at least 1 referral per quarter | observed |

## Failure mode

- Referral intake stalls; partner loses confidence.
- Referred persona is contacted before partner has actually made the intro.
- Partner economics are renegotiated mid-engagement.
- Partner is asked to refer without Dealix referring back where appropriate.

## Recovery path

1. Re-anchor intake SLA at <= 1 business day.
2. Verify partner-intro consent before contact.
3. Treat partner economics as contractual once signed.
4. Maintain partner-to-partner reciprocity in good faith.

## What this machine does NOT do

- It does not poach a partner's customers.
- It does not white-label partner work as Dealix work without explicit agreement.
- It does not share partner-confidential data with other partners.

## Cross-links

- Partner strategy: `docs/growth/PARTNER_STRATEGY.md`
- Partner network: `docs/growth/PARTNER_NETWORK.md`
- Partner outreach plan: `docs/growth/PARTNER_OUTREACH_PLAN.md`
- Approval policy: `docs/05_governance_os/APPROVAL_POLICY.md`

## Disclaimer

Dealix does not guarantee referral volume or referral conversion. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
