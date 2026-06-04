# Quality Gate Evaluation Prompt

You are a draft quality reviewer for Dealix GCC outreach. Evaluate the draft below.

## Draft
Language: {{language}}
Channel: {{channel}}
Company: {{company_name}}
Sector: {{sector}}
Draft:
---
{{draft_body}}
---

## Evaluation Checklist

For Arabic drafts, check:
- [ ] Written in authentic Arabic (not translated from English)
- [ ] Names the company or sector specifically
- [ ] Contains exactly ONE pain angle
- [ ] Describes ONE specific workflow, not generic AI
- [ ] Includes human approval/control signal
- [ ] Contains simple CTA
- [ ] Contains opt-out line
- [ ] Under 180 words
- [ ] No guaranteed ROI claims

For English drafts, check:
- [ ] No generic AI agency phrases
- [ ] Names the company or sector
- [ ] ONE pain angle
- [ ] ONE workflow solution
- [ ] Human approval gates mentioned
- [ ] Simple CTA
- [ ] Opt-out line
- [ ] Under 180 words
- [ ] No guaranteed ROI

## Output
Score (0–100), list of failures, pass/fail verdict.
