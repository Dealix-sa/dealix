# 04 — Founder Daily Sales Cadence — الإيقاع اليومي للمؤسس

> A concrete daily operating rhythm so the founder runs the sales motion without
> improvising. About 2.5 focused hours of sales work per day. Everything is draft-only
> and founder-approved — there is no autonomous sending.

---

## 1. The daily blocks — كتل اليوم

| Block | Time (suggested) | Duration | What happens |
|-------|------------------|----------|--------------|
| **A. Pipeline review** | 08:30 | 15 min | Read the tracker top to bottom. Decide today's one priority. |
| **B. Outreach-draft approval** | 08:45 | 30 min | Personalize and self-approve up to 5 warm drafts (file 01). Send manually. |
| **C. Follow-ups** | 09:15 | 15 min | Handle replies from prior days per the reply table. No "circling back." |
| **D. Discovery calls** | 11:00–13:00 | 2 × 30 min | Up to two booked calls. Run the script in file 02, fill the scorecard inline. |
| **E. Qualify & propose** | 14:00 | 30 min | Run `qualify(...)` for each call. Render proposals for ACCEPT/DIAGNOSTIC_ONLY. |
| **F. Daily wrap** | 16:30 | 10 min | One-paragraph wrap in `friction_log`. Update the tracker. |

Total focused sales time: about 2 hours 30 minutes. The rest of the day is delivery work
(diagnostics, sprints, Proof Packs).

---

## 2. Block A — Pipeline review (15 min)

Walk the pipeline stages and count what is in each:

| Stage | Definition |
|-------|------------|
| Warm leads | Contacts identified, draft not yet sent. |
| Outreach sent | Draft sent manually, awaiting reply. |
| Discovery booked | A 30-minute call is on the calendar. |
| Qualified | `qualify(...)` has returned a decision. |
| Diagnostic in progress | Free diagnostic intake submitted, 24h clock running. |
| Proposal out | A Tier 1/2/3 proposal has been sent. |
| Paid | First (50%) invoice cleared via Moyasar. |

Pick the **single most important action** for today and write it at the top of the
tracker. One priority — not a list.

---

## 3. Block B — Outreach-draft approval (30 min)

- Take up to 5 warm contacts from your real list. **Never more than 5/day** (file 01).
- Personalize one draft per contact using the framework slots. Fill every anchor with
  something true — if you cannot, drop the contact from today.
- Read each draft as if you were the recipient. Approve it yourself.
- Send manually, on the channel the relationship already uses.
- Log each at send time: channel, language, timestamp, relationship_basis.

**Refuse:** no automation, no bulk send, no scraped or purchased contacts, no LinkedIn
automation. If the urge to "just blast it" appears, that is the signal to stop.

---

## 4. Block C — Follow-ups (15 min)

| Situation | Action |
|-----------|--------|
| Reply: interested | Reply within 24h (not sooner than 1h). Offer intake link or a call. |
| Reply: asks detail | One short reply, up to two links, no attachment. |
| Reply: not interested | Thank, log, never push. Offer the no-automation radar. |
| Sent 7+ days ago, silent | Leave alone. Re-engage only on a natural occasion. |
| Proposal sent 3+ days ago | One gentle, non-pressuring check-in. Then wait. |

---

## 5. Block D — Discovery calls (2 × 30 min)

- Two call slots per day, fixed at 11:00 and 11:45 (or your preference). Never more than
  3 in a day — quality over volume.
- Run the five-section script (file 02). Fill the qualification scorecard inline.
- No deck on a discovery call. No price negotiation in the call beyond stating the fixed
  499 / 1,500 figures.

---

## 6. Block E — Qualify & propose (30 min)

For each call held today:
1. Run `qualify(...)` with the eight flags and the verbatim request text.
2. Act on the decision:
   - **ACCEPT** → render the 499 Sprint proposal (Template B).
   - **DIAGNOSTIC_ONLY** → send the free diagnostic intake link.
   - **REFRAME** → send a 3-line reframe, plan a re-qualify.
   - **REJECT** → polite refusal, cite the constitution, log in `friction_log`.
   - **REFER_OUT** → make the partner intro, log in `referral_ledger`.
3. **Before sending any real proposal**, confirm Moyasar is in live mode. If
   `launch-status` says `moyasar.mode == "test"`, run
   `python scripts/moyasar_live_cutover.py` first.
4. All proposals are drafts for your own final review before they leave your hands.

---

## 7. Block F — Daily wrap (10 min)

Write one paragraph in `friction_log`:
- Messages sent, replies received, replies converted to calls.
- The single biggest objection of the day — verbatim, anonymized.
- One change to the script or offer for tomorrow, or "no change" with a reason.

Update the tracker counts. Two minutes of writing compounds into your first sector
pattern asset by the end of week one.

---

## 8. Weekly rhythm — الإيقاع الأسبوعي

| Day | Sales focus |
|-----|-------------|
| Sun–Wed | Full cadence: outreach, calls, proposals, delivery. |
| Thu | Cadence + a 30-min weekly review: pipeline math, conversion rates, what to change. |
| Fri–Sat | Light touch only — reply to inbound, no new outreach. Rest protects the motion. |

**Weekly review questions:** How many warm drafts sent vs. replies vs. calls vs.
proposals vs. paid? Where is the biggest drop-off? What one change do I test next week?

---

## 9. Guardrails — حواجز الأمان

- Maximum 5 new outreach drafts per day. Contact 21+ in week one needs a fresh approval.
- Maximum 3 discovery calls per day.
- Never send anything Dealix drafted without reading and approving it yourself.
- Never automate a send. Never use a scraped or purchased list.
- Never promise an outcome. State methodology metrics only.
- If a request needs a non-negotiable violation, refuse cleanly and offer the safe
  alternative.

---

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
