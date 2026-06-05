"use client";

// ---------------------------------------------------------------------------
// Launch UI kit — reusable bilingual building blocks for the Dealix
// Business OS marketing surface. Premium dark executive look (navy + gold).
// Every block is RTL-aware via next-intl locale. No external claims, no fake
// proof — copy is supplied by the composing page.
// ---------------------------------------------------------------------------

import type { ReactNode } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";
import { Button } from "@/components/ui/button";

export type Bi = { ar: string; en: string };

export type LaunchStatus =
  | "LIVE"
  | "BETA"
  | "INTERNAL"
  | "DOCS_ONLY"
  | "FUTURE"
  | "BLOCKED"
  | "DEPRECATED";

const STATUS_STYLE: Record<LaunchStatus, string> = {
  LIVE: "bg-emerald-500/15 text-emerald-300 border-emerald-400/30",
  BETA: "bg-gold-500/15 text-gold-300 border-gold-400/30",
  INTERNAL: "bg-white/10 text-white/70 border-white/20",
  DOCS_ONLY: "bg-white/5 text-white/50 border-white/15",
  FUTURE: "bg-navy-400/15 text-navy-100 border-navy-300/30",
  BLOCKED: "bg-red-500/15 text-red-300 border-red-400/30",
  DEPRECATED: "bg-white/5 text-white/40 border-white/10",
};

const STATUS_LABEL: Record<LaunchStatus, Bi> = {
  LIVE: { ar: "جاهز", en: "Live" },
  BETA: { ar: "تجريبي", en: "Beta" },
  INTERNAL: { ar: "داخلي", en: "Internal" },
  DOCS_ONLY: { ar: "موثّق", en: "Docs only" },
  FUTURE: { ar: "لاحقًا", en: "Future" },
  BLOCKED: { ar: "محجوب", en: "Blocked" },
  DEPRECATED: { ar: "متوقّف", en: "Deprecated" },
};

export function useBi() {
  const locale = useLocale();
  const isAr = locale === "ar";
  return {
    isAr,
    base: `/${locale}`,
    t: (v: Bi) => (isAr ? v.ar : v.en),
  };
}

export function StatusPill({ status }: { status: LaunchStatus }) {
  const { t } = useBi();
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-[11px] font-semibold tracking-wide ${STATUS_STYLE[status]}`}
    >
      {t(STATUS_LABEL[status])}
    </span>
  );
}

// --- Hero -----------------------------------------------------------------

export function LaunchHero({
  eyebrow,
  title,
  titleAccent,
  subtitle,
  primary,
  secondary,
  status,
}: {
  eyebrow?: Bi;
  title: Bi;
  titleAccent?: Bi;
  subtitle: Bi;
  primary: { label: Bi; href: string };
  secondary?: { label: Bi; href: string };
  status?: LaunchStatus;
}) {
  const { t, base } = useBi();
  const href = (h: string) => (h.startsWith("/") ? `${base}${h}` : h);
  return (
    <section
      className="relative overflow-hidden px-6 py-20 md:py-28"
      style={{ background: "linear-gradient(160deg,#00060d 0%,#001226 55%,#001832 100%)" }}
    >
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-[0.18]"
        style={{
          backgroundImage:
            "radial-gradient(circle at 1px 1px, rgba(212,175,55,0.35) 1px, transparent 0)",
          backgroundSize: "26px 26px",
        }}
      />
      <div className="relative mx-auto max-w-4xl text-center">
        <div className="mb-5 flex items-center justify-center gap-3">
          {eyebrow ? (
            <span className="text-xs font-semibold uppercase tracking-[0.2em] text-gold-300">
              {t(eyebrow)}
            </span>
          ) : null}
          {status ? <StatusPill status={status} /> : null}
        </div>
        <h1 className="font-arabic text-3xl font-bold leading-tight tracking-tight text-white sm:text-4xl md:text-5xl">
          {t(title)}{" "}
          {titleAccent ? (
            <span className="bg-gradient-to-r from-gold-400 to-gold-300 bg-clip-text text-transparent">
              {t(titleAccent)}
            </span>
          ) : null}
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-base leading-relaxed text-white/70 md:text-lg">
          {t(subtitle)}
        </p>
        <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Button
            asChild
            size="lg"
            className="w-full bg-gradient-to-r from-gold-500 to-gold-400 px-8 font-bold text-navy-500 shadow-lg shadow-gold-500/25 hover:from-gold-400 hover:to-gold-300 sm:w-auto"
          >
            <Link href={href(primary.href)}>{t(primary.label)}</Link>
          </Button>
          {secondary ? (
            <Button
              asChild
              size="lg"
              variant="outline"
              className="w-full border-white/20 text-white backdrop-blur-sm hover:bg-white/10 sm:w-auto"
            >
              <Link href={href(secondary.href)}>{t(secondary.label)}</Link>
            </Button>
          ) : null}
        </div>
      </div>
    </section>
  );
}

// --- Section wrapper ------------------------------------------------------

export function Section({
  eyebrow,
  title,
  subtitle,
  children,
  tone = "navy",
}: {
  eyebrow?: Bi;
  title?: Bi;
  subtitle?: Bi;
  children: ReactNode;
  tone?: "navy" | "deep";
}) {
  const { t } = useBi();
  const bg = tone === "deep" ? "#00060d" : "#000c19";
  return (
    <section className="px-6 py-16 md:py-20" style={{ background: bg }}>
      <div className="mx-auto max-w-6xl">
        {(eyebrow || title || subtitle) && (
          <div className="mx-auto mb-12 max-w-2xl text-center">
            {eyebrow ? (
              <p className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-gold-300">
                {t(eyebrow)}
              </p>
            ) : null}
            {title ? (
              <h2 className="text-2xl font-bold text-white md:text-3xl">{t(title)}</h2>
            ) : null}
            {subtitle ? (
              <p className="mt-4 text-base leading-relaxed text-white/60">{t(subtitle)}</p>
            ) : null}
          </div>
        )}
        {children}
      </div>
    </section>
  );
}

// --- Card grid (OS layers, industries, features) --------------------------

export type Card = {
  icon?: string;
  title: Bi;
  body: Bi;
  tag?: Bi;
  status?: LaunchStatus;
};

export function CardGrid({ items, cols = 3 }: { items: Card[]; cols?: 2 | 3 | 4 }) {
  const { t } = useBi();
  const grid =
    cols === 4
      ? "md:grid-cols-4"
      : cols === 2
        ? "md:grid-cols-2"
        : "md:grid-cols-3";
  return (
    <div className={`grid gap-5 sm:grid-cols-2 ${grid}`}>
      {items.map((c) => (
        <div
          key={c.title.en}
          className="flex flex-col gap-3 rounded-2xl border border-white/10 bg-white/[0.04] p-6 transition-colors hover:border-gold-400/30"
        >
          <div className="flex items-center justify-between gap-2">
            {c.icon ? <span className="text-2xl">{c.icon}</span> : <span />}
            {c.status ? <StatusPill status={c.status} /> : null}
          </div>
          <h3 className="text-base font-semibold text-white">{t(c.title)}</h3>
          <p className="text-sm leading-relaxed text-white/60">{t(c.body)}</p>
          {c.tag ? (
            <span className="mt-auto text-xs font-medium text-gold-300">{t(c.tag)}</span>
          ) : null}
        </div>
      ))}
    </div>
  );
}

// --- Numbered step list (delivery / how it works) -------------------------

export function StepList({ steps }: { steps: { title: Bi; body: Bi }[] }) {
  const { t } = useBi();
  return (
    <ol className="grid gap-4">
      {steps.map((s, i) => (
        <li
          key={s.title.en}
          className="flex gap-4 rounded-2xl border border-white/10 bg-white/[0.03] p-5"
        >
          <span className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full bg-gold-500/15 text-sm font-bold text-gold-300">
            {i + 1}
          </span>
          <div>
            <h3 className="font-semibold text-white">{t(s.title)}</h3>
            <p className="mt-1 text-sm leading-relaxed text-white/60">{t(s.body)}</p>
          </div>
        </li>
      ))}
    </ol>
  );
}

// --- Pill row (proof points / trust) --------------------------------------

export function PillRow({ items }: { items: Bi[] }) {
  const { t } = useBi();
  return (
    <div className="flex flex-wrap items-center justify-center gap-3">
      {items.map((p) => (
        <span
          key={p.en}
          className="rounded-xl border border-white/10 bg-white/[0.04] px-4 py-2 text-sm text-white/75"
        >
          {t(p)}
        </span>
      ))}
    </div>
  );
}

// --- CTA band (single CTA per page rule) ----------------------------------

export function CtaBand({
  title,
  subtitle,
  cta,
}: {
  title: Bi;
  subtitle?: Bi;
  cta: { label: Bi; href: string };
}) {
  const { t, base } = useBi();
  const href = cta.href.startsWith("/") ? `${base}${cta.href}` : cta.href;
  return (
    <section
      className="px-6 py-20"
      style={{ background: "linear-gradient(135deg,#001830 0%,#002040 50%,#001830 100%)" }}
    >
      <div className="mx-auto max-w-3xl text-center">
        <h2 className="text-2xl font-bold text-white md:text-3xl">{t(title)}</h2>
        {subtitle ? (
          <p className="mx-auto mt-4 max-w-xl text-base text-white/60">{t(subtitle)}</p>
        ) : null}
        <div className="mt-8 flex justify-center">
          <Button
            asChild
            size="lg"
            className="bg-gradient-to-r from-gold-500 to-gold-400 px-10 font-bold text-navy-500 shadow-lg shadow-gold-500/25 hover:from-gold-400 hover:to-gold-300"
          >
            <Link href={href}>{t(cta.label)}</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}

// --- FAQ ------------------------------------------------------------------

export function Faq({ items }: { items: { q: Bi; a: Bi }[] }) {
  const { t } = useBi();
  return (
    <div className="mx-auto max-w-3xl divide-y divide-white/10 rounded-2xl border border-white/10 bg-white/[0.03]">
      {items.map((f) => (
        <details key={f.q.en} className="group p-6">
          <summary className="cursor-pointer list-none text-base font-semibold text-white marker:hidden">
            {t(f.q)}
          </summary>
          <p className="mt-3 text-sm leading-relaxed text-white/60">{t(f.a)}</p>
        </details>
      ))}
    </div>
  );
}

// --- Disclosure line (required on customer-facing surfaces) ---------------

export function Disclosure() {
  const { t } = useBi();
  return (
    <p className="px-6 py-8 text-center text-xs text-white/35" style={{ background: "#00060d" }}>
      {t({
        ar: "القيمة التقديرية ليست قيمة مُتحقَّقة. لا إرسال خارجي بدون موافقة. لا ادعاءات إيراد مضمونة.",
        en: "Estimated value is not Verified value. No external send without approval. No guaranteed revenue claims.",
      })}
    </p>
  );
}
