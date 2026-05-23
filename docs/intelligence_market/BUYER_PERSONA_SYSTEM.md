# Buyer Persona System

## 1. Persona card shape

Each persona ships as a single artifact with the following sections:

1. Name and role.
2. Three jobs they're hired to do.
3. Three pains that block those jobs.
4. Three gains they'd unlock by removing the pains.
5. Allowed channels (warm intro, LinkedIn, email, contact form, event).
6. Off-limits channels and topics.
7. Vocabulary they use (and the vocabulary they reject).
8. Two trigger events that suggest now is the right moment.
9. Their typical objections and the truthful answer.

## 2. Persona library (Saudi B2B)

- `P-FOUNDER-SCALE` — founder of a 20–200 person Saudi B2B company.
- `P-CRO-MID` — head of revenue at a 100–500 person company.
- `P-COO-ENT` — COO of a regulated enterprise.
- `P-HEAD-OPS-AGENCY` — operations lead at a Saudi B2B agency.
- `P-HEAD-GROWTH-SAAS` — growth lead at a Saudi SaaS company.

Each persona has a card under `data/private_ops_seed/growth/`
(seeded externally; never checked into git for live customer data).

## 3. Persona output

`growth/personas.csv` with columns:

```
persona_id,segment_id,name,role,size_band,allowed_channels,
off_limits_topics,vocab_uses,vocab_rejects,top_pains,
top_gains,sample_lines,collected_at,source
```

## 4. Guardrails

- A persona never contains a real person's identity in this repo;
  only role-based archetypes.
- All persona-driven outbound is **draft-only** and queued.
- Off-limits topics are honoured by the brand_guardian agent.
