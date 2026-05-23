"use client";

// Founder Console v4 — live approvals queue.
// Renders the approval queue from the internal API and submits
// approve / reject / request-edit decisions, each of which writes
// an audit row server-side before this view refreshes.

import { useState, useTransition } from "react";

import {
  submitApprovalDecision,
  type ApprovalDecisionKind,
  type ApprovalDecisionResult
} from "../../lib/dealix-actions";
import type { ApprovalItem } from "../../lib/dealix-runtime";

type Props = {
  initialItems: ApprovalItem[];
};

type DecisionLogEntry = {
  approvalId: string;
  result: ApprovalDecisionResult;
};

const ACTIONS: { kind: ApprovalDecisionKind; label: string }[] = [
  { kind: "approve", label: "Approve" },
  { kind: "request-edit", label: "Request edit" },
  { kind: "reject", label: "Reject" }
];

export function LiveApprovalsQueue({ initialItems }: Props) {
  const [items, setItems] = useState(initialItems);
  const [reasonByItem, setReasonByItem] = useState<Record<string, string>>({});
  const [log, setLog] = useState<DecisionLogEntry[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  async function handleDecision(item: ApprovalItem, kind: ApprovalDecisionKind) {
    setError(null);
    try {
      const result = await submitApprovalDecision(item.id, {
        decision: kind,
        reason: reasonByItem[item.id]?.trim() || undefined
      });
      startTransition(() => {
        setLog((prev) => [{ approvalId: item.id, result }, ...prev].slice(0, 20));
        setItems((prev) => prev.filter((row) => row.id !== item.id));
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  if (items.length === 0 && log.length === 0) {
    return (
      <div className="card">
        <p style={{ margin: 0 }}>Approval queue is empty.</p>
      </div>
    );
  }

  return (
    <div className="grid">
      {error ? (
        <div
          className="card"
          style={{
            background: "#fef2f2",
            borderColor: "#fecaca",
            color: "#991b1b"
          }}
        >
          {error}
        </div>
      ) : null}

      {items.map((item) => (
        <article key={item.id} className="card">
          <header
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "baseline",
              gap: 8,
              flexWrap: "wrap"
            }}
          >
            <div>
              <div style={{ fontSize: 12, color: "#64748b" }}>
                {item.approval_class} · {item.risk_level} · {item.type}
              </div>
              <h3 style={{ margin: "4px 0 0" }}>{item.company || "(no company)"}</h3>
            </div>
            <code style={{ fontSize: 12, color: "#64748b" }}>{item.id}</code>
          </header>

          <p style={{ marginTop: 8 }}>{item.summary || "(no summary)"}</p>
          {item.recommended_action ? (
            <p style={{ marginTop: 4, color: "#475569" }}>
              <strong>Recommended:</strong> {item.recommended_action}
            </p>
          ) : null}
          {item.evidence ? (
            <p style={{ marginTop: 4, color: "#475569", fontSize: 13 }}>
              <strong>Evidence:</strong> {item.evidence}
            </p>
          ) : null}

          <label
            style={{ display: "block", marginTop: 12, fontSize: 12, color: "#475569" }}
          >
            Reason / note
            <textarea
              rows={2}
              value={reasonByItem[item.id] ?? ""}
              onChange={(e) =>
                setReasonByItem((prev) => ({ ...prev, [item.id]: e.target.value }))
              }
              style={{
                width: "100%",
                marginTop: 4,
                padding: 8,
                borderRadius: 8,
                border: "1px solid #e2e8f0",
                fontFamily: "inherit"
              }}
            />
          </label>

          <div style={{ display: "flex", gap: 8, marginTop: 12, flexWrap: "wrap" }}>
            {ACTIONS.map((action) => (
              <button
                key={action.kind}
                type="button"
                disabled={isPending}
                onClick={() => handleDecision(item, action.kind)}
                style={{
                  padding: "8px 14px",
                  borderRadius: 8,
                  border: "1px solid #cbd5f5",
                  background: action.kind === "approve" ? "#0f172a" : "#fff",
                  color: action.kind === "approve" ? "#fff" : "#0f172a",
                  cursor: isPending ? "not-allowed" : "pointer"
                }}
              >
                {action.label}
              </button>
            ))}
          </div>
        </article>
      ))}

      {log.length > 0 ? (
        <section className="card">
          <h3 style={{ marginTop: 0 }}>Recent decisions (audit written)</h3>
          <ul style={{ margin: 0, paddingLeft: 16 }}>
            {log.map((entry) => (
              <li key={`${entry.approvalId}-${entry.result.timestamp}`}>
                <code>{entry.approvalId}</code> · {entry.result.status} ·{" "}
                policy={entry.result.policy_result} · external_allowed=
                {String(entry.result.external_action_allowed)} · {entry.result.timestamp}
              </li>
            ))}
          </ul>
        </section>
      ) : null}
    </div>
  );
}
