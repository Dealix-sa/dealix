# Distribution War Machine

The set of always-on machines that turn intelligence into **approved
drafts**, **scored queues**, and **founder-ready actions** — never
into uncontrolled external sends.

## 1. The machines

| Machine | Output | Approval class | Owner |
|---|---|---|---|
| Outbound draft | Personalised messages in the queue. | per-message | distribution_operator |
| LinkedIn queue | Connection / message drafts, scheduled. | per-message | distribution_operator |
| Email draft | Email drafts (subject + body). | per-message | distribution_operator |
| Contact form queue | Form-fill drafts for prospect sites. | per-form | distribution_operator |
| Follow-up | Cadence-based reminders + drafts. | per-cadence | distribution_operator |
| Reply router | Inbound reply triage + suggested response. | per-reply | sales operator |
| Nurture | Multi-step content sequence drafts. | per-sequence | content_strategist |
| Partner referral | Partner intro drafts + tracking. | per-referral | growth_strategist |
| ABM strategic account | Per-account playbook drafts. | per-account | growth_strategist |
| Content-to-demand | Content surfaced to scored accounts. | per-cycle | content_strategist |
| Proof-to-demand | Closed-deal proof routed to look-alikes. | per-batch | content_strategist |

## 2. Trust gate (mandatory)

Every machine in this list:

1. Reads inputs only from approved sources.
2. Writes only to its **own queue** or ledger.
3. Refuses to call any external send / publish / post API.
4. Annotates every output with: machine_id, run_id, source, fallback_share.
5. Records a row to the audit ledger when an artifact is created.

## 3. Approval classes

| Class | Description | Approver |
|---|---|---|
| per-message | One draft → one approval. | Founder or named operator. |
| per-cadence | A cadence is approved as a template. | Founder. |
| per-segment | A segment is opened for outbound for a window. | Founder. |
| per-campaign | A campaign is opened (purpose, window, segments). | Founder. |

## 4. Output ledgers

- `distribution/outbound_queue.csv`
- `distribution/linkedin_queue.csv`
- `distribution/email_queue.csv`
- `distribution/contact_form_queue.csv`
- `distribution/follow_up_queue.csv`
- `distribution/reply_router.csv`
- `distribution/nurture_queue.csv`
- `distribution/partner_referrals.csv`
- `distribution/abm_playbooks.csv`
- `distribution/content_to_demand.csv`
- `distribution/proof_to_demand.csv`

## 5. KPIs (lagging)

- Drafts produced per day.
- Approval throughput (decisions per day).
- Time from queued → approved.
- Approval-to-reply rate.
- Reply-to-meeting rate.

We measure **execution velocity** and **trust friction**, not send
volume.

## 6. Failure modes and recovery

| Failure | Symptom | Recovery |
|---|---|---|
| Provider outage | Drafts pile up | Reduce intake rate; surface to founder. |
| Voice violation | Brand guardian flags | Block draft; show diff; re-generate. |
| Off-segment routing | Wrong persona | Pause segment; re-link persona. |
| Spam-like cadence | Follow-up density > threshold | Auto-throttle. |
| Queue starvation | < N drafts / day | Trigger intelligence-layer refresh. |
