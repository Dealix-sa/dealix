# Outreach Approval Policy

> كل رسالة تحتاج موافقة المؤسس. لا إرسال تلقائي. أبدًا.

Every outreach message produced by the Draft Lab is a **draft** until the founder
approves it and sends it manually.

---

## The rule

1. The Draft Lab composes drafts (`out/drafts_for_review.md`).
2. Each draft is stamped `APPROVAL_REQUIRED: founder` and `AUTO_SEND: false`.
3. The founder reviews, edits if needed, and **sends manually** through an
   allowed channel.
4. Nothing is sent by any script, scheduler, or agent.

`validate_draft()` rejects any draft where `auto_send` is truthy or
`approval_required != "founder"`.

---

## Sensitive-sector sign-off

Companies in sensitive sectors (`healthcare`, `finance`, `government`) reach the
shortlist flagged `review_required`. Before *any* outreach:

- A governance reviewer confirms the sector context is appropriate.
- The message is checked for sector-specific claims and compliance.
- The sign-off is recorded.

---

## Banned message content

No exaggerated promises or guarantees. Enforced phrase list (extensible) in
`scripts/targeting_draft_lab.py::BANNED_PHRASES`: نضمن، مضمون، 100%، 10x، "double
your", "guaranteed", …

---

## Allowed channels

`official_website_form`, `official_business_email`,
`official_phone_switchboard`, `official_linkedin_company_page` (manual),
`in_person_event`, `warm_introduction`.

No cold WhatsApp automation. See [NO_SPAM_POLICY.md](NO_SPAM_POLICY.md).
