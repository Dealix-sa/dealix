# Custom Systems OS — bespoke per-client design + structure + internal systems

> Governed top-rung capability. Custom design identity + custom architecture +
> a complete bilingual internal-system spec — under the same 11 non-negotiables.

## What it is

`auto_client_acquisition/custom_systems_os/` turns a client company profile into
three governed artifacts:

1. **Custom design profile** — per-client design tokens/theme that override Dealix
   defaults (`designops/design_system_loader` + a locked `visual_directions`
   bundle), inheriting the Dealix forbidden-copy guard.
2. **Custom structure blueprint** — modules, data model, workflows, and the 11
   governance gates baked in by construction.
3. **Complete bilingual internal-system specification** (AR primary + EN) — the
   "كامل وشامل" deliverable, exported as markdown / html / json.

Everything flows through the existing machinery: **Source Passport** gate →
**governance** decision (`governance_os.decide` + `claim_safety`) → **safety gate**
(`designops.safety_gate`) → local **export** (PDF deferred) → **Proof Pack** (14
sections) → **Capital Assets** (≥ 1) → **retainer readiness** (`adoption_os`).

## Governance (no non-negotiable is broken)

- **Entry gate (coded):** `custom_systems_os/entry_gate.py` blocks any build until
  **≥ 3 paid pilots** are completed and a workflow owner is named — the doctrine
  "no customization before 3 paid pilots" rule, enforced in code, not docs.
- **Founder-assisted delivery:** every result carries `delivery_mode =
  "founder_assisted"`, `safe_to_send = False`, and `approval_required = True`.
  Nothing is ever sent externally.
- **Source Passport required** before any AI/build step.
- **Guaranteed-outcome claims** are blocked by governance and cap the proof score.
- **≥ 1 Capital Asset** and a complete 14-section Proof Pack per engagement.

## Surfaces

| Surface | Where |
|---|---|
| Core package | `auto_client_acquisition/custom_systems_os/` |
| Orchestrator | `custom_systems_os/engagement_runner.run_custom_system_engagement(...)` |
| API | `GET /api/v1/custom-systems/health` · `POST /entry-check` · `POST /run` · `GET /engagements/{customer_id}` |
| CLI | `python scripts/dealix_custom_system.py --demo` |
| Proposal | `templates/PROPOSAL_CUSTOM_SYSTEM.md.j2` |
| Ledger | JSONL via `DEALIX_CUSTOM_SYSTEMS_PATH` (default `var/custom-systems-os.jsonl`) |
| Offer rung | `docs/OFFER_LADDER_AND_PRICING.md` (Rung 6) · `docs/COMPANY_SERVICE_LADDER.md` (Rung 5) |
| Tests | `tests/test_custom_systems_os.py` · `tests/test_custom_systems_router.py` · `tests/test_custom_systems_entry_gate.py` |

## Quick start

```bash
python scripts/dealix_custom_system.py --demo
# -> next_step: deliver_for_founder_review · proof 100 · 3 capital assets · safe_to_send: false
```

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
