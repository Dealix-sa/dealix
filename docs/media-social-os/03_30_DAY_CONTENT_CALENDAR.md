# 30-Day Content Calendar

The calendar is **generated** (plan only, no auto-publish):

```bash
python scripts/media_social_calendar_generate.py
```

This writes a 30-day plan to
`outputs/commercial_launch/<today>/media_social/content_calendar.md` (and `.json`).

## Each day includes
- `day`, `date`, `platform`
- `pillar`, `target_vertical`
- `hook_ar`, `hook_en`
- `post_ar`, `post_en`
- `cta`, `asset_idea`, `metric_to_track`
- `auto_publish: false`

## How to use
1. Generate the plan each Monday.
2. Adapt each day's draft in your own voice.
3. Publish **manually** — the system never posts.
4. Log results in the manual metrics template (`14_SOCIAL_METRICS.md`).

Config: `config/media_social_calendar.json`.
