export const dx3Snapshot = {
  summary: { lanes: 10, items: 15, top_items: 7, review_required: 15, auto_execute: 0, avg_score: 83.67 },
  lane_counts: { ceo: 2, growth: 2, sales: 2, partners: 2, marketing: 2, success: 1, delivery: 1, trust: 1, pricing: 1, board: 1 },
  top_items: [
    { lane: 'ceo', title: 'pick top company move', next_step: 'approve three moves only', score: 95 },
    { lane: 'ceo', title: 'review high risk queue', next_step: 'approve or defer risk items', score: 92 },
    { lane: 'sales', title: 'handle objections', next_step: 'prepare objection replies', score: 91 },
    { lane: 'trust', title: 'review claims and channels', next_step: 'review risk gates', score: 90 },
    { lane: 'sales', title: 'move open proposals', next_step: 'prepare proposal push cards', score: 88 },
    { lane: 'pricing', title: 'review scope and range', next_step: 'review pricing ranges', score: 87 },
    { lane: 'growth', title: 'run one sector experiment', next_step: 'prepare clinic segment test', score: 86 }
  ]
} as const;
