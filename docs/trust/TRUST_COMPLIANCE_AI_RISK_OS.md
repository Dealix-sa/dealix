# Trust, Compliance, AI Risk OS

## Purpose
Operate Dealix in a way that customers, regulators, and our future selves can trust.

## Pillars
1. **Approval matrix** — `docs/trust/APPROVAL_MATRIX_V2.md`
2. **Claim governance** — `docs/trust/CLAIM_GOVERNANCE_SYSTEM.md`
3. **Data minimization & retention** — `docs/data/DATA_MINIMIZATION_RETENTION.md`
4. **Redaction system** — `docs/data/REDACTION_SYSTEM.md`
5. **AI risk register** — `docs/ai_management/AI_RISK_REGISTER.md`
6. **Prompt injection defense** — `docs/ai_management/PROMPT_INJECTION_DEFENSE.md`

## Operating cadence
- Daily: log any approval decision.
- Weekly: review the AI risk register.
- Monthly: retention review + access review.
- Quarterly: external claim audit.

## Approval flow (in short)
1. Someone proposes an action that needs approval.
2. The proposer writes a row in `trust/approval_log.csv` with `decision=Pending`.
3. The approver (founder for now) reviews, sets `decision=Approved` or `decision=Rejected`, and adds the evidence path.
4. The action proceeds only after the decision is recorded.

## What requires approval
- Any external claim about a customer.
- Any spend > 1,000 SAR not in the standard expense category.
- Any data movement from private → public.
- Any contractor onboarding with production access.
- Any AI-generated content sent externally without founder review.

## What is forbidden outright
- Public claims without proof level documentation.
- Sending customer data to a service that does not commit to confidentiality.
- Using copyrighted material as if it were original.

## Verifier
`python scripts/verify_trust_ai_risk_os.py`
