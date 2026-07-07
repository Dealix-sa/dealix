# improve Skill — Technical, Strategic & Commercial Integration

Integration of `shadcn/improve` (MIT © shadcn) into Dealix as a native agent
skill. Origin credited; adapted to Dealix gates, doctrine, and the offer ladder.

> Source skill: https://github.com/shadcn/improve — *"Use your most capable model
> to audit a codebase and write plans for cheaper models to execute."*

---

## ملخص تنفيذي (AR)

`improve` مهارة وكيل تدقّق الكود بأقوى موديل (Opus) وتكتب خطط تنفيذ قابلة للتسليم
لموديل أرخص (أو لبشري) — **بدون تعديل الكود نفسها؛ المخرَج هو الخطة**. دمجناها في
Dealix وربطناها بـ:
- بوابات الاختبار الحقيقية (`make full-repo-test` و `apps/web verify` وفحص الأمان).
- الـ11 خط أحمر (منع الإرسال التلقائي، حارس الأسرار في الإنتاج، منع الادعاءات المضمونة).
- سلّم العروض: نفس محرك «تدقيق → خطة → تنفيذ» هو آلية تسليم **التشخيص المجاني** و
  **Transformation Diagnostic Sprint (7,500–25,000 ريال)**.
- «رادار مزوّدي الذكاء المجاني» الموجود أصلاً — فالمنفّذ الرخيص يختار موديلاً من
  الطبقة المجانية، فيبقى هامش الربح مرتفعاً (مستشار غالٍ + منفّذ رخيص).

---

## 1. Technical integration (what shipped)

| Path | Purpose |
|------|---------|
| `.claude/skills/improve/SKILL.md` | The Dealix-native audit → vet → prioritize → plan → execute → reconcile loop |
| `.claude/skills/improve/references/dealix-gates.md` | The **real** verification commands + protected safety surfaces |
| `.claude/skills/improve/references/plan-template.md` | Executable plan format: self-contained, gated, STOP conditions |
| `.claude/agents/improve-executor.md` | The cheap-model executor persona: implements one plan in a worktree, runs its gates/STOP conditions, never merges |
| `plans/` | Committed backlog of executable specs — seeded by the first real audit (`INDEX.md` + 3 vetted plans) |
| `scripts/ops/check_provider_registry_freshness.py` | Freshness guard so `execute` never dispatches to a stale free tier (`make ai-provider-registry-check`) |
| `tests/test_provider_registry_freshness.py` | 7 tests pinning the guard |
| `sales/DIAGNOSTIC_REPORT_TEMPLATE_AR.md` | Bilingual customer deliverable produced from an `improve` run (Free Diagnostic / Sprint) |
| `.gitignore` | Fix: `.claude/*` so subdir whitelists work; tracks `.claude/skills/` |

### The loop, run end-to-end (this PR is the worked example)
The first audit against commit `2ec6a6c` produced `plans/INDEX.md` with three
vetted findings and two recorded rejections (see the "Rejected findings" block —
the `!scripts/lib/` gitignore negation looked like a bug but was verified
by-design). Plan **002** was then executed for real: a provider-registry
freshness guard + 7 passing tests + a `make` target — closing audit → plan →
execute → verify inside one PR.

**Wiring that makes it Dealix-native, not a generic drop-in:**
- Every plan's done-criteria are Dealix gates (`make full-repo-test`,
  `npm --prefix apps/web run verify`, `security_smoke_ci.py`,
  `verify_no_auto_external_send.py`) — never invented commands.
- A dedicated **doctrine & safety** audit category flags anything that would
  weaken the outbound contract, the production secret guard, or a doctrine guard
  test — and the skill's hard rules forbid it from ever *authoring* such a change.
- `direction` suggestions are grounded in the **Wave roadmap** and cite repo
  evidence — no idea-slop, no live-outbound proposals.
- `execute` selects a cheap executor via the existing provider radar and runs it
  in a disposable worktree; **merging stays a founder approval gate**.

### Why this fits Dealix doctrine perfectly
The source skill's hard rules (*never edits source, never mutates the tree,
never reproduces secrets, merging is yours*) are a near-exact match for Dealix's
approval gates and draft-only posture. `improve` is, in effect, a doctrine-shaped
tool: it advises and drafts; the human decides and ships.

---

## 2. Strategic value

**Economics of intelligence.** The compounding value is in *understanding and
judgment*, not typing. `improve` spends the expensive model where it pays off
(recon, vetting, spec-writing) and pushes mechanical execution to cheap models.
This is the same thesis as the "expensive advises / cheap executes" pattern —
and Dealix already owns the cheap-execution half via
`data/ai/free_llm_provider_registry.json` + `scripts/ops/free_llm_provider_radar.py`
(adopted from `cheahjs/free-llm-api-resources`, one of the source references).

```
Opus (advisor)  → plans/001.md  → free-tier executor (via radar) → founder merges
   high $/token       the asset        ~$0/token, in a worktree      approval gate
```

**Compounding backlog.** Plans persist as reviewable markdown. `reconcile` keeps
the backlog honest across sessions (verify DONE, unblock BLOCKED, retire fixed).
The repo accrues a living, prioritized improvement ledger instead of one-off chats.

**Quality flywheel for the launch matrix.** `/improve branch` before every PR
turns the audit into a pre-merge gate that speaks the same language as CI —
fewer red pipelines, tighter Waves.

---

## 3. Commercial value — the audit loop *is* a product

The same audit → plan → (execute) methodology maps directly onto the offer ladder.
For customer engagements it is applied to the **customer's** systems/codebase, in
draft-only mode, with a Proof Pack as the deliverable — never auto-executed.

| Offer | Price | `improve` as delivery engine |
|-------|-------|------------------------------|
| Free Diagnostic | Free | `/improve quick` → a prioritized findings table = the free hook that earns the paid step |
| Micro Sprint | 499 SAR | 2–3 planned findings from a scoped `/improve <category>` |
| Data Pack | 1,500 SAR | `/improve` focused on data/DQ surfaces → evidence-backed report |
| Transformation Diagnostic Sprint | 7,500–25,000 SAR | `/improve deep` → full audit + plan set + INDEX + Proof Pack; optional supervised `execute` |
| Custom Enterprise System | 25,000+ SAR | Recurring `improve` + `reconcile` cadence as a retained operating rhythm |

**Reuse with existing Dealix assets (no new doctrine needed):**
- The `file:line`-evidence + vet discipline mirrors `proof_os`'s evidence rule and
  the **no-fake-data** non-negotiable — findings are grounded, never fabricated.
- Rejections-with-reasons feed the same audit-trail habit as `friction_log`.
- Direction suggestions use hypothesis language ("we expect / the goal is / we
  will measure"), satisfying the commercial-OS claim rules.

**Margin story:** an advisor-hour of Opus produces a plan set that a free-tier
executor implements. High-value judgment is billed; low-value typing is near-zero
cost. That gap is the Diagnostic Sprint's gross margin.

**Full commercial packaging** (so this is sellable, not just a good idea):
- `docs/IMPROVE_COMMERCIAL_PLAYBOOK.md` — funnel, segment fit (be honest — digital
  systems only), margin economics, trust-as-a-selling-point, and what NOT to sell.
- `sales/IMPROVE_DIAGNOSTIC_DELIVERY_SOP_AR.md` — the repeatable delivery runbook:
  each offer rung → exact `improve` command → artifact → the A1→A2 founder-review
  gate → upsell trigger. Plugs into the funnel already in the repo
  (`api/routers/diagnostic.py`, the diagnostic landing pages,
  `customers/_template/02_diagnostic_summary.md`).
- `sales/DIAGNOSTIC_REPORT_TEMPLATE_AR.md` — the customer-facing deliverable.
- `sales/IMPROVE_OFFER_SALES_PAGE_AR.md` — the offer's sales page (draft).
- `sales/IMPROVE_OUTREACH_SEQUENCE_AR.md` — draft-only follow-up cadence.

### Outbound: the full pipeline, up to the human gate (never through it)
`auto_client_acquisition/gtm_os/improve_followup.py` turns vetted findings into
founder-approval outreach cards. It is **draft-only by construction** — there is
no send/dispatch function in the module, every card is stamped
`governance_decision="approval_required"`, `send_status="draft"`,
`dispatchable=False` from birth, recipients are opaque `recipient_ref` handles
(raw email/phone rejected), and guaranteed-outcome claims are blocked. Pinned by
`tests/test_improve_followup_draft_only.py` (8 cases, incl. a structural check
that no send/dispatch/network capability exists). Actual sending stays a founder
action through `approval_center`; enabling live channels still requires a merged
controlled-live approval PR — this code cannot perform either. This is how
"automatic sending" is delivered here: the whole machine is built, the last inch
is a human decision.

---

## 4. The other three references — in/out-of-policy verdict

The shared screenshots included three more tools. Verdicts, so scope stays clean:

| Tool | What it is | Verdict |
|------|-----------|---------|
| **cheahjs/free-llm-api-resources** | List of free LLM API tiers | ✅ **Already adopted** as `data/ai/free_llm_provider_registry.json` + provider radar. `improve execute` now consumes it to pick cheap executors. Keep the registry's review date current. |
| **Taste Skill** (tasteskill.dev) | Paid, closed-source "anti-slop" frontend framework for AI agents | ⚠️ **Cannot integrate** (closed/paid). Adopt the *principle* only: an `apps/web` design-quality checklist as a future `/improve` plan for the frontend. No dependency, no code. |
| **Fastlane** ("Claude for Social Media") | Auto-generates and posts thousands of social videos in one click | ⛔ **Out of policy.** Auto-posting violates the outbound-safety contract (`OUTBOUND_MODE=draft_only`, no auto-send) and the no-cold-outbound rule. **Do not integrate.** Content generation is allowed only as founder-reviewed *drafts*. |

---

## 5. Try it

```
/improve quick        # cheap first pass — safe, read-only, writes only to plans/
/improve branch       # pre-PR audit of the current branch
/improve next         # feature direction grounded in the Wave roadmap
```

Read `.claude/skills/improve/SKILL.md` for the full command set and hard rules.
Nothing here sends an external message, mutates the working tree, or weakens a
guard — the skill's only writes are to `plans/`.
