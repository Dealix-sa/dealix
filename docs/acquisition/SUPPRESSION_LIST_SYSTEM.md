# Suppression List System

## Purpose

Respect opt-outs, rejections, bad-fit leads, and trust boundaries.

## Add to Suppression When

- prospect says not interested
- prospect asks not to be contacted
- company is bad fit
- contact data is questionable
- trust risk exists
- duplicate lead

## Rules

- Do not contact suppressed leads.
- Check suppression before outreach.
- Log reason.

## Storage

Lives at `<private_ops>/outreach/suppression_list.csv`.
Required columns: company, contact, reason, date, status.

## Review

Founder reviews suppression list weekly to catch over-suppression and
ensure trust boundaries hold.
