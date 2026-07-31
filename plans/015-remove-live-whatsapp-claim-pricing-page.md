# 015 — Remove the public live-WhatsApp-send claim from landing/pricing.html

- **Finding:** `landing/pricing.html:260` publicly states, in a FAQ
  answer visible to any visitor:
    ```html
    <details><summary>هل يدعم WhatsApp Business API؟</summary><p>نعم في Starter+. نستخدم رقمك الرسمي عبر مزوّد معتمد.</p></details>
    ```
  ("Does it support the WhatsApp Business API? Yes, in Starter+. We use
  your official number through an approved provider.") This is a public
  promise of live WhatsApp Business API integration — sending/receiving
  through the customer's own official number — for a self-serve tier
  ("Starter+") a visitor can sign up for directly via the page's checkout
  flow. This directly contradicts the repo-wide outbound-safety default
  (`WHATSAPP_SEND_ENABLED=false`, `WHATSAPP_ALLOW_LIVE_SEND=false`,
  `OUTBOUND_MODE=draft_only` — `CLAUDE.md` "Outbound Safety Policy —
  NON-NEGOTIABLE") and the comparison table row at `landing/pricing.html:243`
  ("WhatsApp + Email + Form" marked ✓ for Starter/Growth/Scale) reinforces
  the same claim. A prospective customer reading this page today would
  reasonably expect live WhatsApp sending on signup — a promise the
  product's actual default configuration cannot deliver without a
  separate, currently-nonexistent "controlled-live approval PR"
  (per `CLAUDE.md`'s "Outbound Safety Policy"). This is the single
  highest-severity finding in this reconciliation pass: a live public page
  contradicting a named safety non-negotiable, not just a stale number.
- **Category:** doctrine / safety
- **Wave:** maintenance
- **Effort:** S   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read landing/pricing.html before editing
```

## Context (inlined)
- File in scope: `landing/pricing.html` — this is the static marketing
  site (`landing/`), a **separate codebase from the Next.js `apps/web/`**.
  Do not confuse the two or look for this file under `apps/web/`.
- This plan makes the smallest change that removes the safety-contradicting
  claim: the FAQ answer and the comparison-table cell. It does **not**
  attempt the full page reconciliation to the 2-offer registry model
  (self-serve tiers, checkout flow, Moyasar-invoicing claims) — that is
  plan 018's broader scope. Land this plan first since it's the isolated,
  highest-severity fix; 018 reworks the same file afterward.
- Current state, `landing/pricing.html:260`:
    ```html
    <details><summary>هل يدعم WhatsApp Business API؟</summary><p>نعم في Starter+. نستخدم رقمك الرسمي عبر مزوّد معتمد.</p></details>
    ```
- Current state, `landing/pricing.html:243` (comparison table row):
    ```html
    <tr><td style="padding:10px;border-bottom:1px dashed #e2e8f0;font-weight:600">WhatsApp + Email + Form</td><td style="text-align:center">WhatsApp فقط</td><td style="text-align:center">✓</td><td style="text-align:center;background:#fefce8">✓</td><td style="text-align:center">✓</td></tr>
    ```

## Steps
1. Replace the FAQ answer at `landing/pricing.html:260` with accurate,
   doctrine-compliant language that doesn't promise live sending, e.g.:
    ```html
    <details><summary>هل يدعم WhatsApp Business API؟</summary><p>حالياً نجهّز الردود والمسودات لمراجعتك واعتمادك — الإرسال الفعلي عبر رقمك الرسمي يتطلب موافقة صريحة منفصلة قبل التفعيل.</p></details>
    ```
   (Approximate English sense: "Currently we prepare drafts/replies for
   your review and approval — actual sending via your official number
   requires separate explicit approval before activation.")
   **Gate:** `grep -n "نستخدم رقمك الرسمي عبر مزوّد معتمد" landing/pricing.html` → no output.
2. Fix the comparison-table row at `landing/pricing.html:243` so it
   doesn't imply live channel sending is bundled at every tier — change
   the row label/cells to reflect draft-and-approve behavior (e.g.
   "WhatsApp + Email + Form (مسودات للمراجعة)" / "drafts for review") or,
   if this row's other channels (Email/Form) genuinely are live today,
   split WhatsApp into its own row so it isn't bundled with claims that
   may be accurate for the other channels. Verify what Email/Form actually
   do before deciding — do not assume; check
   `grep -rn "EMAIL_SEND_ENABLED" core/config/settings.py` for the current
   default (should also be `false` per CLAUDE.md, meaning Email likely
   needs the same correction).
   **Gate:** `grep -n "WhatsApp" landing/pricing.html` → no line implies unconditional live sending.
3. Search the rest of `landing/` for the same claim pattern in case it's
   duplicated on another page (e.g. `landing/systems-catalog.html`,
   `landing/services.html`, `landing/index.html`):
   `grep -rln "رقمك الرسمي عبر مزوّد معتمد\|WhatsApp Business API" landing/*.html`
   For any other hit, apply the same correction — do not leave the claim
   live on one page while fixing it on another.
   **Gate:** command output reviewed; all hits corrected or confirmed
   already-compliant.

## Done criteria (machine-checkable)
- [ ] `grep -rn "نستخدم رقمك الرسمي عبر مزوّد معتمد" landing/*.html` → no output
- [ ] `python3 scripts/verify_no_auto_external_send.py` → `NO_AUTO_EXTERNAL_SEND_GATE=PASS`
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not rework the self-serve tier structure, checkout flow, or pricing
  numbers on this page — that's plan 018.
- Do not touch `apps/web/` — it's a separate frontend, not in scope here.
- Do not flip any `*_SEND_ENABLED` env var — this plan only fixes public
  copy to match the existing (correct) default, it does not change backend
  behavior.

## STOP conditions
- If `landing/pricing.html:243,260` no longer match the excerpts above →
  STOP, re-run drift check; the page may have already been corrected.
- If Email/Form sending turns out to already be live in production
  (contradicting the expected `EMAIL_SEND_ENABLED=false` default) → STOP
  and report as a separate, higher-severity finding rather than silently
  reconciling the copy to match an unexpected live-send configuration.
