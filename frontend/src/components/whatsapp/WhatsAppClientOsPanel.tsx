"use client";

import { useEffect, useState } from "react";

import { Card } from "@/components/ui/card";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const BASE = `${API_BASE}/api/v1/whatsapp-client-os`;

export type WhatsAppView = "overview" | "sessions" | "action-cards" | "assessments";

interface Metrics {
  new_sessions?: number;
  assessments_started?: number;
  assessments_completed?: number;
  assessment_completion_rate?: number;
  permission_requests?: number;
  permission_approval_rate?: number;
  proposal_request_rate?: number;
  payment_handoff_rate?: number;
  human_handoff_count?: number;
  human_handoff_rate?: number;
  recommended_offers?: Record<string, number>;
  stages?: Record<string, number>;
}

interface PermissionLevel {
  level: string;
  meaning_ar: string;
  example_ar: string;
  risk: string;
  whatsapp_only_allowed: boolean;
}

interface SessionRow {
  session_id: string;
  company_name?: string;
  stage: string;
  permission_level: string;
  message_count: number;
  handoff_requested: boolean;
  assessment_id?: string;
}

interface ActionCardRow {
  card_id: string;
  kind: string;
  title_ar: string;
  risk: string;
  requires_approval: boolean;
  catalog_ref?: string;
}

interface AssessmentRow {
  assessment_id: string;
  company_name?: string;
  recommended_offer?: string;
  recommended_offer_ar?: string;
  completed: boolean;
  score?: { overall: number; risk: string } | null;
}

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return (await res.json()) as T;
}

export function WhatsAppClientOsPanel({
  view,
  locale,
}: {
  view: WhatsAppView;
  locale: string;
}) {
  const isAr = locale === "ar";
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [levels, setLevels] = useState<PermissionLevel[]>([]);
  const [sessions, setSessions] = useState<SessionRow[]>([]);
  const [cards, setCards] = useState<ActionCardRow[]>([]);
  const [assessments, setAssessments] = useState<AssessmentRow[]>([]);

  useEffect(() => {
    let active = true;
    async function load() {
      setLoading(true);
      setError(false);
      try {
        if (view === "overview") {
          const [m, p] = await Promise.all([
            getJson<Metrics>("/metrics"),
            getJson<{ levels: PermissionLevel[] }>("/permissions/levels"),
          ]);
          if (!active) return;
          setMetrics(m);
          setLevels(p.levels ?? []);
        } else if (view === "sessions") {
          const r = await getJson<{ sessions: SessionRow[] }>("/sessions?limit=100");
          if (active) setSessions(r.sessions ?? []);
        } else if (view === "action-cards") {
          const r = await getJson<{ action_cards: ActionCardRow[] }>("/action-cards?limit=100");
          if (active) setCards(r.action_cards ?? []);
        } else if (view === "assessments") {
          const r = await getJson<{ assessments: AssessmentRow[] }>("/assessments?limit=100");
          if (active) setAssessments(r.assessments ?? []);
        }
      } catch {
        if (active) setError(true);
      } finally {
        if (active) setLoading(false);
      }
    }
    void load();
    return () => {
      active = false;
    };
  }, [view]);

  if (loading) {
    return <p className="text-sm text-muted-foreground">{isAr ? "جارٍ التحميل…" : "Loading…"}</p>;
  }
  if (error) {
    return (
      <Card className="p-4 border-border/80">
        <p className="text-sm text-muted-foreground">
          {isAr
            ? "تعذّر الاتصال بالـ API. تأكد من تشغيل الخادم وضبط NEXT_PUBLIC_API_URL."
            : "Could not reach the API. Ensure the backend is running and NEXT_PUBLIC_API_URL is set."}
        </p>
      </Card>
    );
  }

  if (view === "overview") {
    const m = metrics ?? {};
    const stat = (label: string, value: number | undefined) => (
      <Card className="p-4 border-border/80" key={label}>
        <p className="text-xs text-muted-foreground">{label}</p>
        <p className="text-2xl font-semibold">{value ?? 0}</p>
      </Card>
    );
    return (
      <div className="space-y-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {stat(isAr ? "جلسات جديدة" : "New sessions", m.new_sessions)}
          {stat(isAr ? "تقييمات اكتملت" : "Assessments done", m.assessments_completed)}
          {stat(isAr ? "طلبات صلاحيات" : "Permission requests", m.permission_requests)}
          {stat(isAr ? "تحويلات بشرية" : "Human handoffs", m.human_handoff_count)}
        </div>
        <Card className="p-4 border-border/80">
          <h2 className="font-semibold text-sm mb-2">
            {isAr ? "سلّم الصلاحيات L0–L5" : "Permission ladder L0–L5"}
          </h2>
          <ul className="text-xs space-y-1">
            {levels.map((l) => (
              <li key={l.level} className="flex gap-2">
                <span className="font-mono">{l.level}</span>
                <span className="text-muted-foreground">{l.meaning_ar}</span>
                {!l.whatsapp_only_allowed && (
                  <span className="text-amber-600">
                    {isAr ? "(لا يتم عبر واتساب وحده)" : "(not WhatsApp-only)"}
                  </span>
                )}
              </li>
            ))}
          </ul>
        </Card>
        <p className="text-xs text-muted-foreground" dir="ltr">
          GET /api/v1/whatsapp-client-os/metrics
        </p>
      </div>
    );
  }

  if (view === "sessions") {
    if (sessions.length === 0) {
      return <EmptyState isAr={isAr} />;
    }
    return (
      <div className="space-y-2">
        {sessions.map((s) => (
          <Card key={s.session_id} className="p-3 border-border/80">
            <div className="flex justify-between text-sm">
              <span className="font-medium">{s.company_name || s.session_id}</span>
              <span className="text-muted-foreground">{s.stage}</span>
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {isAr ? "صلاحية" : "perm"}: {s.permission_level} · {isAr ? "رسائل" : "msgs"}:{" "}
              {s.message_count}
              {s.handoff_requested && (
                <span className="text-amber-600"> · {isAr ? "تحويل بشري" : "handoff"}</span>
              )}
            </p>
          </Card>
        ))}
      </div>
    );
  }

  if (view === "action-cards") {
    if (cards.length === 0) {
      return <EmptyState isAr={isAr} />;
    }
    return (
      <div className="space-y-2">
        {cards.map((c) => (
          <Card key={c.card_id} className="p-3 border-border/80">
            <div className="flex justify-between text-sm">
              <span className="font-medium">{c.title_ar}</span>
              <span className="text-muted-foreground">{c.kind}</span>
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {isAr ? "مخاطرة" : "risk"}: {c.risk}
              {c.requires_approval && (
                <span className="text-amber-600"> · {isAr ? "يحتاج موافقة" : "needs approval"}</span>
              )}
              {c.catalog_ref ? ` · ${c.catalog_ref}` : ""}
            </p>
          </Card>
        ))}
      </div>
    );
  }

  // assessments
  if (assessments.length === 0) {
    return <EmptyState isAr={isAr} />;
  }
  return (
    <div className="space-y-2">
      {assessments.map((a) => (
        <Card key={a.assessment_id} className="p-3 border-border/80">
          <div className="flex justify-between text-sm">
            <span className="font-medium">{a.company_name || a.assessment_id}</span>
            <span className="text-muted-foreground">
              {a.score ? `${a.score.overall}/100 · ${a.score.risk}` : "—"}
            </span>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            {isAr ? "التوصية" : "Recommended"}: {a.recommended_offer_ar || a.recommended_offer || "—"}
            {a.completed ? "" : ` · ${isAr ? "غير مكتمل" : "in progress"}`}
          </p>
        </Card>
      ))}
    </div>
  );
}

function EmptyState({ isAr }: { isAr: boolean }) {
  return (
    <Card className="p-4 border-border/80">
      <p className="text-sm text-muted-foreground">
        {isAr
          ? "لا توجد بيانات بعد — تُنشأ عبر POST /api/v1/whatsapp-client-os/message."
          : "No data yet — created via POST /api/v1/whatsapp-client-os/message."}
      </p>
    </Card>
  );
}
