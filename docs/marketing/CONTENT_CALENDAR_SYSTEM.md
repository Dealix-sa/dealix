# Content Calendar System

A single calendar drives all of Dealix's owned marketing. The
calendar is **drafted** by the content_strategist agent and
**approved** by the founder.

## 1. Calendar shape

`marketing/content_calendar.csv`:
```
slot_id,publish_at,surface (linkedin|email|landing|sector_pulse|case_study),
theme,headline,draft_id,evidence_ids[],founder_approved_at,status
```

## 2. Slot density

- LinkedIn: 2–4 / week.
- Sector pulse: 1 / sector / month.
- Case study: 1 per consented proof, ≤ 4 / quarter.
- Email outreach drafts: queue-driven (not slot-driven).

## 3. Approval

- Calendar slots are filled with drafts a week in advance.
- The founder approves the slot before the publish_at time.
- A slot that isn't approved is rolled forward (not auto-published).

## 4. Banned patterns

- ❌ Auto-publish on a schedule with no approval gate.
- ❌ "Filler" content without a clear theme or evidence.
- ❌ Posting the same artifact across surfaces without adaptation.
