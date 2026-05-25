export type Counter = { label: string; value: string | number; hint?: string };

export type TopAction = {
  title: string;
  detail: string;
  cta: string;
  href: string;
};

export type FunnelStage = {
  stage: string;
  count: number;
};

export type FollowUp = {
  leadId: string;
  company: string;
  dueAt: string;
  channel: string;
};

export type ApprovalItem = {
  ticketId: string;
  actionType: string;
  requestedBy: string;
  riskClass: string;
  state: "pending" | "approved" | "rejected" | "expired";
  reason?: string;
};

export type ChannelSectorCell = {
  channel: string;
  sector: string;
  replies: number;
  positive: number;
  status: "double_down" | "fix" | "kill" | "watch";
};

export type WorkerRow = {
  name: string;
  lastRun: string;
  status: "ok" | "degraded" | "failed" | "idle";
  failures: number;
  backlog: number;
  nextRun: string;
};

export type TrustFlag = {
  id: string;
  decision: "ALLOW" | "DENY" | "ESCALATE";
  rule: string;
  reason: string;
  actor: string;
  at: string;
};

export type FinanceSnapshot = {
  cashSar: number;
  mrrSar: number;
  pipelineSar: number;
  weightedPipelineSar: number;
  paymentFollowUpsSar: number;
  monthlyBurnSar: number;
  runwayMonths: number;
};
