# Cold Email Compliance Gate — بوّابة امتثال البريد البارد

Every draft passes six gates before it can be sent. If any gate fails, the
draft is **not sent**. Code:
[`../../dealix/market_production_os/compliance_gate.py`](../../dealix/market_production_os/compliance_gate.py).
The banned-term lists mirror the canonical
`auto_client_acquisition/governance_os/draft_gate.py` and extend it for cold
email. References: Google Email sender guidelines and the US CAN-SPAM Act.

## The six gates — البوّابات الست

```
Brand Voice Gate     → no guarantees, no hype, no forbidden channel terms
Offer Match Gate     → offer ∈ canonical catalog
Personalization Gate → ≥ P1 for cold (warm exempt)
Compliance Gate      → opt-out present · honest subject · accurate sender · not suppressed
Deliverability Gate  → domain health OK + within ramp cap (account layer)
Founder Approval Gate→ explicit approve before any send
```

`check_draft(draft, suppressed_hashes=..., recipient_email_sha256=...)` returns
`allowed`, the list of `failures`, and a per-gate pass map.

## What is blocked — ما يُمنع

| Category | Examples |
|---|---|
| Guaranteed outcomes | "نضمن لك مبيعات" · "we guarantee ROI" · "guaranteed results" |
| Forbidden channels/terms | "cold whatsapp" · "linkedin automation" · "scraping" · "purchased list" · "auto send without approval" |
| Hype | "10x" · "supercharge" · "revolutionary" · "disrupting" · "transform your business" |
| Misleading subject | a cold subject starting with `Re:` / `Fwd:` / `Fw:` / `رد:` |
| Spammy subject | `!!!` · `$$$` · "100% free" · "act now" |
| Missing opt-out | no `unsubscribe_included` / `unsubscribe_method = none` |
| Incomplete sender | missing `from_name`, `from_email`, or `physical_address` |
| Suppressed recipient | recipient hash present in the suppression list |
| Below personalization floor | a cold draft below P1 |

## CAN-SPAM + Google essentials — الأساسيات

- **Accurate sender identity:** real `from`, real reply-to, a valid physical
  address. No deceptive headers.
- **Honest subject:** describes the message; never a fake reply/forward.
- **Working opt-out** in every message; honored immediately and always within
  the legal SLA (CAN-SPAM: ≤ 10 business days). See
  [`UNSUBSCRIBE_POLICY_AR.md`](UNSUBSCRIBE_POLICY_AR.md).
- **No purchased lists, no scraping.** Sources are lawful only
  ([`PROSPECT_RESEARCH_OS_AR.md`](PROSPECT_RESEARCH_OS_AR.md)).
- **Spam-complaint rate < 0.3%**, bounce rate < 3% — enforced as ceilings in
  the [sending ramp](SENDING_RAMP_PLAN_AR.md).

## Optional canonical fold-in — الربط بالحوكمة

When the full app stack is importable, the gate also folds in
`governance_os.policy_check_draft`. When it is not (lightweight runtime), the
self-contained checks above fully enforce the rules.

Tests: [`../../tests/test_no_cold_email_without_optout.py`](../../tests/test_no_cold_email_without_optout.py) ·
[`../../tests/test_market_production_os.py`](../../tests/test_market_production_os.py).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
