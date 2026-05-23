/**
 * Founder Console v5 — Policy Evaluator
 *
 * Classifies approval requests into A1/A2/A3 classes:
 *  - A1: Founder approves — low risk, no external action
 *  - A2: Requires evidence — needs documentation/justification
 *  - A3: Never auto-execute — always blocked at external boundary
 */

export type PolicyClass = "A1" | "A2" | "A3";

export interface ApprovalSubject {
  agentType?: string;
  action?: string;
  riskLevel?: "low" | "medium" | "high" | string;
  target?: string;
  policyClass?: string;
  metadata?: Record<string, unknown>;
}

export interface PolicyDecision {
  policyClass: PolicyClass;
  external_action_allowed: boolean;
  reasons: string[];
  recommendedAction: "approve" | "request_evidence" | "block";
  riskLevel: "low" | "medium" | "high";
}

const NEVER_AUTO_KEYWORDS = [
  "send_email_external",
  "post_public",
  "publish",
  "linkedin",
  "whatsapp_send",
  "wire_transfer",
  "payment",
  "charge",
  "production_deploy",
];

const REQUIRES_EVIDENCE_KEYWORDS = [
  "discount",
  "refund",
  "credit",
  "contract_change",
  "price_change",
  "outreach_external",
  "draft",
  "client_pack",
];

export function evaluatePolicy(subject: ApprovalSubject): PolicyDecision {
  const reasons: string[] = [];
  const action = (subject.action || "").toLowerCase();
  const agentType = (subject.agentType || "").toLowerCase();
  const declared = (subject.policyClass || "").toUpperCase();
  const riskLevel = (subject.riskLevel || "medium").toLowerCase() as
    | "low"
    | "medium"
    | "high";

  let policyClass: PolicyClass = "A1";

  if (declared === "A1" || declared === "A2" || declared === "A3") {
    policyClass = declared as PolicyClass;
    reasons.push(`declared_policy_class:${declared}`);
  }

  if (NEVER_AUTO_KEYWORDS.some((kw) => action.includes(kw) || agentType.includes(kw))) {
    policyClass = "A3";
    reasons.push("matched_never_auto_keyword");
  } else if (
    REQUIRES_EVIDENCE_KEYWORDS.some((kw) => action.includes(kw)) ||
    riskLevel === "high" ||
    riskLevel === "medium"
  ) {
    if (policyClass !== "A3") policyClass = "A2";
    reasons.push("requires_evidence_or_elevated_risk");
  } else {
    if (policyClass !== "A3" && policyClass !== "A2") policyClass = "A1";
    reasons.push("low_risk_auto_class");
  }

  const external_action_allowed = policyClass !== "A3";

  let recommendedAction: "approve" | "request_evidence" | "block";
  if (policyClass === "A3") recommendedAction = "block";
  else if (policyClass === "A2") recommendedAction = "request_evidence";
  else recommendedAction = "approve";

  return {
    policyClass,
    external_action_allowed,
    reasons,
    recommendedAction,
    riskLevel: ["low", "medium", "high"].includes(riskLevel)
      ? riskLevel
      : "medium",
  };
}
