# Incident Response — استجابة الحوادث

## Purpose
Define how Dealix detects, classifies, communicates, and learns from incidents. The playbook applies to delivery, trust, AI, and security incidents.

## Owner
Founder (Sev-1, Sev-2). Head of Delivery (Sev-3).

## Inputs
- Incident detection signals (scanner hits, client complaints, internal observations).
- Severity matrix below.

## Outputs
- Logged incident in `docs/trust/registers/incident_log.md`.
- Communication artifacts (internal note, client message if applicable).
- Post-incident learning entry in `docs/learning/COMPANY_MEMORY.md`.

## Rules (numbered)
1. Every incident is logged within 1 hour of detection.
2. Severity is assigned within 2 hours; can be raised but not silently lowered.
3. Sev-1 and Sev-2 require founder notification at detection time.
4. Client-affecting incidents trigger client communication within 24h.
5. Every incident closes with a learning entry.
6. No incident is closed without a written cause statement.

## Metrics
- Mean time to detect, classify, communicate, resolve.
- Sev-1 count per quarter (target 0).
- Repeat incidents per category.
- Learning-entry completion rate (target 100).

## Cadence
Continuous. Monthly aggregate review in the strategy update.

## Evidence (paths)
- `docs/trust/registers/incident_log.md`
- `docs/learning/COMPANY_MEMORY.md`

## Verifier
Founder.

## Runtime Command
`make trust.incident.open SEV=<n> TITLE=<t>` opens a new incident with timestamp.

## Severity matrix

**Sev-1 — critical.** PII leak, public boundary violation, irreversible action taken without A3, named-overclaim published. Founder leads. Communications within 24h. Post-mortem within 7 days.

**Sev-2 — high.** Banned phrase in published material, scanner hit in a shipped pack, A2 action taken without review, evidence-system gap discovered. Founder notified at detection. Resolution within 72h.

**Sev-3 — medium.** Internal process violation that did not affect a client. QA gate skipped without consequence. Schema drift caught before ship. Head of Delivery resolves within 5 days.

**Sev-4 — low.** Near-miss. No action taken, but worth logging for pattern detection.

## Playbook per severity

For each severity, the playbook covers:

**Detection.** Who detected, what signal, what time.

**Containment.** Immediate action to prevent further harm.

**Classification.** Severity assignment and rationale.

**Communication.** Who is told, when, what.

**Investigation.** Cause analysis, written.

**Remediation.** Specific fix with owner and deadline.

**Learning.** Entry in company memory, change to a checklist, template, or policy if appropriate.

**Closure.** Written cause statement, signature.

## Communication templates

**Internal Sev-1 note.** Concise, factual. What happened, blast radius, current containment, who is on it, next update time. No speculation.

**Client communication, Sev-1.** Acknowledges the issue, states what we know and do not know, describes containment, names the owner, commits to a next update time. Apology is appropriate; over-promising on fixes is not.

**Internal Sev-3 note.** One paragraph. What happened, why it did not become Sev-2, the change being made.

## Operating substance
Most incidents are small. The discipline is logging them anyway so patterns emerge. A pattern of Sev-3 schema-drift catches is the signal to upgrade the schema validation; without the log, the pattern is invisible.

We do not punish people for incidents they reported. We punish people for incidents they hid. The logging culture survives only if reporting is safe. The founder owns making it safe.

Client communication on Sev-1 and Sev-2 is hard and necessary. The cost of telling a client about an issue is almost always lower than the cost of them discovering it later. We communicate factually, briefly, and quickly.

The learning entry is the closing artifact. It is the bridge between this file and `docs/learning/COMPANY_MEMORY.md`. Without it, the incident is logged but not learned from.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
