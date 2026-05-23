# Lead Source System

Dealix lead sources are explicitly enumerated. If a source is not on this
list, it cannot feed the Distribution War Machine. The list is short and
boring on purpose — that is the cost of running a trust-first operation.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Why sources are enumerated

Lead source hygiene is the single largest predictor of pipeline quality
in Saudi B2B. Mixed sources contaminate ICP fit, distort the account
scoring model, and break trust signals. By enumerating every allowed
source, we make contamination visible and auditable.

## 2. Allowed sources

### 2.1 Warm referrals

- Definition: A named, real person who introduces a named, real account.
- Recording: `outreach/warm_intro_log.csv` with introducer, account,
  date, channel.
- Approval: A2 — the introducer's consent to be named is required and
  recorded.
- Notes: This is the single highest-quality source.

### 2.2 Sector reports and public publications

- Definition: Public, dated sector reports with named authors.
- Recording: `growth/source_refs.csv` with publication, date, URL,
  page or section.
- Approval: A1.
- Notes: Used as a signal, not a contact list. We do not extract personal
  contacts from public reports.

### 2.3 Founder content engagement

- Definition: Engagement on Dealix-owned channels (LinkedIn posts,
  newsletter, articles) where the buyer has chosen to interact.
- Recording: `marketing/engagement_log.csv`.
- Approval: A1 to record; A2 to convert to outreach draft.
- Notes: This is consented engagement; outreach drafts reference the
  specific piece the buyer engaged with.

### 2.4 Partner introductions

- Definition: Accounts introduced by named partners under an executed
  partner agreement.
- Recording: `customer_success/referral_queue.csv`.
- Approval: A2 per introduction.
- Notes: Partner Revenue Agent owns the queue. The partner agreement
  must be active.

### 2.5 Sector events and roundtables

- Definition: In-person and online events where the buyer has opted into
  a follow-up.
- Recording: `marketing/event_attendees.csv` with opt-in posture.
- Approval: A2.
- Notes: Opt-in evidence is required.

### 2.6 Inbound contact form submissions

- Definition: Submissions on Dealix-owned forms with explicit consent.
- Recording: `outreach/inbound_queue.csv`.
- Approval: A1 to log; A2 to respond.
- Notes: These are the only inbound submissions accepted.

### 2.7 Founder personal network (with consent)

- Definition: Named individuals in the founder's network who have opted
  in to be contacted on behalf of Dealix.
- Recording: `outreach/network_consent.csv` with consent date.
- Approval: A2 per contact.
- Notes: The consent is per-purpose; we do not lift a personal
  connection into a sales list without explicit yes.

### 2.8 Trigger event signals

- Definition: Public, dated events that justify an outreach as defined
  in `TRIGGER_EVENT_SYSTEM.md`.
- Recording: `growth/trigger_events.csv`.
- Approval: A1 to record; A2 to draft outreach.
- Notes: Trigger alone is insufficient; ICP + persona + trigger together
  drive a draft.

## 3. Banned sources (explicit)

- Scraped contact lists, scraped LinkedIn exports, scraped trade-show
  attendee lists.
- Purchased "Saudi B2B leads" lists from data brokers.
- Email lists from unrelated mailings that were not consented per
  Dealix outreach.
- Personal connections lifted from social networks without explicit
  per-contact consent.
- Contact information obtained by ruse (e.g. anonymous request for a
  brochure that hides commercial intent).
- Recordings, transcripts, or notes from third-party meetings without
  recorded consent.
- "Trigger feeds" without source attribution.

If a source is unsure, it is treated as banned until reclassified by the
Trust Guardian.

## 4. CSV output schema

`growth/lead_source_registry.csv`:

- `source_id`
- `source_type` — one of the allowed sections above
- `source_owner` — agent or operator
- `consent_evidence` — reference to consent record
- `account_count`
- `last_used_at`
- `notes`

## 5. Hygiene rules

- Every account in `growth/account_universe.csv` carries a `source_id`
  referencing this registry.
- Accounts with no source are quarantined and not scored.
- Accounts with banned-source provenance are removed and ledgered.
- The same account may have multiple sources; the strongest source is
  used for the warm_path_score in the Account Scoring Model.

## 6. Cadence

| Cadence | Activity |
|---|---|
| Weekly | Source-by-source quality review (reply rate, conversion) |
| Monthly | Consent evidence audit |
| Quarterly | Source list review — add, retire, reclassify |

## 7. Saudi specifics

- Verbal consent is logged with a date and the named witness; written
  consent is preferred.
- Bilingual consent text is the default — the consent record records
  which language was used.
- PDPL alignment is the floor; ZATCA and sector regulators may add
  further requirements.

## 8. Owners and approval

- Owner: Growth Strategist.
- Approver: Founder Console for source additions or retirements.
- Auditor: Trust Guardian.

## 9. Failure modes and recovery

| Failure | Recovery |
|---|---|
| Banned source detected | Affected accounts removed; ledger entry |
| Consent evidence missing | Account quarantined; outreach blocked |
| Source mix drift | Performance Analyst raises alert |
| Re-entry of a removed account | Requires founder override + new source |

## 10. Non-negotiables

- We do not scrape.
- We do not buy lists.
- We do not exploit ambiguous consent.
- We do not let A3 anywhere near source acquisition.
- Source decisions are reversible and ledgered.

Slow, attributable lead acquisition compounds. Fast, mixed lead acquisition
degrades trust faster than it ever fed the pipeline.
