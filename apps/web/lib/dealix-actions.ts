// Founder Console v4 — approval action client (browser-side).
// Every decision routes through the internal API which writes an
// audit record before returning. External-impact actions still need
// a Trust pass; this client just records and surfaces the result.

export type ApprovalDecisionKind = "approve" | "reject" | "request-edit";

export type ApprovalDecisionPayload = {
  decision: ApprovalDecisionKind;
  reason?: string;
  actor?: string;
};

export type ApprovalDecisionResult = {
  approval_id: string;
  status: string;
  actor: string;
  reason: string | null;
  audit_written: boolean;
  policy_result: string;
  external_action_allowed: boolean;
  timestamp: string;
};

const ENDPOINT_BY_KIND: Record<ApprovalDecisionKind, string> = {
  approve: "approve",
  reject: "reject",
  "request-edit": "request-edit"
};

export async function submitApprovalDecision(
  approvalId: string,
  payload: ApprovalDecisionPayload
): Promise<ApprovalDecisionResult> {
  const suffix = ENDPOINT_BY_KIND[payload.decision];
  const body = {
    decision: payload.decision === "approve" ? "approve" : payload.decision,
    reason: payload.reason ?? null,
    actor: payload.actor ?? "sami"
  };
  const res = await fetch(`/api/v1/internal/approvals/${approvalId}/${suffix}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body)
  });
  if (!res.ok) {
    throw new Error(`Approval decision failed: HTTP ${res.status}`);
  }
  return (await res.json()) as ApprovalDecisionResult;
}
