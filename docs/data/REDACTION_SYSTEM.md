# Redaction System

## Purpose
Remove personal or sensitive data from artifacts when no longer needed, while keeping the artifact useful.

## Redaction targets
- Personal names → role + sector.
- Email addresses → `<redacted-email>`.
- Phone numbers → `<redacted-phone>`.
- Internal financials of customers → ranges or removed.
- API keys and secrets → never appear in artifacts; if found, rotate immediately.

## Process
1. Identify the artifact and the trigger (retention window, customer request, public reuse).
2. Make a copy of the artifact to the redacted destination.
3. Replace targets in the copy.
4. Verify the original cannot be recovered from the copy.
5. Log the action in `trust/redaction_log.csv`.

## Tools
- For text: use scripted find-and-replace; verify by re-reading.
- For CSVs: rewrite with a Python script; do not edit in place.
- For PDFs: re-export from source, do not "black-box" overlay.

## Verification
- Random sample 10% of redacted artifacts monthly.
- Re-scan for targets to ensure no leakage.

## Anti-patterns
- "Soft redaction" via formatting (e.g., white text on white).
- Renaming a file without changing its content.
- Distributing a redacted file via an unauthenticated channel.
