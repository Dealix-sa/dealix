# Dealix Agent Output Contract — عقد مخرجات الوكلاء

Every Dealix agent ends its work with this contract. The point is **high signal,
low waste**: no long output without a decision, an impact, and a next action. Keep
it short — this is a footer, not an essay.

Read with [`AGENT_TEAM_REGISTRY.md`](AGENT_TEAM_REGISTRY.md) and
[`AGENT_PERMISSION_MATRIX.md`](AGENT_PERMISSION_MATRIX.md).

---

## The 8 fields

### 1. Decision summary
- What changed?
- Why does it matter?
- What should the founder do next?

### 2. Business impact
Pick exactly one: **Revenue · Conversion · Delivery · Compliance · Security ·
Product readiness · Founder clarity · Cost reduction.**

### 3. Evidence level
Use the Dealix evidence ladder (`GET /api/v1/decision-passport/evidence-levels`):

| Level | Meaning | External use |
|---|---|---|
| L0 | Assumption | never |
| L1 | Repo file / definition | internal |
| L2 | Test / script output | internal |
| L3 | Staging / production signal | internal |
| L4 | Customer / prospect data (`source_ref`) | with approval |
| L5 | Paid / revenue evidence (signed) | case-study eligible |

This mirrors the Value Ledger tiers (`estimated → observed → verified →
client_confirmed`). Never auto-promote a tier; never claim above what you can cite.

### 4. Files touched
List exact paths. "None" if read-only.

### 5. Verification
The exact command(s) run or recommended — e.g. `make doctor`, `make prod-verify`,
`bash scripts/revenue_os_master_verify.sh`, `python scripts/audit_agent_team.py`.
State pass/fail honestly. If a check was skipped, say so.

### 6. Risk
`low` · `medium` · `high`. If the task needed a permission level above the agent's
default (see the matrix), say which level and that a human granted it.

### 7. Rollback
How to revert — branch/commit to drop, file to restore, flag to flip back.

### 8. Next action
Exactly one practical next action. Not a list.

---

## Copy-paste template

```text
**Decision:** <what changed / why / what next>
**Impact:** <Revenue|Conversion|Delivery|Compliance|Security|Product readiness|Founder clarity|Cost reduction>
**Evidence:** L<0–5> — <cite the file/test/source>
**Files:** <paths or None>
**Verification:** <commands + pass/fail>
**Risk:** <low|medium|high>
**Rollback:** <how to revert>
**Next:** <one action>
```

> If the work would violate a [non-negotiable](AGENT_TEAM_REGISTRY.md#the-11-non-negotiables-enforced-in-code-by-passing-tests),
> the only valid output is a clean refusal + a safe alternative.
