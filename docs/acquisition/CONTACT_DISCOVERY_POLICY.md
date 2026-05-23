# Contact Discovery Policy

## Purpose
Find appropriate, public, business contact paths without unsafe scraping or
spam behavior.

## Preferred Contact Paths
1. Public contact form on the company website.
2. Public sales / info email published on the website.
3. Public partnership / channel email.
4. Company LinkedIn page (company-level, not individual scraping).
5. Public founder / CEO profile when professional contact is appropriate
   and the contact path is published by the person themselves.
6. Website demo / "request quote" form.

## Forbidden
- Personal phone numbers unless publicly listed by the company itself for
  business contact.
- Private emails not published by the company.
- Scraped personal data from third-party tools.
- Mass sending without per-lead relevance.
- Restricted-platform scraping (LinkedIn member search via automation,
  WhatsApp number scraping, etc.).
- Contacting employees unrelated to the buying decision.

## Rules
- Prefer company-level contact over personal.
- If personal contact is used, it must be publicly available **and**
  business-relevant to the message.
- Every message must be specific to the company (no spray-and-pray).
- Stop on the first decline; remove from queue.
- Record the source URL of every contact path in
  `acquisition/contact_discovery_queue.csv`.
- A founder approval row in `acquisition/approvals/<batch>.md` is required
  before any send.

## Audit Trail
Each contact-discovery row carries: `company, website,
preferred_contact_path, contact_found, contact_type, source,
approval_status, next_action`. The CSV is the audit record.
