// Type definitions for the Full Ops Console.
// These mirror the backend API contract for /api/v1/full-ops/* and /api/v1/approvals/*.

export type AgentStatus = string;

export interface AgentNode {
  agent_id: string;
  name: string;
  role_ar: string;
  role_en: string;
  autonomy_level: number;
  status: AgentStatus;
  capabilities?: string[];
}

export interface DirectorNode extends AgentNode {
  operators: AgentNode[];
}

export interface HierarchyTotals {
  directors: number;
  operators: number;
  max_autonomy_level: number;
}

export interface HierarchyResponse {
  orchestrator: AgentNode;
  directors: DirectorNode[];
  totals: HierarchyTotals;
}

export interface StageCount {
  count: number;
}

export interface QualifiedStage extends StageCount {
  accept: number;
  diagnostic: number;
  reject: number;
}

export interface CycleStages {
  intake: StageCount;
  enriched: StageCount;
  scored: StageCount;
  qualified: QualifiedStage;
  drafts: StageCount;
  proof_events: StageCount;
}

export interface ApprovalCardItem {
  approval_id?: string;
  id?: string;
  summary_ar?: string;
  summary_en?: string;
  action_type?: string;
  action_mode?: string;
  object_type?: string;
  object_id?: string;
  channel?: string;
  risk_level?: string;
  status?: string;
  proof_impact?: string;
  created_at?: string;
  updated_at?: string;
}

export interface BilingualText {
  ar: string;
  en: string;
}

export interface WorkItem {
  id?: string;
  title_ar?: string;
  title_en?: string;
  priority?: string;
  [key: string]: unknown;
}

export interface ApprovalsBlock {
  count: number;
  items: ApprovalCardItem[];
}

export interface WorkItemsBlock {
  count: number;
  by_priority: Record<string, number>;
  top: WorkItem[];
}

export interface CycleResponse {
  cycle_id: string;
  generated_at: string;
  on_date: string;
  title_ar: string;
  title_en: string;
  stages: CycleStages;
  approvals_pending: ApprovalsBlock;
  work_items: WorkItemsBlock;
  next_actions: BilingualText[];
  hard_gates: string[];
  report_paths: { json?: string; md?: string };
}

export interface QueueBlock {
  count: number;
  top_3: BilingualText[];
}

export interface ComplianceAlerts {
  count: number;
  escalated: number;
  top_3: BilingualText[];
}

export interface ExecutiveSummary {
  total_items: number;
  by_priority: Record<string, number>;
}

export interface BlockedActions {
  count: number;
  first_3: BilingualText[];
}

export interface CommandCenterResponse {
  title_ar: string;
  title_en: string;
  today_top_3_decisions: BilingualText[];
  growth_queue: QueueBlock;
  sales_queue: QueueBlock;
  support_queue: QueueBlock;
  cs_queue: QueueBlock;
  delivery_queue: QueueBlock;
  compliance_alerts: ComplianceAlerts;
  executive_summary: ExecutiveSummary;
  blocked_actions: BlockedActions;
  hard_gates: string[];
}

export interface ApprovalsPendingResponse {
  pending: ApprovalCardItem[];
  cards: ApprovalCardItem[];
}
