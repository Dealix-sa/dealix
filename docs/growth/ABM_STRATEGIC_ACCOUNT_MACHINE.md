# ABM Strategic Account Machine

> Orchestrates multi-touch motion on a small list of named strategic accounts.

## 1. Purpose

For our top 10–20 strategic accounts at any time, orchestrate a personalised, multi-touch, multi-channel motion (LinkedIn post engagement → comment → DM draft → email draft → warm intro request → sample share → meeting request) over 8–12 weeks.

## 2. Input

- The `strategic_accounts` slice of `data/growth/account_scores.csv` (priority A, picked by the founder).
- Buyer persona map for each account.
- Sector sample artefacts.

## 3. Output

- A weekly **per-account motion plan** with up to 5 next-step drafts queued for approval.
- A motion ledger in `data/growth/strategic_motion.csv`.

## 4. Approval class

**A2.** Founder approves the motion plan once at start; each individual draft still requires founder approval at send time.

## 5. Owner

Distribution Operator + founder.

## 6. Worker name

`abm_strategic_worker`.

## 7. KPI

- Active strategic accounts: 10–20.
- Motion freshness: no account left silent > 14 days.
- Meeting conversion: ≥ 1 booked meeting per 5 strategic accounts per quarter.

## 8. Doctrine

- Strategic accounts are **founder-picked**. The machine cannot promote an account into the strategic list autonomously.
- Drafts must always cite **fresh** evidence (≤ 21 days old).
- We do not run more than 20 strategic accounts at once — focus is the point.

## 9. Failure modes

| Failure                                | Recovery                                          |
|----------------------------------------|---------------------------------------------------|
| Plan recommends 6+ touches in a week    | Cap at 4; founder reviews                         |
| Two strategic accounts conflict (same buyer) | Refuse; founder picks one                   |
| Account goes silent for 6 weeks         | Move to nurture; document reason                  |
