# Dealix Free Agent Stack Integration

## Source integrated

External reference:

- `Moh4696/build-ai-agents-free`
- Pattern: free/free-tier agent setup using a model, tools, memory, and a plan-act-observe loop.

This integration does **not** copy the repo as-is into Dealix. It translates the useful pattern into Dealix-safe infrastructure.

## What we are taking from the source repo

### 1. Model + agent loop

The source repo shows a minimal agent created with `langchain.agents.create_agent` and a Groq-hosted model. The important Dealix lesson is not the exact model, but the loop:

```txt
user task
→ model reasons
→ tool call if needed
→ observe result
→ continue until answer/draft is ready
```

### 2. Tools as explicit capabilities

The source repo turns a Python function into a callable tool. Dealix should use the same concept, but only for approved internal capabilities:

- company brain lookup
- opportunity scoring
- draft generation
- approval queue write
- proof log write
- safe research draft

Dealix must not expose live send/publish/payment/deploy/merge tools to the free agent loop.

### 3. Memory/thread IDs

The source repo uses a checkpointer and `thread_id` to keep conversation memory. Dealix maps this to:

- `client_workspace` memory for client-specific context
- `founder_only` memory for sensitive Dealix context
- approval/proof memory for auditability

### 4. Free-tier caveat

The source repo explicitly warns that free tiers change and that sensitive prompts should not be sent to them. Dealix adopts this as a hard policy:

- founder-only data never goes to free cloud tiers
- customer-internal data should prefer local/private endpoints
- public/aggregated research can use free tiers when rate limits and caveats are acceptable
- low-confidence outputs route to human approval

## Where this fits inside Dealix

Dealix already has a safer model-router direction:

```txt
local/private first
→ confidence scoring
→ cloud fallback only if privacy allows
→ degraded_to_human when unsafe or unavailable
```

The free agent stack adapter sits above that router and below the Company OS runners:

```txt
Dealix Company OS runners
→ free_agent_stack adapter
→ existing model router / local model / allowed free tier
→ safe tools
→ approval queue
→ proof ledger
```

## New files added

```txt
dealix/free_agent_stack/__init__.py
dealix/free_agent_stack/adapter.py
scripts/commercial/verify_free_agent_stack.py
docs/commercial/FREE_AGENT_STACK_INTEGRATION.md
```

## Default profile

The default profile is `dealix_free_agent_stack_adapter`.

Preferred model order:

```txt
1. existing_dealix_local_router
2. ollama_or_vllm_private_endpoint
3. groq_free_tier_for_public_non_sensitive_tasks
4. gemini_free_tier_for_public_non_sensitive_long_context_tasks
5. human_handoff
```

## Tool manifest

| Tool | Purpose | Max autonomy | Approval |
|---|---|---:|---:|
| `company_brain_lookup` | Read offers, personas, restrictions, tone | L1 | No |
| `opportunity_score_preview` | Score allowed/provided prospects | L2 | No |
| `outreach_draft_builder` | Create draft-only outbound scripts | L2 | Yes |
| `approval_queue_writer` | Move risky actions to approval | L3 | No |
| `proof_log_writer` | Record evidence and caveats | L3 | No |
| `free_web_research_draft` | Public non-sensitive research drafts | L2 | No |

## Hard blocks

The adapter blocks these as non-negotiable defaults:

- live outbound
- cold WhatsApp blast
- mass LinkedIn automation
- auto-posting
- payment capture
- production mutation
- public LLM endpoint
- hardcoded secret
- fake proof
- guaranteed revenue claim
- government access claim

## How Dealix uses it for maximum benefit

### P0 — Cost and speed

Use free/local-first agents for cheap internal work:

- classify opportunities
- summarize allowed public research
- draft first-pass messages
- write approval notes
- generate proof-log summaries
- create content outlines

### P1 — Company OS execution

Map the agent loop to Dealix daily operating outputs:

```txt
plan: choose safest money-now or trust-building action
act: load Company Brain + score opportunities + draft messages
observe: write approval queue + proof log + learning note
```

### P2 — Revenue Command

Use it for draft-only daily revenue work:

- top 10 prospects
- reason for targeting
- offer match
- first message draft
- follow-up draft
- objection handling notes
- approval item

### P3 — Saudi Market Access

Use it for public, non-sensitive research:

- segment scan
- company category notes
- Saudi expansion signals
- partner/distributor hypothesis
- B2G readiness caveats

### P4 — Self-improvement

Use it to review results safely:

- rejected drafts
- no replies
- weak CTAs
- poor target fit
- repeated objections
- data-quality issues

## What is intentionally not enabled

This PR does not:

- install LangChain/Groq as mandatory dependencies
- add a live Groq API call
- send emails or WhatsApp messages
- post content
- create payment capture
- modify production
- merge PRs
- expose local models publicly

## Verification

Run:

```bash
python scripts/commercial/verify_free_agent_stack.py
```

Expected:

```txt
free_agent_stack verification passed
```

## Next integration steps

1. Wire `dealix.free_agent_stack.run_plan_act_observe_preview()` into the existing daily Company OS report.
2. Use the adapter's tool manifest in the Approval Center UI/API.
3. Add an optional `[agents-free]` dependency group later if we decide to run LangChain/Groq in development mode.
4. Keep production on the existing model router until the free-tier path has tests, rate-limit handling, and privacy gates.
