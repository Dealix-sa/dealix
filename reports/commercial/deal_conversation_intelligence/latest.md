# Deal Conversation Intelligence

- messages_classified: `10`
- intents_detected: `['ask_for_details', 'proposal_request', 'discount_request', 'not_interested', 'price_question', 'trust_objection', 'interested', 'legal_terms', 'unsubscribe', 'timing_objection']`
- live_sends: `0`
- final_commitments: `0`
- approval_gates_triggered: `4`

## Classifications
- [price_question] كم السعر؟ → ask_one_discovery_question_and_listen
- [proposal_request] ارسل العرض → prepare_proposal_folder_queue_for_founder_review
- [not_interested] ما نحتاج → send_polite_close_note_and_add_to_long_nurture
- [unsubscribe] وقف التواصل → mark_do_not_contact_immediately
- [ask_for_details] what does it include? → run_discovery_questions_and_map_owner
- [trust_objection] we need more proof before deciding → prepare_proof_pack_and_pilot_proposal
- [timing_objection] not now, maybe next quarter → ask_one_discovery_question_and_listen
- [legal_terms] send us the contract terms → ask_one_discovery_question_and_listen
- [discount_request] can you give us a discount? → review_scope_then_confirm_value_anchor
- [interested] we are interested, tell me more → ask_one_discovery_question_and_listen
