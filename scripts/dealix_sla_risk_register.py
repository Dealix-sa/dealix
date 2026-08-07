risks=[
 ('Lead API failure','High','Add smoke test and fallback ledger'),
 ('Scope creep','High','Use SOW and acceptance criteria'),
 ('Secret exposure','Critical','Run secret smoke and keep env out of repo'),
 ('No daily outbound','Medium','Founder daily war room'),
 ('Poor conversion copy','Medium','Use conversion copy review')]
print('| Risk | Severity | Mitigation |')
print('|---|---|---|')
for r in risks: print(f'| {r[0]} | {r[1]} | {r[2]} |')
