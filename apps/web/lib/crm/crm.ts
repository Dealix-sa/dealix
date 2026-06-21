import fs from "node:fs";
import path from "node:path";

export interface Account {
  id: string;
  name: string;
  segment: string;
  city: string;
  sourceType: string;
  sourceNote: string;
  visibleSignal: string;
  weaknessHypothesis: string;
  recommendedOffer: string;
  score: number;
  stage: string;
  owner: string;
  reviewStatus: string;
  demo: boolean;
  createdAt: string;
  nextAction: string;
  nextActionDate: string;
  monthlyValue: number;
  setupValue: number;
}

export interface OutreachDraft {
  id: string;
  accountId: string;
  channel: string;
  language: string;
  body: string;
  createdAt: string;
  reviewStatus: string;
  reviewer?: string;
  decidedAt?: string;
  rejectionReason?: string;
  demo: boolean;
}

const ROOT = path.join(process.cwd(), "..", "..");

function _read<T>(rel: string, fallback: T): T {
  try {
    const p = path.join(ROOT, rel);
    if (!fs.existsSync(p)) return fallback;
    const raw = fs.readFileSync(p, "utf-8");
    return JSON.parse(raw) as T;
  } catch {
    return fallback;
  }
}

export function loadAccounts(): Account[] {
  const data = _read<{ accounts: Account[] }>("business/_data/scored_leads.json", { accounts: [] });
  return data.accounts ?? [];
}

export function loadOutreachQueue(): OutreachDraft[] {
  const data = _read<{ drafts: OutreachDraft[] }>("business/_data/outreach_review_queue.json", { drafts: [] });
  return data.drafts ?? [];
}

export function summarize(accounts: Account[]) {
  const stages = new Map<string, number>();
  for (const a of accounts) stages.set(a.stage, (stages.get(a.stage) ?? 0) + 1);
  const totalMrr = accounts.reduce((s, a) => s + (a.monthlyValue ?? 0), 0);
  const totalSetup = accounts.reduce((s, a) => s + (a.setupValue ?? 0), 0);
  return {
    count: accounts.length,
    stages: Array.from(stages.entries()).map(([stage, count]) => ({ stage, count })),
    pipelineMrr: totalMrr,
    pipelineSetup: totalSetup,
    avgScore: accounts.length ? Math.round(accounts.reduce((s, a) => s + a.score, 0) / accounts.length) : 0,
  };
}

export function pendingReviewCount(drafts: OutreachDraft[]): number {
  return drafts.filter((d) => (d.reviewStatus ?? "").includes("pending")).length;
}
