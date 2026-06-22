# Delivery SOP — Standard Operating Procedure

## Purpose

This is the standard operating procedure for delivering any Dealix product. Every product (Revenue Command Room OS, Company Brain OS, WhatsApp/Inbox Follow-up OS, Email Outreach Review OS, SMS Notification/Follow-up OS, AI Trust & Compliance OS, Client Delivery OS, Controlled Live Outbound OS) follows this SOP. The specific deliverables vary by product, but the process is the same.

## Stages

### 1. Intake

- Trigger: client signs diagnostic or sprint agreement
- Participants: Dealix delivery lead + client founder/operations lead + relevant team members
- Duration: 60 minutes
- Activities:
  - Confirm scope and product(s) in scope
  - Identify data sources and access requirements
  - Identify key stakeholders and roles
  - Confirm timeline and milestones
  - Document any constraints (regulatory, technical, organizational)
  - Confirm communication channel and cadence (daily or every-other-day updates)
- Output: Intake document (signed by both parties, stored in client workspace)

### 2. Diagnosis

- Duration: Day 1–2
- Participants: Dealix delivery lead + Dealix engineer
- Activities:
  - Audit current data sources (WhatsApp, email, spreadsheets, CRM, documents)
  - Identify data quality issues and gaps
  - Map current processes (even informal ones)
  - Identify risks and constraints
  - Validate access (test connections, permissions, exports)
- Output: Diagnosis report (gaps, risks, data quality assessment, access confirmation)

### 3. Blueprint

- Duration: Day 2–3
- Participants: Dealix delivery lead + client founder/operations lead
- Activities:
  - Document what will be built (features, integrations, outputs)
  - Define what is in scope and out of scope
  - Define success criteria (how we know it works)
  - Define access matrix (who sees what)
  - Define approval workflow (who approves what before it goes live)
  - Get explicit client sign-off on the blueprint
- Output: Blueprint document (signed by client, stored in client workspace)
- Gate: No build begins without signed blueprint

### 4. Build

- Duration: Day 3–7 (sprint) or Day 3–14 (14-day) or Day 3–25 (30-day)
- Participants: Dealix engineer + Dealix delivery lead
- Activities:
  - Implement features per blueprint
  - Connect data sources and integrations
  - Build dashboards, queues, templates, and workflows
  - Draft initial content (templates, messages, reports) for client review
  - Daily or every-other-day progress update to client
  - Flag any blockers or scope changes immediately
- Output: Working system (staging/preview environment)
- Communication: Client is informed of progress at least every 2 days

### 5. QA (Quality Assurance)

- Duration: Day 7 (sprint) or Day 14 (14-day) or Day 26 (30-day)
- Participants: Dealix delivery lead (QA role)
- Activities:
  - Test all features against blueprint
  - Validate data accuracy (sample checks against source data)
  - Test edge cases (empty data, missing access, permission errors)
  - Test approval workflow end-to-end
  - Test compliance controls (opt-out, suppression, rate limits, logging)
  - Check for any errors, broken links, or incomplete features
  - Document any issues found
- Output: QA checklist (completed, with issues logged and resolved)
- Gate: No UAT if QA has unresolved critical issues

### 6. UAT (User Acceptance Testing)

- Duration: Day 7–8 (sprint) or Day 14–15 (14-day) or Day 27–28 (30-day)
- Participants: Client founder/operations lead + client team members + Dealix delivery lead
- Activities:
  - Client tests the system with real data and real scenarios
  - Client reviews draft content (templates, messages, reports)
  - Client provides feedback (what works, what needs change, what is missing)
  - Dealix logs all feedback and categorizes: must-fix, should-fix, nice-to-have
  - Must-fix items are resolved before launch
- Output: UAT feedback log with resolution status
- Gate: No launch until all must-fix items are resolved and client approves

### 7. Launch

- Duration: Day 8 (sprint) or Day 15 (14-day) or Day 29 (30-day)
- Participants: Dealix delivery lead + client team
- Activities:
  - System goes live for daily use
  - Any remaining staging data is replaced with live data
  - Access is granted to all approved users
  - Approval workflow is activated
  - Daily/weekly reporting cadence begins
  - Dealix monitors first 48 hours for any issues
- Output: Live system, launch confirmation

### 8. Training

- Duration: 1–2 hours, within 48 hours of launch
- Participants: Dealix delivery lead + client team (all users)
- Activities:
  - Live training session (walkthrough of system, features, workflow)
  - Q&A with team
  - Record session for future reference
  - Provide quick-start guide (1-page, Arabic-first)
  - Provide contact for support questions
- Output: Training recording, quick-start guide, trained team

### 9. Proof

- Duration: Day 14 and Day 30 (or at retainer monthly cycle)
- Participants: Dealix delivery lead + client founder
- Activities:
  - Compile proof pack: what was built, what changed since launch, what data is flowing, what KPIs are tracking
  - Present proof pack to founder
  - Discuss what is working, what needs improvement, what is next
  - Document any decisions (expand, adjust, maintain)
- Output: Proof pack document (stored in client workspace)
- Purpose: Transparency and accountability — the client sees exactly what they got

### 10. Handoff

- Duration: Day 30 (or at retainer cancellation)
- Participants: Dealix delivery lead + client founder/operations lead
- Activities:
  - Compile handoff document:
    - System overview and architecture
    - Access map (who has access to what, how to revoke, how to grant)
    - Credentials and provider accounts (transferred to client)
    - Playbook (SOPs, templates, rules)
    - Maintenance guide (what needs updating, when, by whom)
    - Support contacts (if retainer) or self-service guidance (if no retainer)
  - Walk through handoff document with client
  - Confirm retainer decision (start, decline, or defer)
  - Archive client workspace (retain for 90 days post-handoff)
- Output: Handoff document (signed by client, stored in client workspace)

## Communication Cadence

- During build: update every 2 days minimum (WhatsApp or email)
- During QA/UAT: daily updates
- Post-launch: weekly update during first month
- Retainer: monthly report + ad-hoc as needed

## Escalation

- If a blocker is identified during build, Dealix escalates to client within 24 hours
- If client is unresponsive for 3+ days, Dealix pauses build and documents the pause
- If scope changes are requested mid-build, a Change Request is required before proceeding
- If compliance issues are identified, build pauses until resolved

## Change Requests

- Any change to scope, timeline, or pricing requires a documented Change Request
- Change Request includes: what changed, why, impact on timeline, impact on price
- Client must approve Change Request before work resumes
- No undocumented changes — everything is written and signed

## What This SOP Does Not Include

- Guaranteed revenue or ROI
- Guaranteed adoption by the client's team
- Guaranteed market response
- Legal advice (for AI Trust & Compliance OS, external legal review may be needed)
- Ongoing support without a retainer (handoff is self-service unless retainer is active)

## No Fake Guarantees

This SOP guarantees a disciplined delivery process with documentation, approval gates, quality checks, and proof packs. It does not guarantee business outcomes, revenue, or adoption. The system is built to work; whether the client's team uses it and whether the market responds is beyond our control. We do not fabricate clients, testimonials, or case study results.