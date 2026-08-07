import fs from "node:fs";
import path from "node:path";

export interface Deal {
  id?: string;
  account_id?: string;
  accountId?: string;
  status?: string;
  stage?: string;
  offer?: string;
  setup_value?: number;
  setupValue?: number;
  monthly_value?: number;
  monthlyValue?: number;
  decided_at?: string;
  decidedAt?: string;
  decided_by?: string;
  decidedBy?: string;
  loss_reason?: string;
  lossReason?: string;
  demo?: boolean;
}

export interface Quote {
  id: string;
  accountId: string;
  offer: string;
  setupPrice: number;
  monthlyPrice: number;
  currency: string;
  scope?: string;
  outOfScope?: string;
  validUntil?: string;
  createdAt: string;
  status: string;
  reviewer?: string;
  demo?: boolean;
}

const ROOT = path.join(process.cwd(), "..", "..");

function _read<T>(rel: string, fallback: T): T {
  try {
    const p = path.join(ROOT, rel);
    if (!fs.existsSync(p)) return fallback;
    return JSON.parse(fs.readFileSync(p, "utf-8")) as T;
  } catch {
    return fallback;
  }
}

export function loadDeals(): Deal[] {
  const data = _read<{ deals: Deal[] }>("business/_data/deals.ledger.json", { deals: [] });
  return data.deals ?? [];
}

export function loadQuotes(): Quote[] {
  const data = _read<{ quotes: Quote[] }>("business/_data/quotes.index.json", { quotes: [] });
  return data.quotes ?? [];
}

export function dealStatus(d: Deal): string {
  return d.status ?? d.stage ?? "open";
}

export function setupValue(d: Deal): number {
  return Number(d.setup_value ?? d.setupValue ?? 0);
}

export function mrrValue(d: Deal): number {
  return Number(d.monthly_value ?? d.monthlyValue ?? 0);
}

export function summarizeDeals(deals: Deal[]) {
  const won = deals.filter((d) => dealStatus(d) === "won");
  const lost = deals.filter((d) => dealStatus(d) === "lost");
  const open = deals.filter((d) => dealStatus(d) === "open");
  return {
    won: won.length,
    lost: lost.length,
    open: open.length,
    wonSetup: won.reduce((s, d) => s + setupValue(d), 0),
    wonMrr: won.reduce((s, d) => s + mrrValue(d), 0),
    pipelineMrr: open.reduce((s, d) => s + mrrValue(d), 0),
    pipelineSetup: open.reduce((s, d) => s + setupValue(d), 0),
  };
}
