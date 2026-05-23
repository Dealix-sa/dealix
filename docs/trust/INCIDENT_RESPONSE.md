# Incident Response

> Something will break. The question is how we respond.
> A good response can preserve trust. A bad response will end the company.

## What counts as an incident

- A customer-facing overclaim or factual error
- An agent acting outside its autonomy tier
- Customer data exposure in a public surface
- A credential leak (committed secret, exposed key)
- A delivery failure (missed scope, late > 50% of budget)
- A trust-damaging public claim (by us or made about us we did not correct)

## Severity Tiers

| Tier | Definition | Response time |
|------|------------|---------------|
| S0 | Material customer harm or legal exposure | Immediate; founder all-hands |
| S1 | Customer-facing factual error, no harm yet | Within 24 hours |
| S2 | Internal incident, no customer impact | Within 7 days |
| S3 | Near-miss caught before customer impact | Logged, debriefed weekly |

## Response Steps

1. **Stop.** Halt the workflow or system that caused the incident.
2. **Contain.** Remove the artifact from public surfaces if applicable.
3. **Communicate.** If customer-facing, the founder communicates within
   the SLA, in plain language, with no euphemism.
4. **Diagnose.** Root cause analysis within 72 hours (S0/S1) or 7 days
   (S2/S3).
5. **Repair.** Fix the broken artifact or process.
6. **Prevent.** Update the policy, template, or system to prevent
   recurrence.
7. **Log.** In `dealix-ops-private/trust/incident_log.md`.

## Customer Communication Templates

For S0/S1 incidents involving a customer, the founder personally writes:

```
Subject: A correction about [artifact / claim]

[Customer name],

I am writing to correct [specific item] in [artifact / channel] on
[date]. The correct information is [correct version].

I take responsibility for the error. We have updated [artifact], and we
have updated our internal process to prevent recurrence [one sentence
on the prevention step].

If this changes how you would like to proceed, please tell me. If you
would like to talk live, my number is [number].

— Sami
```

No marketing language. No legalese. Plain, direct, accountable.

## Incident Log Format

```
- id: I-yyyy-mm-dd-NN
  severity: S0 / S1 / S2 / S3
  detected_on: yyyy-mm-dd
  detected_by: founder / audit / customer
  description: "..."
  customer_impact: "..."
  root_cause: "..."
  containment: "..."
  prevention: "..."
  policy_or_template_updated: "..."
  closed_on: yyyy-mm-dd
```

## Quarterly Incident Drill

Once per quarter, the founder runs a tabletop drill:

- Pick one plausible scenario (e.g. credential leak, public overclaim,
  customer data exposure).
- Walk through the response steps.
- Time-box: 30 minutes.
- Record gaps. Update policies.

## Anti-Patterns

- Quiet correction without telling the customer.
- "Legal will draft a response."
- Blaming the agent / the tool. The founder is accountable for what
  the agent did.
- Skipping the prevention step ("it was a one-off").
