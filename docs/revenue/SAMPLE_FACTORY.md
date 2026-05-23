# Sample Factory

The Sample Factory produces and tracks sample artefacts that Dealix
sends to qualified buyers — diagnostics, sector briefs, audit-style
outputs. A sample is what a buyer reads to decide whether a paid
engagement is worth their time.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Produce credible, specific, named sample artefacts on a fast cadence,
so that qualified buyers have something real to evaluate within days,
not weeks.

## 2. Input

Sources:

- `sales/pipeline.csv` (opportunities at stage = qualified_call or
  beyond).
- `growth/personas.csv`, `growth/icp_segments.csv`.
- `growth/trigger_events.csv` (sample is anchored to a real, named
  trigger when possible).
- `proof/proof_library.csv` (approved proof for embedding).
- `marketing/objection_library.csv` (sample anticipates objections).

A sample is produced only on operator request, on a specific named
opportunity. The factory does not auto-generate samples.

## 3. Output

Two outputs:

- The sample document itself (PDF or HTML), stored under
  `samples/{opportunity_id}/`.
- The queue row in `sales/sample_queue.csv`.

`sales/sample_queue.csv` columns:

- `sample_id`
- `opportunity_id`
- `account_id`
- `persona_id`
- `sample_type` — diagnostic | sector_brief | sample_output |
  audit_view
- `language`
- `embedded_proof_refs`
- `delivery_format` — pdf | html | inline
- `state` — drafted | reviewed | approved | sent | discussed
- `approval_state`
- `drafted_by`
- `drafted_at`
- `sent_at`
- `notes`

The sample document itself is the load-bearing artefact. The queue row
tracks state.

## 4. Source of truth

`sales/sample_queue.csv` for state; `samples/` directory for the
artefacts.

## 5. Approval class

A2. The Sample Factory drafts; the founder approves before send. The
operator delivers the sample manually (attached to an approved email
or shared in a meeting).

## 6. Trust gate

- Guarantee scan (no guaranteed outcome language in the sample).
- Brand voice check.
- Proof integrity: every embedded proof must be approved.
- Redaction respect: customer names and identifiable data follow the
  proof's redaction posture.
- Source attribution: every external fact in the sample is cited.
- Bilingual integrity: where the sample is bilingual, Arabic and
  English content must match.
- Confidentiality: the sample does not reveal information from another
  account.

## 7. Owner

`delivery_copilot` agent in `registries/agent_registry.yaml`. Allowed
write target: `sales/`.

## 8. Worker

`scripts/dealix_sample_factory.py` (planned). The worker:

1. Reads the opportunity.
2. Selects sample type per persona, sector, and operator request.
3. Drafts the document from parametric templates.
4. Embeds approved proof and citations.
5. Writes the document and the queue row.

## 9. KPI

- Sample-to-Proposal Rate.
- Sample Review Cycle Time (days from sent to discussed).
- Brand voice first-pass rate.
- Confidentiality violations (target: 0).
- Citation completeness (every external fact cited).

## 10. Failure mode

- Sample contains a guaranteed-outcome line. Brand Guardian blocks;
  rewrite.
- Sample references unapproved proof. Worker rejects.
- Sample reveals redacted info. Trust Guardian halts; critical
  incident.
- Sample drift to generic SaaS one-pager. Brand Guardian rewrites.
- Bilingual mismatch (Arabic and English do not say the same thing).
  Worker holds.

## 11. Recovery path

- For guarantee scan failure: rewrite; ledger entry.
- For unapproved proof: proof safety agent expedites or sample uses a
  redacted form.
- For confidentiality breach: incident opened in `trust/incidents.csv`.
- For drift: paused; rewrite session; resume.
- For bilingual mismatch: copy aligned; reviewer rechecks.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Daily | New sample drafts on request |
| Weekly | Sample-to-proposal review |
| Monthly | Template audit |
| Quarterly | Sample-type retire/add |

## 13. Saudi specifics

- Bilingual samples are common; Arabic-primary samples often work best
  for founder-CEOs.
- Sector-specific samples outperform generic; the worker prioritises
  sector templates.
- Saudi buyers value structure: every sample includes an executive
  summary in 5 bullets.

## 14. Non-negotiables

- No guaranteed claims.
- No reveal of other accounts' data.
- No unapproved proof.
- No external send.
- A3 not used.

The sample is the first time the buyer sees what Dealix actually does.
Generic samples kill more deals than missing samples do.
