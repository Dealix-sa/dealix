# Dealix — Commercial Launch OS

**Dealix is a Saudi/GCC B2B AI Revenue & Operations OS.**
ديالكس نظام تشغيل إيرادات وعمليات مدعوم بالذكاء الاصطناعي للشركات السعودية والخليجية.

> **Golden rule:** AI drafts and ranks. Founder reviews and approves. The system never sends anything externally.

This directory holds the official commercial launch system: verticals, offers,
the 400+ daily founder-review draft factory, sales and delivery playbooks,
metrics, and go-live requirements.

## What this OS is

- **Lead Engine** — turns research into ranked, founder-reviewed drafts.
- **Service Engine** — productized offers from Audit → Enterprise OS.
- **Trust Engine** — approval-first, no blind automation, audit trail.
- **Founder Review OS** — every draft is approval-gated; nothing auto-sends.

## What it is NOT

It is not a bulk sender, a scraper, a chatbot, a generic marketing agency, or
blind automation. There is **no** SMTP, WhatsApp outbound, LinkedIn automation,
or website auto-submit anywhere in this system — by design and enforced by the
safety audit (`scripts/commercial_safety_audit.py`).

## First 5 verticals

1. [Facilities Management & Maintenance](verticals/01_facilities_management.md)
2. [Contracting & Project Controls](verticals/02_contracting_project_controls.md)
3. [Real Estate & Property Operations](verticals/03_real_estate_property_ops.md)
4. [Legal & Professional Services](verticals/04_legal_professional_services.md)
5. [Consulting, Training & B2B Services](verticals/05_consulting_training_b2b.md)

## Daily commands

```bash
python scripts/commercial_generate_400_drafts.py --target 400
python scripts/commercial_safety_audit.py
python scripts/commercial_launch_readiness.py
python scripts/media_social_calendar_generate.py
python scripts/commercial_metrics_summary.py
```

Outputs are written to `outputs/commercial_launch/<YYYY-MM-DD>/`.

## Key documents

- [Offer ladder (SAR)](02_OFFER_LADDER_SAR.md)
- [Pricing & packaging](03_PRICING_AND_PACKAGING.md)
- [Founder daily review playbook](08_FOUNDER_DAILY_REVIEW_PLAYBOOK.md)
- [Daily execution rhythm](09_DAILY_EXECUTION_RHYTHM.md)
- [Sales messaging (AR/EN)](10_SALES_MESSAGING_AR_EN.md)
- [Objection handling](11_OBJECTION_HANDLING.md)
- [Delivery operating system](15_DELIVERY_OPERATING_SYSTEM.md)
- [Commercial metrics dashboard](20_COMMERCIAL_METRICS_DASHBOARD.md)
- [External go-live requirements](21_EXTERNAL_GO_LIVE_REQUIREMENTS.md)
- [Lead intake & CRM OS](22_LEAD_INTAKE_AND_CRM_OS.md)
- [Final readiness report](99_FINAL_COMMERCIAL_LAUNCH_READINESS_REPORT.md)
