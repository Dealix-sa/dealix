"use client";

import { useCallback, useEffect, useState } from "react";

import { api } from "@/lib/api";

interface ApprovalItem {
  id?: string;
  approval_id?: string;
  ticketId?: string;
  action_type?: string;
  actionType?: string;
  requested_by?: string;
  requestedBy?: string;
  state?: string;
  status?: string;
  summary?: string;
  [k: string]: unknown;
}

const ACTOR = "founder";

function itemList(data: unknown): ApprovalItem[] {
  if (Array.isArray(data)) return data as ApprovalItem[];
  const obj = (data ?? {}) as { items?: ApprovalItem[]; pending?: ApprovalItem[] };
  return obj.items ?? obj.pending ?? [];
}

function idOf(it: ApprovalItem): string {
  return String(it.id ?? it.approval_id ?? it.ticketId ?? "");
}

export default function ApprovalsPage() {
  const [items, setItems] = useState<ApprovalItem[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getApprovalsPending();
      setItems(itemList(res.data));
    } catch {
      setError("تعذّر تحميل طابور الموافقات — Could not load the approvals queue.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const decide = useCallback(
    async (it: ApprovalItem, action: "approve" | "reject") => {
      const id = idOf(it);
      if (!id) return;
      setBusy(id);
      try {
        if (action === "approve") {
          await api.postApprovalApprove(id, ACTOR);
        } else {
          await api.postApprovalReject(id, ACTOR, "rejected from approvals console");
        }
        await load();
      } catch {
        setError("تعذّر تنفيذ القرار — The decision could not be recorded.");
      } finally {
        setBusy(null);
      }
    },
    [load],
  );

  return (
    <main>
      <section style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "var(--sp-4)" }}>
        <div>
          <p className="eyebrow">Approvals</p>
          <h1>طابور الموافقات · Approvals queue</h1>
          <p className="stat-label">لا إرسال خارجي بدون موافقتك — كل إجراء ينتظر هنا. · Nothing is sent externally without your approval.</p>
        </div>
        <div className="actions" style={{ marginTop: 0 }}>
          <button className="btn btn-primary" onClick={load} disabled={loading}>{loading ? "تحديث…" : "تحديث · Refresh"}</button>
        </div>
      </section>

      {error && (
        <section className="card" style={{ borderColor: "rgba(239,68,68,0.4)" }}>
          <p style={{ color: "#f87171" }}>{error}</p>
        </section>
      )}

      {!items && loading && <section className="card"><p>جارٍ التحميل… · Loading…</p></section>}

      {items && (
        <section className="card">
          <h2>المعلّقة · Pending ({items.length})</h2>
          {items.length === 0 ? (
            <p className="stat-label" style={{ marginTop: "var(--sp-4)" }}>
              لا إجراءات معلّقة الآن. · No pending actions right now.
            </p>
          ) : (
            <ul style={{ listStyle: "none", padding: 0, marginTop: "var(--sp-4)" }}>
              {items.map((it, i) => {
                const id = idOf(it) || String(i);
                return (
                  <li key={id} style={{ padding: "12px 0", borderBottom: "1px solid rgba(255,255,255,.07)", display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
                    <div>
                      <b>{it.action_type ?? it.actionType ?? it.summary ?? "action"}</b>
                      <div className="stat-label">
                        {(it.requested_by ?? it.requestedBy ?? "—")} · <span className="badge badge-amber">{it.state ?? it.status ?? "pending"}</span>
                      </div>
                    </div>
                    <div className="actions" style={{ marginTop: 0 }}>
                      <button className="btn btn-primary" disabled={busy === id} onClick={() => decide(it, "approve")}>موافقة · Approve</button>
                      <button className="btn btn-ghost" disabled={busy === id} onClick={() => decide(it, "reject")}>رفض · Reject</button>
                    </div>
                  </li>
                );
              })}
            </ul>
          )}
        </section>
      )}
    </main>
  );
}
