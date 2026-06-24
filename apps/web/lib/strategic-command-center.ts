export type CommandLaneStatus = "active" | "guarded" | "ready" | "locked";

export interface CommandLane {
  id: string;
  title: string;
  status: CommandLaneStatus;
  question: string;
  metrics: string[];
  action: string;
}

export const dailyNumbers = [
  { label: "Research companies", value: "100" },
  { label: "Verify targets", value: "40" },
  { label: "Draft messages", value: "25" },
  { label: "Manual contacts", value: "10-15" },
  { label: "Call attempts", value: "3-5" },
  { label: "Discovery calls", value: "1-2" },
  { label: "Proposals", value: "1" },
];

export const commandLanes: CommandLane[] = [
  {
    id: "revenue_war_room",
    title: "Revenue War Room",
    status: "active",
    question: "What revenue action must move today?",
    metrics: ["Hot accounts", "Open proposals", "Overdue follow-ups", "Negotiation risks"],
    action: "Prepare one scoped proposal and push three qualified follow-ups.",
  },
  {
    id: "targeting_engine",
    title: "Targeting Engine",
    status: "active",
    question: "Which sector wedge gives the best chance today?",
    metrics: ["100 researched", "40 verified", "25 drafts", "10-15 manual contacts"],
    action: "Pick one sector and generate company-specific sales packs.",
  },
  {
    id: "sales_agent_os",
    title: "AI Sales Agent OS",
    status: "guarded",
    question: "What should the authorized sales assistant say next?",
    metrics: ["Voice mode", "Objections", "Negotiation levers", "Approval queue"],
    action: "Generate drafts and negotiation guidance, then require founder approval.",
  },
  {
    id: "company_brain",
    title: "Company Brain",
    status: "active",
    question: "What does the CEO need to decide today?",
    metrics: ["CEO decision", "Future radar", "Risks", "Knowledge gaps"],
    action: "Turn scattered context into one daily decision and weekly board memo.",
  },
  {
    id: "client_delivery_os",
    title: "Client Delivery OS",
    status: "ready",
    question: "What proof must be delivered for clients?",
    metrics: ["Scope cards", "Acceptance criteria", "Proof pack", "Renewal chances"],
    action: "Update proof pack and identify one renewal opportunity.",
  },
  {
    id: "safety_trust_gates",
    title: "Safety & Trust Gates",
    status: "locked",
    question: "What must remain blocked until approved?",
    metrics: ["draft_only", "Opt-out", "Identity clarity", "No fake claims"],
    action: "Keep external sends blocked until DNS, consent, rate limits, and audit are ready.",
  },
];

export const serviceStack = [
  "Revenue Command Room OS",
  "Company Brain OS",
  "AI Sales Agent OS",
  "Follow-up Recovery OS",
  "AI Trust & Governance OS",
  "Client Delivery OS",
];

export const commandCenterPayload = {
  generatedBy: "Dealix Strategic Command Center OS",
  mode: "draft_only",
  executiveVerdict: "Ready for founder-led commercial execution after manual review.",
  northStar: {
    metric: "qualified discovery calls booked",
    dailyTarget: 2,
    weeklyTarget: 8,
  },
  dailyNumbers,
  commandLanes,
  serviceStack,
  safety: {
    externalSending: false,
    emailSending: false,
    whatsappSending: false,
    smsSending: false,
    humanApprovalRequired: true,
    identityTransparencyRequired: true,
  },
};
