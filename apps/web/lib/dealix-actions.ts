// Dealix actions — read-only typed wrappers for the Founder Console.
//
// No mutation actions in this session. Every wrapper calls fetchInternal
// and returns a {data, source, freshness, is_estimate} envelope.

import { fetchInternal, type RuntimeEnvelope } from "./dealix-runtime";

export const dealixActions = {
  ceoDailyBrief: () =>
    fetchInternal<Array<Record<string, string>>>(
      "/api/v1/internal/founder-console/ceo/daily-brief",
    ),
  capitalAllocation: () =>
    fetchInternal<Array<Record<string, string>>>(
      "/api/v1/internal/founder-console/capital-allocation",
    ),
  marketAttack: () =>
    fetchInternal<Array<Record<string, string>>>(
      "/api/v1/internal/founder-console/market-attack",
    ),
  aiGovernance: () =>
    fetchInternal<Array<Record<string, string>>>(
      "/api/v1/internal/founder-console/ai-governance",
    ),
  trustFlags: () =>
    fetchInternal<Array<Record<string, string>>>(
      "/api/v1/internal/founder-console/trust/flags",
    ),
  auditRecent: () =>
    fetchInternal<Array<Record<string, string>>>(
      "/api/v1/internal/founder-console/audit/recent",
    ),
} as const;

export type DealixEnvelope<T = Array<Record<string, string>>> = RuntimeEnvelope<T>;
