# Research Source Policy

> سياسة المصادر: نبحث باحترام، ونرفض أي مصدر فيه مخاطرة.

This policy governs where the Dealix Intelligence-to-Revenue-to-Delivery OS is
allowed to collect company information. It is enforced in code by
`scripts/targeting_compliance_gate.py` and `data/targeting/blocked_sources.yml`.

---

## Allowed sources

- Official company websites (home, services, clients, case studies, careers).
- Company press / news pages.
- Public business directories and chambers of commerce.
- Events and exhibitions.
- Open Data portals.
- Public search results that point to the above.
- LinkedIn **viewed manually** — to read a public company page only.

## Disallowed sources (hard reject)

- Anything **behind a login** (Sales Navigator, gated portals).
- Pages obtained by **ignoring `robots.txt`** or violating source terms.
- **CAPTCHA bypass** of any kind.
- **Leaked datasets** / paste dumps.
- **Purchased personal contact lists**.
- **Personal phone numbers** or personal-email-only contacts as the channel.

See [ROBOTS_AND_TERMS_POLICY.md](ROBOTS_AND_TERMS_POLICY.md).

---

## Evidence floor

A company needs at least `minimum_evidence_count` (default **2**) independent
sources to enter the scored pool. Single-source companies are penalised; zero
official channel → reject.

---

## Sensitive sectors

`healthcare`, `finance`, `government` are **not auto-rejected** but are held as
`review_required` until a governance reviewer signs off. See
[OUTREACH_APPROVAL_POLICY.md](OUTREACH_APPROVAL_POLICY.md).

---

## Enforcement

```bash
python scripts/targeting_compliance_gate.py \
  --in data/targeting/company_master.jsonl --out data/targeting/out
# → out/approved_research_pool.csv  +  out/rejected_targets.csv (each reject has a reason)
```

Tested by `tests/test_targeting_compliance_gate.py`.
