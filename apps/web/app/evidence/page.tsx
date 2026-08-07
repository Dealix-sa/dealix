"use client";

import { useCallback, useEffect, useState } from "react";

import { useAdminKey } from "@/hooks/useAdminKey";
import { api } from "@/lib/api";

// Evidence ledger event (shape is permissive — backend returns a list of events).
interface EvidenceEvent {
  id?: string;
  event_type?: string;
  entity_type?: string;
  entity_id?: string;
  summary?: string;
  created_at?: string;
  occurred_at?: string;
  [k: string]: unknown;
}

function eventList(data: unknown): EvidenceEvent[] {
  if (Array.isArray(data)) return data as EvidenceEvent[];
  const obj = (data ?? {}) as { events?: EvidenceEvent[]; items?: EvidenceEvent[] };
  return obj.events ?? obj.items ?? [];
}

export default function EvidencePage() {
  const { adminKey, setAdminKey, clearAdminKey, ready } = useAdminKey();
  const [keyInput, setKeyInput] = useState("");
  const [events, setEvents] = useState<EvidenceEvent[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!adminKey) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.getEvidenceLedger(adminKey);
      setEvents(eventList(res.data));
    } catch (e: unknown) {
      const status = (e as { response?: { status?: number } })?.response?.status;
      if (status === 401 || status === 403) {
        setError("مفتاح الأدمن غير صالح — Invalid admin key.");
        clearAdminKey();
        setEvents(null);
      } else {
        setError("تعذّر تحميل سجل الإثبات — Could not load the evidence ledger.");
      }
    } finally {
      setLoading(false);
    }
  }, [adminKey, clearAdminKey]);

  useEffect(() => {
    if (adminKey) load();
  }, [adminKey, load]);

  if (ready && !adminKey) {
    return (
      <main>
        <section className="card" style={{ maxWidth: 480, margin: "0 auto" }}>
          <p className="eyebrow">Evidence Ledger</p>
          <h1>سجل الإثبات</h1>
          <p className="stat-label" style={{ marginBottom: "var(--sp-3)" }}>
            أدخل مفتاح الأدمن للوصول · Enter your admin key
          </p>
          <input
            type="password"
            value={keyInput}
            onChange={(e) => setKeyInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && setAdminKey(keyInput)}
            placeholder="X-Admin-API-Key"
            className="form-control"
            style={{ marginBottom: "var(--sp-4)" }}
          />
          <div className="actions">
            <button className="btn btn-primary" onClick={() => setAdminKey(keyInput)}>دخول · Enter</button>
          </div>
          <p className="stat-label" style={{ marginTop: "var(--sp-4)", opacity: 0.7 }}>
            يُحفظ على جهازك فقط (localStorage) ولا يُرسل إلا لواجهة Dealix.
          </p>
        </section>
      </main>
    );
  }

  return (
    <main>
      <section style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "var(--sp-4)" }}>
        <div>
          <p className="eyebrow">Evidence Ledger</p>
          <h1>سجل الإثبات · Proof &amp; evidence</h1>
          <p className="stat-label">كل حدث مُوثّق يدعم الادعاءات التجارية (L0–L5) · Every logged proof event behind commercial claims</p>
        </div>
        <div className="actions" style={{ marginTop: 0 }}>
          <button className="btn btn-primary" onClick={load} disabled={loading}>{loading ? "تحديث…" : "تحديث · Refresh"}</button>
          <button className="btn btn-ghost" onClick={clearAdminKey}>تبديل المفتاح</button>
        </div>
      </section>

      {error && (
        <section className="card" style={{ borderColor: "rgba(239,68,68,0.4)" }}>
          <p style={{ color: "#f87171" }}>{error}</p>
        </section>
      )}

      {!events && loading && <section className="card"><p>جارٍ التحميل… · Loading…</p></section>}

      {events && (
        <section className="card">
          <h2>الأحداث · Events ({events.length})</h2>
          {events.length === 0 ? (
            <p className="stat-label" style={{ marginTop: "var(--sp-4)" }}>
              لا أحداث بعد — ستظهر هنا مع تقدّم التسليم. · No events yet — they appear as delivery progresses.
            </p>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "var(--sp-4)" }}>
              <thead>
                <tr>
                  <th style={{ textAlign: "start", padding: "8px", borderBottom: "1px solid rgba(255,255,255,.1)" }}>النوع / Type</th>
                  <th style={{ textAlign: "start", padding: "8px", borderBottom: "1px solid rgba(255,255,255,.1)" }}>الملخص / Summary</th>
                  <th style={{ textAlign: "start", padding: "8px", borderBottom: "1px solid rgba(255,255,255,.1)" }}>الكيان / Entity</th>
                  <th style={{ textAlign: "start", padding: "8px", borderBottom: "1px solid rgba(255,255,255,.1)" }}>التاريخ / When</th>
                </tr>
              </thead>
              <tbody>
                {events.map((ev, i) => (
                  <tr key={ev.id ?? i}>
                    <td style={{ padding: "8px", borderBottom: "1px solid rgba(255,255,255,.06)" }}>
                      <span className="badge badge-emerald">{ev.event_type ?? "event"}</span>
                    </td>
                    <td style={{ padding: "8px", borderBottom: "1px solid rgba(255,255,255,.06)" }}>{ev.summary ?? "—"}</td>
                    <td style={{ padding: "8px", borderBottom: "1px solid rgba(255,255,255,.06)" }} className="stat-label">
                      {[ev.entity_type, ev.entity_id].filter(Boolean).join(":") || "—"}
                    </td>
                    <td style={{ padding: "8px", borderBottom: "1px solid rgba(255,255,255,.06)" }} className="stat-label">
                      {(ev.occurred_at ?? ev.created_at ?? "").slice(0, 19).replace("T", " ") || "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      )}
    </main>
  );
}
