# GitHub Organisation Branding — Dealix

> How the Dealix brand renders on GitHub: the org profile, each repository's
> README, social previews, and contributor surfaces.
>
> Companion to [`BRAND_GUIDELINES.md`](./BRAND_GUIDELINES.md).

---

## 1. Organisation profile

### 1.1 Avatar

- **Image:** `landing/assets/logos/dealix-icon.svg` exported to `512×512 PNG`.
- **Background:** `--deep-navy` (`#0B1220`).
- **Padding:** 12% on every side — GitHub rounds the corners; the icon must not touch them.

### 1.2 Display name & description

- **Display name:** `Dealix`
- **Description (≤ 160 chars):**
  *AI Operating Team for Saudi B2B SMBs. Built Arabic-first. PDPL-compliant. Intelligent Deals. Real Growth.*
- **URL:** `https://dealix.com`
- **Location:** `Riyadh, Saudi Arabia`
- **Twitter/X:** `@dealix` (or current handle — confirm before populating)

### 1.3 Pinned repositories

Pin **6** repos. Order matters — these are the first thing a visitor (often
an investor or recruit) sees. Suggested order:

1. `dealix` — main monorepo
2. `dealix-landing` — website (if split out)
3. `dealix-design` — Figma exports, brand assets
4. `dealix-sdk-python` — public SDK (when published)
5. `dealix-docs` — public-facing developer docs (when published)
6. `dealix-blog` — engineering blog (optional, only if active)

Re-pin in this exact order after any new public repo lands. Empty pins look
sloppier than fewer pins — five well-maintained beats six half-finished.

### 1.4 Org profile README (`.github/profile/README.md`)

Required sections, in this order:

1. **Hero banner** — `og-image.png` (1280×640) at the top, full-width.
2. **One-line pitch** — bilingual, EN first, AR below.
3. **What we ship** — three short bullets (Sprint, Data Pack, Managed Ops).
4. **Open work** — short list of repos with a one-liner each.
5. **Hiring** — if hiring, one line + link. Otherwise omit (don't fake it).
6. **Contact** — email, website, X handle.

Keep it under 60 lines. No emojis. No "Hi, we're Dealix!". No stats badges
(stargazers, contributors counts) on the org README — they go on repo READMEs.

A template lives at the end of this document (§5).

---

## 2. Per-repository README pattern

Every public Dealix repository ships with a README that follows this shape.
This makes the org legible at a glance — a visitor jumping from one repo to
the next never has to re-learn where to find what.

### 2.1 Required structure

```markdown
# <repo-name>

> One-sentence purpose. Specific, not aspirational.

[badges row — see §2.2]

[hero image — optional, only if visual product]

## What this is
Three bullets max. What it does, who it's for, what's not in scope.

## Quick start
The 60-second path to running it. If it can't be 60 seconds, link to a
QUICK_START.md.

## Status
Live / Pilot / Internal Only / Draft — one of the four canonical statuses
from the operational design system. Pair with a date.

## Docs
Links to the deeper documentation. Bilingual where applicable.

## Contributing
Link to CONTRIBUTING.md or a one-paragraph rule set.

## License
The license line — usually a one-liner pointing at LICENSE.

## Contact
Founder email and brand URL.
```

### 2.2 Badge row (canonical order)

Always in this order, left to right:

1. **License** — `![License](https://img.shields.io/badge/License-MIT-007A5C)` (use `--teal-ink` `007A5C`)
2. **CI** — GitHub Actions status badge for the main workflow.
3. **Coverage** — only if real and ≥ 70%. Don't show a 12% coverage badge.
4. **Status** — `![Status](https://img.shields.io/badge/Status-Live-10B981)` using `--success` for Live, `--warn` `F59E0B` for Pilot, `--silver-2` `6B7480` for Internal/Draft.
5. **Arabic-ready** — `![Arabic](https://img.shields.io/badge/RTL-ready-0B1220?labelColor=00D1A1)` — brand-coloured marker, when the repo supports Arabic UI.

Don't add: stars, forks, contributors, "Made with ❤️", "Awesome List"
badges, or any shield that requires no maintenance to acquire.

### 2.3 Repo description (the one-liner under the repo name)

- ≤ 100 chars.
- Starts with a verb or a noun, not "A library for…".
- No emoji.
- End with a period.

Good: *Founder-approval gated AI Operating Team for Saudi B2B SMBs.*
Bad: *🚀 The next-gen AI platform that revolutionizes sales for SMBs!*

### 2.4 Repo topics

Apply these topics to every Dealix public repo, plus repo-specific ones:

`dealix` · `ai-operating-team` · `saudi-arabia` · `pdpl-compliant` ·
`arabic-first` · `b2b-smb`

Then add 1–3 specific topics (e.g. `python`, `fastapi`, `tailwindcss`,
`design-system`).

---

## 3. Social preview cards (OG images)

GitHub renders an Open Graph card when a repo URL is shared on Twitter/X,
LinkedIn, Slack, Notion, etc. Set a custom social preview image on **every
public repo**.

### 3.1 Spec

- **Dimensions:** 1280 × 640 px (GitHub's preferred ratio).
- **Background:** `--deep-navy` with a 1 px Emerald-Teal hairline along the bottom.
- **Logo:** horizontal lockup, vertically centred-left, height = 80 px, 64 px left padding.
- **Repo name:** Space Grotesk 600, 48 px, `--white`, vertically centred-right of the divider.
- **One-line description:** Inter 400, 22 px, `--soft-silver`, under the repo name.
- **Bottom-right corner badge:** the status pill (e.g. `LIVE` in `--success`).

Master template lives at `landing/assets/og/repo-og-template.svg`. Duplicate
it per repo and swap the repo name + description.

### 3.2 Where to set it

Settings → Social preview → Upload image.

Do this **once per repo**. GitHub caches aggressively, so the change can
take 24–48 h to propagate to social platforms.

---

## 4. Issue & PR templates (brand-consistent)

The existing `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md`
files set the contributor tone. They should:

- Use the same five-pillar values language (Trust, Growth, Deals, Results, Global) where relevant.
- Reference the operational forbidden-claims list when reviewing copy
  changes (`tests/test_landing_forbidden_claims.py`).
- Default the PR body to a checklist that includes "Tokens updated in
  all 3 places" when the change touches `docs/brand/` or
  `design-systems/dealix-brand/`.

A future PR can update these templates — out of scope for the initial
brand-guidelines drop.

---

## 5. Org profile README template

Drop this verbatim into `.github/profile/README.md` (in a separate
`dealix/.github` repo or the main repo if GitHub's org-profile feature uses
this monorepo). Substitute the placeholders marked `<…>`.

```markdown
<!-- HERO -->
<p align="center">
  <img src="https://dealix.com/assets/og/dealix-org-hero.png" alt="Dealix" width="100%">
</p>

# Dealix

**Intelligent Deals. Real Growth.**
*صفقات ذكية. نموّ حقيقي.*

The AI Operating Team that turns Saudi B2B pipelines into evidence-backed
revenue. Built Arabic-first. PDPL-compliant. Founder-approval gated by
design.

فريق تشغيل بالذكاء الاصطناعي يحوّل خطّ مبيعات الشركات السعودية إلى إيرادات
مدعومة بالدليل. مبنيّ بالعربيّة. متوافق مع PDPL. كلّ خطوة بموافقة المؤسّس.

---

## What we ship

- **7-Day Revenue Proof Sprint** — SAR 499 · diagnostic + first proof pack.
- **Sector Data Pack** — SAR 1,500 · vertical-specific account scoring.
- **Managed Revenue Ops** — SAR 2,999–4,999 / month · full AI operating team.

## Open work

- [`dealix`](https://github.com/<org>/dealix) — main monorepo (Python · FastAPI · landing)
- [`dealix-design`](https://github.com/<org>/dealix-design) — design tokens, brand assets

## Contact

- **Web** — https://dealix.com
- **Email** — founder@dealix.com
- **X** — @dealix
```

Keep it under 60 lines, no emojis, no stat badges, no marketing fluff.

---

## 6. PR submission for org-level changes

Brand-level changes to the org (avatar, description, pinned repos, profile
README) require founder approval. Workflow:

1. Open a PR against this file or `.github/profile/README.md` with the
   proposed change.
2. Tag the founder for review.
3. After merge, the founder applies the change in GitHub UI (org settings
   are not Terraform-managed today).
4. Note the change in `BRAND_GUIDELINES.md` §9 (Decision log) with the date.
