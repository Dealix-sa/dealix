# PDPL Checklist

## Purpose
This checklist defines the minimum privacy and data handling controls required for Dealix to operate in a Saudi B2B context.

## Core Principles
- Collect only data necessary to run the requested workflow
- Keep a clear business purpose for every collected field
- Avoid hidden secondary use of customer data
- Make approval, review, and outbound activity auditable

## Data Categories Used in Dealix
- contact and booking data
- company and prospect data
- conversation and outbound draft data
- decision, risk, and opportunity records
- operational reports and proof artifacts

## Required Controls

### 1. Lawful Basis and Purpose
- [x] Booking flow collects only relevant qualification inputs
- [x] Outreach and follow-up are tied to explicit business purpose
- [x] Consent signals are stored when applicable

### 2. Data Minimization
- [x] Default forms avoid unnecessary personal fields
- [x] Internal ledgers focus on business context, not excess personal data
- [x] Generated drafts are stored for review, not sprayed automatically

### 3. Transparency
- [x] Users can understand what the platform is doing
- [x] AI-generated outbound is reviewable before send
- [x] Decision and risk records are visible in the operating interface

### 4. Retention and Review
- [x] Reports and outbox artifacts should not be committed into Git
- [x] Teams should define a retention window for conversations and drafts
- [x] Stale sensitive data should be reviewed and removed periodically

### 5. Security and Access
- [x] Secrets remain outside the repository
- [x] Outbound defaults are disabled unless explicitly enabled
- [x] Sensitive operational changes require human review

### 6. Data Subject and Client Requests
- [x] Client delivery workflow must identify where data lives
- [x] Teams should be able to locate booking, contact, and conversation records
- [x] Deletion or export requests should be handled through controlled internal procedures

## WhatsApp-Specific Controls
- [x] Official WhatsApp Cloud API only
- [x] Webhook verification token required
- [x] No live send by default
- [x] Template and message events should remain auditable

## Operating Notes
Dealix should describe itself as compliance-aware and reviewable.
Dealix should not claim formal certification unless that certification actually exists.