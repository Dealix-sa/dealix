"use client";

import { useCallback, useEffect, useState } from "react";

import MetricCard from "@/components/MetricCard";
import { StageBadge } from "@/components/crm/StageBadge";
import { useAdminKey } from "@/hooks/useAdminKey";
import { api } from "@/lib/api";

interface WarRoomRow {
  lead_id: string;
  target: string;
  segment?: string;
  offer?: string;
  next_action?: string;
  next_action_due?: string | null;
  status?: string;
  stage?: string;
  lead_score?: number;
}

interface Summary {
  generated_at?: string;
  today: { approved_touches_target: number; follow_ups_target: number; top_targets_count: number; follow_ups_due: number };
  revenue: { conversations: number; meetings: number; scopes: number; invoices: number; paid: number };
  queues: Record<string, number>;
  risks: Record<string, boolean>;
  top_targets: WarRoomRow[];
}

const QUEUE_LABELS: Record<string, string> = {
  needs_proof: "بحاجة إثبات · Needs proof",
  ready_meeting: "جاهز لاجتماع · Ready for meeting",
  needs_scope: "بحاجة نطاق · Needs scope",
  needs_invoice: "بحاجة فاتورة · Needs invoice",
  needs_delivery: "بحاجة تسليم · Needs delivery",
  upsell: "فرصة توسعة · Upsell",
};

const RISK_LABELS: Record<string, string> = {
  no_live_auto_send: "لا إرسال تلقائي · No auto-send",
  no_cold_whatsapp: "لا واتساب بارد · No cold WhatsApp",
  no_fake_proof: "لا إثبات زائف · No fake proof",
  no_revenue_claim_before_payment: "لا ادعاء إيراد قبل الدفع · No revenue claim before payment",
};

export default function WarRoomPage() {
  const { adminKey, setAdminKey, clearAdminKey, ready } = useAdminKey();
  const [keyInput, setKeyInput] = useState("");
  const [data, setData] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!adminKey) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.getWarRoomSummary(adminKey);
      setData(res.data as Summary);
    } catch (e: unknown) {
      const status = (e as { response?: { status?: number } })?.response?.status;
      if (status === 401 || status === 403) {
        setError("مفتاح الأدمن غير صالح — Invalid admin key.");
        clearAdminKey();
        setData(null);
      } else {
        setError("تعذّر تحميل غرفة الحرب — Could not load the war room.");
      }
    } finally {
      setLoading(false);
    }
  }, [adminKey, clearAdminKey]);

  useEffect(() => {
    if (!adminKey) return;
    load();
    const id = setInterval(load, 60_000);
    return () => clearInterval(id);
  }, [adminKey, load]);

  if (ready && !adminKey) {
    return (
      <main>
        <section className="card" style={{ maxWidth: 480, margin: "0 auto" }}>
          <p className="eyebrow">Founder War Room</p>
          <h1>غرفة حرب المؤسس</h1>
          <p className="stat-label" style={{ marginBottom: "var(--sp-3)" }}>أدخل مفتاح الأدمن · Enter your admin key</p>
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
          <p className="stat-label" style={{ marginTop: "var(--sp-4)", opacity: 0.7 }}>يُحفظ على جهازك فقط — لا يُرسل إلا لواجهة Dealix.</p>
        </section>
      </main>
    );
  }

  const s = data;
  const maxQueue = s ? Math.max(1, ...Object.values(s.queues)) : 1;

  return (
    <main>
      <section style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "var(--sp-4)" }}>
        <div>
          <p className="eyebrow">Founder War Room</p>
          <h1>غرفة حرب المؤسس · Daily CEO moves</h1>
          <p className="stat-label">شاشة واحدة كل صباح — أهم تحرّكات الإيراد اليوم، حيّة. · One live view, every morning.</p>
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

      {!data && loading && <section className="card"><p>جارٍ التحميل… · Loading…</p></section>}

      {s && (
        <>
          <section className="grid-3">
            <MetricCard value={String(s.revenue.conversations)} label="محادثات · Conversations" />
            <MetricCard value={String(s.revenue.meetings)} label="اجتماعات · Meetings" />
            <MetricCard value={String(s.revenue.scopes)} label="نطاقات · Scopes" />
            <MetricCard value={String(s.revenue.invoices)} label="فواتير · Invoices" />
            <MetricCard value={String(s.revenue.paid)} label="مدفوع · Paid" />
            <MetricCard value={`${s.today.follow_ups_due}/${s.today.follow_ups_target}`} label="متابعات مستحقة · Follow-ups due" />
          </section>

          <div className="grid-2">
            <article className="card">
              <h3>أهداف اليوم · Top targets ({s.top_targets.length})</h3>
              {s.top_targets.length === 0 ? (
                <p className="stat-label" style={{ marginTop: "var(--sp-4)" }}>لا أهداف بعد — أضف أول هدف عبر الـAPI أو الاستيراد. · No targets yet.</p>
              ) : (
                <ul style={{ listStyle: "none", padding: 0, marginTop: "var(--sp-4)" }}>
                  {s.top_targets.slice(0, 10).map((t) => (
                    <li key={t.lead_id} style={{ padding: "10px 0", borderBottom: "1px solid rgba(255,255,255,.07)" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", gap: 8, alignItems: "center" }}>
                        <b>{t.target}</b>
                        <StageBadge stage={t.stage || t.status || "new"} />
                      </div>
                      <div className="stat-label">{t.next_action || "—"}{t.next_action_due ? ` · ${t.next_action_due}` : ""}</div>
                    </li>
                  ))}
                </ul>
              )}
              <div className="actions">
                <a href="/founder/command-room">غرفة القيادة · Command Room</a>
                <a href="/approvals">الموافقات · Approvals</a>
                <a href="/evidence">سجل الإثبات · Evidence</a>
              </div>
            </article>

            <article className="card">
              <h3>الطوابير · Pipeline queues</h3>
              <div style={{ marginTop: "var(--sp-4)" }}>
                {Object.entries(s.queues).map(([k, v]) => (
                  <div key={k} style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
                    <span style={{ flex: "0 0 46%", fontSize: ".85rem" }}>{QUEUE_LABELS[k] ?? k}</span>
                    <span style={{ flex: 1, background: "rgba(255,255,255,.08)", borderRadius: 8, height: 16, overflow: "hidden", display: "block" }}>
                      <span style={{ display: "block", height: "100%", width: `${Math.round((v / maxQueue) * 100)}%`, background: "linear-gradient(90deg,#0066FF,#10B981)" }} />
                    </span>
                    <b style={{ flex: "0 0 28px", textAlign: "left" }}>{v}</b>
                  </div>
                ))}
              </div>
            </article>
          </div>

          <section className="card">
            <h3>حدود العقيدة · Operating guardrails</h3>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "var(--sp-3)", marginTop: "var(--sp-4)" }}>
              {Object.entries(s.risks).map(([k, ok]) => (
                <span key={k} className={`badge ${ok ? "badge-emerald" : "badge-coral"}`}>{ok ? "✓" : "✗"} {RISK_LABELS[k] ?? k}</span>
              ))}
            </div>
            <p className="stat-label" style={{ marginTop: "var(--sp-4)" }}>
              لا إرسال خارجي بدون مراجعتك — كل مسودة تحمل review_status. · No external action runs without human review.
            </p>
          </section>
        </>
      )}
    </main>
  );
}
