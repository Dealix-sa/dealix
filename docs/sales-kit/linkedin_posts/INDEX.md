# LinkedIn Long-Form Posts · فهرس

> 10 posts (this directory) + 3 originals at `../linkedin_longform_posts.md`.
> Bilingual. Doctrine-aligned. No emojis. Designed for Tuesday/Thursday/Saturday
> 09:00 KSA publishing.

## Cluster breakdown

| # | File | Cluster | Topic |
|---|------|---------|-------|
| 04 | `post_04_no_autonomous_send.md` | Counter-narrative | Why we refuse autonomous send |
| 05 | `post_05_arabic_first_ai.md`     | Technical Proof | Arabic-first AI vs translated AI |
| 06 | `post_06_pdpl_lawful_basis.md`   | Technical Proof | PDPL lawful basis in B2B outreach |
| 07 | `post_07_no_cold_whatsapp.md`    | Counter-narrative | Why cold WhatsApp is a category error |
| 08 | `post_08_proof_ledger.md`        | Technical Proof | What a proof ledger is and why we built one |
| 09 | `post_09_icp_ranking_pattern.md` | Case-safe Pattern | What we noticed in Saudi B2B ICP data |
| 10 | `post_10_founder_approves_all.md`| Counter-narrative | Approval queue isn't slow — fake automation is |
| 11 | `post_11_dq_score_pattern.md`    | Case-safe Pattern | Data quality patterns in 50 Saudi CRMs |
| 12 | `post_12_zatca_receipts.md`      | Technical Proof | ZATCA Phase 2 receipts for B2B SaaS |
| 13 | `post_13_no_linkedin_automation.md` | Counter-narrative | We don't automate LinkedIn — here's why |

## Publishing cadence

- Tuesday 09:00 KSA — Technical Proof or Case-safe Pattern
- Thursday 09:00 KSA — Counter-narrative
- Saturday 09:00 KSA — Open slot (Q&A or curated retweet thread)

## Doctrine reminders before each publication

- No invented metrics. Every number cites either a proof_id, a public
  source, or carries an `is_estimate=True` caveat in the body.
- No competitor names (positive or negative).
- No emojis (Saudi B2B professional voice).
- Arabic primary, English secondary. RTL-readable.
- CTA at the end: book demo / read more / reply.

## Approval workflow (per post)

1. Founder edits the draft (this file).
2. Pastes into LinkedIn scheduled-post UI.
3. Reviews preview.
4. Schedules. (LinkedIn's own automation — no third-party tool.)
5. After publishing: log `linkedin_post_published` event in
   `proof_ledger`.
