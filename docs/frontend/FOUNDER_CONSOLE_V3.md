# Founder Console v3

## Purpose
Turn Dealix into a founder-operated revenue company controlled from one internal console.

## Core Principle
The console shows decisions and bottlenecks, not raw data.

## Primary Pages

### /ceo
One top CEO action, company status, revenue movement, trust risk, worker health.

### /sales-cockpit
Lead intelligence, approvals, outreach, replies, samples, proposals, payment capture.

### /approvals
A1/A2/A3 approval inbox for outreach, proposals, pricing, proof, and trust escalations.

### /workers
Background machine health, last run, failures, backlog, stale jobs.

### /trust
Suppression, approval breaches, overclaims, AI evals, incidents.

### /finance
Cash, MRR, pipeline, weighted pipeline, expenses, payment follow-ups.

### /distribution
Channels, sectors, experiments, double-down / fix / kill decisions.

### /delivery
Active sprints, deliverable state, on-time delivery, blockers.

### /retention
Renewal queue, NPS detractors, churn risk, expansion candidates.

### /proof
Proof library, case studies, evidence packs, citation count.

## Required Behavior

- Every number has source of truth.
- Every action has approval class.
- Every external-impact action goes through Trust.
- Every approval writes audit.
- Every page has fallback state but does not claim production readiness from fallback.

## Production Rule

Founder Console is production-ready only when it reads real runtime data and
approval actions write audit records.
