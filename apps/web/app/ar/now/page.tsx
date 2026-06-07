"use client";

import { useEffect, useState } from "react";
import {
  approveDraft,
  buildMailto,
  buildWhatsapp,
  getNowPack,
  rejectDraft,
} from "../../../lib/api";
import type {
  NowDraft,
  NowLead,
  NowPack,
  TierColor,
} from "../../../lib/now-types";

// ── Helpers ──────────────────────────────────────────────────────────────

const sar = (n: number) =>
  new Intl.NumberFormat("en-US").format(Math.round(n));

const tierStyles: Record<
  TierColor,
  { dot: string; text: string; border: string; bg: string }
> = {
  green: {
    dot: "bg-emerald-400",
    text: "text-emerald-300",
    border: "border-emerald-400/40",
    bg: "bg-emerald-400/10",
  },
  yellow: {
    dot: "bg-amber-400",
    text: "text-amber-300",
    border: "border-amber-400/40",
    bg: "bg-amber-400/10",
  },
  orange: {
    dot: "bg-orange-400",
    text: "text-orange-300",
    border: "border-orange-400/40",
    bg: "bg-orange-400/10",
  },
  red: {
    dot: "bg-red-400",
    text: "text-red-300",
    border: "border-red-400/40",
    bg: "bg-red-400/10",
  },
};

const tierLabel: Record<string, string> = {
  high: "أولوية عالية",
  medium: "مرشحة",
  nurture: "متابعة لاحقة",
  disqualified: "مستبعدة",
};

function barColor(color: TierColor) {
  return tierStyles[color]?.dot ?? "bg-cyan-400";
}

// ── Loading skeleton ─────────────────────────────────────────────────────

function Skeleton() {
  return (
    <div className="animate-pulse space-y-8">
      <div className="h-10 w-2/3 rounded-2xl bg-white/[0.06]" />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className="h-28 rounded-3xl bg-white/[0.04]" />
        ))}
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="h-40 rounded-3xl bg-white/[0.04]" />
        ))}
      </div>
      <div className="h-64 rounded-3xl bg-white/[0.04]" />
    </div>
  );
}

// ── Lead row (expandable) ──────────────────────────────────────────────────

function LeadCard({ lead }: { lead: NowLead }) {
  const [open, setOpen] = useState(false);
  const t = tierStyles[lead.tier_color] ?? tierStyles.green;

  return (
    <article
      className={`rounded-3xl border ${t.border} bg-white/[0.03] p-6 transition`}
    >
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-3">
            <h3 className="text-lg font-black text-slate-100">
              {lead.company_name}
            </h3>
            <span
              className={`inline-flex items-center gap-1.5 rounded-full border ${t.border} ${t.bg} px-3 py-1 text-xs font-bold ${t.text}`}
            >
              <span className={`h-1.5 w-1.5 rounded-full ${t.dot}`} />
              {tierLabel[lead.tier] ?? lead.tier}
            </span>
          </div>
          <p className="mt-1 text-sm text-slate-400">
            {lead.sector_ar} · {lead.city}
          </p>
        </div>
        <div className="text-left">
          <div className="text-2xl font-black text-slate-100">
            {lead.fit_score}
            <span className="text-sm font-semibold text-slate-500">/100</span>
          </div>
          <p className="text-xs text-slate-500">درجة الملاءمة</p>
        </div>
      </div>

      {/* fit bar */}
      <div className="mt-4 h-2 w-full overflow-hidden rounded-full bg-white/[0.06]">
        <div
          className={`h-full rounded-full ${barColor(lead.tier_color)}`}
          style={{ width: `${Math.max(0, Math.min(100, lead.fit_score))}%` }}
        />
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <div className="rounded-2xl border border-white/10 bg-white/[0.02] px-4 py-3">
          <p className="text-xs text-slate-500">العرض المقترح</p>
          <p className="mt-1 text-sm font-bold text-cyan-200">
            {lead.recommended_offer.name_ar}
          </p>
        </div>
        <div className="rounded-2xl border border-white/10 bg-white/[0.02] px-4 py-3">
          <p className="text-xs text-slate-500">جهة الشراء المستهدفة</p>
          <p className="mt-1 text-sm font-bold text-slate-200">
            {lead.best_buyer_title}
          </p>
        </div>
      </div>

      <p className={`mt-3 text-sm ${t.text}`}>{lead.tier_action_ar}</p>

      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="mt-4 text-sm font-semibold text-cyan-300 hover:text-cyan-200"
      >
        {open ? "إخفاء التفاصيل ▲" : "عرض التفاصيل ▼"}
      </button>

      {open && (
        <div className="mt-4 space-y-5 border-t border-white/10 pt-5">
          {/* dimension scores */}
          {lead.dimension_scores.length > 0 && (
            <div>
              <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-500">
                أبعاد التقييم
              </p>
              <div className="grid gap-2 sm:grid-cols-2">
                {lead.dimension_scores.map((d) => (
                  <div
                    key={d.id}
                    className="flex items-center justify-between rounded-xl border border-white/10 bg-white/[0.02] px-3 py-2 text-xs"
                  >
                    <span className="text-slate-400" dir="ltr">
                      {d.id}
                    </span>
                    <span className="font-bold text-slate-200">
                      {d.score} · {d.level}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="grid gap-5 sm:grid-cols-2">
            {lead.top_strengths.length > 0 && (
              <div>
                <p className="mb-2 text-xs font-bold uppercase tracking-wide text-emerald-300">
                  نقاط القوة
                </p>
                <ul className="space-y-1.5">
                  {lead.top_strengths.map((s) => (
                    <li
                      key={s}
                      className="flex items-start gap-2 text-sm text-slate-300"
                    >
                      <span className="mt-0.5 text-emerald-400">+</span>
                      {s}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {lead.top_weaknesses.length > 0 && (
              <div>
                <p className="mb-2 text-xs font-bold uppercase tracking-wide text-orange-300">
                  نقاط الضعف
                </p>
                <ul className="space-y-1.5">
                  {lead.top_weaknesses.map((w) => (
                    <li
                      key={w}
                      className="flex items-start gap-2 text-sm text-slate-300"
                    >
                      <span className="mt-0.5 text-orange-400">−</span>
                      {w}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {lead.pain_points.length > 0 && (
            <div>
              <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-500">
                نقاط الألم
              </p>
              <div className="flex flex-wrap gap-2">
                {lead.pain_points.map((p) => (
                  <span
                    key={p}
                    className="rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 text-xs text-slate-300"
                  >
                    {p}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="rounded-2xl border border-cyan-400/20 bg-cyan-400/5 px-4 py-3">
            <p className="text-xs font-bold text-cyan-300">
              لماذا {lead.recommended_offer.name_ar}؟
            </p>
            <p className="mt-1 text-sm leading-7 text-slate-300">
              {lead.recommended_offer.why_fit_ar}
            </p>
          </div>
        </div>
      )}
    </article>
  );
}

// ── Draft card ──────────────────────────────────────────────────────────────

type DraftState = {
  status: "idle" | "approved" | "rejected";
  message?: string;
  copied: boolean;
};

function DraftCard({ draft }: { draft: NowDraft }) {
  const [state, setState] = useState<DraftState>({
    status: "idle",
    copied: false,
  });
  const [busy, setBusy] = useState(false);

  const handleCopy = async () => {
    const text = `${draft.subject}\n\n${draft.body}`;
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      // clipboard blocked — fall back to a temporary textarea
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy");
      } catch {
        /* noop */
      }
      document.body.removeChild(ta);
    }
    setState((s) => ({ ...s, copied: true }));
    setTimeout(() => setState((s) => ({ ...s, copied: false })), 2000);
  };

  const handleApprove = async () => {
    setBusy(true);
    const res = await approveDraft(draft.id);
    setBusy(false);
    setState((s) => ({ ...s, status: "approved", message: res.status }));
  };

  const handleReject = async () => {
    setBusy(true);
    const res = await rejectDraft(draft.id);
    setBusy(false);
    setState((s) => ({ ...s, status: "rejected", message: res.status }));
  };

  const rejected = state.status === "rejected";
  const approved = state.status === "approved";

  return (
    <article
      className={`rounded-3xl border border-white/10 bg-white/[0.03] p-6 transition ${
        rejected ? "opacity-50 grayscale" : ""
      }`}
    >
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-xs text-slate-500">{draft.company_name}</p>
          <h3 className="mt-1 text-lg font-black leading-7 text-slate-100">
            {draft.subject}
          </h3>
        </div>
        <div className="flex flex-wrap gap-2">
          <span className="rounded-full border border-emerald-400/30 bg-emerald-400/10 px-3 py-1 text-xs font-bold text-emerald-300">
            أمان {draft.safety.safety_score}
          </span>
          <span className="rounded-full border border-violet-400/30 bg-violet-400/10 px-3 py-1 text-xs font-bold text-violet-300">
            تخصيص {draft.safety.personalization_score}
          </span>
          <span className="rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 text-xs text-slate-400">
            {draft.word_count} كلمة
          </span>
        </div>
      </div>

      <p className="mt-4 whitespace-pre-line rounded-2xl border border-white/10 bg-black/30 p-4 text-sm leading-7 text-slate-200">
        {draft.body}
      </p>

      {/* contact warning */}
      <div className="mt-3 flex items-start gap-2 rounded-2xl border border-amber-400/30 bg-amber-400/10 px-4 py-3 text-sm text-amber-100">
        <span className="mt-0.5">⚠</span>
        <span>{draft.contact.note_ar}</span>
      </div>

      {/* approval state banner */}
      {approved && (
        <div className="mt-3 rounded-2xl border border-emerald-400/40 bg-emerald-400/10 px-4 py-3 text-sm">
          <p className="font-bold text-emerald-200">
            ✓ {state.message ?? "تمت الموافقة"}
          </p>
          <p className="mt-1 text-emerald-100/80">
            الموافقة تجهّز الرسالة فقط — لا إرسال آلي. أرسلها يدويًا عبر البريد أو
            واتساب من الأزرار أدناه.
          </p>
        </div>
      )}
      {rejected && (
        <div className="mt-3 rounded-2xl border border-white/10 bg-white/[0.04] px-4 py-3 text-sm text-slate-400">
          تم رفض هذه المسودة. لن تُرسل.
        </div>
      )}

      {/* action bar */}
      <div className="mt-4 flex flex-wrap gap-2">
        <button
          type="button"
          onClick={handleCopy}
          disabled={rejected}
          className="rounded-xl border border-white/15 bg-white/[0.04] px-4 py-2 text-sm font-bold text-slate-100 hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {state.copied ? "تم النسخ ✓" : "نسخ النص"}
        </button>

        {/* mailto / whatsapp: always available after approval; the founder sends */}
        <a
          href={approved ? buildMailto(draft) : undefined}
          aria-disabled={!approved || rejected}
          onClick={(e) => {
            if (!approved || rejected) e.preventDefault();
          }}
          className={`rounded-xl border px-4 py-2 text-sm font-bold ${
            approved && !rejected
              ? "border-cyan-400/40 bg-cyan-400/10 text-cyan-200 hover:bg-cyan-400/20"
              : "cursor-not-allowed border-white/10 bg-white/[0.02] text-slate-600"
          }`}
        >
          فتح بالبريد
        </a>
        <a
          href={approved ? buildWhatsapp(draft) : undefined}
          target="_blank"
          rel="noopener noreferrer"
          aria-disabled={!approved || rejected}
          onClick={(e) => {
            if (!approved || rejected) e.preventDefault();
          }}
          className={`rounded-xl border px-4 py-2 text-sm font-bold ${
            approved && !rejected
              ? "border-emerald-400/40 bg-emerald-400/10 text-emerald-200 hover:bg-emerald-400/20"
              : "cursor-not-allowed border-white/10 bg-white/[0.02] text-slate-600"
          }`}
        >
          واتساب
        </a>

        <div className="flex-1" />

        <button
          type="button"
          onClick={handleApprove}
          disabled={busy || rejected || approved}
          className="rounded-xl bg-emerald-400 px-5 py-2 text-sm font-black text-[#06111f] hover:bg-emerald-300 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {approved ? "تمت الموافقة ✓" : busy ? "..." : "موافقة"}
        </button>
        <button
          type="button"
          onClick={handleReject}
          disabled={busy || rejected || approved}
          className="rounded-xl border border-red-400/40 px-4 py-2 text-sm font-bold text-red-300 hover:bg-red-400/10 disabled:cursor-not-allowed disabled:opacity-40"
        >
          رفض
        </button>
      </div>

      <p className="mt-3 text-xs text-slate-500">
        AI كتب هذه المسودة. الموافقة تجهّزها للإرسال فقط — لا شيء يُرسَل تلقائيًا؛
        أنت ترسل بنفسك.
      </p>
    </article>
  );
}

// ── Metric card ──────────────────────────────────────────────────────────────

function Metric({
  label,
  value,
  accent,
}: {
  label: string;
  value: string;
  accent?: string;
}) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-5">
      <p className="text-xs text-slate-500">{label}</p>
      <p className={`mt-2 text-3xl font-black ${accent ?? "text-slate-100"}`}>
        {value}
      </p>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────

export default function NowPage() {
  const [pack, setPack] = useState<NowPack | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    let alive = true;
    getNowPack()
      .then((p) => {
        if (alive) setPack(p);
      })
      .catch(() => {
        if (alive) setError(true);
      });
    return () => {
      alive = false;
    };
  }, []);

  const doctrineChips =
    pack &&
    [
      pack.doctrine.no_auto_send ? "بدون إرسال آلي" : null,
      pack.doctrine.public_data_only ? "بيانات عامة فقط" : null,
      pack.doctrine.approval_first ? "الموافقة أولاً" : null,
    ].filter((x): x is string => Boolean(x));

  const sortedLeads = pack
    ? [...pack.leads].sort((a, b) => b.fit_score - a.fit_score)
    : [];

  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      <div className="mx-auto max-w-6xl px-6 py-12 md:py-16">
        {!pack && !error && <Skeleton />}

        {error && !pack && (
          <div className="rounded-3xl border border-red-400/30 bg-red-400/10 p-8 text-center">
            <p className="text-lg font-bold text-red-200">
              تعذّر تحميل بيانات غرفة القيادة.
            </p>
            <p className="mt-2 text-sm text-slate-400">
              حاول تحديث الصفحة. سيتم استخدام العيّنة الثابتة عند توفرها.
            </p>
          </div>
        )}

        {pack && (
          <>
            {/* ── Header ── */}
            <header>
              <div className="flex flex-wrap items-end justify-between gap-4">
                <div>
                  <p className="mb-3 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
                    Founder Operating Console
                  </p>
                  <h1 className="text-4xl font-black leading-tight md:text-5xl">
                    غرفة القيادة — الآن
                  </h1>
                </div>
                <p className="text-sm text-slate-400">
                  {pack.date} · {pack.tz}
                </p>
              </div>

              <div className="mt-5 flex flex-wrap gap-2">
                <span className="rounded-full border border-cyan-400/40 bg-cyan-400/10 px-4 py-2 text-sm font-black text-cyan-200">
                  {pack.doctrine.tagline_ar || "AI يكتب، أنت ترسل"}
                </span>
                {doctrineChips?.map((c) => (
                  <span
                    key={c}
                    className="rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-sm text-slate-300"
                  >
                    {c}
                  </span>
                ))}
              </div>

              {pack.is_sample && (
                <p className="mt-4 rounded-2xl border border-amber-400/20 bg-amber-400/10 px-4 py-3 text-sm leading-7 text-amber-100">
                  {pack.note_ar}
                </p>
              )}
            </header>

            {/* ── Metrics ── */}
            <section className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
              <Metric
                label="إجمالي العملاء المحتملين"
                value={String(pack.metrics.leads_total)}
              />
              <Metric
                label="أولوية عالية"
                value={String(pack.metrics.priority_high)}
                accent="text-emerald-300"
              />
              <Metric
                label="مسودات جاهزة"
                value={String(pack.metrics.drafts_ready)}
                accent="text-cyan-300"
              />
              <Metric
                label="متوسط الملاءمة"
                value={`${pack.metrics.avg_fit_score}`}
                accent="text-violet-300"
              />
              <Metric
                label="قيمة الـ pipeline (ريال)"
                value={sar(pack.metrics.pipeline_value_sar.typical)}
                accent="text-amber-300"
              />
            </section>

            {/* ── Priorities ── */}
            <section className="mt-14">
              <h2 className="text-2xl font-black">أولويات اليوم الثلاث</h2>
              {pack.priorities.length === 0 ? (
                <p className="mt-4 text-sm text-slate-500">
                  لا توجد أولويات لهذا اليوم.
                </p>
              ) : (
                <div className="mt-6 grid gap-5 md:grid-cols-3">
                  {pack.priorities.map((p) => (
                    <article
                      key={p.rank}
                      className="relative rounded-3xl border border-white/10 bg-white/[0.03] p-6"
                    >
                      <div className="flex h-9 w-9 items-center justify-center rounded-full bg-cyan-400 text-base font-black text-[#06111f]">
                        {p.rank}
                      </div>
                      <h3 className="mt-4 text-base font-black leading-7 text-slate-100">
                        {p.what_ar}
                      </h3>
                      <p className="mt-2 text-sm leading-7 text-slate-400">
                        {p.why_now_ar}
                      </p>
                      <p className="mt-4 text-xs font-bold text-cyan-300">
                        ≈ {p.est_minutes} دقيقة
                      </p>
                    </article>
                  ))}
                </div>
              )}
            </section>

            {/* ── Leads ── */}
            <section className="mt-14">
              <h2 className="text-2xl font-black">العملاء المحتملون</h2>
              <p className="mt-1 text-sm text-slate-500">
                مرتّبون حسب درجة الملاءمة
              </p>
              {sortedLeads.length === 0 ? (
                <p className="mt-4 text-sm text-slate-500">
                  لا يوجد عملاء محتملون بعد.
                </p>
              ) : (
                <div className="mt-6 grid gap-5">
                  {sortedLeads.map((lead) => (
                    <LeadCard key={lead.id} lead={lead} />
                  ))}
                </div>
              )}
            </section>

            {/* ── Drafts ── */}
            <section className="mt-14">
              <h2 className="text-2xl font-black">مسودات بانتظار موافقتك</h2>
              <p className="mt-1 text-sm text-slate-500">
                AI يكتب، أنت ترسل. الموافقة تجهّز الرسالة — الإرسال يدوي دائمًا.
              </p>
              {pack.drafts.length === 0 ? (
                <p className="mt-4 text-sm text-slate-500">
                  لا توجد مسودات بانتظار الموافقة.
                </p>
              ) : (
                <div className="mt-6 grid gap-5">
                  {pack.drafts.map((draft) => (
                    <DraftCard key={draft.id} draft={draft} />
                  ))}
                </div>
              )}
            </section>

            {/* ── Alerts ── */}
            <section className="mt-14">
              <h2 className="text-2xl font-black">تنبيهات</h2>
              {pack.intelligence_alerts.length === 0 ? (
                <p className="mt-4 text-sm text-slate-500">لا توجد تنبيهات.</p>
              ) : (
                <ul className="mt-6 space-y-3">
                  {pack.intelligence_alerts.map((a, i) => (
                    <li
                      key={i}
                      className="flex items-start gap-3 rounded-2xl border border-white/10 bg-white/[0.03] px-5 py-4 text-sm leading-7 text-slate-300"
                    >
                      <span className="mt-0.5 text-amber-400">●</span>
                      {a}
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </>
        )}
      </div>

      {/* ── Footer nav ── */}
      <footer className="border-t border-white/5 py-10">
        <div className="mx-auto flex max-w-6xl flex-wrap justify-between gap-6 px-6 text-sm text-slate-500">
          <a href="/ar" className="font-black text-white hover:text-cyan-300">
            ← Dealix
          </a>
          <nav className="flex flex-wrap gap-6">
            <a href="/ar" className="hover:text-white">
              الرئيسية
            </a>
            <a href="/ar/services" className="hover:text-cyan-300">
              الخدمات
            </a>
            <a href="/ar/p1" className="hover:text-cyan-300">
              P1 تشخيص
            </a>
            <a href="/ar/p2" className="hover:text-emerald-300">
              P2 تشغيل شهري
            </a>
            <a href="/ar/pricing" className="hover:text-white">
              الأسعار
            </a>
            <a href="mailto:hello@dealix.me" className="hover:text-white">
              تواصل معنا
            </a>
          </nav>
        </div>
      </footer>
    </main>
  );
}
