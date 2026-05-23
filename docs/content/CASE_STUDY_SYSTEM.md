# Case Study System

> Case studies are the highest-trust artifact we publish.
> Client consent at every step. No exceptions.

## Cadence
- Target: 1 publishable case study per quarter (after first paid sprint)
- Drafted from sprints + Managed Ops engagements where client consented

## Source
- `CASE_STUDY_CAPTURE.md` filled at handoff
- `clients/{client}/feedback.md` for ongoing evidence
- `clients/{client}/deliverables/` for sanitized artifacts

## Production Workflow

1. **Draft** — founder writes in `content/drafts/case-study-{pseudonym}.md` (private)
2. **claim_guard pass** — every claim cited or qualified
3. **Internal review** — founder + advisor for first case study in a sector
4. **Client review** — send draft to client; give 5 business days
5. **Address comments** — change anything they want changed
6. **Final claim_guard pass + final client approval**
7. **Publish** — `content/case_studies/` (public-safe path)
8. **Distribute** — LinkedIn post + landing page + proposal kit

## Case Study Format

```markdown
# {Sector} · {Engagement type} · {time period}

## The situation
{client's challenge, in their language, sanitized}

## What we did
{Dealix's specific actions, with deliverables linked}

## What changed
{Measurable outcomes IF measured; client-reported clearly labeled}

## What we refused
{Scope creep, automation we declined, decisions made — this builds trust}

## What we learned
{Honest takeaway, including what didn't work}

## Client quote (with consent)
{Verbatim, attributed per consent level}

## Trust posture
{Reference to approval matrix + evidence pack + client review}

## Engagement details
{Rung, duration, price — productized pricing is itself a trust signal}
```

## Consent Levels (per `TESTIMONIAL_CAPTURE.md`)

Defaults if unclear: anonymous + sector-only.

## What Goes In Public Case Studies

- Sector + region
- Engagement type (Sprint / Managed Ops / Revenue Desk)
- Timeline
- Approved client quotes
- Sanitized deliverable examples
- Methodology + trust posture
- Approved numbers (with source)

## What Doesn't Go In

- Client name (without explicit consent for that)
- Verbatim deliverable content (sanitize)
- Unverified numbers
- Competitive comparison
- Anything not pre-approved by client
- Anything the client hasn't seen in this exact form

## Anti-Patterns

- "Composite" case studies framed as single client
- Cherry-picked numbers
- Implied results ("clients like this typically see X")
- Case studies of customers who later churned (without their revised consent)
- Case studies published before client signoff in writing

## Maintenance

- Annually: re-confirm consent with featured clients
- If client churns: ask if they want case study removed (default: ask first, default to remove if no answer)
- If incident: pause use until resolved
- If sector strategy changes: archive (don't delete) outdated case studies

## Storage

- Drafts: `content/drafts/` (private)
- Originals (with all approval evidence): `clients/{client}/case-study-{version}.md` (private)
- Published: `content/case_studies/` (public-safe)
- Approval evidence: `content/case_study_approvals/{pseudonym}-{date}.md` (private)

## Distribution Rights

Even after publication, we use case studies only as approved:
- Landing page: yes (per consent)
- Proposals: yes (per consent)
- Sales decks: yes (per consent)
- Conference talks: separate consent
- Paid ads (if ever): separate consent
- Modifications / new edits: separate consent
