# Delivery Acceptance Criteria

> متى نعتبر التسليم مكتملًا — بدون ادعاءات بلا دليل.

A Command Sprint (or any offer) delivery is **done** only when all criteria pass.

---

## Per-engagement checklist

- [ ] `customers/{slug}/` exists with all 11 canonical files.
- [ ] Every file has complete governance front-matter.
- [ ] `00_intake.md` records company, sector, offer, weakness→OS, paid date.
- [ ] `03_…_scope.md` lists the offer deliverables and they are all addressed.
- [ ] `04_revenue_map.md` identifies opportunities + leakage with evidence.
- [ ] `05_proof_register.md` maps every claim to evidence.
- [ ] `07_executive_command_brief.md` is a single reviewable page.
- [ ] `06_next_action_board.md` has who / what / when for each action.
- [ ] `08_delivery_log.md` records each delivery step + artifact.
- [ ] `09_proof_pack.md` reaches **at least L2/L3**.
- [ ] `10_upsell_recommendation.md` states a clear upsell/renewal decision.

---

## Quality gates

- **No unsupported claim.** Every claim in the proof register has evidence.
- **No overclaim.** Recommendations carry a confidence level.
- **Reviewable.** The exec brief fits one page; the client can act from it.
- **Governed.** Sensitive content has the required approvals.

---

## System-level acceptance

The OS is considered strong when:

- **Research:** 300–400 raw/day, deduped, non-compliant sources rejected.
- **Scoring:** every company scored, every score reasoned, every target evidenced.
- **Drafting:** every draft tailored, evidence-based, founder-approved, no auto-send.
- **Delivery:** every paid target → customer folder → delivery plan → proof pack.
- **Learning:** every reply/reject/diagnostic/sale logged → next targeting plan.

Verified by:

```bash
python -m pytest tests/test_targeting_scorecard.py \
  tests/test_targeting_compliance_gate.py \
  tests/test_targeting_delivery_handoff.py \
  tests/test_targeting_pipeline.py -q
```
