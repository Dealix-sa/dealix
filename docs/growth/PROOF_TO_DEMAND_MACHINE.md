# Proof-to-Demand Machine | آلة تحويل الإثبات إلى طلب

## Purpose | الغرض
When a new proof artifact (case study, sample, peer outcome) is published, instantly
generate drafts to *every* account in the matching segment so the proof is used at
its hottest moment. All sends are drafts. Approval required.

## Inputs | المدخلات
- New proof artifact event (`proof.artifacts.published`)
- Segment match: which ICP / sector / persona this artifact lands hardest with
- Account list filtered to: not currently in active reply state, not in
  cooldown, not trust-risk flagged
- 24-hour fast-lane priority window

## Outputs | المخرجات
- Burst of drafts queued in Outbound, LinkedIn, ABM, Nurture machines
- `proof_demand.events`: event_id, artifact_id, target_accounts_count,
  drafts_generated, drafts_approved, drafts_sent, replies_received

## Fast-lane rules | قواعد المسار السريع
- 24-hour priority over normal outbound queues
- ABM accounts get personalized treatment first
- B-bucket gets standard outbound treatment
- C-bucket gets nurture treatment
- Hard no's and trust-risk accounts excluded

## Draft pattern | نمط المسودة
1. Reference the new proof artifact ("we just published…")
2. Pin to a buyer pain the artifact addresses
3. Soft CTA: 15-min walkthrough or share the artifact
4. No revenue guarantee, no price, no contract terms

## Capacity guardrails | قيود الطاقة
- Max 200 drafts generated per proof event
- Founder approval queue capped; overflow goes to standard queue next day
- Channel diversification: not all 200 on one channel

## Data source | مصدر البيانات
`proof.artifacts`, `intelligence.icp_segments`, downstream draft machines.

## Approval class | فئة الموافقة
- A1: artifact-event ingestion, draft generation, queueing
- A2: per-draft approval before send; proof publication itself is A2
- A3: any artifact referencing a regulated/government client

## Trust gate | بوابة الثقة
- Proof artifact must itself have been approved (proof_approval_os)
- Per-draft policy snapshot + audit row
- Anonymization rules preserved (client names only with written consent)
- No guaranteed-outcome language in drafts

## Owner | المالك
Founder approves the proof publication AND each downstream draft.

## Worker name
`growth.proof_to_demand`

## KPI | المؤشرات
- Drafts generated per proof event
- Approval rate during 24-hr fast-lane
- Reply rate vs baseline outbound reply rate
- Proposal-drafted rate per proof event

## Failure mode | حالات الفشل
- Proof published before approval triggers downstream flood
- Same buyer hit on 3 channels in 24 hours (collision)
- Drafts reference an artifact that was edited post-publication

## Recovery path | مسار الاسترداد
- Hard gate: artifact must have A2 approval state to trigger this machine
- Channel collision detector enforced even in fast-lane
- Artifact version pinned at draft time; edits trigger redraft, not silent change
