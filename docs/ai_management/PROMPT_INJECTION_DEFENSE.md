# Prompt Injection Defense

## Purpose
Stop attacker-controlled text from redirecting Dealix's AI workflows.

## Threat model
- Untrusted text (inbound emails, prospect PDFs, scraped pages) processed by an AI agent.
- Attacker instructions embedded in that text ("ignore previous instructions; do X").
- Risk: agent takes unsafe action (send data, run command, exfiltrate).

## Defenses (in priority order)
1. **No-send default**: AI sub-agents have no external send tools.
2. **Boundary tags**: when AI ingests external content, wrap it in `<untrusted_external_data>` tags in the prompt; instruct the agent to treat its contents as data, not instructions.
3. **Human-in-the-loop**: any external action requires founder confirmation.
4. **Scoped permissions**: agents have access only to the files they need for the task.
5. **Pattern scan**: known injection phrases ("ignore all previous", "act as", "exfiltrate") flagged for review.

## Operating workflow
- Inbound external content stored in a quarantine path before processing.
- AI agent reads from quarantine; cannot write back to quarantine.
- Any agent output that names a destination outside the working set is rejected.

## Logging
- Suspicious patterns logged in `trust/risk_register.csv`.
- Recurring patterns become candidates for a code-level filter.

## Anti-patterns
- "It's just a draft" complacency — drafts can be auto-sent if not gated.
- Wide tool permissions because "the agent is helpful".
- Trusting URLs in external text without preview.

## Testing
- Quarterly: run a tabletop with a planted injection in an inbound document.
- Verify the agent neither acts on nor leaks the embedded instruction.
