# Demand Creation System

> Demand creation = building *future* pipeline. Capture is for *now*.
> This system covers both, but the wording, claims, and KPIs are
> proof-safe.

## Channels we run

| Channel               | Purpose                  | Approval class    |
| --------------------- | ------------------------ | ----------------- |
| founder_linkedin_post | authority + demand       | founder_review    |
| sector_report_release | demand + authority       | founder + governance |
| webinar               | demand + capture         | founder_review    |
| event_booth           | capture                  | founder_review    |
| warm_intro            | capture                  | founder_only      |
| partner_referral      | capture                  | partner + founder |
| approved_email_outreach | capture                | founder_review    |

## Hard "no" list

- No paid ads with vanity targeting (cookie pools, generic remarketing).
- No scraped emails or unconsented lists.
- No "AI agent automatically sends 100 emails/day".
- No public claims that cannot survive `verify_prompt_output_quality`.

## Demand → capture → conversion

```
authority content  →  signal observed  →  warm conversation
        ↓                                       ↓
sector report      →  inbound interest    →  proposal
        ↓                                       ↓
webinar attended   →  follow-up requested →  sample / managed pilot
```

Every transition is logged in
`<PRIVATE_OPS>/campaigns/campaign_results.csv`.

## Weekly review

`make campaign-command` produces the **Conversion Command Room** report.
The founder reviews:

- channels that produced positive replies
- channels with zero signal
- assets that produced replies
- assets that produced proposals
- learnings to fold into `MARKET_LEARNING_MEMORY.md`
