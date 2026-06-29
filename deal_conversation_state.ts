export type DealIntent =
  | 'price_question'
  | 'proposal_request'
  | 'meeting_request'
  | 'ask_for_details'
  | 'discount_request'
  | 'price_objection'
  | 'timing_objection'
  | 'trust_objection'
  | 'procurement_request'
  | 'legal_terms'
  | 'not_interested'
  | 'unsubscribe'
  | 'interested'
  | 'unknown';

export type DealStage =
  | 'cold'
  | 'aware'
  | 'interested'
  | 'discovery'
  | 'proposal'
  | 'negotiation'
  | 'procurement'
  | 'closed_won'
  | 'closed_lost'
  | 'renewal'
  | 'expansion';

export type ObjectionType =
  | 'price'
  | 'timing'
  | 'trust'
  | 'authority'
  | 'details'
  | 'competition'
  | 'scope'
  | 'legal'
  | 'none'
  | 'unknown';

export type Sentiment = 'positive' | 'negative' | 'neutral';
export type Urgency = 'high' | 'medium' | 'low';
export type CloseProbabilityBand = 'low' | 'medium' | 'high' | 'very_high';

export interface ConversationReadout {
  message: string;
  intent: DealIntent;
  deal_stage: DealStage;
  sentiment: Sentiment;
  urgency: Urgency;
  objection_type: ObjectionType;
  missing_info: string[];
  recommended_response_angle: string;
  next_best_action: string;
  approval_required: boolean;
  risk_flags: string[];
  suggested_offer: string;
  suggested_discovery_questions: string[];
  live_send: false;
  final_commitment: false;
}

export interface DealStrategy {
  account: string;
  sector: string;
  message: string;
  conversation_intel: ConversationReadout;
  deal_score: number;
  close_probability_band: CloseProbabilityBand;
  best_offer: string;
  pricing_range: string;
  recommended_discount_policy: {
    max_discount_pct: number;
    discount_requires_approval: true;
    never_discount_below_floor: true;
    floor_rule: string;
    auto_commit: false;
  };
  negotiation_position: {
    stance: string;
    message: string;
    concession_order: string[];
    never_do: string[];
  };
  must_ask_questions: string[];
  next_best_action: string;
  do_not_do: string[];
  approval_gates: string[];
  proof_to_show: string[];
  live_sends: 0;
  final_commitments: 0;
}

export interface ApprovalQueueItem {
  action: string;
  status: 'pending_approval';
  auto_run: false;
  triggered_by: string;
}

export interface ClientServicePack {
  summary: {
    auto_prepared_items: number;
    approval_queue_items: number;
    live_sends: 0;
    final_commitments: 0;
    lifecycle_stages: number;
    deliverables: number;
  };
  client_workspace: {
    account: string;
    sector: string;
    offer: string;
    status: string;
    created: string;
    folders: string[];
  };
  intake_pack: Record<string, unknown>;
  conversation_readout: ConversationReadout;
  deal_strategy: DealStrategy;
  proposal_folder: Record<string, unknown>;
  daily_delivery_plan: {
    items: string[];
    auto_run: boolean;
    live_send: false;
  };
  weekly_review_pack: Record<string, unknown>;
  proof_report_template: Record<string, unknown>;
  approval_queue: ApprovalQueueItem[];
  renewal_plan: Record<string, unknown>;
  auto_prepared: string[];
}
