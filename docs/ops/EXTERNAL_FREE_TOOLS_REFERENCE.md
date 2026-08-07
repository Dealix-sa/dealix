# External Free Tools Reference

Curated from [Moh4696/300-free-resource-websites](https://github.com/Moh4696/300-free-resource-websites)
(~300 free tools across 19 categories) — this doc keeps only the subset with
a concrete tie to ongoing Dealix work. Not a dependency list; these are
external websites/services used manually, not installed into the repo.

## Design assets (Wave 4 / homepage image gap)

The taste-skill audit (`docs/ops/TASTE_SKILL_DESIGN_AUTOMATION_PLAN.md`)
flagged the homepage as text-only with no real images — "a pure-text page
is not minimalism, it is incomplete work." These are free, real-photo
sources to close that gap, in the priority order the skill itself
recommends (image-gen tool first if available, real photography second):

- [unsplash.com](https://unsplash.com), [pexels.com](https://pexels.com),
  [pixabay.com](https://pixabay.com) — free stock photography
- [coverr.co](https://coverr.co), [mixkit.co](https://mixkit.co) — free
  stock video, if a hero video is ever wanted

## Icon libraries (already the skill's stated preference)

`design-taste-frontend/SKILL.md` §3.C already names these as the preferred
icon families over Lucide — no new decision needed, just where to get them:

- [heroicons.com](https://heroicons.com)
- [phosphoricons.com](https://phosphoricons.com)
- [tabler.io](https://tabler.io) icons

## Color/contrast tools (Wave 4 token unification)

For unifying `/pricing`+`/offers`+`/cases`'s amber theme onto `/`'s
navy/gold `globals.css` tokens:

- [coolors.co](https://coolors.co) — palette generation/exploration
- [realtimecolors.com](https://realtimecolors.com) — live-preview a palette
  against real UI
- WebAIM contrast checker (webaim.org) — verify the redesign-existing-
  projects skill's WCAG AA contrast rule on any new pairing

## Production auditing (run once `dealix.me` is confirmed live)

These could not be run from this session's sandbox (network policy blocks
this specific domain) — run manually once production access is confirmed:

- [securityheaders.com](https://securityheaders.com) — HTTP security header
  grade
- [ssllabs.com/ssltest](https://www.ssllabs.com/ssltest/) — TLS
  configuration grade
- [haveibeenpwned.com](https://haveibeenpwned.com) — check if any project
  email/domain has appeared in a breach
- [pagespeed.web.dev](https://pagespeed.web.dev) — Core Web Vitals /
  performance audit

## Writing / bilingual polish

For tightening `sales/*.md` and website copy (AR/EN):

- [languagetool.org](https://languagetool.org) — grammar check, supports
  Arabic and English
- [deepl.com](https://deepl.com) — translation quality check for parity
  between AR and EN copy

## Not adopted

The other ~14 categories in the source list (media/streaming, PDF
conversion, free courses, research/academic, dev-tool generators, free
hosting beyond Vercel, whiteboards/productivity, general privacy/security,
everyday utilities, career/job tools, health/fitness) don't have a current
tie to Dealix work and aren't included here to keep this reference
actionable rather than exhaustive. Re-visit if a specific need comes up.
