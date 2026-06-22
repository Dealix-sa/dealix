# Outbound Approval Policy

## Purpose
Keep every sensitive outbound action reviewable and controlled.

## Default Rule
- All outbound remains `draft_only` by default
- No live external send without explicit human approval

## Applies To
- email drafts
- WhatsApp drafts
- proposal messages
- follow-up sequences

## Minimum Approval Flow
1. draft is generated
2. reviewer checks content and context
3. reviewer approves or rejects
4. only approved items can be sent
5. send result remains auditable

## Reviewer Checklist
- Is the message relevant?
- Is the claim truthful?
- Is the call to action appropriate?
- Is there any compliance or trust risk?
- Should the channel be used at all?