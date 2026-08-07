# Outreach Review Gate

## Policy
No message may be sent to a prospect or client without human review and explicit approval.

## Review Checklist
- [ ] Recipient is opted-in or has a legitimate business relationship
- [ ] Message is personalized, not bulk
- [ ] No false claims or guaranteed ROI
- [ ] Arabic/English grammar checked
- [ ] Sender identity is clear (Dealix representative)
- [ ] Unsubscribe/opt-out path included where required

## Approval Matrix
- Standard draft: Account lead reviews
- High-value prospect (>50k SAR potential): Founder reviews
- Sensitive sector (healthcare, government): Compliance review

## Enforcement
- All drafts stored with `review_status = pending_review`
- Only `review_status = approved` may be marked for send
- Auto-send flags are prohibited in code
