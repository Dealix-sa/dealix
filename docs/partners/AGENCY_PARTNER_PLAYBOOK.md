# Dealix — Agency Partner Playbook

**Full implementation:** `docs/sales-kit/dealix_agency_partnerships.md`

## Quick Reference

### 3 Partner Models
1. **Referral Partner** (10% commission, 12 months)
2. **Service Provider** (20% commission, lifetime)
3. **Agency Partner** (25-40% commission, possible white-label)

### Stage-1 Targets
- Peak Content
- Digital8
- Brand Lounge
- Qatar Digital
- 5 freelance consultants on LinkedIn

### Onboarding (4 weeks)
- Week 1: Training + access
- Week 2: First test implementation
- Week 3: First real client
- Week 4: Performance review

### Success metrics
- Active partners: target 3 by month 2
- Leads from partners: target 10% by month 3
- Revenue from partners: target 30% by month 6

See full playbook for detailed flow.

---

## Market Attack Layer — Agency Playbook (v12)

> This section is added by the Dealix Market Attack & Scaling System.
> It defines the *attack* discipline on top of the existing program.

### Who fits

- Saudi marketing / digital agencies serving B2B mid-market or enterprise.
- Existing book of business in the locked beachhead sector.
- Comfortable with PDPL and signed contracts.

### What we offer them

- Co-branded sector report.
- Referral fee per closed Managed Pilot (per approved partner terms;
  see `PARTNER_REFERRAL_TERMS_GUARDRAILS.md`).
- Optional white-label of selected services after a 6-month pilot
  (governance review required).

### What they offer us

- Warm intros into their book.
- Co-presenting at events.
- Joint sector content.

### What we never do

- Hand them raw lead data.
- Promise exclusivity outside a written, governance-reviewed contract.
- Pay for "listings" without measurable referral attribution.

### How to add a new agency partner

1. Add row to `<PRIVATE_OPS>/partners/partner_pipeline.csv` with `type=agency`.
2. Run `make partner-pipeline`.
3. Founder approves status transition `prospect → intro_meeting`.
4. After intro, decide: `pilot_partner` or `paused`.

