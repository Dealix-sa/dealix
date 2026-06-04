# Social & Media Operating System

A daily, **review-only** marketing factory. It drafts social posts, content
outlines, ad copy, and PR pitches — bilingual AR + EN — and places them in the
founder review queue. **It never posts, schedules, or spends.**

> No auto-posting. No scheduling APIs. No ad spend. No bought engagement. No
> secrets. The founder reviews, approves, and publishes manually.

Sources: `config/commercial_social.json`, `dealix/commercial_launch/social.py`.

## Daily platform mix (minimum 80)

| Platform | Min/day |
|----------|---------|
| LinkedIn post | 20 |
| X / Twitter post | 20 |
| Instagram caption | 12 |
| Email newsletter section | 4 |
| Blog / article outline | 6 |
| Google ad copy (no spend) | 10 |
| Meta ad copy (no spend) | 10 |
| PR / media pitch | 6 |
| **Total** | **80+** |

A typical run produces ~130 posts after the gates.

## Content pillars

`educational` · `proof` · `founder_pov` · `offer` · `question` · `case_angle` —
rotated across the 5 verticals and both languages.

## How to run

```bash
python scripts/commercial_social_factory.py
python scripts/commercial_social_factory.py --target 120 --date 2026-06-04
```

Standard-library only. No secrets, no network.

## Every post carries

```
post_id, created_at, platform, vertical, language, pillar, hook, body,
hashtags, cta, char_count, quality_score, compliance_score, risk_level,
post_allowed (false), external_post_blocked (true),
requires_founder_approval (true), no_ad_spend (true), status (founder_review)
```

## Gates

- **Quality:** length fit per platform, tied to a vertical, has a CTA, no
  exaggeration/banned terms.
- **Compliance:** no guaranteed-ROI claims, no data-access claims, review-only
  invariants intact.
- **Safety audit:** the shared `commercial_safety_audit.py` scans `social_queue.jsonl`
  and fails on any `post_allowed=true`, `external_post_blocked=false`, scheduling
  API, or posting automation.

## Outputs

Under `outputs/commercial_launch/YYYY-MM-DD/`:

- `social_queue.jsonl` — accepted posts
- `social_rejected.jsonl` — rejected posts + reasons
- `social_review.md` — founder review (by platform, vertical, pillar; top 15)
- `social_metrics.json` — counts + target status

## Publishing rules (founder, do not break)

1. No auto-posting, scheduling, or ad spend.
2. Personalise one real detail, then publish manually from your own accounts.
3. Keep claims conservative and provable — no guarantees.
4. Respect each platform's terms of service.
