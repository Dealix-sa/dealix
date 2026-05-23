# LinkedIn Queue Machine

## purpose
Generate LinkedIn connection and message **drafts** for approved
accounts. No automated sending, no scraping.

## inputs
- `growth/account_scores.csv` (tier A/B)
- `growth/personas.csv`
- founder-supplied LinkedIn profile URLs (no scraping)

## outputs
`distribution/linkedin_queue.csv`:
```
draft_id,account_id,persona_id,profile_url,message_type
  (connect|message|comment|share),body,founder_note,
  fallback_share,created_at,status
```

## source
- Founder-supplied URLs only.
- Public, named individuals only — never scraped at scale.

## approval_class
per-message — each LinkedIn draft is one founder approval.

## trust_gate
- No connection / message / comment is sent by Dealix.
- The founder takes the approved draft to LinkedIn manually, or
  hands it to a delegate via the founder console.

## owner
distribution_operator (drafter) → founder (sender).

## worker
`distribution_linkedin_queue_worker` (runs on cadence).

## KPI
- Drafts per week.
- Approval rate.
- Reply rate post-send (founder logs back into the queue).

## failure_mode
- Off-voice copy.
- Outdated profile_url.

## recovery_path
- Voice rejection → regenerate.
- Bad URL → mark `dismissed:invalid_profile`.

## kill_switch
`make growth-kill-linkedin` or
`DEALIX_DISTRIBUTION_LINKEDIN_ENABLED=0`.

## audit
`audit/distribution_linkedin_runs.jsonl`.

## hard refusals
- ❌ No LinkedIn scraping.
- ❌ No automated InMail.
- ❌ No fake personas.
- ❌ No bulk connect by tool integration.
