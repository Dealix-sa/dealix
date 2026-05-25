import type { KPIMetric } from "@/types";
import type { Deal, DealStage } from "@/types";

type DashboardMetricsPayload = {
  leads?: { total?: number; new?: number; qualified?: number; won?: number };
  deals?: { total?: number; paid?: number; revenue_sar_paid?: number };
  conversations?: { total?: number; today?: number };
  tasks?: { pending?: number; overdue?: number };
};

const STAGE_MAP: Record<string, DealStage> = {
  warm_intro_selected: "lead",
  message_drafted: "lead",
  founder_sent_manually: "qualified",
  replied: "qualified",
  diagnostic_requested: "proposal",
  diagnostic_delivered: "proposal",
  pilot_offered: "negotiation",
  commitment_received: "negotiation",
  payment_received: "closed_won",
  closed_won: "closed_won",
  closed_lost: "lead",
};

export function metricsToKpiCards(
  data: DashboardMetricsPayload,
  labels: {
    leads: string;
    deals: string;
    conversations: string;
    tasks: string;
  },
): KPIMetric[] {
  return [
    {
      label: labels.leads,
      value: data.leads?.total ?? 0,
      change: data.leads?.new ?? 0,
      trend: (data.leads?.new ?? 0) > 0 ? "up" : "neutral",
    },
    {
      label: labels.deals,
      value: data.deals?.revenue_sar_paid ?? 0,
      change: data.deals?.paid ?? 0,
      trend: (data.deals?.paid ?? 0) > 0 ? "up" : "neutral",
    },
    {
      label: labels.conversations,
      value: data.conversations?.total ?? 0,
      change: data.conversations?.today ?? 0,
      trend: "neutral",
    },
    {
      label: labels.tasks,
      value: data.tasks?.pending ?? 0,
      change: data.tasks?.overdue ?? 0,
      trend: (data.tasks?.overdue ?? 0) > 0 ? "down" : "neutral",
    },
  ];
}

export function pipelineSummaryToDeals(
  pipelineSummary: Record<string, unknown>,
  leads: Array<Record<string, unknown>>,
): Record<DealStage, Deal[]> {
  const empty: Record<DealStage, Deal[]> = {
    lead: [],
    qualified: [],
    proposal: [],
    negotiation: [],
    closed_won: [],
  };

  const leadList = leads.length
    ? leads
    : (pipelineSummary.by_stage as Record<string, unknown> | undefined)
      ? []
      : [];

  for (const raw of leadList) {
    const stageKey = String(raw.stage || raw.pipeline_stage || "warm_intro_selected");
    const col = STAGE_MAP[stageKey] || "lead";
    const deal: Deal = {
      id: String(raw.id || raw.lead_id || raw.slot_id || Math.random()),
      title: String(raw.slot_id || raw.sector || "Lead"),
      company: String(raw.sector || "—"),
      value: Number(raw.expected_amount_sar || raw.actual_amount_sar || 0),
      currency: "SAR",
      stage: col,
      probability: col === "closed_won" ? 100 : 40,
      closeDate: new Date().toISOString().slice(0, 10),
      assignedTo: "Sami",
      lastActivity: String(raw.last_touch_at || raw.created_at || new Date().toISOString()),
      tags: [String(raw.relationship_strength || "warm")],
      aiScore: Math.round(Number((raw.score as { fit?: number })?.fit ?? 0.5) * 100),
    };
    empty[col].push(deal);
  }

  return empty;
}

export function commandCenterActivities(
  payload: Record<string, unknown>,
  isAr: boolean,
): Array<{
  id: string;
  agent: string;
  actionAr: string;
  actionEn: string;
  status: string;
  timestamp: string;
}> {
  const decisions =
    (payload.today_top_3_decisions as string[] | undefined) ||
    (payload.top_decisions as string[] | undefined) ||
    [];
  const now = new Date().toISOString();
  return decisions.slice(0, 5).map((text, i) => ({
    id: `cc-${i}`,
    agent: "command_center",
    actionAr: String(text),
    actionEn: String(text),
    status: "pending",
    timestamp: now,
  }));
}
