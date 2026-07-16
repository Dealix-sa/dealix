"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

import MetricCard from "@/components/MetricCard";
import { api } from "@/lib/api";

interface Snapshot {
  tenant_id: string;
  counts: {
    sources: number;
    signals: number;
    objectives: number;
    relationships: number;
    opportunities: number;
    opportunity_signal_edges: number;
  };
  high_priority_opportunities: number;
  external_action_allowed: boolean;
}

interface SourceScorecard {
  source_id: string;
  name: string;
  policy_status: string;
  source_score: number;
  signals: number;
  stale_signals: number;
  average_signal_confidence: number;
}

interface Objective {
  id: string;
  department: string;
  objective: string;
  metric: string;
  target_value: number | null;
  target_unit: string | null;
  priority: number;
  evidence_required: string;
}

interface Opportunity {
  id: string;
  company_name: string;
  title: string;
  offer_id: string;
  stage: string;
  evidence_level: string;
  score: number;
  confidence_band: string;
  blockers: string[];
  next_action: string;
  proof_target: string;
  approval_required: boolean;
  external_action_allowed: boolean;
}

interface BuyerDecisionPlan {
  plan_id: string;
  opportunity_id: string;
  mode: string;
  persuasion_thesis_ar: string;
  offer_architecture: {
    recommended_motion: string;
    duration_days: number;
    price_status: string;
    price_sar: number | null;
  };
  buying_committee: Array<{
    role: string;
    decision_question_ar: string;
    value_frame_ar: string;
    proof_required: string;
  }>;
  approval_queue: Array<{
    id: string;
    owner: string;
    question_ar: string;
  }>;
  blockers: string[];
  price_included: boolean;
  external_action_allowed: boolean;
}

const POLICY_LABELS: Record<string, string> = {
  approved: "معتمد · Approved",
  research_only: "بحث فقط · Research only",
  review_required: "يتطلب مراجعة · Review required",
  blocked: "محظور · Blocked",
};

const EVIDENCE_LABELS: Record<string, string> = {
  l0_unknown: "L0 · غير معروف",
  l1_hypothesis: "L1 · فرضية",
  l2_public_signal: "L2 · إشارة عامة",
  l3_first_party: "L3 · تحقق مباشر",
  l4_verified: "L4 · موثّق",
  l5_measured_outcome: "L5 · نتيجة مقاسة",
};

export default function CommercialIntelligencePage() {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [sources, setSources] = useState<SourceScorecard[]>([]);
  const [objectives, setObjectives] = useState<Objective[]>([]);
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [planLoadingId, setPlanLoadingId] = useState("");
  const [decisionPlan, setDecisionPlan] = useState<BuyerDecisionPlan | null>(null);
  const [error, setError] = useState<"auth" | "load" | null>(null);
  const [refreshedAt, setRefreshedAt] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [snapshotResponse, sourceResponse, objectiveResponse, opportunityResponse] =
        await Promise.all([
          api.getCommercialIntelligenceSnapshot(),
          api.getCommercialIntelligenceSourceScorecards(),
          api.getCommercialIntelligenceObjectives(),
          api.getCommercialIntelligenceOpportunities(),
        ]);
      setSnapshot(snapshotResponse.data as Snapshot);
      setSources((sourceResponse.data as { items: SourceScorecard[] }).items);
      setObjectives((objectiveResponse.data as { items: Objective[] }).items);
      setOpportunities((opportunityResponse.data as { items: Opportunity[] }).items);
      setRefreshedAt(new Date().toLocaleTimeString("ar-SA"));
    } catch (reason: unknown) {
      const status = (reason as { response?: { status?: number } })?.response?.status;
      setError(status === 401 || status === 403 ? "auth" : "load");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const buildDecisionPlan = useCallback(async (opportunityId: string) => {
    setPlanLoadingId(opportunityId);
    setError(null);
    try {
      const response = await api.postCommercialIntelligenceBuyerDecisionPlan(
        opportunityId,
        {},
      );
      setDecisionPlan(response.data as BuyerDecisionPlan);
    } catch (reason: unknown) {
      const status = (reason as { response?: { status?: number } })?.response?.status;
      setError(status === 401 || status === 403 ? "auth" : "load");
    } finally {
      setPlanLoadingId("");
    }
  }, []);

  return (
    <main>
      <section
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          flexWrap: "wrap",
          gap: "var(--sp-4)",
        }}
      >
        <div>
          <p className="eyebrow">Governed Commercial Intelligence</p>
          <h1>الذكاء التجاري المحكوم</h1>
          <p className="stat-label">
            المصادر ← الأدلة ← أهداف الإدارات ← العلاقات ← الفرص
            {refreshedAt && ` · آخر تحديث ${refreshedAt}`}
          </p>
        </div>
        <div className="actions" style={{ marginTop: 0 }}>
          <button className="btn btn-primary" onClick={load} disabled={loading}>
            {loading ? "تحديث…" : "تحديث البيانات"}
          </button>
          <Link className="btn btn-ghost" href="/founder/command-room">
            غرفة القيادة
          </Link>
        </div>
      </section>

      {error && (
        <section className="card" style={{ borderColor: "rgba(239,68,68,0.4)" }}>
          <h3>{error === "auth" ? "الدخول بحساب المستأجر مطلوب" : "تعذّر تحميل البيانات"}</h3>
          <p>
            {error === "auth"
              ? "هذه اللوحة معزولة حسب المنشأة. سجّل الدخول بحساب Dealix المصرّح له ثم أعد المحاولة."
              : "تحقق من اتصال API ومن تطبيق مهاجرة قاعدة البيانات الجديدة."}
          </p>
          {error === "auth" && (
            <div className="actions">
              <Link href="/login">تسجيل الدخول · Login</Link>
            </div>
          )}
        </section>
      )}

      {loading && !snapshot && !error && (
        <section className="card"><p>جارٍ بناء صورة القرار…</p></section>
      )}

      {snapshot && (
        <>
          <section className="card card-gold">
            <span className="badge badge-emerald">Evidence-governed</span>
            <h3 style={{ marginTop: "var(--sp-4)" }}>حدود التشغيل ثابتة</h3>
            <p>
              اللوحة تقرأ وتحلل فقط. لا إرسال ولا تواصل ولا تغيير مرحلة تجارية خارجية دون موافقة بشرية موثقة.
            </p>
          </section>

          <section className="grid-3">
            <MetricCard value={String(snapshot.counts.sources)} label="مصادر محكومة · Sources" />
            <MetricCard value={String(snapshot.counts.signals)} label="إشارات بأدلة · Signals" />
            <MetricCard value={String(snapshot.counts.objectives)} label="أهداف إدارات · Objectives" />
            <MetricCard value={String(snapshot.counts.relationships)} label="علاقات استراتيجية · Relationships" />
            <MetricCard value={String(snapshot.counts.opportunities)} label="فرص حقيقية · Opportunities" />
            <MetricCard
              value={String(snapshot.high_priority_opportunities)}
              label="أولوية عالية · High priority"
            />
          </section>

          <section className="grid-2">
            <article className="card">
              <h3>لوحات جودة المصادر · Source scorecards</h3>
              {sources.length === 0 ? (
                <p>لا توجد مصادر مسجلة بعد. ابدأ من سجل المصادر المحكوم.</p>
              ) : (
                <div style={{ marginTop: "var(--sp-4)" }}>
                  {sources.slice(0, 10).map((source) => (
                    <div
                      key={source.source_id}
                      style={{ padding: "12px 0", borderBottom: "1px solid rgba(255,255,255,.07)" }}
                    >
                      <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                        <b>{source.name}</b>
                        <span className={`badge ${source.source_score >= 75 ? "badge-emerald" : "badge-amber"}`}>
                          {source.source_score}/100
                        </span>
                      </div>
                      <p className="stat-label">
                        {POLICY_LABELS[source.policy_status] ?? source.policy_status} · {source.signals} إشارات · {source.stale_signals} قديمة
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </article>

            <article className="card">
              <h3>أهداف الإدارات · Department objectives</h3>
              {objectives.length === 0 ? (
                <p>لا توجد أهداف مفعلة بعد.</p>
              ) : (
                <ol style={{ marginTop: "var(--sp-4)", paddingInlineStart: 20 }}>
                  {objectives.slice(0, 10).map((objective) => (
                    <li key={objective.id} style={{ marginBottom: 12 }}>
                      <b>{objective.department} · {objective.metric}</b>
                      <div className="stat-label">{objective.objective}</div>
                      <span className="badge badge-gold">
                        {EVIDENCE_LABELS[objective.evidence_required] ?? objective.evidence_required}
                      </span>
                    </li>
                  ))}
                </ol>
              )}
            </article>
          </section>

          <section className="card">
            <h3>طابور الفرص المبني على الدليل · Evidence opportunity queue</h3>
            {opportunities.length === 0 ? (
              <p>
                لا توجد فرص حقيقية بعد — وهذا أفضل من بيانات مصطنعة. أضف إشارة مصرّح بها، اربطها بهدف إداري، ثم اطلب مراجعة الفرصة.
              </p>
            ) : (
              <div style={{ overflowX: "auto", marginTop: "var(--sp-4)" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", minWidth: 760 }}>
                  <thead>
                    <tr>
                      {[
                        "الشركة / الفرصة",
                        "المرحلة",
                        "الدليل",
                        "الدرجة",
                        "الإجراء التالي",
                        "الاعتماد",
                        "مسار القرار",
                      ].map((label) => (
                        <th key={label} style={{ textAlign: "right", padding: 12, borderBottom: "1px solid rgba(255,255,255,.12)" }}>
                          {label}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {opportunities.map((opportunity) => (
                      <tr key={opportunity.id}>
                        <td style={{ padding: 12, borderBottom: "1px solid rgba(255,255,255,.07)" }}>
                          <b>{opportunity.company_name}</b>
                          <div className="stat-label">{opportunity.title}</div>
                        </td>
                        <td style={{ padding: 12 }}>{opportunity.stage}</td>
                        <td style={{ padding: 12 }}>{EVIDENCE_LABELS[opportunity.evidence_level] ?? opportunity.evidence_level}</td>
                        <td style={{ padding: 12 }}><span className="badge badge-gold">{opportunity.score}/100</span></td>
                        <td style={{ padding: 12 }}>{opportunity.next_action}</td>
                        <td style={{ padding: 12 }}>
                          <span className="badge badge-amber">
                            {opportunity.approval_required ? "موافقة مطلوبة" : "—"}
                          </span>
                        </td>
                        <td style={{ padding: 12 }}>
                          <button
                            className="btn btn-ghost"
                            onClick={() => void buildDecisionPlan(opportunity.id)}
                            disabled={planLoadingId === opportunity.id}
                          >
                            {planLoadingId === opportunity.id ? "يبني…" : "بناء الحجة"}
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>

          {decisionPlan && (
            <section className="card card-gold" aria-live="polite">
              <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap" }}>
                <div>
                  <p className="eyebrow">Buyer Decision Spine · Internal draft</p>
                  <h3>مسار قرار لجنة الشراء</h3>
                </div>
                <span className="badge badge-amber">
                  {decisionPlan.offer_architecture.duration_days} يوماً · السعر محجوب
                </span>
              </div>
              <p>{decisionPlan.persuasion_thesis_ar}</p>
              <div className="grid-3" style={{ marginTop: "var(--sp-4)" }}>
                {decisionPlan.buying_committee.map((member) => (
                  <article className="card" key={member.role}>
                    <span className="badge badge-gold">{member.role}</span>
                    <h4>{member.decision_question_ar}</h4>
                    <p>{member.value_frame_ar}</p>
                    <p className="stat-label">الدليل: {member.proof_required}</p>
                  </article>
                ))}
              </div>
              <div className="grid-2" style={{ marginTop: "var(--sp-4)" }}>
                <article>
                  <h4>ما يمنع الانتقال</h4>
                  <ul>
                    {decisionPlan.blockers.map((blocker) => <li key={blocker}>{blocker}</li>)}
                  </ul>
                </article>
                <article>
                  <h4>طابور الموافقات</h4>
                  <ul>
                    {decisionPlan.approval_queue.map((item) => (
                      <li key={item.id}>{item.question_ar} · {item.owner}</li>
                    ))}
                  </ul>
                </article>
              </div>
              <p className="stat-label">
                لا سعر، لا إرسال، ولا التزام خارجي من هذه الشاشة. كل مخرج مسودة داخلية.
              </p>
            </section>
          )}
        </>
      )}
    </main>
  );
}
