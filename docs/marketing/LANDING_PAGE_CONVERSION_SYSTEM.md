# Landing Page Conversion System

How we design, instrument, and improve the public landing surfaces.

## 1. Doctrine

- One **primary CTA per page**.
- One **trust note per page**, always visible above the fold.
- One **proof artefact** referenced per page (or a link to /proof).
- No urgency tricks (no countdown timers, no "only 3 left").
- No claims of guaranteed outcome.

## 2. Primary surfaces

| Page                    | Purpose                                     | Primary CTA                       |
|-------------------------|---------------------------------------------|-----------------------------------|
| `/`                     | Brand introduction                           | "Start a Revenue Sprint"          |
| `/diagnostic.html`      | Free Sample / Diagnostic request             | "Request a sample"                |
| `/start.html`           | Revenue Sprint signup                        | "Book the Sprint"                 |
| `/founder.html`         | Founder Console pitch                        | "See the Founder Console"         |
| `/proof.html`           | Proof artefacts                              | "Read the proof"                  |
| `/pricing.html`         | Transparent price bands                      | "Talk pricing"                    |
| `/trust.html`           | Trust posture, governance, kill switches    | "How we govern"                   |

## 3. Page template

```
[ Hero ]
  - Eyebrow (sector / pillar)
  - H1: 6–12 words, leads with the pillar
  - Subtitle: 2–3 lines, names the buyer and the promise
  - Trust note inline
  - Primary CTA + 1 ghost CTA
[ Pillar section ]
  - 3 cards (one per active pillar relevant to the page)
[ Proof section ]
  - 1 anonymised metric or short case study
[ Offer section ]
  - Rung-specific packaging
[ FAQ ]
  - 4–6 questions; each cites a doctrine link
[ Footer ]
  - Brand pillars · AI-assisted, trust-gated, founder-approved
```

## 4. Conversion instrumentation (heuristic)

| Event                          | What we measure                          |
|--------------------------------|------------------------------------------|
| Page view                      | per page                                 |
| CTA click                      | per page, per CTA                        |
| Form submit                    | per page                                 |
| Sample / diagnostic requested  | per page                                 |
| Sprint signup                  | per page                                 |

Targets are heuristics, not promises. We move them via experiments documented in `docs/performance/EXPERIMENT_BACKLOG.md`.

## 5. Refusal patterns (verifier-enforced)

The landing verifier flags:

- Pages with a banned phrase.
- Pages with > 1 primary CTA.
- Pages with no trust note.
- Pages claiming a guaranteed outcome.
- Pages using auto-translated AR/EN without a `lang` attribute.

## 6. Accessibility

- Contrast ≥ 4.5:1 for body, ≥ 3:1 for large text and UI components.
- `lang` attribute set per page.
- `dir` attribute set per page.
- Focus rings visible.
- Keyboard navigable.
