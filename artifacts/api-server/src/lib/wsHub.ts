import { WebSocketServer, WebSocket } from "ws";
import type { Server } from "http";
import { env } from "../env.js";

export interface AgentEvent {
  id: string;
  agentType: "outreach" | "scoring" | "compliance" | "intelligence" | "orchestrator";
  action: string;
  target: string;
  status: "running" | "completed" | "pending" | "failed";
  timestamp: string;
  duration?: number;
  metadata?: Record<string, unknown>;
  requiresApproval?: boolean;
}

const AGENT_TYPES: AgentEvent["agentType"][] = [
  "outreach",
  "scoring",
  "compliance",
  "intelligence",
  "orchestrator",
];

const ACTIONS_BY_TYPE: Record<AgentEvent["agentType"], string[]> = {
  outreach: [
    "Draft outreach for Aramco",
    "Send LinkedIn message to STC Solutions",
    "Schedule follow-up for SABIC",
    "Translate proposal to Arabic",
  ],
  scoring: [
    "Score lead: Neom Tech",
    "Recompute pipeline probability",
    "Detect at-risk deal",
    "Update engagement index",
  ],
  compliance: [
    "Run PDPL check on outbound",
    "Review contract clause v2",
    "Audit channel policy",
    "Verify consent token",
  ],
  intelligence: [
    "Enrich account: Maaden",
    "Pull news for top 10 accounts",
    "Detect competitor mention",
    "Summarize CRM activity",
  ],
  orchestrator: [
    "Run morning ops sequence",
    "Trigger weekly retro",
    "Compile founder daily pack",
    "Reconcile evidence ledger",
  ],
};

const SAUDI_COMPANIES = [
  "Aramco",
  "SABIC",
  "STC",
  "Neom",
  "Maaden",
  "Almarai",
  "Saudia",
  "stc Bank",
  "Riyad Bank",
  "Al Rajhi Bank",
  "Tabby",
  "Tamara",
  "Mrsool",
  "Foodics",
  "Salla",
  "Zid",
];

function rand<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)] as T;
}

function uid(): string {
  return Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
}

export class WsHub {
  private wss: WebSocketServer | null = null;
  private clients: Set<WebSocket> = new Set();
  private heartbeat: NodeJS.Timeout | null = null;
  private simulator: NodeJS.Timeout | null = null;

  attach(server: Server) {
    this.wss = new WebSocketServer({ noServer: true });

    server.on("upgrade", (req, socket, head) => {
      const url = req.url || "/";
      if (url.startsWith("/ws/agents") || url.startsWith("/ws")) {
        this.wss!.handleUpgrade(req, socket, head, (ws) => {
          this.wss!.emit("connection", ws, req);
        });
      } else {
        socket.destroy();
      }
    });

    this.wss.on("connection", (ws: WebSocket) => {
      this.clients.add(ws);
      ws.send(
        JSON.stringify({
          type: "hello",
          ts: new Date().toISOString(),
          message: "connected to dealix agent feed",
        }),
      );
      ws.on("close", () => this.clients.delete(ws));
      ws.on("error", () => this.clients.delete(ws));
    });

    this.startSimulator();
    this.startHeartbeat();
  }

  broadcast(event: AgentEvent | { type: string; [k: string]: unknown }) {
    const payload = JSON.stringify(event);
    for (const ws of this.clients) {
      if (ws.readyState === WebSocket.OPEN) {
        try {
          ws.send(payload);
        } catch {
          /* ignore */
        }
      }
    }
  }

  private startSimulator() {
    const interval = 5000 + Math.floor(Math.random() * 3000);
    this.simulator = setInterval(() => {
      if (this.clients.size === 0) return;
      const ev = this.makeSimulatedEvent();
      this.broadcast(ev);
    }, interval);
  }

  private startHeartbeat() {
    this.heartbeat = setInterval(() => {
      for (const ws of this.clients) {
        if (ws.readyState === WebSocket.OPEN) {
          try {
            ws.ping();
          } catch {
            /* ignore */
          }
        }
      }
    }, env.WS_HEARTBEAT_MS);
  }

  private makeSimulatedEvent(): AgentEvent {
    const agentType = rand(AGENT_TYPES);
    const action = rand(ACTIONS_BY_TYPE[agentType]);
    const status = (rand(["running", "completed", "completed", "pending"]) as AgentEvent["status"]);
    return {
      id: uid(),
      agentType,
      action,
      target: rand(SAUDI_COMPANIES),
      status,
      timestamp: new Date().toISOString(),
      duration: Math.floor(200 + Math.random() * 4500),
      requiresApproval: Math.random() < 0.12,
      metadata: { simulated: true },
    };
  }

  close() {
    if (this.simulator) clearInterval(this.simulator);
    if (this.heartbeat) clearInterval(this.heartbeat);
    this.wss?.close();
    for (const ws of this.clients) ws.close();
    this.clients.clear();
  }

  count(): number {
    return this.clients.size;
  }
}

export const wsHub = new WsHub();
