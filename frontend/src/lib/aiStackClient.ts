/**
 * Typed client for /api/v1/ai-stack/*.
 *
 * All requests target the FastAPI backend. Server-rendered pages call this
 * module on the server side; client components import the same surface for
 * the demo run form.
 */

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type LayerName =
  | "L1_source_passport"
  | "L2_data_quality"
  | "L3_intelligence"
  | "L4_model_router"
  | "L5_agent_mesh"
  | "L6_governance"
  | "L7_proof_pack"
  | "L8_value_ledger"
  | "L9_capital_ledger"
  | "L10_adoption"
  | "L11_self_evolving";

export interface LayerHealth {
  layer: LayerName;
  label: string;
  module: string;
  healthy: boolean;
  version: string;
  detail: string;
}

export interface StackStatus {
  overall_healthy: boolean;
  snapshot_at: string;
  hard_gates: Record<string, boolean>;
  layers: LayerHealth[];
}

export interface LayerResult {
  layer: LayerName;
  status: "ok" | "skipped" | "degraded" | "blocked" | "error";
  summary_ar: string;
  summary_en: string;
  duration_ms: number;
  payload: Record<string, unknown>;
  blocked_reason: string | null;
}

export type OfferTier =
  | "free_diagnostic"
  | "sprint_499"
  | "data_pack_1500"
  | "managed_ops"
  | "custom_ai";

export interface AIStackResult {
  run_id: string;
  tenant_id: string;
  customer_handle: string;
  offer_tier: OfferTier;
  started_at: string;
  completed_at: string;
  duration_ms: number;
  layers: LayerResult[];
  proof_pack_id: string | null;
  proof_score: number;
  decision_passport_ids: string[];
  evidence_head_hash: string;
  governance_blocked: boolean;
  doctrine_clean: boolean;
  recommended_offer: string;
  proof_pack_markdown: string;
}

export interface RunRequestBody {
  tenant_id: string;
  customer_handle: string;
  company_name: string;
  sector?: string;
  challenge_ar: string;
  challenge_en?: string;
  offer_tier?: OfferTier;
  source_passport: {
    source_id: string;
    source_type?: string;
    owner: string;
    allowed_use?: string[];
    contains_pii?: boolean;
    sensitivity?: string;
    retention_policy?: string;
    ai_access_allowed?: boolean;
    external_use_allowed?: boolean;
  };
  rag_documents?: Array<Record<string, unknown>>;
  actor?: string;
  locale_primary?: "ar" | "en";
}

async function fetchJson<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      ...(init?.headers ?? {}),
    },
    // Server-rendered status calls should be fresh — no Next cache.
    cache: "no-store",
  });
  if (!response.ok) {
    const detail = await response.text().catch(() => "");
    throw new Error(
      `AI Stack request failed: ${response.status} ${response.statusText} — ${detail}`,
    );
  }
  return (await response.json()) as T;
}

/**
 * Fetch the eleven-layer health snapshot. Safe to call on the server during
 * SSR — never returns secrets.
 */
export async function fetchStackStatus(): Promise<StackStatus> {
  return fetchJson<StackStatus>("/api/v1/ai-stack/status");
}

/**
 * Submit a demo run against the orchestrator. The free_diagnostic tier runs
 * in <50ms with deterministic handlers, so the call is fire-and-forget from
 * the client's perspective.
 */
export async function runDemo(
  body: RunRequestBody,
): Promise<AIStackResult> {
  return fetchJson<AIStackResult>("/api/v1/ai-stack/run", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

/**
 * List shadow-mode improvement proposals for a tenant. Always returns
 * pending_approval records — applying a proposal requires founder action.
 */
export interface ProposalsResponse {
  tenant_id: string;
  proposal_count: number;
  proposals: Array<{
    proposal_id: string;
    title: string;
    rationale: string;
    target_layer: string;
    state: string;
    created_at: string;
  }>;
}

export async function fetchProposals(
  tenantId: string,
  sinceDays = 30,
): Promise<ProposalsResponse> {
  const params = new URLSearchParams({ since_days: String(sinceDays) });
  return fetchJson<ProposalsResponse>(
    `/api/v1/ai-stack/proposals/${encodeURIComponent(tenantId)}?${params}`,
  );
}
