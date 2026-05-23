export type CEOSummary = {
  top_action: string;
  status: string;
  risk_flags: number;
  cash_collected_sar: number;
  approved_outreach: number;
  positive_replies: number;
  proposals_due: number;
  payment_followups_due: number;
  last_updated: string;
};

const API_BASE = process.env.DEALIX_API_BASE_URL || "http://localhost:8000";

export async function getCEOSummary(): Promise<CEOSummary> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/internal/ceo/summary`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error(`API failed: ${res.status}`);
    return await res.json();
  } catch {
    return {
      top_action: "Connect internal API data source",
      status: "Frontend fallback",
      risk_flags: 0,
      cash_collected_sar: 0,
      approved_outreach: 0,
      positive_replies: 0,
      proposals_due: 0,
      payment_followups_due: 0,
      last_updated: new Date().toISOString(),
    };
  }
}
