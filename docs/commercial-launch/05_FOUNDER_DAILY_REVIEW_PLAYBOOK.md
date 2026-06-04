# Founder Daily Review Playbook

Every morning the factory drops a fresh queue. Here is how to work it in ~30
minutes. **You are the only sender. The system never sends.**

## 1. Open today's folder

```
outputs/commercial_launch/YYYY-MM-DD/
```

## 2. Read the summary

Open `founder_review.md`. It gives you:

- Summary (counts, avg quality/compliance, real-leads flag, warnings)
- Vertical distribution
- Channel distribution
- **Top 50 drafts** (ranked by priority)
- **Top 10 opportunities**
- **Top 10 risks to watch**
- Drafts needing extra research
- Rejected drafts and why
- Founder recommendation for today
- Go/No-Go by channel

## 3. Work the priority list

Open `top_50_priority.md`. Each entry shows company, vertical, buyer, channel,
draft summary, why the lead matters, risk, and a **recommended manual action**.

For each draft you approve:

1. Open the full body in `draft_queue.jsonl` (or `founder_review.csv`).
2. **Personalise one real, specific detail** (a recent project, a named site, a
   public announcement). Generic sends are weak sends.
3. Confirm the opt-out line is present.
4. Send **manually** from your own inbox / LinkedIn / the company's form.
5. Log the touch in your CRM.

## 4. Respect the gates

- Anything in `rejected_drafts.jsonl` was rejected for a reason — do not send it.
- Anything `research_required` needs a real buyer name + verified **business**
  email first. Never scrape personal emails.
- Regulated verticals (legal) lead with privacy-first language.

## 5. Before any cold-email batch

Confirm the [domain readiness checklist](04_CHANNEL_POLICY.md) is green and a
suppression-list owner is named. The OS is **GO for drafting, NO-GO for
automated sending** — always.

## Output files reference

| File | What it is |
|------|------------|
| `draft_queue.jsonl` | All accepted drafts (one JSON per line) |
| `founder_review.csv` | Sortable queue (open in Excel/Sheets) |
| `founder_review.md` | The full daily review (start here) |
| `top_50_priority.md` | Fast-scan priority list |
| `rejected_drafts.jsonl` | Rejected drafts + reasons |
| `compliance_report.json` | Compliance gate summary |
| `safety_audit.json` | Safety audit result (must be `passed: true`) |
| `daily_metrics.json` | Counts, distributions, target status |
| `next_actions.md` | Your to-do list for the day |
