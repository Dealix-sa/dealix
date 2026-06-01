# Dealix — Client Onboarding
# استقبال العميل

**Version:** 1.0 | Gate: scope document must be signed before any build starts.

---

## Onboarding Checklist

### Step 1: Kickoff Call (Day 1)
- [ ] Introduce the team (founder + any delivery support)
- [ ] Confirm scope and deliverables from the proposal
- [ ] Agree on communication channel (email preferred; not WhatsApp for project comms)
- [ ] Confirm primary contact on client side (name, title, availability)
- [ ] Set next 3 milestone dates
- [ ] Agree on data access approach: sample data first, production later

### Step 2: Scope Document Sign-Off (Day 1-3)
- [ ] Send scope document (use SCOPE_TEMPLATE)
- [ ] Client reviews and confirms in writing
- [ ] Any scope changes → Change Request before proceeding
- [ ] Gate: no build starts without signed scope

### Step 3: Data Collection (Day 3-7)
- [ ] Collect sample data (anonymized where possible)
- [ ] Confirm data format and source systems
- [ ] Document any API or system access requirements
- [ ] Gate: no production API access until sandbox is validated
- [ ] Gate: must get founder approval before requesting client credentials

### Step 4: Acceptance Criteria (Day 3-7)
- [ ] Define measurable acceptance criteria (not "it works" but specific outcomes)
- [ ] Client confirms acceptance criteria in writing
- [ ] Gate: no QA pass without acceptance criteria met

### Step 5: Environment Setup (Day 5-10)
- [ ] Sandbox environment confirmed
- [ ] No production system access yet
- [ ] Document which systems will be connected in Phase 2

---

## Onboarding Anti-Patterns

- Never start building before scope is signed
- Never request production credentials before sandbox is proven
- Never accept vague acceptance criteria ("we'll know it when we see it")
- Never let scope grow without a Change Request
- Never commit to timelines before scope is confirmed

---

## Handover from Sales to Delivery

Sales hands over:
1. Signed proposal
2. Qualification scorecard
3. Discovery call notes
4. Company context (signals, buyer, pain)

Delivery confirms:
1. Scope aligns with what was sold
2. Timeline is realistic
3. Resources are available

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
