# Client Intake — استمارة استقبال العميل

## Purpose
Single source of truth for every variable that drives a Revenue Sprint. If the intake is incomplete, the sprint does not start. This document is the form and the operating rules behind it.

## Owner
Head of Delivery (form custodian). Founder (signer on first sprint per client).

## Inputs
- Signed SOW.
- Client kickoff call notes.
- Any prior Dealix engagement history with this client.

## Outputs
- Filled intake file at `docs/audit/sprints/SPRINT_<ID>/intake.md`.
- Confirmed ICP, geo, deal-size band, channels in scope, exclusions.
- Approval signatures (client + Dealix).

## Rules (numbered)
1. No empty cells. Unknown fields are marked "TO CONFIRM" and resolved before Day 2.
2. Exclusions are explicit and named. A blank exclusion list is rejected.
3. Channels in scope are confirmed in writing. Anything not listed is out of scope.
4. PII (personal email, phone, national ID) is never copied into the intake. Only role and company.
5. Intake is countersigned by the founder for the first sprint per client and per new sector.
6. Any change to the intake mid-sprint follows `docs/delivery/CHANGE_REQUEST_PROCESS.md`.

## Metrics
- Intake completion time from SOW signature: target ≤ 24h.
- Intake defect rate (returned for missing fields): target ≤ 10%.
- Mid-sprint change requests per sprint: target ≤ 1.

## Cadence
Once per sprint, before G1 closes.

## Evidence (paths)
- `docs/audit/sprints/SPRINT_<ID>/intake.md`
- `docs/audit/sprints/SPRINT_<ID>/intake_signatures.md`

## Verifier
Head of Delivery. Founder for first-time clients and new sectors.

## Runtime Command
`make sprint.intake.new SPRINT=<ID>` — scaffolds the intake file from this template.

## Intake fields

**Client identity.** Legal name, registered jurisdiction, primary contact name and role, billing contact, decision-maker name and role. No personal emails or phones — use corporate addresses only.

**Engagement frame.** SOW reference, sprint number for this client, start date, target handoff date, total contracted lead count, contracted deal-size band (SAR), currency.

**Ideal Customer Profile (ICP).** Buyer company size band (employees and revenue), sector codes, sub-sector if applicable, buying-center role we target, typical procurement cycle, typical deal size at the buyer side.

**Geography.** Country list, city list (if relevant), exclusions by region. For Saudi Arabia, list of regions explicitly in or out (Riyadh, Makkah, Eastern, etc.).

**Channels in scope.** Which channels Dealix is allowed to source through (public registers, sector associations, tender boards, news, public filings). Channels explicitly out of scope (scraping, bought lists, social platform automation, cold WhatsApp automation).

**Sending policy.** Does the client want the outreach pack as deliverable only, or does the client request Dealix to assist with sending? If the latter, route to A3 approval (`docs/trust/APPROVAL_MATRIX.md`).

**Exclusions.** Named competitors of the client. Companies the client is already engaging. Companies the client has explicitly de-prioritized. Any regulated entities to avoid.

**Evidence requirements.** What level of source citation does the client require per row? Default is one public source URL per row.

**Definitions of done.** What the client will treat as a successful handoff. We anchor on artifact completeness and evidence coverage, not on downstream revenue.

**Risk flags.** Any legal, regulatory, or reputational sensitivity the client has flagged.

**Signatures.** Client signer, Dealix signer (founder or head of delivery), date.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
