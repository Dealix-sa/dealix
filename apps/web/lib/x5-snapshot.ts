export const x5Snapshot = {
  summary: { actions: 7, approval_items: 7, audit_events: 7, auto_execute: 0 },
  actions: [
    { action_id: 'x5-001', lane: 'ceo', owner: 'CEO', title: 'approve top priorities', priority: 95, status: 'ready_for_review' },
    { action_id: 'x5-002', lane: 'sales', owner: 'Sales Director', title: 'review commercial queue', priority: 92, status: 'ready_for_review' },
    { action_id: 'x5-006', lane: 'trust', owner: 'Trust Owner', title: 'review safety queue', priority: 90, status: 'ready_for_review' }
  ]
} as const;
