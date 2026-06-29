# Deal Conversation Intelligence — Runbook

## Purpose

Classifies any client message (Arabic or English) and returns a structured intelligence readout: intent, stage, objection, sentiment, urgency, missing info, recommended response angle, next best action, and approval requirements.

## What It Returns

| Field | Description |
|-------|-------------|
| intent | What the client is asking for |
| deal_stage | Where the client is in the buying journey |
| sentiment | positive / negative / neutral |
| urgency | high / medium / low |
| objection_type | price / timing / trust / authority / details / none |
| missing_info | What information is still needed |
| recommended_response_angle | How to respond strategically |
| next_best_action | One concrete action to take |
| approval_required | Whether a human must review before acting |
| risk_flags | Safety flags (e.g. no_final_price_without_scope) |
| suggested_offer | Best offer to recommend for this stage |
| suggested_discovery_questions | Questions to ask to advance the deal |

## Intent Types

- price_question
- proposal_request
- meeting_request
- ask_for_details
- discount_request
- price_objection
- timing_objection
- trust_objection
- procurement_request
- legal_terms
- not_interested
- unsubscribe
- interested
- unknown

## Deal Stages

cold → aware → interested → discovery → proposal → negotiation → procurement → closed_won / closed_lost → renewal → expansion

## Safety Rules

- `live_send` is always `False`
- `final_commitment` is always `False`
- Approval required for: price_question (final), proposal_request, discount_request, legal_terms, procurement_request

## Usage

```bash
python deal_conversation_intelligence.py
```

```python
import deal_conversation_intelligence as dci

result = dci.classify('كم السعر؟')
print(result['next_best_action'])
print(result['suggested_offer'])
```

## Example: Arabic Price Question

Input: `كم السعر؟`

Output:
- intent: `price_question`
- deal_stage: `interested`
- approval_required: `True`
- risk_flags: `['no_final_price_without_scope']`
- next_best_action: `present_scoped_pricing_range_do_not_commit_final`

## Example: Unsubscribe

Input: `وقف التواصل`

Output:
- intent: `unsubscribe`
- next_best_action: `mark_do_not_contact_immediately`
- approval_required: `False`
- live_send: `False`
