# Market Research Protocol

This document defines how Dealix conducts market research — including the
allowed sources, the cadence, the ethical guardrails, and the way research
output is turned into operating intelligence. The protocol exists because
research is the upstream input to every other intelligence document; if
the research process is sloppy, everything downstream is too.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Research objectives

Research is conducted to answer specific operating questions, not to
produce general "market reports." Allowed question shapes:

- Which sectors meet our rubric threshold this quarter?
- Which ICPs inside a ranked sector have a credible buyer to reach?
- What objections have buyers in this ICP carried from previous tools?
- What trigger events have fired in the last 30 days?
- What sources do buyers in this ICP trust?
- Which partners have a real route into this ICP?

A research task always starts with a named question and a named owner.

## 2. Source policy

### 2.1 Allowed primary sources

- Buyer interviews (1:1, by invitation, with recorded consent).
- Partner conversations (with named partners under active agreements).
- Founder content engagement (Dealix-owned channels).

### 2.2 Allowed secondary sources

- Public sector reports with named authors and publication dates.
- Regulator publications.
- Public company announcements (press releases, official social).
- Analyst notes with attribution and date.
- Public academic studies.

### 2.3 Banned sources

- Scraping any site against its terms of use.
- Purchased lists, lead packs, or contact databases.
- Recorded conversations without explicit recorded consent.
- Information obtained under false pretence.
- Internal documents of other companies obtained outside of a sanctioned
  channel.
- Anything that cannot be re-traced to a named, dated origin.

## 3. Research cadence

| Cadence | Activity | Output |
|---|---|---|
| Daily | Trigger event scan from sanctioned sources | `growth/trigger_events.csv` |
| Weekly | Buyer-interview pulse (1-2 calls) | `growth/buyer_interview_log.md` |
| Monthly | Sector deep dive (one sector) | `growth/sector_briefs/{sector_id}.md` |
| Quarterly | Persona re-interview cycle | `growth/persona_review.md` |
| Quarterly | Scoring calibration with real outcomes | `growth/scoring_calibration.md` |

The daily and weekly cadences are bounded — no more than 2 interviews per
week unless the founder authorises a research sprint. The point is steady
compounding, not bursts.

## 4. Buyer interviews

Buyer interviews are the highest-signal research activity. They follow a
standard structure:

1. Invitation — bilingual, named, voluntary, no commercial bait.
2. Consent — recorded consent for: notes, anonymised quote use,
   identification (separate consent each).
3. Discovery script — pain anchors, current tools, objections, trust
   signals.
4. Notes — written to `growth/buyer_interview_log.md` with date,
   account_id, persona_id, and consent flags.
5. Follow-up — thank you note; offer artefact if appropriate.

Interviews never include guarantee-of-revenue framing or competitor
attacks. The interview is for learning, not selling.

## 5. Secondary research workflow

1. Define the question (one sentence).
2. List the sources to be consulted (named).
3. Read and extract — capture quotes and dates with the citation.
4. Synthesise into the relevant intelligence document.
5. Cite — every claim has a citation reference.

## 6. Ethical guardrails

- Consent is recorded with date, language used, and the consenting
  party's name.
- Bilingual operating reality is respected; consent in Arabic or English
  is equivalent if both texts are equivalent.
- Distress signals are handled with extra sensitivity — research that
  exploits buyer distress is forbidden.
- No piece of research is used to fabricate a "guaranteed outcome"
  claim.
- No personal data is moved between systems without an explicit reason
  and a logged justification.

## 7. Research output formats

- Insights: 3-5 bullets per insight, each with source citation.
- Briefs: one-page sector briefs in `growth/sector_briefs/`.
- Updates: weekly research delta in `growth/research_delta.md`.

All research outputs include a `last_reviewed_at` date and a named
reviewer.

## 8. Saudi-specific overlays

- Some sources are Arabic-primary; the protocol explicitly allows Arabic
  citations.
- Some buyers prefer not to be quoted by name; the consent step has a
  separate flag for quote attribution.
- Regulator publications change frequently; the daily scan includes the
  regulators relevant to active sectors.

## 9. Owners and approval

- Owner: Growth Strategist.
- Approver: Founder Console for any research that touches sensitive
  topics or that changes the sector list.
- Auditor: Trust Guardian.

## 10. Failure modes and recovery

| Failure | Recovery |
|---|---|
| Unattributed source | Quarantine; re-derive from clean source |
| Consent missing | Notes redacted; interview not used |
| Source contradicts another | Both held; corroboration required |
| Stale research (>90 days) | Force re-validation |
| Research used to back guarantee | Brand Guardian blocks; ledger entry |

## 11. Non-negotiables

- No source, no use.
- No consent, no quote.
- No guarantee, no draft.
- No A3.
- No external action triggered by research alone.

Research is a forcing function for honesty. It is not a marketing exercise
and it does not produce sales material directly. It produces the input
the rest of the operating system depends on.

## 12. Bilingual research notes

- Interview notes are kept in the language the interview was held in,
  with a one-paragraph summary in the other language for retrieval.
- Quotes are not translated unless the interviewee has explicitly
  consented to translation; back-translation is checked.
- Bilingual citations are accepted as first-class for any source in
  Arabic.

## 13. Tooling boundary

- Research uses general-purpose reading, note-taking, and citation
  tools.
- Research does not run scrapers, list builders, or "AI research
  agents" that pull data from arbitrary endpoints.
- Any data pulled from a public source is read by an operator with
  attribution, not by an unattended job.
