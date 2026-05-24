# Learning Loop | حلقة التعلم

## Purpose | الغرض
Convert every experiment result, founder edit, reply transcript, win, and loss
into a structured learning entry — then propagate those learnings into the
playbooks, prompts, and machines that produced them.

This is how Dealix gets smarter over time without losing trust controls.

## Inputs | المدخلات
- Experiment Backlog closed-experiment memos
- Founder edits on AI-drafted content (edit distance per draft)
- Reply Router transcripts (anonymized)
- Won-deal retros + lost-deal retros
- Delivery defect logs from Delivery QA OS
- Client survey feedback

## Outputs | المخرجات
- `performance.learning_loop`: id, source_type, summary, evidence_pointers,
  affected_playbooks, affected_workers, propagation_state
- Patch proposals for playbooks, prompts, and worker logic
- Quarterly learning digest

## Learning categories | فئات التعلم
1. **Won-pattern** — what reliably moves a buyer from reply to paid
2. **Lost-pattern** — what reliably causes a buyer to drop
3. **Channel-pattern** — what works on which channel
4. **Persona-pattern** — what resonates per persona
5. **Sector-pattern** — what unique signal a sector responds to
6. **Failure mode** — recurring system mistake that should be guard-railed
7. **Founder preference drift** — what the founder consistently edits

## Propagation pipeline | خط النشر
1. Learning entry created with evidence
2. Worker identifies affected playbooks and workers
3. Patch proposal drafted (prompt change, threshold tweak, gate addition)
4. Founder reviews and approves patch (A2)
5. Patch deployed to affected machines
6. Post-patch telemetry monitored for 30 days to confirm improvement

## Anti-patterns | ما يجب تجنبه
- Learning entry without evidence pointer → rejected
- Patch that violates a non-negotiable → blocked
- Single-event learnings (need ≥ 3 supporting cases)

## Data source | مصدر البيانات
`performance.learning_loop`, `performance.experiments`,
anonymized `reply.transcripts`, `delivery.qa_reviews`, `crm.deals.closed`.

## Approval class | فئة الموافقة
- A1: learning entry creation, pattern detection, internal propagation drafts
- A2: every playbook/prompt/worker patch before deployment
- A3: patches affecting regulated workflows or external commitments

## Trust gate | بوابة الثقة
- All transcripts anonymized before storage
- All patches lint-checked against non-negotiables
- All deployed patches reversible
- Policy snapshot + audit row per learning entry and per patch

## Owner | المالك
Founder approves every patch propagated into the live system.

## Worker name
`performance.learning_loop`

## KPI | المؤشرات
- # learnings captured per week
- # patches deployed per quarter
- Post-patch KPI lift (rolling 30d after patch)
- Founder edit-distance trend on AI drafts (should fall)
- Lost-pattern recurrence rate (should fall as fixes deploy)

## Failure mode | حالات الفشل
- Patches deploy but no post-patch monitoring confirms lift
- Learnings captured but never propagated to all affected playbooks
- Anonymization slip in a transcript

## Recovery path | مسار الاسترداد
- Post-patch monitoring is mandatory; un-monitored patches auto-rolled-back
- Cross-playbook propagation checklist per patch
- Anonymization auditor scans new transcript entries on ingestion
