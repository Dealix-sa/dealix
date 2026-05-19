"use client";

import { useCallback, useEffect, useState } from "react";
import {
  ChevronLeft,
  ChevronRight,
  Download,
  Info,
  Languages,
  Lock,
  Presentation,
  ScrollText,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { BeforeAfterChart, RoiChart } from "./PitchCharts";
import type {
  Block,
  Lang,
  PitchContent,
  Slide,
  SlideContent,
} from "./types";

interface PitchDeckProps {
  content: PitchContent;
  lang: Lang;
}

type Mode = "deck" | "scroll";

const GRADIENT_TEXT =
  "bg-gradient-to-r from-gold-500 to-emerald-500 bg-clip-text text-transparent";

export function PitchDeck({ content, lang }: PitchDeckProps) {
  const slides = content.slides;
  const ui = content.ui[lang];
  const total = slides.length;
  const isRTL = lang === "ar";

  const [mode, setMode] = useState<Mode>("deck");
  const [index, setIndex] = useState(0);
  const [ready, setReady] = useState(false);

  // Read initial mode/slide from the URL (client only — avoids Suspense).
  useEffect(() => {
    const p = new URLSearchParams(window.location.search);
    if (p.get("mode") === "scroll") setMode("scroll");
    const s = parseInt(p.get("s") ?? "", 10);
    if (!Number.isNaN(s) && s > 0 && s <= total) setIndex(s - 1);
    setReady(true);
  }, [total]);

  // Keep the URL in sync so a deck position can be shared / reloaded.
  useEffect(() => {
    if (!ready) return;
    const q =
      `?mode=${mode}` + (mode === "deck" ? `&s=${index + 1}` : "");
    window.history.replaceState(null, "", q);
  }, [mode, index, ready]);

  const go = useCallback(
    (next: number) => {
      setIndex((cur) => {
        const clamped = Math.max(0, Math.min(total - 1, next));
        return clamped === cur ? cur : clamped;
      });
    },
    [total],
  );

  useEffect(() => {
    if (mode !== "deck") return;
    const onKey = (e: KeyboardEvent) => {
      const fwd = isRTL ? "ArrowLeft" : "ArrowRight";
      const back = isRTL ? "ArrowRight" : "ArrowLeft";
      if (e.key === fwd || e.key === " " || e.key === "PageDown") {
        e.preventDefault();
        setIndex((c) => Math.min(total - 1, c + 1));
      } else if (e.key === back || e.key === "PageUp") {
        e.preventDefault();
        setIndex((c) => Math.max(0, c - 1));
      } else if (e.key === "Home") {
        e.preventDefault();
        setIndex(0);
      } else if (e.key === "End") {
        e.preventDefault();
        setIndex(total - 1);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [mode, isRTL, total]);

  useEffect(() => {
    if (mode === "deck") window.scrollTo({ top: 0, behavior: "smooth" });
  }, [index, mode]);

  // Charts measure their width lazily; switch to scroll mode (all slides
  // laid out) before printing so every chart renders into the PDF.
  const handlePrint = useCallback(() => {
    setMode("scroll");
    window.setTimeout(() => window.print(), 350);
  }, []);

  const otherLocale = lang === "ar" ? "en" : "ar";

  return (
    <div className="pitch-root min-h-screen bg-background text-foreground">
      {/* ── Top control bar ──────────────────────────────────────── */}
      <div className="pitch-chrome sticky top-0 z-40 flex flex-wrap items-center gap-3 border-b border-border bg-background/85 px-4 py-3 backdrop-blur-md sm:px-8">
        <div className="flex items-center gap-2 text-lg font-extrabold">
          <span className="h-3 w-3 rounded bg-gradient-to-br from-gold-500 to-emerald-500" />
          Dealix
        </div>
        <div className="flex-1" />

        <div className="flex rounded-full border border-border bg-card p-1">
          <button
            type="button"
            onClick={() => setMode("deck")}
            aria-pressed={mode === "deck"}
            className={cn(
              "flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-bold transition",
              mode === "deck"
                ? "bg-gradient-to-r from-gold-500 to-emerald-500 text-background"
                : "text-muted-foreground hover:text-foreground",
            )}
          >
            <Presentation className="h-3.5 w-3.5" />
            {ui.deck}
          </button>
          <button
            type="button"
            onClick={() => setMode("scroll")}
            aria-pressed={mode === "scroll"}
            className={cn(
              "flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-bold transition",
              mode === "scroll"
                ? "bg-gradient-to-r from-gold-500 to-emerald-500 text-background"
                : "text-muted-foreground hover:text-foreground",
            )}
          >
            <ScrollText className="h-3.5 w-3.5" />
            {ui.scroll}
          </button>
        </div>

        <a
          href={`/${otherLocale}/pitch?mode=${mode}`}
          className="flex items-center gap-1.5 rounded-full border border-border bg-card px-3.5 py-2 text-xs font-bold text-foreground transition hover:bg-muted"
        >
          <Languages className="h-3.5 w-3.5" />
          {ui.lang}
        </a>
        <button
          type="button"
          onClick={handlePrint}
          className="flex items-center gap-1.5 rounded-full bg-gradient-to-r from-gold-500 to-emerald-500 px-3.5 py-2 text-xs font-extrabold text-background transition hover:opacity-90"
        >
          <Download className="h-3.5 w-3.5" />
          {ui.pdf}
        </button>
      </div>

      {/* ── Progress ─────────────────────────────────────────────── */}
      <div className="pitch-chrome h-1 w-full bg-muted">
        <div
          className="h-full bg-gradient-to-r from-gold-500 to-emerald-500 transition-[width] duration-300"
          style={{ width: `${((index + 1) / total) * 100}%` }}
        />
      </div>

      {/* ── Slides ───────────────────────────────────────────────── */}
      <div className="mx-auto max-w-6xl px-4 sm:px-8">
        {slides.map((slide, i) => (
          <section
            key={slide.id}
            id={`slide-${slide.id}`}
            aria-roledescription="slide"
            className={cn(
              "pitch-slide flex-col gap-6 sm:gap-8",
              mode === "deck"
                ? i === index
                  ? "flex min-h-[calc(100vh-13rem)] animate-fade-in justify-center py-10"
                  : "hidden"
                : "flex border-b border-border py-12 last:border-0 sm:py-20",
            )}
          >
            <SlideView slide={slide} lang={lang} />
          </section>
        ))}
      </div>

      {mode === "scroll" && (
        <p className="pitch-chrome pb-10 text-center text-xs text-muted-foreground">
          {ui.scroll_hint}
        </p>
      )}

      {/* ── Bottom navigation ────────────────────────────────────── */}
      {mode === "deck" && (
        <div className="pitch-chrome sticky bottom-0 z-30 flex items-center justify-center gap-3 border-t border-border bg-background/85 p-3 backdrop-blur-md">
          <button
            type="button"
            onClick={() => go(index - 1)}
            disabled={index === 0}
            aria-label={ui.prev}
            className="flex h-10 w-10 items-center justify-center rounded-full border border-border bg-card transition hover:bg-muted disabled:opacity-30"
          >
            {isRTL ? (
              <ChevronRight className="h-5 w-5" />
            ) : (
              <ChevronLeft className="h-5 w-5" />
            )}
          </button>
          <div className="flex max-w-[55vw] flex-wrap justify-center gap-1.5">
            {slides.map((s, i) => (
              <button
                key={s.id}
                type="button"
                onClick={() => go(i)}
                aria-label={`${i + 1} ${ui.of} ${total}`}
                className={cn(
                  "h-2.5 w-2.5 rounded-full transition",
                  i === index
                    ? "scale-125 bg-gradient-to-r from-gold-500 to-emerald-500"
                    : "bg-muted-foreground/40 hover:bg-muted-foreground",
                )}
              />
            ))}
          </div>
          <span className="min-w-[4rem] text-center text-xs font-bold text-muted-foreground">
            {index + 1} / {total}
          </span>
          <button
            type="button"
            onClick={() => go(index + 1)}
            disabled={index === total - 1}
            aria-label={ui.next}
            className="flex h-10 w-10 items-center justify-center rounded-full border border-border bg-card transition hover:bg-muted disabled:opacity-30"
          >
            {isRTL ? (
              <ChevronLeft className="h-5 w-5" />
            ) : (
              <ChevronRight className="h-5 w-5" />
            )}
          </button>
        </div>
      )}
    </div>
  );
}

/* ── Slide ──────────────────────────────────────────────────────── */

function SlideView({ slide, lang }: { slide: Slide; lang: Lang }) {
  const c: SlideContent = slide[lang];

  if (slide.layout === "cover") {
    return (
      <div className="flex flex-col items-start gap-5">
        {c.kicker && (
          <span className="text-xs font-bold uppercase tracking-[0.18em] text-emerald-500">
            {c.kicker}
          </span>
        )}
        <h1
          className={cn(
            "text-7xl font-extrabold leading-none tracking-tight sm:text-8xl lg:text-[9rem]",
            GRADIENT_TEXT,
          )}
        >
          {c.title}
        </h1>
        <h2 className="max-w-3xl text-2xl font-extrabold leading-tight sm:text-4xl">
          {c.headline}
        </h2>
        <p className="max-w-2xl text-base leading-relaxed text-muted-foreground sm:text-lg">
          {c.subtitle}
        </p>
        <p className="text-sm text-muted-foreground">{c.meta}</p>
        <div className="flex flex-wrap gap-2.5">
          {(c.tags ?? []).map((t) => (
            <span
              key={t}
              className="rounded-full border border-border bg-card px-4 py-1.5 text-xs font-bold"
            >
              {t}
            </span>
          ))}
        </div>
      </div>
    );
  }

  const isCta = slide.layout === "cta";

  return (
    <div
      className={cn("flex flex-col gap-5", isCta && "items-center text-center")}
    >
      {c.eyebrow && (
        <span className="inline-flex w-fit items-center rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3.5 py-1.5 text-xs font-bold uppercase tracking-[0.08em] text-emerald-500">
          {c.eyebrow}
        </span>
      )}
      <h2 className="text-2xl font-extrabold leading-tight tracking-tight sm:text-4xl">
        {c.title}
      </h2>
      {c.subtitle && (
        <p
          className={cn(
            "max-w-3xl text-base leading-relaxed text-muted-foreground sm:text-lg",
            isCta && "mx-auto",
          )}
        >
          {c.subtitle}
        </p>
      )}

      {isCta ? (
        <>
          <div className="flex flex-wrap justify-center gap-3.5 pt-2">
            {(c.buttons ?? []).map((b) => (
              <a
                key={b.label}
                href={b.href}
                className={cn(
                  "rounded-2xl px-7 py-3.5 text-base font-extrabold transition hover:-translate-y-0.5",
                  b.primary
                    ? "bg-gradient-to-r from-gold-500 to-emerald-500 text-background"
                    : "border border-border bg-card text-foreground",
                )}
              >
                {b.label}
              </a>
            ))}
          </div>
          {c.contact && (
            <p className="text-sm text-muted-foreground">{c.contact}</p>
          )}
        </>
      ) : (
        <div className="flex flex-col gap-5">
          {(c.blocks ?? []).map((b, i) => (
            <BlockView key={i} block={b} lang={lang} />
          ))}
        </div>
      )}
    </div>
  );
}

/* ── Blocks ─────────────────────────────────────────────────────── */

function BlockView({ block, lang }: { block: Block; lang: Lang }) {
  switch (block.type) {
    case "kpis":
      return (
        <div className="grid gap-4 sm:grid-cols-3">
          {block.items.map((it, i) => (
            <div
              key={i}
              className="flex flex-col gap-1.5 rounded-2xl border border-border bg-card/60 p-6"
            >
              <span
                className={cn(
                  "text-3xl font-extrabold tracking-tight sm:text-4xl",
                  GRADIENT_TEXT,
                )}
              >
                {it.num}
              </span>
              <span className="text-sm leading-snug">{it.label}</span>
              {it.note && (
                <span className="text-xs font-semibold uppercase tracking-wide text-emerald-500">
                  {it.note}
                </span>
              )}
            </div>
          ))}
        </div>
      );

    case "cards":
      return (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {block.items.map((it, i) => (
            <div
              key={i}
              className={cn(
                "flex flex-col gap-2.5 rounded-2xl border p-5 transition hover:-translate-y-1",
                block.tone === "danger"
                  ? "border-destructive/25 bg-destructive/5"
                  : "border-border bg-card/60",
              )}
            >
              {it.icon && (
                <span
                  className={cn(
                    "flex h-11 w-11 items-center justify-center rounded-xl text-xl",
                    block.tone === "danger"
                      ? "bg-destructive/10"
                      : "bg-emerald-500/10",
                  )}
                >
                  {it.icon}
                </span>
              )}
              <div className="flex items-center justify-between gap-2">
                <h3 className="text-lg font-extrabold">{it.title}</h3>
                {it.stat && (
                  <span
                    className={cn(
                      "text-lg font-extrabold",
                      block.tone === "danger"
                        ? "text-destructive"
                        : "text-emerald-500",
                    )}
                  >
                    {it.stat}
                  </span>
                )}
              </div>
              <p className="text-sm leading-relaxed text-muted-foreground">
                {it.desc}
              </p>
            </div>
          ))}
        </div>
      );

    case "flow":
      return (
        <div className="flex flex-col items-stretch gap-3 md:flex-row md:items-center">
          {block.items.map((it, i) => (
            <div key={i} className="flex flex-col gap-3 md:flex-1 md:flex-row md:items-center">
              <div className="flex flex-1 flex-col gap-1.5 rounded-2xl border border-border bg-card/60 p-5">
                <span className="text-3xl">{it.icon}</span>
                <h3 className="text-base font-extrabold">{it.title}</h3>
                <p className="text-sm leading-relaxed text-muted-foreground">
                  {it.desc}
                </p>
              </div>
              {i < block.items.length - 1 && (
                <span className="self-center text-2xl text-emerald-500 rtl:rotate-180 max-md:rotate-90">
                  →
                </span>
              )}
            </div>
          ))}
        </div>
      );

    case "steps":
      return (
        <div className="grid gap-4 sm:grid-cols-3">
          {block.items.map((it, i) => (
            <div
              key={i}
              className="flex flex-col gap-2 rounded-2xl border border-border bg-card/60 p-5"
            >
              <span className="w-fit rounded-full bg-gradient-to-r from-gold-500 to-emerald-500 px-3 py-1 text-xs font-extrabold text-background">
                {it.n}
              </span>
              <h3 className="text-base font-extrabold">{it.title}</h3>
              <p className="text-sm leading-relaxed text-muted-foreground">
                {it.desc}
              </p>
            </div>
          ))}
        </div>
      );

    case "table":
      return (
        <div className="overflow-x-auto rounded-2xl border border-border">
          <table className="w-full min-w-[640px] border-collapse text-sm">
            <thead>
              <tr>
                {block.head.map((h, i) => (
                  <th
                    key={i}
                    className={cn(
                      "border-b border-border px-3.5 py-3 text-start text-xs font-extrabold",
                      i === block.highlight
                        ? "bg-emerald-500/15 text-emerald-500"
                        : "bg-muted/50",
                    )}
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {block.rows.map((row, ri) => (
                <tr key={ri}>
                  {row.map((cell, ci) => (
                    <td
                      key={ci}
                      className={cn(
                        "border-b border-border/60 px-3.5 py-3",
                        ci === 0 && "font-bold",
                        ci === block.highlight &&
                          "bg-emerald-500/10 font-extrabold text-emerald-500",
                      )}
                    >
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );

    case "bars":
      return <BeforeAfterChart items={block.items} lang={lang} />;

    case "roi":
      return (
        <div className="flex flex-col gap-4">
          <RoiChart cols={block.cols} unit={block.unit} />
          <div className="grid gap-3 sm:grid-cols-2">
            {block.cols.map((col, i) => (
              <div
                key={i}
                className={cn(
                  "rounded-2xl border p-4",
                  col.tone === "danger"
                    ? "border-destructive/25 bg-destructive/5"
                    : "border-emerald-500/25 bg-emerald-500/5",
                )}
              >
                <p className="mb-2 text-sm font-extrabold">{col.label}</p>
                <ul className="flex flex-col gap-1">
                  {col.items.map((x, xi) => (
                    <li key={xi} className="text-xs text-muted-foreground">
                      <span className="text-emerald-500">·</span> {x}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          {block.delta && (
            <div className="flex flex-wrap items-baseline justify-center gap-3 rounded-2xl bg-gradient-to-r from-gold-500 to-emerald-500 p-4 text-center text-background">
              <span className="text-sm font-bold">{block.delta.label}</span>
              <span className="text-xl font-extrabold sm:text-2xl">
                {block.delta.value}
              </span>
            </div>
          )}
        </div>
      );

    case "gates":
      return (
        <div className="grid gap-3 sm:grid-cols-2">
          {block.items.map((it, i) => (
            <div
              key={i}
              className="flex items-center gap-3 rounded-xl border border-emerald-500/25 bg-emerald-500/5 px-4 py-3"
            >
              <Lock className="h-4 w-4 shrink-0 text-emerald-500" />
              <div className="flex flex-col">
                <span className="font-mono text-xs font-bold text-emerald-500">
                  {it.code}
                </span>
                <span className="text-sm">{it.label}</span>
              </div>
            </div>
          ))}
        </div>
      );

    case "pricing":
      return (
        <div className="grid gap-3.5 sm:grid-cols-2 lg:grid-cols-5">
          {block.items.map((it, i) => (
            <div
              key={i}
              className={cn(
                "relative flex flex-col gap-3 rounded-2xl border bg-card/60 p-5",
                it.featured
                  ? "border-2 border-emerald-500 shadow-[0_0_0_4px_rgba(16,185,129,0.12)]"
                  : "border-border",
              )}
            >
              {it.badge && (
                <span className="absolute -top-3 start-4 rounded-full bg-gradient-to-r from-gold-500 to-emerald-500 px-3 py-0.5 text-[11px] font-extrabold text-background">
                  {it.badge}
                </span>
              )}
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/10 text-sm font-extrabold text-emerald-500">
                {it.tier}
              </span>
              <h3 className="text-base font-extrabold">{it.name}</h3>
              <div>
                <span className="text-2xl font-extrabold tracking-tight">
                  {it.price}
                </span>
                {it.period && (
                  <span className="block text-xs text-muted-foreground">
                    {it.period}
                  </span>
                )}
              </div>
              <ul className="flex flex-col gap-1.5">
                {it.items.map((x, xi) => (
                  <li
                    key={xi}
                    className="text-xs leading-snug text-muted-foreground"
                  >
                    <span className="font-bold text-emerald-500">✓</span> {x}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      );

    case "bullets":
      return (
        <div className="flex flex-col gap-3">
          {block.title && (
            <h3 className="text-lg font-extrabold sm:text-xl">{block.title}</h3>
          )}
          <ul className="flex flex-col gap-2.5">
            {block.items.map((x, i) => (
              <li
                key={i}
                className="flex gap-3 rounded-xl border border-border bg-card/60 px-4 py-3.5 text-sm leading-relaxed sm:text-base"
              >
                <span className="shrink-0 font-extrabold text-emerald-500 rtl:rotate-180">
                  →
                </span>
                {x}
              </li>
            ))}
          </ul>
        </div>
      );

    case "note":
      return (
        <div className="flex gap-2.5 rounded-xl border border-gold-500/25 bg-gold-500/5 px-4 py-3 text-xs leading-relaxed text-muted-foreground">
          <Info className="h-4 w-4 shrink-0 text-gold-500" />
          <span>{block.text}</span>
        </div>
      );

    default:
      return null;
  }
}
