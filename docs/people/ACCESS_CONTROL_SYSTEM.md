# Access Control System

## Purpose
Protect Dealix systems, data, and clients when working with contractors,
partners, or tools.

## Access Levels

### Access 0 — Public
Public docs, templates, demo data.

### Access 1 — Task-Limited
Only specific files needed for a task.

### Access 2 — Client-Limited
Only one client workspace, no finance or secrets.

### Access 3 — Ops-Limited
Some private ops trackers, no secrets/payment data.

### Access 4 — Admin
Reserved for founder or trusted operator.

## Rules
- give minimum access
- remove access when task ends
- never share API keys
- never share full private ops by default
- never share payment credentials
- track access in `people/access_log.csv`

## Evidence
- `people/access_log.csv`
- `people/contractor_tracker.csv`
