import fs from "node:fs";
import path from "node:path";

export interface Deliverable { id: string; title: string; status: string; completedAt?: string; due?: string; }
export interface Approval { id: string; item: string; status: string; requestedAt?: string; decidedAt?: string; reviewer?: string; }
export interface Risk { id: string; title: string; severity: string; openedAt?: string; }
export interface ProofItem { id: string; title: string; evidence: string; date: string; }
export interface Workspace {
  id: string;
  clientId: string;
  clientName: string;
  offer: string;
  status: string;
  startDate: string;
  nextReview?: string;
  deliverables: Deliverable[];
  approvals: Approval[];
  risks: Risk[];
  proofItems: ProofItem[];
}

const ROOT = path.join(process.cwd(), "..", "..");

function _read<T>(rel: string, fallback: T): T {
  try {
    const p = path.join(ROOT, rel);
    if (!fs.existsSync(p)) return fallback;
    return JSON.parse(fs.readFileSync(p, "utf-8")) as T;
  } catch { return fallback; }
}

export function loadDemoWorkspaces(): Workspace[] {
  const data = _read<{ workspaces: Workspace[] }>("business/_data/client_portal.demo.json", { workspaces: [] });
  return data.workspaces ?? [];
}

export function loadWorkspaces(): Workspace[] {
  const data = _read<{ workspaces: Workspace[] }>("business/_data/client_workspaces.json", { workspaces: [] });
  return data.workspaces ?? [];
}

export function findWorkspace(id: string): Workspace | undefined {
  return [...loadDemoWorkspaces(), ...loadWorkspaces()].find((w) => w.id === id || w.clientId === id);
}
