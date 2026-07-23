#!/usr/bin/env python3
"""Prints GitHub issue bodies for manual creation when integration lacks write access."""
issues = [
('P0 Launch Website', 'Add Home, Services, Pricing, Custom AI, Industries, Contact, Privacy, Terms.'),
('P0 Daily Prospecting OS', 'Run lead scoring and daily command center. Produce reviewed outreach drafts only.'),
('P0 Trust Layer', 'Publish privacy, terms, anti-spam outbound policy, and data handling rules.'),
('P1 Sales Kit', 'Finalize call script, WhatsApp sequence, email sequence, proposal, SOW, objections.'),
('P1 Proof Engine', 'Create first 2 anonymized case studies and before/after reports.'),
]
for title, body in issues:
    print('\n---')
    print('# '+title)
    print(body)
