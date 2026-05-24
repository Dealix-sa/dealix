# Buyer Persona System | نظام شخصيات المشتري

## Purpose | الغرض
Build the buyer-side mental model: who they are, what they care about, what they
fear, what they have already tried, what proof actually moves them. Every draft
that leaves the queue is keyed to a persona.

Personas are research artifacts, not selling tools. They never appear in external
copy verbatim.

## Inputs | المدخلات
- LinkedIn public profile signals
- Public talks, podcasts, articles by the buyer
- Company website "about" / "leadership" pages
- Founder interviews and notes
- Reply transcripts from Reply Router Machine (anonymized)
- Sector + ICP context

## Outputs | المخرجات
- `personas.profiles`: persona_id, role, sector, top_3_jobs, top_3_pains,
  top_3_objections, preferred_channel, preferred_proof_type, language_pref
- Persona-tagged draft templates (subject, opener, proof line, CTA)
- Persona evolution log (what changed and why)

## Canonical Saudi B2B personas | الشخصيات الأساسية
1. **Founder-CEO of a 10-50 person services firm** — owns revenue, time-starved
2. **Head of Sales / CRO at mid-market** — quota under pressure, pipeline anxious
3. **Marketing Lead at B2B agency** — proof + brand sensitive
4. **COO / Ops Lead at ERP/Cyber implementer** — process and delivery focused
5. **Founder of B2B SaaS pre-seed → series A** — runway and PMF anxious
6. **Partner / Channel Lead** — looking for revenue multipliers
7. **Procurement / Vendor Manager (enterprise)** — risk and trust focused

## Persona fields | حقول الشخصية
- Demographics: title patterns, seniority, tenure
- Day-in-the-life: top 3 jobs-to-be-done
- Pains: top 3 ranked by frequency in evidence
- Triggers: what gets them to reply
- Objections: top 3 with rebuttal pattern (internal only)
- Proof appetite: which artifact type they respond to (sample, case, demo, peer)
- Trust gates: what they must see before saying yes (security, contract, PDPL)
- Channel preference: LinkedIn DM, email, form, WhatsApp, in-person

## Data source | مصدر البيانات
`intelligence.personas`, anonymized `reply.transcripts`, public web evidence.

## Approval class | فئة الموافقة
- A1: persona refresh and field updates from evidence
- A2: activating a new persona for drafting
- A3: persona that targets regulated decision makers or government

## Trust gate | بوابة الثقة
- No real names stored in persona records (use role + sector only)
- Reply transcripts anonymized before feeding persona learning
- No claim about what a persona "will do" — only what evidence suggests
- Policy snapshot + audit row on persona activation

## Owner | المالك
Founder approves activation and quarterly persona reviews.

## Worker name
`intelligence.persona_synthesizer`

## KPI | المؤشرات
- # active validated personas
- Persona-tagged reply rate vs untagged baseline
- Persona evolution velocity (healthy update rate without churn)
- Founder edit rate on persona-driven drafts (should fall over time)

## Failure mode | حالات الفشل
- Persona drift: silently grows in scope until it represents no one
- Evidence rot: persona based on 12-month-old data still active
- Overlapping personas: two personas with > 70% field overlap

## Recovery path | مسار الاسترداد
- Quarterly persona audit, merge or retire overlaps
- Auto-flag personas with > 90 day-old evidence base
- Founder review queue for persona refresh proposals
