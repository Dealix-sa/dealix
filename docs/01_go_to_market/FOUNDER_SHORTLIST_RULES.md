# Founder Shortlist Rules

> أفضل 20 شركة اليوم — للمراجعة، وليس للإرسال الآلي.

The founder shortlist is the 09:00 decision surface. Engine:
`scripts/targeting_daily_brief.py` (`_shortlist`). Config:
`data/targeting/scoring_weights.yml` (`founder_shortlist_min_grade`,
`founder_shortlist_size`).

---

## Selection rules

1. Company must have passed the **compliance gate** (approved or review_required).
2. Company must **not** be a compliance reject.
3. Grade must be **≥ `founder_shortlist_min_grade`** (default `A`).
4. Sort high→low by score.
5. Take the top **`founder_shortlist_size`** (default 20).

Sensitive-sector companies (`review_required`) are *eligible* for scoring but
flagged — they only proceed to outreach after a governance sign-off
(see `docs/03_governance/OUTREACH_APPROVAL_POLICY.md`).

---

## Output: `out/founder_shortlist.md`

A ranked table: `# | Company | Sector | Score | Grade | Decision`.

Alongside it, `out/daily_targeting_brief.md` gives the founder:

- Best sector today.
- Best OS angle today.
- Biggest compliance risk today.
- Top 5 targets.

---

## What the founder does with it

- Review the top 20.
- Approve ≤ 10 drafts.
- Manually send 3–5.
- Book diagnostics from replies.

> The shortlist is a **decision aid**, not an action queue. Nothing leaves Dealix
> without the founder's manual send.
