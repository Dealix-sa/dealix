"use client";

import { useCallback, useEffect, useState } from "react";

import { api } from "@/lib/api";

// Opens WhatsApp with the draft prefilled and lets the founder pick the
// recipient — the card itself never knows or stores a customer number.
function waShareLink(message: string): string {
  return `https://wa.me/?text=${encodeURIComponent(message)}`;
}

interface GrowthCard {
  card_id: string;
  company_name: string;
  sector: string;
  city: string;
  motion: string;
  recommended_channel: string;
  risk_level: string;
  approval_required: boolean;
  send_status: string;
  source_url: string;
  verification_status: string;
  pain_hypothesis: string;
  dealix_angle: string;
  recommended_product: string;
  draft_message_ar: string;
  draft_message_en: string;
  buttons: { id: string; title: string }[];
  owner_decision: string;
  next_action: string;
}

interface GrowthCardsReport {
  generated_at: string | null;
  summary?: { cards: number; errors: number; draft_only: boolean; live_send: boolean };
  cards: GrowthCard[];
  note?: string;
}

const RISK_STYLE: Record<string, string> = {
  high: "border-rose-400/40 text-rose-300",
  medium: "border-amber-400/40 text-amber-300",
  low: "border-emerald-400/40 text-emerald-300",
};

export default function GrowthCardsPage() {
  const [report, setReport] = useState<GrowthCardsReport | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getGrowthCardsLatest();
      setReport(res.data as GrowthCardsReport);
    } catch (e) {
      setError(e instanceof Error ? e.message : "تعذر تحميل الكروت — تأكد أن الخادم يعمل");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  async function copyDraft(card: GrowthCard) {
    try {
      await navigator.clipboard.writeText(card.draft_message_ar);
      setCopied(card.card_id);
      setTimeout(() => setCopied(null), 2000);
    } catch {
      /* clipboard unavailable — WhatsApp button still works */
    }
  }

  const cards = report?.cards ?? [];

  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] px-6 py-14 text-white">
      <div className="mx-auto max-w-5xl">
        <p className="mb-4 inline-flex rounded-full border border-emerald-300/30 px-4 py-2 text-sm text-emerald-100">
          كروت واتساب اليومية
        </p>
        <h1 className="text-3xl font-black md:text-5xl">
          مسودات اليوم — <span className="text-emerald-400">أنت توافق، أنت ترسل</span>
        </h1>
        <p className="mt-4 max-w-3xl leading-8 text-slate-300">
          يولّدها <code className="text-cyan-300">dealix_command_day.sh</code> يومياً من حساباتك
          المستهدفة. كل كرت مسودة فقط — لا شيء يُرسل بدون قرارك.
        </p>

        <div className="mt-6 flex flex-wrap items-center gap-3 text-sm">
          <button
            onClick={() => void load()}
            disabled={loading}
            className="rounded-xl border border-white/20 px-4 py-2 font-bold hover:bg-white/10 disabled:opacity-50"
          >
            {loading ? "جارٍ التحديث..." : "تحديث"}
          </button>
          {report?.generated_at && (
            <span className="text-slate-500">آخر توليد: {report.generated_at}</span>
          )}
          {report?.summary && (
            <span className="rounded-full border border-emerald-400/30 px-3 py-1 text-emerald-300">
              draft-only ✓ · لا إرسال تلقائي ✓
            </span>
          )}
        </div>

        {error && (
          <p className="mt-6 rounded-2xl border border-red-400/30 bg-red-400/[0.06] px-4 py-3 text-sm text-red-300">
            {error}
          </p>
        )}

        {!error && cards.length === 0 && !loading && (
          <div className="mt-10 rounded-3xl border border-white/10 bg-white/[0.03] p-8 text-center text-slate-400">
            لا توجد كروت بعد — شغّل{" "}
            <code className="text-cyan-300">bash scripts/dealix_command_day.sh</code>{" "}
            أو غذِّ حساباتك في{" "}
            <code className="text-cyan-300">data/commercial/growth_accounts.sample.json</code>
          </div>
        )}

        <div className="mt-8 space-y-6">
          {cards.map((card) => (
            <article
              key={card.card_id}
              className="rounded-3xl border border-white/10 bg-white/[0.03] p-6"
            >
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 className="text-xl font-black">{card.company_name}</h2>
                  <p className="mt-1 text-sm text-slate-400">
                    {card.sector} · {card.city} · {card.motion}
                  </p>
                </div>
                <div className="flex flex-wrap gap-2 text-xs">
                  <span
                    className={`rounded-full border px-3 py-1 ${RISK_STYLE[card.risk_level] ?? "border-white/20 text-slate-300"}`}
                  >
                    خطورة: {card.risk_level}
                  </span>
                  <span className="rounded-full border border-cyan-300/30 px-3 py-1 text-cyan-200">
                    {card.recommended_channel}
                  </span>
                  <span className="rounded-full border border-white/20 px-3 py-1 text-slate-400">
                    {card.send_status}
                  </span>
                </div>
              </div>

              <div className="mt-4 grid gap-3 text-sm md:grid-cols-2">
                <div className="rounded-2xl border border-white/5 bg-white/[0.02] p-4">
                  <p className="font-bold text-slate-200">فرضية الألم</p>
                  <p className="mt-1 leading-7 text-slate-400">{card.pain_hypothesis}</p>
                </div>
                <div className="rounded-2xl border border-white/5 bg-white/[0.02] p-4">
                  <p className="font-bold text-slate-200">زاوية Dealix</p>
                  <p className="mt-1 leading-7 text-slate-400">{card.dealix_angle}</p>
                  <p className="mt-2 text-cyan-300">{card.recommended_product}</p>
                </div>
              </div>

              <div className="mt-4 rounded-2xl border border-emerald-400/20 bg-emerald-400/[0.04] p-4">
                <p className="text-xs font-bold text-emerald-400">مسودة الرسالة (عربي)</p>
                <pre className="mt-2 whitespace-pre-wrap font-sans text-sm leading-8 text-slate-200">
                  {card.draft_message_ar}
                </pre>
              </div>

              <div className="mt-4 flex flex-wrap items-center gap-3">
                <a
                  href={waShareLink(card.draft_message_ar)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="rounded-xl bg-emerald-500 px-5 py-2.5 text-sm font-bold text-white hover:bg-emerald-400"
                >
                  افتح في واتساب واختر المستلم
                </a>
                <button
                  onClick={() => void copyDraft(card)}
                  className="rounded-xl border border-white/20 px-5 py-2.5 text-sm font-bold hover:bg-white/10"
                >
                  {copied === card.card_id ? "✓ نُسخت" : "انسخ المسودة"}
                </button>
                <span className="text-xs text-slate-500">
                  التالي: {card.next_action} · القرار: {card.owner_decision}
                </span>
              </div>
            </article>
          ))}
        </div>

        <p className="mt-10 text-center text-xs text-slate-500">
          كل الكروت approval_required · القناة عالية الخطورة تتطلب مراجعة إلزامية ·
          مصدر كل حساب موثق (source_url)
        </p>
      </div>
    </main>
  );
}
