# Objections Log — Public Schema

> The handler. Private log lives in `dealix-ops-private/sales/objections_log.md`.

## Standard Objections

### "We need to think."

**Response:**
"Tamam. Specifically, is it scope, price, or timing? Whichever it is,
I can address it now or we can schedule a 15-minute follow-up next week."

### "Do you guarantee revenue / leads?"

**Response:**
"No. We do not guarantee revenue or leads. We guarantee delivery of the
scope — qualified accounts, outreach pack, executive memo — at the
quality our case studies show. I can share the most recent Proof Pack if
that helps."

### "It is expensive."

**Response:**
"Compared to what? Internal hire? Outsourced SDR agency? Self-serve
tooling? Each has different trade-offs. For our Sprint price, you get
2 weeks of founder-led work that would take an internal team 6–8 weeks.
If the budget is tight, we can scope down to fewer accounts at a lower
price — we do not lower quality."

### "Send us a deck."

**Response:**
"We do not have a deck. We have samples. Let me build you a Signal
Sample — 3 accounts in your sector with our research style applied.
That will tell you more than a deck."

### "We do not need outbound; we get inbound."

**Response:**
"Great. Then this is the wrong fit today. If your inbound dips or you
want to expand into an adjacent segment, we are here."

### "We already work with [competitor]."

**Response:**
"How is that going? If it is working, keep going. If there is a
specific gap — Saudi-native context, evidence per claim, founder-level
trust — that is where we tend to win. Otherwise, no need to switch."

## Logging Format

In private:

```
- date: yyyy-mm-dd
- prospect: name
- objection (verbatim): "..."
- response_used: short
- outcome: closed / lost / pending
- pattern_tag: price / guarantee / fit / timing / process / trust
```

## Pattern Review

Monthly: cluster objections by pattern_tag.
- Pattern that repeats > 3 times in a month becomes a sales-collateral
  update.
- Pattern that repeats in 3 consecutive months becomes a strategy
  question (ICP fit? Pricing?).
