export const trustControlSnapshot = {
  generated_at: "not_generated_yet",
  company: "Dealix",
  control_name: "Trust and Claims Control",
  purpose: "protect commercial launch quality by reviewing claims, proof language, and AI operating guardrails",
  verdict: "TRUST_CONTROL_READY",
  checks: [
    { name: "Claims Review", goal: "block fake ROI, fake testimonials, and guaranteed revenue language" },
    { name: "Data Handling Review", goal: "confirm only needed data is requested" },
    { name: "AI Review Gate", goal: "keep sensitive actions under owner review" },
    { name: "Proof Language", goal: "use operational evidence instead of unsupported claims" }
  ],
  blocked_phrases: ["guaranteed revenue", "guaranteed ROI", "fake testimonial"],
  approved_language: ["pain hypothesis", "founder review", "proof pack", "operational evidence", "scoped diagnostic"],
  required_guardrails: ["no fake ROI", "no fake testimonials", "no guaranteed revenue claim", "owner review required"]
} as const;
