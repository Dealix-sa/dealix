# Dealix Master Lite OS

## Purpose
A safer daily operating layer for Dealix.

This version avoids heavy builds and recursive scripts. It only:
- checks production health if available
- runs company day if available
- runs founder day if available
- creates CEO daily report
- creates approval queue
- indexes CRM
- prints next founder actions

## It does not
- run frontend build
- run Docker build
- send WhatsApp
- send email
- issue invoices
- sign contracts
- commit generated daily files
- merge PRs automatically

## Founder daily intervention
1. Open CEO report.
2. Open approval queue.
3. Pick top 20.
4. Send manually.
5. Update CRM.
6. Push Diagnostic Sprint to warm leads.
