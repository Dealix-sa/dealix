# Client Data Handling

> What we do (and don't do) with data clients give us.

## Core Rule

**Client data lives only in the private repo workspace for that client. Period.**

`clients/{client_name}/` in `dealix-ops-private`. Nowhere else by default.

## What Counts As Client Data

- Anything they give us that isn't already public
- CRM exports, lead lists, customer lists
- Sales scripts, internal playbooks they share
- Org charts, team composition info
- Pricing, revenue, financial figures
- Conversations (verbatim or paraphrased) we capture from calls
- Screenshots from their tools

If it came from them, it's their data.

## Where It Can Live

| Allowed | Not allowed |
|---|---|
| `dealix-ops-private/clients/{client}/` | Public repo |
| Founder local machine (encrypted disk) | USB drives / unencrypted laptops |
| Stripe / banking (financial only) | Personal email forwarding |
| Encrypted backup (private repo) | Slack / WhatsApp screenshots |
| Custom AI: encrypted at rest in scoped store | Founder's personal note-taking apps |

## Access Control

- Founder: full access
- Agents: read-access only via API to the client's workspace, with logged access
- Contractor (if any): scoped access to a single client's workspace under NDA + DPA
- Advisor: no access to client data by default; only when explicitly granted for incident review

## Data Movement

- Client data **never** moves to the public repo
- Public-safe excerpts (sanitized) may be drafted for case studies — and only after client review + Trust signoff
- Cross-client analysis (e.g., "what do all our logistics clients have in common") requires aggregation with n ≥ 3 and full anonymization

## What CI Enforces

`scripts/verify_public_safety.py` runs on every PR to:
- Block commits containing patterns that look like client data (long lists with sector + revenue + buyer name)
- Block commits to the public repo from `clients/` paths
- Block commits with file types associated with client data (`.xlsx`, `.csv` over a size threshold, etc.)
- Block patterns matching common Saudi PII formats (phone, ID number)

If you need to commit a sanitized sample, it must use the `SAMPLE ARTIFACT` header per `SAMPLE_GENERATION_SYSTEM.md`.

## Onboarding A New Client

1. Create `clients/{client_name}/` from `_template/` in private repo
2. Fill `intake.md` per `CLIENT_INTAKE.md`
3. Confirm DPA in place (for Managed Ops month 1+; required for Revenue Desk)
4. Confirm what data we will / will not collect
5. Note retention period (defaults from `DATA_RETENTION_POLICY.md`)

## Offboarding A Client

1. Per DPA retention period
2. Generate deletion proof
3. Return any client artifacts they want returned
4. Archive notes (anonymized) to `learning/` for company memory
5. Mark `clients/{client}/STATUS.md` as `offboarded`

## Cross-Tool Discipline

If a client shares a file via:
- Email → save to `clients/{client}/inbound/` immediately, delete from email
- WhatsApp → screenshot + save to private repo, delete from chat
- Cloud share link → download + save, do not bookmark
- In-meeting chat → save transcript, do not rely on tool retention

The goal: one source of truth per client, in one private repo location.

## When Things Go Wrong

- Client data appears in public repo → SEV-1 incident, immediate force-push removal + reflog cleanup, client notification, post-mortem
- Client data appears in a public PR review by agent → SEV-2 incident, log, fix the agent, client notification if data was visible to others
- Client data shared via Slack / WhatsApp by founder → SEV-3 incident, log, retrain founder

## What This Refuses

- "Just this once" exceptions to private-only rule
- Storing client data on personal devices
- Forwarding client data to advisors or contractors without explicit scoped consent
- Using one client's data to inform another client's deliverables (without aggregation + anonymization)
- Keeping client data after the retention period expires
