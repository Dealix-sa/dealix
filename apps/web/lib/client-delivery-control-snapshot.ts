export const clientDeliveryControlSnapshot = {
  generated_at: "not_generated_yet",
  company: "Dealix",
  control_name: "Client Delivery Control",
  delivery_method: "Map, Design, Build, Operate, Scale",
  purpose: "turn a sold sprint into a controlled delivery workflow with proof and renewal path",
  verdict: "CLIENT_DELIVERY_TEMPLATE_REVIEW_NEEDED",
  stages: [
    { name: "Intake", goal: "capture business context and success criteria" },
    { name: "Diagnosis", goal: "map current state, bottlenecks, opportunity, and risk" },
    { name: "Blueprint", goal: "turn diagnosis into system scope and workflow design" },
    { name: "Sprint Delivery", goal: "build the first working operating workflow" },
    { name: "Proof Pack", goal: "prove what changed and define the next cycle" },
    { name: "Renewal Path", goal: "convert sprint into managed monthly partnership" }
  ],
  client_files_status: [],
  delivery_guardrails: [
    "no scope expansion without acceptance criteria",
    "proof pack required before renewal pitch",
    "client success metric required before build"
  ],
  next_delivery_actions: [
    "Create a workspace from clients/_template for every new client.",
    "Confirm outcome, owner, workflow, and acceptance criteria before build.",
    "Start with one high-value workflow before expanding scope.",
    "Generate proof notes before renewal or expansion."
  ]
} as const;
