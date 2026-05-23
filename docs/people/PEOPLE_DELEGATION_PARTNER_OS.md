# People, Delegation, Partner OS

## Purpose
Move work off the founder safely, and grow capacity through partners without losing trust.

## Sub-systems
- Founder bottleneck — `docs/people/FOUNDER_BOTTLENECK_SYSTEM.md`
- Delegation ladder — `docs/people/DELEGATION_LADDER.md`
- Role architecture — `docs/people/ROLE_ARCHITECTURE.md`
- Hiring triggers — `docs/people/HIRING_TRIGGER_SYSTEM.md`
- Contractor onboarding — `docs/people/CONTRACTOR_ONBOARDING_SYSTEM.md`
- Access control — `docs/people/ACCESS_CONTROL_SYSTEM.md`
- Partner OS — `docs/partners/PARTNER_OPERATING_SYSTEM.md`
- Referral terms — `docs/partners/REFERRAL_TERMS_SYSTEM.md`
- White-label guardrails — `docs/partners/WHITE_LABEL_GUARDRAILS.md`

## Operating principles
1. **Founder first, founder less**: do the work once, then move it down the ladder.
2. **Document before delegate**: never hand off undocumented work.
3. **Scope before access**: contractors get only the scope they need.
4. **Partners are commercial relationships, not friendships**: written terms.

## Cadence
- Weekly: review `founder/founder_bottleneck_log.csv`; move one task down the ladder.
- Monthly: access review; partner pipeline review.
- Quarterly: hiring trigger review.

## Trust integration
- Every contractor access change logged in `people/access_log.csv`.
- Every partner agreement logged in `partners/partner_tracker.csv`.

## Verifier
`python scripts/verify_people_partner_os.py`
