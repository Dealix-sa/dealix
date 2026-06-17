# VISUAL IDENTITY SYSTEM — نظام الهوية البصرية

> Look-and-feel for `landing/` and `frontend/`. Grounded in the **real tokens already in the repo**.
> Improve incrementally; do not start a from-scratch restyle. Pairs with `BRAND_IDENTITY_SYSTEM.md`.

## Design direction

Saudi/GCC enterprise · premium · executive · command-center · high-contrast · spacious ·
sharp hierarchy · Arabic-first · serious (not playful). **No childish AI gradients.**

## Current token reality (two surfaces — reconcile, don't rewrite)

| Token | `landing/styles.css` | `frontend/tailwind.config.ts` |
|---|---|---|
| Primary | slate ink scale `--ink-900 #0b1220` … `--ink-50 #f1f5f9` | **navy** `primary.500 #001F3F` (50→950 scale) |
| Accent | sky `--accent #0ea5e9`, cyan `--accent-2 #22d3ee` | **gold** `#D4AF37` (50→700 scale) |
| Status | success `#10b981` · warn `#f59e0b` · danger `#ef4444` | — |
| Radius | 8 / 14 / 20 / 28 px | (Tailwind defaults) |

> **Decision needed (founder):** the **navy `#001F3F` + gold `#D4AF37`** pair (frontend) reads as the
> premium executive identity; the landing slate+sky is lighter/generic. Recommended direction:
> converge the public surfaces toward **navy + gold on dark**, keeping slate as neutral support.
> This is a convergence task, not a rewrite — do it section-by-section behind the build gate.

## Typography

- Arabic-first: **IBM Plex Sans Arabic** (fallback Noto Naskh Arabic, system-ui).
- Latin: **Inter** (fallback IBM Plex Sans Arabic).
- Type scale (suggested, rem): 0.75 · 0.875 · 1 · 1.125 · 1.25 · 1.5 · 2 · 2.5 · 3.25.
- Headings: tight leading, high weight; body: comfortable leading for Arabic legibility.
- Numbers are first-class (we lead with numbers, not adjectives) — use tabular figures in metrics.

## Spacing & layout

- Base unit 4px; spacing scale 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96.
- Generous section padding (≥64px desktop) — premium = space, not clutter.
- Max content width ~1120–1200px; strong vertical rhythm.
- **RTL-first:** mirror layouts; logical properties (`margin-inline`, `padding-inline`); icons/arrows flip.

## Color usage rules

- Dark, high-contrast surfaces for executive/command sections; navy base, gold for emphasis only.
- Gold accent is **rare and intentional** (primary CTA, key metric) — never a background wash.
- Status colors only for real status; never decorative.

## Components (style rules)

- **Cards:** radius 14–20px, 1px low-contrast border, subtle elevation; no neon glow.
- **CTA (primary):** one per page, gold/high-contrast, generous tap target.
- **CTA (secondary):** ghost/outline; must never compete with primary.
- **Metrics:** large tabular number + short label + evidence/source link.
- **OS layer cards:** uniform grid; each shows name + one line + status label.

## Visual dos & don'ts

| Do | Don't |
|---|---|
| dark premium navy + restrained gold | rainbow AI gradients / glow |
| one emphatic CTA per page | multiple competing CTAs |
| space, hierarchy, tabular numbers | clutter, decorative icons everywhere |
| RTL-correct mirroring | LTR layout with Arabic pasted in |
| evidence next to every claim | unlabeled hero superlatives |

## Verify any code change

`cd frontend && npm run build` (and `npm run lint`). Scope diffs; keep them reviewable.

## References

`DESIGN_SYSTEM.md`, `design-systems/`, `landing/styles.css`, `frontend/tailwind.config.ts`.
