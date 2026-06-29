# Open Design Integration Validation

## Scope

This integration is documentation and project-agent guidance only.

It does not:

- import Open Design code
- add Open Design dependencies
- add Electron
- add Node 24 constraints
- change Dealix runtime
- change Railway settings
- enable live outbound
- add generated media assets

## Manual checks

```bash
find docs/open-design docs/design .agents/skills/dealix reports/design -maxdepth 5 -type f | sort
python scripts/verify_no_auto_external_send.py || true
npm --prefix apps/web run verify || true
```

## Expected changed areas

```text
docs/open-design/
docs/design/
.agents/skills/dealix/design-command-room/SKILL.md
.agents/skills/dealix/README.md
reports/design/README.md
```

## Merge posture

Low risk. Markdown-only operating system layer for design/product artifacts.
