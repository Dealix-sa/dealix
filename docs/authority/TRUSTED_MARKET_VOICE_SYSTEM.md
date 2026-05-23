# Trusted Market Voice System

> The compound effect: when authority posts + sector reports + sector
> one-pagers + objection responses are aligned, Dealix becomes the
> *voice* of the beachhead sector. This file describes how to keep
> that voice coherent.

## The four voices that must agree

1. **Founder posts** (`founder_posts.csv`).
2. **Sector reports** (`report_ideas.csv`).
3. **Sector one-pagers** (`assets/sales/one_pagers/`).
4. **Objection responses** (`assets/sales/objections/`).

The Conversion Command Room flags when these contradict each other.

## Coherence rules

- The sector thesis in `MARKET_LEARNING_MEMORY.md` is the canonical
  one-paragraph version of the voice.
- No outward-facing artifact can contradict the canonical thesis.
- When the thesis changes (every 90 days), all four voices update.

## Anti-patterns

- Saying "Saudi SMEs need X" in posts but "Saudi enterprises need X"
  in one-pagers.
- Citing a study in a report but a different one in a post.
- "We help everyone" — the voice always specifies the beachhead.

## Verifier check

`scripts/verify_market_attack_system.py` warns when:

- The latest founder posts reference a sector outside the locked
  beachhead.
- The latest sector report references different evidence than the
  most recent insights for that sector.
