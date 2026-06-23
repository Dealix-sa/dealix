"use client";

import { useState } from "react";
import Link from "next/link";

interface OutboundChannel {
  key: string;
  labelAr: string;
  labelEn: string;
  description: string;
  enabled: boolean;
}

const DEFAULT_CHANNELS: OutboundChannel[] = [
  {
    key: "whatsapp_send",
    labelAr: "إرسال واتساب",
    labelEn: "WhatsApp send",
    description: "إرسال رسائل واتساب للعملاء والعملاء المحتملين.",
    enabled: false,
  },
  {
    key: "email_send",
    labelAr: "إرسال إيميل",
    labelEn: "Email send",
    description: "إرسال رسائل بريد إلكتروني خارجية.",
    enabled: false,
  },
  {
    key: "crm_auto_update",
    labelAr: "تحديث CRM تلقائي",
    labelEn: "CRM auto-update",
    description: "تحديث سجلات CRM دون موافقة بشرية.",
    enabled: false,
  },
  {
    key: "public_post",
    labelAr: "نشر عام",
    labelEn: "Public post",
    description: "نشر محتوى عام على قنوات خارجية.",
    enabled: false,
  },
  {
    key: "invoice_send",
    labelAr: "إرسال فاتورة",
    labelEn: "Invoice send",
    description: "إرسال فواتير للعملاء تلقائياً.",
    enabled: false,
  },
];

export default function OutboundSafetySettingsPage() {
  const [mode, setMode] = useState<"draft_only" | "auto">("draft_only");
  const [channels, setChannels] = useState<OutboundChannel[]>(DEFAULT_CHANNELS);

  const toggleChannel = (key: string) => {
    setChannels((prev) =>
      prev.map((c) => (c.key === key ? { ...c, enabled: !c.enabled } : c))
    );
  };

  const allDisabled = channels.every((c) => !c.enabled);

  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-4xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">
            Settings · Outbound Safety
          </p>
          <h1 className="mt-3 text-4xl font-semibold">إعدادات السلامة الصادرة</h1>
          <p className="mt-2 text-sm text-white/60">
            Outbound safety — all channels disabled by default (draft_only mode)
          </p>
          <p className="mt-4 max-w-2xl text-sm text-white/70">
            كل القنوات الخارجية معطّلة افتراضياً. لا إرسال تلقائي، لا تحديث
            CRM دون موافقة. الوضع الافتراضي:{" "}
            <span className="font-medium text-amber-200">draft_only</span> —
            كل مسوّد يحتاج موافقة بشرية قبل أي خروج.
          </p>
        </header>

        {/* Mode selector */}
        <section className="mt-10 rounded-2xl border border-white/10 bg-white/5 p-6">
          <p className="text-xs uppercase tracking-widest text-amber-300/80">
            وضع التشغيل
          </p>
          <div className="mt-4 flex flex-wrap gap-3">
            <button
              type="button"
              onClick={() => setMode("draft_only")}
              className={`rounded-full px-5 py-2 text-sm font-medium transition ${
                mode === "draft_only"
                  ? "bg-amber-300 text-black"
                  : "border border-white/20 text-white hover:border-white/40"
              }`}
            >
              draft_only (افتراضي)
            </button>
            <button
              type="button"
              onClick={() => setMode("auto")}
              className={`rounded-full px-5 py-2 text-sm font-medium transition ${
                mode === "auto"
                  ? "bg-amber-300 text-black"
                  : "border border-white/20 text-white hover:border-white/40"
              }`}
            >
              auto (متقدم — يحتاج تفعيل يدوي لكل قناة)
            </button>
          </div>
          <p className="mt-4 text-xs text-white/60">
            {mode === "draft_only"
              ? "كل الإرسال يحتاج موافقة بشرية قبل الخروج. هذا هو الوضع الآمن."
              : "تحذير: الوضع auto يسمح بالإرسال التلقائي للقنوات المُفعّلة. فعّل فقط ما تحتاجه وتثق به."}
          </p>
        </section>

        {/* Channels list */}
        <section className="mt-8">
          <h2 className="text-lg font-semibold text-amber-300">
            القنوات الخارجية
          </h2>
          <ul className="mt-4 space-y-3">
            {channels.map((c) => (
              <li
                key={c.key}
                className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 p-5"
              >
                <div>
                  <p className="font-medium">{c.labelAr}</p>
                  <p className="text-xs text-white/50">{c.labelEn}</p>
                  <p className="mt-1 text-xs text-white/60">{c.description}</p>
                </div>
                <button
                  type="button"
                  onClick={() => toggleChannel(c.key)}
                  aria-pressed={c.enabled}
                  className={`relative h-7 w-12 rounded-full transition ${
                    c.enabled
                      ? "bg-amber-300"
                      : "bg-white/15 border border-white/20"
                  }`}
                >
                  <span
                    className={`absolute top-0.5 h-6 w-6 rounded-full bg-[#070A12] transition-all ${
                      c.enabled ? "left-[22px]" : "left-0.5"
                    }`}
                  />
                </button>
              </li>
            ))}
          </ul>
        </section>

        {/* Status banner */}
        <section
          className={`mt-8 rounded-2xl border p-6 text-sm ${
            allDisabled
              ? "border-amber-300/20 bg-amber-300/5 text-white/80"
              : "border-rose-300/30 bg-rose-300/5 text-white/80"
          }`}
        >
          <p
            className={`font-medium ${
              allDisabled ? "text-amber-200" : "text-rose-200"
            }`}
          >
            {allDisabled ? "كل القنوات معطّلة (draft_only)" : "بعض القنوات مُفعّلة"}
          </p>
          <p className="mt-2">
            {allDisabled
              ? "الوضع الآمن الافتراضي. كل مسوّد يبقى داخلياً حتى موافقة بشرية."
              : "تأكد أن كل قناة مُفعّلة لها مالك بشري و cadence مراجعة. لا تفعّل قناة بدون سبب تشغيلي واضح."}
          </p>
        </section>

        <section className="mt-10 flex flex-wrap gap-3">
          <Link
            href="/safety"
            className="rounded-full border border-white/20 px-6 py-3 text-sm font-medium text-white transition hover:border-white/40"
          >
            طبقة السلامة العامة
          </Link>
          <Link
            href="/products/ai-trust-compliance-os"
            className="rounded-full border border-white/20 px-6 py-3 text-sm font-medium text-white transition hover:border-white/40"
          >
            نظام الثقة والامتثال
          </Link>
        </section>

        <p className="mt-8 text-xs text-white/40">
          هذه الصفحة تفاعلية للعرض فقط. التغييرات هنا لا تُحفظ في الخادم حتى
          تُكتب عبر API الإعدادات بموافقة مسؤول.
        </p>
      </div>
    </main>
  );
}