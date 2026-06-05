# Robots & Terms Policy

> نحترم robots.txt وشروط المصدر. لا تجاوز، لا التفاف.

All research collection respects `robots.txt` and each source's terms of service.

---

## Rules

- **Honor `robots.txt`.** Do not fetch paths disallowed for the user agent.
- **Honor source terms.** If terms forbid automated collection, do it manually or
  not at all.
- **No login bypass.** Never access content behind authentication.
- **No CAPTCHA bypass.** A CAPTCHA is a stop sign.
- **No rate-abuse.** Human-paced, manual collection where automation is unclear.

A company carrying `no_robots_respect: true` (source obtained while ignoring
robots) is a **compliance reject** in the scorecard and a red-flag reject in the
gate.

---

## Practical guidance

- Reading a public page in a browser, by hand → fine.
- Using a search API to *find* public pages → fine.
- Pointing a crawler at a site that disallows it → not allowed.
- Manual LinkedIn company-page view → fine; LinkedIn automation/Sales Navigator
  scraping → not allowed.

See [RESEARCH_SOURCE_POLICY.md](RESEARCH_SOURCE_POLICY.md) for the source list and
`data/targeting/blocked_sources.yml` for the enforced patterns.
