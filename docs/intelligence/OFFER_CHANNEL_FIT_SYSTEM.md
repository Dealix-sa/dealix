# Offer-Channel Fit System

Every Dealix offer needs to land in a channel where the buyer actually
listens. This document defines the offer-by-channel matrix, the fit notes,
and the trust-gate rules that decide whether a given offer can be drafted
into a given channel at all.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Why this layer exists

We can have a strong offer and the right ICP, and still fail if the offer
is delivered in a channel the buyer ignores or distrusts. Generic SaaS
pipelines push the same offer through every channel; Dealix does not. The
offer-channel fit system declares, for every offer in the ladder, which
channels are sanctioned and at what intensity.

## 2. Channels Dealix operates

The Distribution War Machine operates only the following channels:

- WARM — warm introductions and named referrals.
- LI — LinkedIn (founder voice, personalised, draft only, queued for
  approval).
- EM — Structured email (single-account, personalised, drafted to a
  queue).
- CF — Contact-form drafts (when the buyer has invited contact via their
  public site).
- CC — Founder content channels (LinkedIn posts, articles, newsletter)
  — content-led demand, not direct contact.
- PA — Partner-introduced (handled by Partner Referral Machine).
- EV — Events and roundtables (in-person, by invitation).

Banned at the system level (Dealix does not run these as growth channels):
- Cold WhatsApp without prior consent.
- Mass SMS.
- Mass cold email from purchased lists.
- Anonymous "ghost" contact-form spam.

## 3. Offer-channel matrix

| Offer | WARM | LI | EM | CF | CC | PA | EV | Notes |
|---|---|---|---|---|---|---|---|---|
| Founder Diagnostic | strong | strong | strong | medium | strong | strong | strong | Lead offer; bilingual |
| RevOS Pilot | strong | strong | strong | weak | medium | strong | medium | Requires call discovery |
| Sample Pack (sector) | medium | strong | strong | medium | strong | strong | weak | Sector-specific |
| Proposal (custom) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | Only after qualified call |
| Retainer | strong | medium | medium | weak | medium | strong | medium | Expansion offer |
| Productised Workshop | strong | strong | medium | medium | strong | strong | strong | Group + 1:1 |
| Partner Co-Sell | n/a | n/a | n/a | n/a | n/a | strong | medium | Partner-led |
| Trust Pack (proof) | strong | medium | medium | weak | strong | medium | weak | Read-only material |

Definitions:
- strong: sanctioned with default intensity.
- medium: sanctioned but with stricter trust-gate checks and lower
  volume.
- weak: only when a named operator override is filed.
- n/a: not a distribution channel — the offer is reached only through a
  prior qualified path.

## 4. Trust gates by channel

Each channel has explicit trust-gate rules enforced by the Trust Guardian
and embedded in the policy-as-code rules:

- WARM: requires named introducer in `outreach/warm_intro_log.csv`.
- LI: drafts must pass brand voice check; volume capped; no auto-connect.
- EM: drafts must pass suppression check, no list mailing, single-account
  drafts only; queue requires founder approval per send.
- CF: only used where the buyer has invited contact; never used as a
  workaround for outreach restrictions.
- CC: content drafts pass brand and proof checks; no embedded
  guaranteed-claim language.
- PA: partner referrals require an executed partner agreement and a
  named introducer.
- EV: invitations are tracked with the buyer's consent posture.

## 5. Output schema

`growth/offer_channel_fit.csv`:

- `offer_id`
- `channel_id`
- `fit_level` — strong | medium | weak | none
- `intensity_cap` — max drafts per week per channel per offer
- `trust_gate_refs`
- `notes`

A weekly delta is appended to `growth/offer_channel_fit_delta.md`.

## 6. Intensity caps

Channel intensity is capped to keep brand integrity and avoid degradation.
Caps are conservative on purpose; we would rather under-send than burn the
channel.

| Channel | Default weekly cap (per offer) | Notes |
|---|---|---|
| WARM | unlimited | Bounded by introducer goodwill |
| LI | 10 | Personalised drafts only |
| EM | 20 | Single-account drafts |
| CF | 3 | Only on invited contact forms |
| CC | unlimited | Brand voice gated |
| PA | bounded by partner | Per-partner agreement |
| EV | event-driven | Per-event capacity |

Caps may be lowered automatically by the Performance Analyst if reply
quality drops below band, and may not be raised without a founder
approval entry.

## 7. Bilingual default

For Saudi accounts, the default operating language is captured in the
ICP and persona entries. Outreach drafts default to the buyer's primary
language. Bilingual drafts (Arabic + English) are used when the buyer
operates in both.

## 8. Cadence

| Cadence | Activity |
|---|---|
| Weekly | Reply quality review; intensity recalibration |
| Monthly | Matrix refresh; add new offers; retire dead ones |
| Quarterly | Channel posture review |

## 9. Owners and approval

- Owner: Growth Strategist + Offer Architect.
- Approver: Founder Console on matrix changes.
- Auditor: Trust Guardian on every channel-gate breach.

## 10. Failure modes and recovery

| Failure | Recovery |
|---|---|
| Channel saturation | Intensity cap lowered; reply quality re-baselined |
| Offer in wrong channel | Draft blocked; offer architect notified |
| Brand drift on a channel | Brand Guardian holds drafts; rebuild voice |
| Buyer marks Dealix as spam | Channel suspended; trust ledger entry |
| Partner overrun on PA | Partner agreement renegotiated |

## 11. Non-negotiables

- No external send without explicit per-draft founder approval.
- No "guaranteed" claim appears in any channel.
- No channel runs against suppressed identities.
- A3 is banned across the system.

The matrix is a filter on what we can do, not a wish list. If an offer
does not fit any channel cleanly, the offer is the problem, not the
channel.
