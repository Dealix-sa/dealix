# Delivery QA OS

How Dealix ensures every signed engagement ships the artifact
promised in the proposal — on time, branded, audit-ready.

## 1. Delivery contract

Every signed proposal triggers a delivery row with:

```
delivery_id,proposal_id,account_id,scope_lines[],owner,
kickoff_at,first_artifact_due_at,checkpoints[],
artifact_urls[],customer_acknowledged,status
```

## 2. Day-1 pack

Every engagement opens with the same Day-1 pack:

- Bilingual welcome note.
- Roles + responsibilities.
- Communication cadence.
- Privacy + data handling statement (PDPL-aware).
- Approval flow for any external action Dealix produces.

## 3. QA gates

- Every artifact passes the brand_guardian voice check.
- Every artifact has a `source` annotation.
- Every artifact is reviewed before customer release.
- Customer acknowledgement is recorded per artifact.

## 4. Customer health

A daily health roll-up signals:

- On-time rate vs SLA.
- Open issues count.
- Last interaction recency.
- Sentiment from the reply router.

A drop in health surfaces immediately on the founder console.

## 5. Banned patterns

- ❌ Marking a delivery "complete" without an artifact + acknowledgement.
- ❌ Reusing other customers' confidential data in this delivery.
- ❌ Auto-publishing the delivery as proof without consent.
