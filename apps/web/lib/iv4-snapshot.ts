export const iv4Snapshot = {
  summary: {
    dx3_items: 15,
    growth_cards: 3,
    proposal_briefs: 3,
    negotiation_plans: 3,
    command_queue: 7,
    approval_required: 7,
    auto_execute: 0,
    external_sends: 0,
    final_commitments: 0
  },
  command_queue: [
    { lane: 'ceo', owner: 'CEO', title: 'pick top company move', next_step: 'approve three moves only', source: 'dx3', score: 95 },
    { lane: 'sales', owner: 'Sales Director', title: 'review negotiation plans', next_step: 'review_negotiation_plans', source: 'negotiation_operator', score: 93 },
    { lane: 'sales', owner: 'Sales Director', title: 'review commercial growth cards', next_step: 'review_growth_cards_and_proposals', source: 'commercial_growth_os', score: 89 }
  ]
} as const;
