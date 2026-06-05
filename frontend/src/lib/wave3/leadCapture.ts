import { api } from "@/lib/api";

/**
 * Centralized, compliant lead capture for Wave 3 free tools.
 *
 * Compliance is enforced at the data layer:
 *  - we whitelist the fields we send (name / email / company / consent),
 *  - we NEVER set any outreach / auto-send field,
 *  - hold_stage is always false (no pipeline auto-progression),
 *  - every tool passes a distinct `source` for attribution.
 *
 * Human approval is required before any external action — this function only
 * records interest; it does not message anyone.
 */
export type ToolSource =
  | "tool_business_os_score"
  | "tool_proof_gap_audit"
  | "tool_revenue_leakage"
  | "tool_ai_governance"
  | "start_diagnostic";

export interface LeadForm {
  name: string;
  email: string;
  company?: string;
  consent: boolean;
}

export interface CaptureExtras {
  /** Non-PII summary of the tool result, for context only. */
  score?: number;
  band?: string;
  locale?: string;
}

export async function captureLead(
  source: ToolSource,
  form: LeadForm,
  extras: CaptureExtras = {},
): Promise<{ leadId: string | null }> {
  const payload: Record<string, unknown> = {
    name: form.name.trim(),
    email: form.email.trim(),
    company: (form.company ?? "").trim(),
    consent: Boolean(form.consent),
    source,
    hold_stage: false,
    locale: extras.locale ?? "ar",
  };
  if (typeof extras.score === "number") payload.tool_score = extras.score;
  if (extras.band) payload.tool_band = extras.band;

  try {
    const { data } = await api.postPublicLead(payload);
    const leadId =
      data && typeof data === "object" && "lead_id" in data
        ? String((data as { lead_id: unknown }).lead_id)
        : null;
    return { leadId };
  } catch {
    // Lead capture is best-effort; the tool result is still shown to the user.
    return { leadId: null };
  }
}
