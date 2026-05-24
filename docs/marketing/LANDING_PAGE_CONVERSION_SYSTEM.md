# Landing Page Conversion System

> Every landing page is an experiment under the brand voice. Iteration is welcomed; brand drift is not.

## 1. Page roles

| Role | Path |
|---|---|
| Hero / index | `/` |
| Diagnostic CTA | `/diagnostic` |
| Pricing transparency | `/pricing` |
| Trust Center | `/trust-center` |
| Founder POV | `/founder` |
| Compare frames (per category) | `/compare-*` |

## 2. Page anatomy

1. Eyebrow (category line)
2. Hero title (brand line / promise line)
3. Subline (operating line)
4. Hero CTA primary (Open the Console, Get the Diagnostic)
5. Hero CTA secondary (See how it works)
6. Proof strip (consented logos / outcomes only)
7. Why-now section
8. How-it-works section
9. Trust section
10. Pricing transparency
11. CTA repeat

## 3. Experiments

- Run one experiment at a time per page.
- Document hypothesis, metric, duration in `marketing/experiments.csv`.
- Brand Guardian validates every variant.
- No paid traffic experiments without founder approval.

## 4. Metrics

- Time to first scroll
- CTA click rate
- Form completion rate
- Booked-call rate
- Diagnostic-request rate

## 5. Forbidden

- Pop-ups, exit-intent modals, dark-pattern asks.
- Counters, urgency timers, scarcity flags.
- Auto-playing video with sound.
- Inflated metrics on the proof strip.
