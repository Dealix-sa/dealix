# Contact Form Queue Machine

**Owner:** Operations + Founder
**Source of truth:** This doc + `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md`

## Purpose

The Contact Form Queue Machine handles inbound submissions to the Dealix website Contact Form. It triages each submission, auto-acknowledges with a non-promissory confirmation, classifies the submission against the active ICP, and queues a tailored response draft for Founder approval.

It is the front door for inbound demand. Misrouting here costs trust.

## Inputs

- **Contact Form submissions** — payload includes name, company, role, message body, source (UTM if available), submission time.
- **Active ICP definition** — `docs/intelligence/ICP_SEGMENTATION_SYSTEM.md`.
- **Active persona matcher** — `docs/intelligence/BUYER_PERSONA_SYSTEM.md`.
- **Active sprint catalog** — to recommend a first sprint in the response.

## Outputs

- **Auto-acknowledge email** sent within 60 seconds of submission. Non-promissory. Confirms receipt, names the next step.
- **Queued response draft** for Founder approval (A2). Draft proposes a Diagnostic call or a relevant first sprint based on submission content.
- **Account record** created in the operator's CRM or pipeline tool with ICP fit tag and sprint hypothesis.

## Auto-acknowledge template

```
Subject: Your message to Dealix — received

Body:
Hi <first name>,

Thanks for reaching out to Dealix. Your message reached the founder. I'll review and respond personally within one business day.

If your question is about a specific sprint or sector, you can also reply with one sentence about your current revenue setup — it shortens the back-and-forth.

— <Founder name>
Dealix
```

Bilingual variant in Arabic is sent in parallel where the submission language is Arabic.

## Source of truth

This doc + the Contact Form submission log + the approval queue.

## Approval class

- **A1** — Intake (auto-acknowledge). Approved at machine level by published template.
- **A2** — Personal response draft. Founder + Operator approve per draft.

## Trust gate

- The auto-acknowledge promises nothing beyond "we received your message."
- No marketing follow-up sequence triggers from a Contact Form submission without explicit opt-in.
- Personal response drafts pass the voice checklist before queueing.
- No customer data from Contact Form submissions is shared with third parties.
- PDPL-compliant retention: submissions are retained per the data retention policy in `docs/04_data_os/DATA_RETENTION_POLICY.md`.

## Owner

- **Code owner:** Operations Engineering.
- **Operational owner:** Founder (per response).

## Worker script (placeholder)

`workers/contact_form_queue_worker.py` (planned). Webhook from the website triggers intake; ICP classifier tags submission; response drafter populates queue.

## KPI

| Metric | Target |
|---|---|
| Auto-acknowledge latency | <= 60 seconds |
| Personal response latency | <= 1 business day |
| ICP classification accuracy (Founder agrees with tag) | >= 85 percent |
| Submission-to-Diagnostic-call rate | observed; published in distribution review |

## Failure mode

- Auto-acknowledge fails; submitter never hears back.
- ICP classifier mis-tags; out-of-ICP submission gets a sprint pitch it does not need.
- Personal response drifts into marketing copy.
- Submission data leaks to a third party.

## Recovery path

1. Repair the webhook.
2. Re-tag submission and re-draft response.
3. Re-run the voice checklist.
4. Notify Founder and customer if data was mishandled; correct retention state.

## What this machine does NOT do

- It does not enroll submitters in a marketing automation sequence without opt-in.
- It does not share submitter data with partners or third parties.
- It does not auto-send a sprint proposal without Founder approval.

## Cross-links

- Outbound Draft Machine: `docs/growth/OUTBOUND_DRAFT_MACHINE.md`
- ICP segmentation: `docs/intelligence/ICP_SEGMENTATION_SYSTEM.md`
- Data retention: `docs/04_data_os/DATA_RETENTION_POLICY.md`
- Approval policy: `docs/05_governance_os/APPROVAL_POLICY.md`

## Disclaimer

Dealix does not guarantee a sprint fit for every Contact Form submission. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
