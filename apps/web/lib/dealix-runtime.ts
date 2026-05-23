/**
 * Server-side runtime client for the Dealix internal API.
 *
 * Every helper:
 *   - reads DEALIX_INTERNAL_TOKEN from env (server-only) and forwards it.
 *   - falls back to a safe empty shape with source = 'fallback' on any
 *     error, so pages render even when the backend is offline.
 */

import "server-only";

const DEFAULT_BASE = "http://127.0.0.1:8000";

function apiBase(): string {
  return process.env.DEALIX_INTERNAL_API_BASE || DEFAULT_BASE;
}

interface RuntimePayload<T> {
  source: "api" | "fallback";
  auth_mode?: string;
  data: T;
  error?: string;
}

async function fetchInternal<T>(
  path: string,
  fallback: T,
): Promise<RuntimePayload<T>> {
  const url = `${apiBase()}${path}`;
  const token = process.env.DEALIX_INTERNAL_TOKEN || "";
  const headers: Record<string, string> = { Accept: "application/json" };
  if (token) headers["X-Dealix-Internal-Token"] = token;

  try {
    const resp = await fetch(url, {
      method: "GET",
      headers,
      cache: "no-store",
    });
    if (!resp.ok) {
      return { source: "fallback", data: fallback, error: `http_${resp.status}` };
    }
    const payload = (await resp.json()) as {
      source?: string;
      auth_mode?: string;
      data?: T;
    };
    const data = (payload?.data ?? fallback) as T;
    return {
      source: "api",
      auth_mode: payload?.auth_mode,
      data,
    };
  } catch (err) {
    return {
      source: "fallback",
      data: fallback,
      error: err instanceof Error ? err.message : "unknown_error",
    };
  }
}

// ── Shared payload shapes ──────────────────────────────────────────
export interface RowsPayload {
  rows: Array<Record<string, unknown>>;
}

export interface SummaryPayload {
  metrics: Array<{ label: string; value: string | number; delta?: string }>;
  highlights?: string[];
}

const EMPTY_ROWS: RowsPayload = { rows: [] };
const EMPTY_SUMMARY: SummaryPayload = { metrics: [], highlights: [] };

// ── 25 GET helpers ─────────────────────────────────────────────────
export const getCEOSummary = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/ceo/summary", EMPTY_SUMMARY);

export const getSalesFunnel = () =>
  fetchInternal<RowsPayload>("/api/v1/internal/sales/funnel", EMPTY_ROWS);

export const getApprovals = () =>
  fetchInternal<RowsPayload>("/api/v1/internal/approvals", EMPTY_ROWS);

export const getWorkerHealth = () =>
  fetchInternal<RowsPayload>("/api/v1/internal/workers/health", EMPTY_ROWS);

export const getTrustFlags = () =>
  fetchInternal<RowsPayload>("/api/v1/internal/trust/flags", EMPTY_ROWS);

export const getFinanceSummary = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/finance/summary", EMPTY_SUMMARY);

export const getDistributionSummary = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/distribution/summary", EMPTY_SUMMARY);

export const getDeliveryQueue = () =>
  fetchInternal<RowsPayload>("/api/v1/internal/delivery/queue", EMPTY_ROWS);

export const getRetentionQueue = () =>
  fetchInternal<RowsPayload>("/api/v1/internal/retention/queue", EMPTY_ROWS);

export const getProofLibrary = () =>
  fetchInternal<RowsPayload>("/api/v1/internal/proof/library", EMPTY_ROWS);

export const getAuditEvents = () =>
  fetchInternal<RowsPayload>("/api/v1/internal/audit/events", EMPTY_ROWS);

export const getControlPlaneSummary = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/control/summary", EMPTY_SUMMARY);

export const getPolicies = () =>
  fetchInternal<RowsPayload>("/api/v1/internal/control/policies", EMPTY_ROWS);

export const getAgentRegistry = () =>
  fetchInternal<RowsPayload>("/api/v1/internal/control/agents", EMPTY_ROWS);

export const getEvalStatus = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/evals/status", EMPTY_SUMMARY);

export const getProductization = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/product/productization", EMPTY_SUMMARY);

export const getSecurityStatus = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/security/status", EMPTY_SUMMARY);

export const getOperatingScorecard = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/control/scorecard", EMPTY_SUMMARY);

export const getSovereignReadiness = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/sovereign/readiness", EMPTY_SUMMARY);

export const getBrandSummary = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/brand/summary", EMPTY_SUMMARY);

export const getGrowthTargeting = () =>
  fetchInternal<RowsPayload>("/api/v1/internal/growth/targeting", EMPTY_ROWS);

export const getMarketingSummary = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/marketing/summary", EMPTY_SUMMARY);

export const getProductDistribution = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/product/distribution", EMPTY_SUMMARY);

export const getCustomerSuccessSummary = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/customer-success/summary", EMPTY_SUMMARY);

export const getFinanceOpsSummary = () =>
  fetchInternal<SummaryPayload>("/api/v1/internal/finance-ops/summary", EMPTY_SUMMARY);

export const getControlRisks = () =>
  fetchInternal<RowsPayload>("/api/v1/internal/control/risks", EMPTY_ROWS);
