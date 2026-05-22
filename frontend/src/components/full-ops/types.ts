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

// Strategic Autonomy Layer.
// Mirrors the backend API contract for /api/v1/strategy/autonomous/*.

export interface StrategicAgentNode {
  agent_id: string;
  name: string;
  role_ar: string;
  role_en: string;
  autonomy_level: number;
  status: AgentStatus;
}

export interface StrategicCeoNode extends StrategicAgentNode {
  delegates_to: string[];
}

export interface StrategicTierTotals {
  board_directors: number;
  max_autonomy_level: number;
}

export interface StrategicTierResponse {
  ceo: StrategicCeoNode;
  board_directors: StrategicAgentNode[];
  delegates_to_operational: string;
  totals: StrategicTierTotals;
}

export interface GateEvaluationItem {
  gate_id: string;
  title_ar: string;
  title_en: string;
  passed: boolean;
  observed_value: number;
  decision_type: string | null;
  note_ar: string;
  note_en: string;
}

export interface StrategicDecisionItem {
  decision_id: string;
  decision_type: string;
  target: string;
  rationale_ar: string;
  rationale_en: string;
  score: number;
  decision_band: string;
  status: string;
  irreversible: boolean;
  requires_approval: boolean;
}

export interface DelegatedCycleItem {
  cycle_id: string;
  summary: string;
}

export interface StrategicApprovalsPending {
  count: number;
  items: ApprovalCardItem[];
}

export interface StrategicCycleResponse {
  cycle_id: string;
  generated_at: string;
  on_date: string;
  cadence: string;
  title_ar: string;
  title_en: string;
  signal_snapshot: Record<string, unknown>;
  gate_evaluations: GateEvaluationItem[];
  decisions: StrategicDecisionItem[];
  approvals_pending: StrategicApprovalsPending;
  delegated_cycles: DelegatedCycleItem[];
  next_actions: BilingualText[];
  hard_gates: string[];
  report_paths: { json?: string; md?: string };
  warnings: string[];
}

export interface GateRuleItem {
  gate_id: string;
  source: string;
  title_ar: string;
  title_en: string;
  window_day: number | null;
  metric: string;
  comparator: string;
  threshold: number;
  severity: string;
}

export interface StrategicDecisionsResponse {
  decisions: StrategicDecisionItem[];
}

export interface StrategicGatesResponse {
  gates: GateRuleItem[];
}

// Customer Success Autonomy Layer
// Mirrors the contract for /api/v1/customer-success/autonomous/*.

export interface CsSummary {
  active_customers?: number;
  opportunities_total?: number;
  at_risk?: number;
  expansion_ready?: number;
  renewals_due?: number;
  nps_detractors?: number;
}

export interface CsOpportunity {
  type?: string;
  customer_id?: string;
  urgency?: string;
  recommended_action_ar?: string;
  recommended_action_en?: string;
  evidence?: string[];
  [key: string]: unknown;
}

export interface CsCycleResponse {
  cycle_id?: string;
  generated_at?: string;
  on_date?: string;
  title_ar?: string;
  title_en?: string;
  summary?: CsSummary;
  opportunities?: CsOpportunity[];
  approvals_created?: number;
  work_items_created?: number;
  hard_gates?: string[];
  warnings?: string[];
  report_paths?: { json?: string; md?: string };
}

// Financial Autonomy Layer
// Mirrors the contract for /api/v1/financial/autonomous/*.

export interface FinancialMetrics {
  mrr_sar?: number;
  arr_sar?: number;
  nrr_pct?: number;
  churn_pct_monthly?: number;
  runway_months?: number;
  gross_margin_pct?: number;
  ltv_sar?: number;
  cac_payback_months?: number;
  [key: string]: unknown;
}

export interface FinancialAnomaly {
  kind?: string;
  observed?: number;
  expected?: number;
  delta_pct?: number;
  severity?: string;
  title_ar?: string;
  title_en?: string;
  [key: string]: unknown;
}

export interface FinancialThresholdRule {
  rule_id?: string;
  source?: string;
  title_ar?: string;
  title_en?: string;
  metric?: string;
  comparator?: string;
  threshold?: number;
  severity?: string;
  action_on_violation?: string;
}

export interface FinancialThresholdViolation {
  rule?: FinancialThresholdRule;
  observed_value?: number;
  breached?: boolean;
  action_on_violation?: string;
}

export interface FinancialCycleResponse {
  empty?: boolean;
  cycle_id?: string;
  generated_at?: string;
  period_end?: string;
  cadence?: string;
  title_ar?: string;
  title_en?: string;
  metrics?: FinancialMetrics;
  unit_economics?: Record<string, unknown>;
  anomalies?: FinancialAnomaly[];
  threshold_violations?: FinancialThresholdViolation[];
  approvals_pending?: { count?: number; items?: ApprovalCardItem[] };
  hard_gates?: string[];
  warnings?: string[];
  report_paths?: { json?: string; md?: string };
}

export interface FinancialThresholdsResponse {
  thresholds: FinancialThresholdRule[];
}

export interface BoardMemoSection {
  title_ar?: string;
  title_en?: string;
  body_ar?: string;
  body_en?: string;
  [key: string]: unknown;
}

export interface BoardMemoResponse {
  empty?: boolean;
  cycle_id?: string;
  generated_at?: string;
  month?: string;
  title_ar?: string;
  title_en?: string;
  approval_id?: string | null;
  sections?: Record<string, BoardMemoSection>;
  section_order?: string[];
  sections_complete?: boolean;
  missing_sections?: string[];
  warnings?: string[];
  report_paths?: { json?: string; md?: string };
  error?: string;
}
