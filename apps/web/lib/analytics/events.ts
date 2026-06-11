// Analytics events (no PII)
export type EventName =
  | "page_view"
  | "cta_click"
  | "sales_pack_download"
  | "ceo_brief_download"
  | "proposal_generated"
  | "lead_imported"
  | "draft_reviewed"
  | "proof_report_generated";

export interface AnalyticsEvent {
  name: EventName;
  props: Record<string, string | number | boolean>;
  ts: string;
}

export function track(name: EventName, props: Record<string, string | number | boolean> = {}): void {
  if (typeof process !== "undefined" && process.env.NEXT_PUBLIC_ANALYTICS_ENABLED !== "true") {
    return;
  }
  if (typeof window === "undefined") return;
  const evt: AnalyticsEvent = { name, props, ts: new Date().toISOString() };
  if (process.env.NODE_ENV !== "production") {
    // eslint-disable-next-line no-console
    console.log("[analytics]", evt);
  }
}
