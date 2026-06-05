# Prospect Research Compliance Policy — سياسة امتثال بحث العملاء المحتملين

> Governs how the **Dealix Research & Targeting OS** collects, stores, scores, and
> drafts. This policy is binding on the engine
> [`scripts/research_targeting_os.py`](../../scripts/research_targeting_os.py) and on
> any operator running it. It exists so Dealix never becomes a legal or
> reputational risk.
>
> تحكم كيفية جمع وتخزين وتقييم وصياغة **نظام الاستخبارات والاستهداف في Dealix**.
> ملزِمة للمحرك ولأي مشغّل يستخدمه، حتى لا يصبح Dealix خطرًا قانونيًا أو على السمعة.

Related: [RESEARCH_TARGETING_OS](../go-to-market/RESEARCH_TARGETING_OS.md) ·
Doctrine guard: [`safe_send_gateway/doctrine.py`](../../auto_client_acquisition/safe_send_gateway/doctrine.py) ·
Source registry: [`revenue_os/source_registry.py`](../../auto_client_acquisition/revenue_os/source_registry.py)

---

## 1. Allowed sources — المصادر المسموحة

Pinned in [`data/targeting/source_allowlist.json`](../../data/targeting/source_allowlist.json):

- Official company website, services page, contact page, careers page.
- Customers / case-study pages.
- Public allowed directories and **open data portals** (CSV/JSON/XML).
- Search API result **metadata** (title/link/snippet).
- Founder-provided lists, warm intros, partner referrals.
- Public business info explicitly allowed for processing.
- Manual reading of public LinkedIn profiles by a human.

> Saudi Open Data is a central portal for government open data in processable
> formats — useful as a **supporting indicator only**, never a substitute for
> per-company manual verification.

Any row whose `source` is not on the allowlist is **rejected and logged** (not
processed). Blocked sources always override the allowlist.

---

## 2. Forbidden — ممنوع منعًا باتًا

The following are hard-blocked and enforced by the doctrine guard
(`enforce_doctrine_non_negotiables`) and the source policy:

- **No scraping behind a login.** No bypassing `robots.txt`. No CAPTCHA bypass.
- **No LinkedIn automation** (manual public-profile reading only).
- **No cold/bulk WhatsApp.** No mass email. No purchased lists.
- **No autonomous external sends** — drafts only, founder approves each send.
- **No personal phone numbers.**
- **No claim without evidence.** No invented metrics. No guaranteed-results claims.

`robots.txt` is a voluntary-compliance standard; Dealix holds a stricter line: we
do not collect from a platform whose terms prohibit it, regardless of `robots.txt`.

---

## 3. The two-evidence / warm-path rule — قاعدة الدليلين / المسار الدافئ

A company may only be **targeted** when it has **either**:

1. two clear, independent pain evidences from allowlisted sources, **or**
2. a warm path (warm intro / partner / referral).

Otherwise the verdict is **research more**: the engine caps the grade at **B** and
recommends a free Diagnostic instead of a paid offer. This is enforced in
`evaluate()` and covered by tests.

---

## 4. Storage & retention — التخزين والاحتفاظ

- Store only business-level, lawfully obtained fields needed for scoring + drafting.
- Evidence URLs are retained to justify every score and every draft.
- No special-category personal data. No minors' data. Sensitive sectors
  (government, defense, gambling, …) carry a risk penalty and require human review.
- Outputs live under `data/targeting/out/` and are treated as internal until the
  founder approves any external use.

---

## 5. Drafting & sending — الصياغة والإرسال

- Drafts are **review-only** (`auto_send: false`) and bilingual (AR+EN).
- Every draft is evidence-anchored and runs through the claim-safety auditor
  ([`governance_os.claim_safety`](../../auto_client_acquisition/governance_os/claim_safety.py));
  forbidden-claim language is blocked.
- Drafts are produced **only** for targeting-ready A/A+ companies, capped at 10/day.
- Sending is always a **manual founder action** on a small set (3–5/day target).

---

## 6. Audit & review — التدقيق والمراجعة

- Rejected rows (blocked / non-allowlisted source) are listed in the daily brief.
- The engine calls `enforce_doctrine_non_negotiables` at startup; a clean run
  crosses no line. Any attempt to request scraping/automation/auto-send raises.
- This policy is reviewed whenever the source allowlist or the offer ladder changes.

---

## 7. Provider note — ملاحظة عن مزوّد البحث

Discovery uses Google Programmable Search (Custom Search JSON API) when keys exist.
That product is in a transition path for existing customers; if access lapses, the
provider can be swapped (Vertex AI Search / SerpAPI / Tavily / Brave) without
changing the engine or this policy — the allowlist and non-negotiables stay the same.
